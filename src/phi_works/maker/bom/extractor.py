"""
Assembly BOM Extractor

Crawls FreeCAD assembly object trees, enforces component boundaries for
acquired COTS items, derives stock specifications for fabricated parts,
classifies standard hardware, and aggregates raw stock requisitions.
"""

import os
import re
import math
import datetime
import FreeCAD

from phi_works.maker.bom.models import (
    CommercialItem,
    FabricatedPart,
    HardwareItem,
    StockSummaryItem,
    BOMReport,
)
from phi_works.maker.components.metadata import get_component_metadata, CATALOG_METADATA
from phi_works.maker.materials import init_materials


def get_density_for_object(obj) -> float:
    """
    Returns material density in kg/m^3 for a FreeCAD object.
    Defaults to 7850 kg/m^3 (A36 mild steel).
    """
    mat = getattr(obj, "ShapeMaterial", None)
    if not mat:
        return 7850.0

    card = getattr(mat, "Card", {})
    if hasattr(card, "get"):
        phys = card.get("Physical", {})
        d_val = phys.get("Density", "7850 kg/m^3")
        try:
            match = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", str(d_val))
            if match:
                return float(match[0])
        except Exception:
            pass
    return 7850.0


def calculate_shape_mass(shape, density_kg_m3: float = 7850.0) -> float:
    """
    Computes mass in kg from FreeCAD TopoShape volume in mm^3 and density.
    """
    if shape.isNull() or shape.Volume <= 0:
        return 0.0
    vol_m3 = shape.Volume * 1e-9
    return vol_m3 * density_kg_m3


def compute_document_mass(comp_doc) -> float:
    """
    Calculates total mass in kg for all physical solids in an external component document.
    """
    total_kg = 0.0
    for obj in comp_doc.Objects:
        if hasattr(obj, "Shape") and not obj.Shape.isNull() and obj.Shape.Volume > 0:
            density = get_density_for_object(obj)
            total_kg += calculate_shape_mass(obj.Shape, density)
    return total_kg


def identify_stock_profile(dims_mm, label="", name=""):
    """
    Infers the raw stock type and standard imperial/metric specification from
    sorted dimensions [thickness, width, length] in mm, taking into account
    component labels, text annotations, and sheet metal folding.
    """
    t, w, l = dims_mm
    t_in = t / 25.4
    w_in = w / 25.4
    l_in = l / 25.4

    comb = f"{label} {name}".lower()

    # 1. 14-Gauge Sheet Steel Cowl & Skirts (Folded / Formed Sheet Metal)
    if "14-gauge" in comb or "14-ga" in comb or "cowl" in comb:
        return (
            "Sheet Metal",
            "14-Ga (0.075\") Sheet Steel",
            "CNC plasma cut vents, press brake 90° perimeter skirt bends, corner seam welds",
            (0.075 * 25.4, min(w, l), max(w, l)),  # Normalized stock sheet dimensions
        )

    # 2. Skid Runners (1.5" x 3/16" Flat Bar)
    if "skid" in comb:
        return (
            "Flat Bar",
            "1-1/2\" × 3/16\" Flat Bar",
            "Cut 2x runners to 21.5\" length, 30° cold tip bends front & rear, drill mounting holes",
            (4.76, 38.1, l),
        )

    # 3. Suspension Bridge & Transit Latch Catch Tower
    if "bridge" in comb or "catch tower" in comb:
        return (
            "Flat Bar & Pin",
            "2-1/2\" × 3/16\" Flat Bar & Ø1/2\" Pin",
            "Cut bridge plate to 15.4\" length, cut upright tower riser, weld Ø1/2\" catch pin",
            (4.76, 60.0, l),
        )

    # 4. Propane Harness Clamping Brackets
    if "clamp" in comb or "bracket" in comb:
        return (
            "Flat Bar",
            "2.0\" × 3/16\" Flat Bar",
            "Cut 2x clamp plates to 4.0\" length, form retention lips, drill 1/4\" bolt holes",
            (4.76, 50.0, l),
        )

    # 5. Foot-Release Snap Latch
    if "latch" in comb or "pedal" in comb:
        return (
            "Flat Bar & Pin",
            "5/8\" × 1/4\" Flat Bar & Ø3/8\" Pin",
            "Cut latch bar to length, weld 2.0\" × 1.4\" pedal pad, weld Ø3/8\" hook pin",
            (6.0, 15.0, l),
        )

    # 6. Triangular Suspension Straps (1.0" x 3/16" Flat Bar + Sleeve Bushings)
    if "strap" in comb or "suspension" in comb or "arm" in comb:
        return (
            "Flat Bar & Bushing",
            "1.0\" × 3/16\" Flat Bar & 1.0\" OD Sleeve",
            "Miter cut 4x struts to length, ream axle pivot sleeve bushings, weld triangulated A-frames",
            (4.76, 25.4, l),
        )

    # Generic Sheet Metal / Plate
    if t <= 3.5:
        return "Sheet Metal", f"{t_in:.3f}\" Sheet Steel", "CNC plasma/laser cut & brake form", (t, w, l)
    elif t <= 6.35:
        return "Steel Plate", f"{t_in:.3f}\" Plate Stock", "Cut and machine to print", (t, w, l)
    return "Solid Billet", f"{w_in:.1f}\" x {t_in:.1f}\" Stock", "Fabricate / machine to print", (t, w, l)




def extract_bom(doc, config: dict = None) -> BOMReport:
    """
    Crawls `doc` and builds a complete BOMReport.

    Parameters:
      doc: FreeCAD Document
      config: Optional dictionary with customization options:
        - `project_name`: str (default from doc.Name)
        - `version`: str (default "1.0.0")
        - `expand_components`: list of component names to expand into sub-parts
        - `hardware_keywords`: list of extra keywords for hardware classification
        - `operations_map`: dict of name/label patterns to fabrication notes
        - `part_marks`: dict of name/label patterns to part marks (e.g. "P-01")

    Returns:
      BOMReport instance
    """
    init_materials()
    config = config or {}

    project_name = config.get("project_name", getattr(doc, "Name", "Project").replace("_", " ").title())
    version = config.get("version", "1.0.0")
    expand_components = set(config.get("expand_components", []))
    hw_keywords = [
        "valve", "regulator", "hose", "wire", "clip", "bolt",
        "screw", "nut", "washer", "pin", "fitting", "spark"
    ] + config.get("hardware_keywords", [])

    commercial_items = []
    fabricated_parts = []
    hardware_items = []

    # Map to track component counts and deduplicate
    comp_counts = {}

    def is_hardware(name: str, label: str) -> bool:
        combined = f"{name} {label}".lower()
        # Exclude structural clamps or pins that are welded assemblies
        if "clamp" in combined and "strap" in combined:
            return False
        if "catch" in combined or "latch" in combined:
            return False
        return any(kw in combined for kw in hw_keywords)

    def traverse(obj_list, current_subassembly="General"):
        for obj in obj_list:
            type_id = getattr(obj, "TypeId", "")
            name = getattr(obj, "Name", "")
            label = getattr(obj, "Label", name)

            # Ignore non-physical / metadata objects
            if (
                type_id.startswith("Assembly::Joint")
                or type_id.startswith("Assembly::View")
                or type_id.startswith("Sketcher::")
                or type_id in ("App::Origin", "App::Line", "App::Plane", "App::Point", "App::VarSet")
                or type_id.startswith("App::Origin")
                or name in ("dims", "Origin", "Joints", "Exploded_Views", "Materials")
                or name.lower().startswith("origin")
                or "_axis" in name.lower()
                or "_plane" in name.lower()
            ):
                continue

            # 1. Detect External Component (App::Link to external doc or component path)
            linked = getattr(obj, "LinkedObject", None)
            is_external_comp = False
            comp_id = ""
            comp_doc = None

            if linked and getattr(linked, "Document", None) != doc:
                is_external_comp = True
                comp_doc = linked.Document
                comp_file = getattr(comp_doc, "FileName", "")
                comp_id = os.path.basename(os.path.dirname(comp_file)) if comp_file else linked.Name
                abs_comp_file = os.path.abspath(comp_file) if comp_file else ""
                is_cots = "/components/" in abs_comp_file or comp_id in CATALOG_METADATA

                # If it's a project subassembly (e.g. subassemblies/), traverse inside it
                if not is_cots:
                    sub_title = label or comp_id.replace("_", " ").title()
                    if hasattr(linked, "Group") and len(linked.Group) > 0:
                        traverse(linked.Group, current_subassembly=sub_title)
                    elif comp_doc:
                        traverse(comp_doc.RootObjects, current_subassembly=sub_title)
                    continue

                # Check if user requested expanding this specific commercial component
                if comp_id in expand_components:
                    sub_title = f"{current_subassembly} / {label}"
                    if hasattr(linked, "Group") and len(linked.Group) > 0:
                        traverse(linked.Group, current_subassembly=sub_title)
                    elif comp_doc:
                        traverse(comp_doc.RootObjects, current_subassembly=sub_title)
                    continue

                # ATOMIC COTS COMPONENT BOUNDARY: Do NOT recurse into internal sub-parts!
                meta = get_component_metadata(comp_id)

                # Mass calculation: prefer spec_mass_lb if present, else aggregate 3D CAD mass
                if meta.get("spec_mass_lb"):
                    mass_lb = float(meta["spec_mass_lb"])
                    mass_kg = float(meta.get("spec_mass_kg", mass_lb / 2.20462))
                elif comp_doc:
                    mass_kg = compute_document_mass(comp_doc)
                    mass_lb = mass_kg * 2.20462
                else:
                    mass_kg = 0.0
                    mass_lb = 0.0

                # Deduplicate or increment count
                if comp_id in comp_counts:
                    idx = comp_counts[comp_id]
                    commercial_items[idx].qty += 1
                else:
                    item = CommercialItem(
                        name=meta.get("title", label),
                        component_id=comp_id,
                        category=meta.get("category", "Commercial Hardware"),
                        qty=1,
                        vendor=meta.get("vendor", "Commercial Supplier"),
                        part_number=meta.get("part_number", comp_id.upper()),
                        description=meta.get("description", ""),
                        subassembly=current_subassembly,
                        mass_kg=mass_kg,
                        mass_lb=mass_lb,
                        reference_url=meta.get("reference_url", ""),
                    )
                    comp_counts[comp_id] = len(commercial_items)
                    commercial_items.append(item)
                continue

            # 2. Container Groups / Subassemblies
            if type_id in ("App::DocumentObjectGroup", "App::Part", "Assembly::AssemblyObject"):
                if hasattr(obj, "Group") and len(obj.Group) > 0:
                    sub_title = label if label != name else label.replace("_", " ").title()
                    traverse(obj.Group, current_subassembly=sub_title)
                    continue

            # 3. Leaf CAD part with physical shape
            if hasattr(obj, "Shape") and not obj.Shape.isNull() and obj.Shape.Volume > 0:
                density = get_density_for_object(obj)
                mass_kg = calculate_shape_mass(obj.Shape, density)
                mass_lb = mass_kg * 2.20462

                mat_name = "Steel-A36"
                if getattr(obj, "ShapeMaterial", None) and obj.ShapeMaterial.Name:
                    mat_name = obj.ShapeMaterial.Name

                # Check if hardware vs fabricated
                if is_hardware(name, label):
                    # Classify hardware category
                    cat = "Hardware & Fasteners"
                    if any(k in name.lower() for k in ["hose", "valve", "regulator", "fitting"]):
                        cat = "Plumbing & Fuel Lines"
                    elif any(k in name.lower() for k in ["wire", "spark", "piezo"]):
                        cat = "Electrical & Ignition"
                    elif any(k in name.lower() for k in ["clip", "strap", "tie"]):
                        cat = "Retention & Fasteners"

                    hw_item = HardwareItem(
                        name=label,
                        category=cat,
                        subassembly=current_subassembly,
                        material=mat_name,
                        specification=name.replace("_", " "),
                        qty=1,
                        mass_kg=mass_kg,
                        mass_lb=mass_lb,
                    )
                    hardware_items.append(hw_item)
                else:
                    bb = obj.Shape.BoundBox
                    dims = sorted([bb.XLength, bb.YLength, bb.ZLength])
                    stock_type, stock_spec, default_ops, norm_dims = identify_stock_profile(dims, label=label, name=name)

                    # Custom operations mapping override (longer patterns match first)
                    ops_override = config.get("operations_map", {})
                    ops = default_ops
                    for pat, custom_op in sorted(ops_override.items(), key=lambda x: len(x[0]), reverse=True):
                        if pat.lower() in name.lower() or pat.lower() in label.lower():
                            ops = custom_op
                            break

                    # Part mark (longer patterns match first)
                    part_marks = config.get("part_marks", {})
                    mark = f"P{len(fabricated_parts) + 1:02d}"
                    for pat, custom_mark in sorted(part_marks.items(), key=lambda x: len(x[0]), reverse=True):
                        if pat.lower() in name.lower() or pat.lower() in label.lower():
                            mark = custom_mark
                            break

                    part = FabricatedPart(
                        name=label,
                        part_mark=mark,
                        subassembly=current_subassembly,
                        material=mat_name,
                        stock_type=stock_type,
                        stock_spec=stock_spec,
                        length_mm=norm_dims[2],
                        width_mm=norm_dims[1],
                        thickness_mm=norm_dims[0],
                        qty=1,
                        mass_kg=mass_kg,
                        mass_lb=mass_lb,
                        operations=ops,
                        bounding_box_mm=(bb.XLength, bb.YLength, bb.ZLength),
                    )
                    fabricated_parts.append(part)

    # Begin traversal from top-level root objects
    root_objects = [
        o for o in doc.Objects
        if not [p for p in getattr(o, "InList", []) if getattr(p, "Document", None) == doc]
    ]
    traverse(root_objects)

    # 4. Generate Aggregated Raw Stock Requisition Summary
    stock_groups = {}
    for part in fabricated_parts:
        key = (part.material, part.stock_spec, part.stock_type)
        if key not in stock_groups:
            stock_groups[key] = {
                "count": 0,
                "linear_in": 0.0,
                "area_sq_in": 0.0,
                "mass_lb": 0.0,
                "pieces": [],
            }
        g = stock_groups[key]
        g["count"] += part.qty
        g["mass_lb"] += part.mass_lb * part.qty
        g["pieces"].append(part.part_mark or part.name)

        if part.stock_type in ("Sheet Metal", "Steel Plate"):
            # Area in square inches
            area = part.length_in * part.width_in * part.qty
            g["area_sq_in"] += area
        else:
            # Linear stock in inches
            g["linear_in"] += part.length_in * part.qty

    stock_summary = []
    for (mat, spec, stype), vals in sorted(stock_groups.items()):
        summary_item = StockSummaryItem(
            stock_spec=spec,
            material=mat,
            stock_type=stype,
            piece_count=vals["count"],
            total_linear_in=vals["linear_in"],
            total_linear_ft=vals["linear_in"] / 12.0,
            total_area_sq_in=vals["area_sq_in"],
            total_area_sq_ft=vals["area_sq_in"] / 144.0,
            total_mass_lb=vals["mass_lb"],
            pieces=vals["pieces"],
        )
        stock_summary.append(summary_item)

    report = BOMReport(
        project_name=project_name,
        version=version,
        date_str=datetime.datetime.now().strftime("%Y-%m-%d"),
        commercial_items=commercial_items,
        fabricated_parts=fabricated_parts,
        hardware_items=hardware_items,
        stock_summary=stock_summary,
    )

    return report
