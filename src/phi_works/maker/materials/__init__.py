"""
Physical Materials & Mass Properties Engine

Provides project-native FreeCAD 1.0/1.1 material management, automatic library registration,
material assignment, and parametric mass/weight/center-of-gravity calculation.
"""

import os
import re
import math
import FreeCAD
import Materials

_MATERIALS_INITIALIZED = False

def get_materials_dir():
    """
    Returns the absolute path to the project `materials/` directory.
    Resolved dynamically relative to this module.
    """
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    maker_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "..", ".."))
    mat_dir = os.path.join(maker_dir, "materials")
    if not os.path.exists(mat_dir):
        os.makedirs(mat_dir, exist_ok=True)
    return mat_dir

def init_materials(force_refresh=False):
    """
    Registers the project `materials/` directory as FreeCAD's active CustomMaterialsDir
    and refreshes the FreeCAD MaterialManager.
    """
    global _MATERIALS_INITIALIZED
    if _MATERIALS_INITIALIZED and not force_refresh:
        return Materials.MaterialManager()

    mat_dir = get_materials_dir()
    param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
    param.SetString("CustomMaterialsDir", mat_dir)
    param.SetBool("UseMaterialsFromCustomDir", True)
    param.SetBool("UseBuiltInMaterials", True)

    mm = Materials.MaterialManager()
    mm.refresh()
    _MATERIALS_INITIALIZED = True
    return mm

def list_materials():
    """
    Returns a dictionary of all available materials: {Name: MaterialObject}.
    """
    mm = init_materials()
    mat_dict = {}
    for uuid in mm.Materials:
        mat = mm.getMaterial(uuid)
        if mat and mat.Name:
            mat_dict[mat.Name] = mat
    return mat_dict

def get_material(name_or_uuid):
    """
    Retrieves a Materials.Material instance by Name or UUID.
    
    Parameters:
      name_or_uuid: String, e.g. "Steel-A36" or "856988e2-8719-47c0-b934-b12aa2052c6f"
      
    Returns:
      Materials.Material object
      
    Raises:
      KeyError if material cannot be found.
    """
    mm = init_materials()
    
    # Try direct UUID lookup if it looks like a UUID
    try:
        mat = mm.getMaterial(name_or_uuid)
        if mat:
            return mat
    except (LookupError, ValueError, Exception):
        pass

    # Normalize search name (strip .FCMat if provided)
    search_name = name_or_uuid[:-6] if name_or_uuid.endswith(".FCMat") else name_or_uuid
    search_lower = search_name.lower()

    # Search by Name
    for uuid in mm.Materials:
        m = mm.getMaterial(uuid)
        if m and m.Name:
            if m.Name == search_name or m.Name.lower() == search_lower:
                return m

    available = sorted(list_materials().keys())
    raise KeyError(
        f"Material '{name_or_uuid}' not found. Available materials: {available}"
    )

def parse_color_tuple(color_str):
    """
    Parses a color string like '(0.42, 0.44, 0.48, 1.0)' into an RGB/RGBA float tuple.
    """
    if not color_str:
        return (0.8, 0.8, 0.8)
    match = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", color_str)
    if not match:
        return (0.8, 0.8, 0.8)
    vals = [float(v) for v in match]
    if len(vals) >= 3:
        return (vals[0], vals[1], vals[2])
    return (0.8, 0.8, 0.8)

def apply_material(obj, material_or_name, color_fallback=None):
    """
    Assigns a physical material to a FreeCAD DocumentObject and synchronizes its visual appearance.
    
    Parameters:
      obj: FreeCAD DocumentObject (Part::Feature, Part::Box, etc.)
      material_or_name: Materials.Material object or string material name (e.g. 'Steel-A36')
      color_fallback: Optional RGB/RGBA float tuple fallback for display if appearance model is missing
      
    Returns:
      The assigned Materials.Material object
    """
    if isinstance(material_or_name, str):
        mat = get_material(material_or_name)
    else:
        mat = material_or_name

    # Assign physical material to object
    if hasattr(obj, "ShapeMaterial"):
        obj.ShapeMaterial = mat

    # Sync visual appearance if ViewObject is accessible
    vobj = getattr(obj, "ViewObject", None)
    if vobj:
        color = None
        if hasattr(mat, "getAppearanceValue"):
            diffuse = mat.getAppearanceValue("DiffuseColor")
            if diffuse:
                color = parse_color_tuple(diffuse)
        if color is None and color_fallback is not None:
            if isinstance(color_fallback, (list, tuple)):
                color = (float(color_fallback[0]), float(color_fallback[1]), float(color_fallback[2]))
            else:
                color = parse_color_tuple(str(color_fallback))

        if color is not None:
            try:
                vobj.ShapeColor = (color[0], color[1], color[2])
                vobj.DisplayMode = "Flat Lines"
            except Exception:
                pass

        # Safeguard ShapeAppearance against uninitialized EmissiveColor memory in Coin3D
        if hasattr(vobj, "ShapeAppearance") and vobj.ShapeAppearance:
            for sa in vobj.ShapeAppearance:
                try:
                    if hasattr(sa, "EmissiveColor"):
                        sa.EmissiveColor = (0.0, 0.0, 0.0, 1.0)
                except Exception:
                    pass

    return mat

def _extract_parts(target):
    """
    Helper to extract all leaf CAD objects with shapes from an object, group, or document.
    """
    parts = []
    if isinstance(target, FreeCAD.Document):
        for o in target.Objects:
            if hasattr(o, "Shape") and not o.Shape.isNull() and o.Shape.Volume > 0:
                parts.append(o)
    elif hasattr(target, "Group"): # App::DocumentObjectGroup or App::Part
        for o in target.Group:
            parts.extend(_extract_parts(o))
    elif isinstance(target, (list, tuple, set)):
        for o in target:
            parts.extend(_extract_parts(o))
    elif hasattr(target, "Shape") and not target.Shape.isNull() and target.Shape.Volume > 0:
        parts.append(target)
    return parts

def get_shape_center_of_gravity(shape):
    """
    Safely retrieves the center of gravity/mass for Solids and Compounds.
    """
    if hasattr(shape, "CenterOfGravity"):
        try:
            return shape.CenterOfGravity
        except Exception:
            pass
    if hasattr(shape, "CenterOfMass"):
        try:
            return shape.CenterOfMass
        except Exception:
            pass
    if hasattr(shape, "BoundBox"):
        return shape.BoundBox.Center
    return FreeCAD.Vector(0, 0, 0)

def get_mass_properties(target):
    """
    Calculates exact volume, mass, and center of mass (CoM) for a part, subassembly group, or document.
    
    Parameters:
      target: FreeCAD.Document, App::DocumentObjectGroup, Part::Feature, or list of objects
      
    Returns:
      Dictionary containing:
        - total_mass_kg (float)
        - total_mass_lb (float)
        - total_volume_mm3 (float)
        - total_volume_in3 (float)
        - center_of_mass_mm (FreeCAD.Vector)
        - center_of_mass_in (FreeCAD.Vector)
        - items (list of individual item dicts)
        - by_material (dict of aggregated mass per material)
    """
    parts = _extract_parts(target)
    
    items = []
    by_material = {}
    
    total_mass_kg = 0.0
    total_volume_mm3 = 0.0
    weighted_com_x = 0.0
    weighted_com_y = 0.0
    weighted_com_z = 0.0

    for p in parts:
        vol_mm3 = float(p.Shape.Volume)
        if vol_mm3 <= 0:
            continue
            
        mat_name = "Unassigned"
        density_kg_m3 = 0.0
        
        if hasattr(p, "ShapeMaterial") and p.ShapeMaterial:
            mat = p.ShapeMaterial
            mat_name = mat.Name or "Unknown"
            density_q = mat.getPhysicalValue("Density")
            if density_q is not None:
                # FreeCAD internal density unit is kg/mm^3
                # 1 kg/m^3 = 1e-9 kg/mm^3
                density_kg_m3 = float(density_q.Value) * 1.0e9

        # Mass: Volume (mm^3) * (Density in kg/m^3 / 1e9 mm^3/m^3)
        mass_kg = vol_mm3 * (density_kg_m3 / 1.0e9)
        mass_lb = mass_kg * 2.20462262
        vol_in3 = vol_mm3 / (25.4 ** 3)
        
        com = get_shape_center_of_gravity(p.Shape)

        items.append({
            "name": p.Name,
            "label": getattr(p, "Label", p.Name),
            "material": mat_name,
            "density_kg_m3": density_kg_m3,
            "volume_mm3": vol_mm3,
            "volume_in3": vol_in3,
            "mass_kg": mass_kg,
            "mass_lb": mass_lb,
            "center_of_mass": com,
        })
        
        # Aggregate by material
        if mat_name not in by_material:
            by_material[mat_name] = {
                "material": mat_name,
                "count": 0,
                "mass_kg": 0.0,
                "mass_lb": 0.0,
                "volume_mm3": 0.0,
                "volume_in3": 0.0,
            }
        by_material[mat_name]["count"] += 1
        by_material[mat_name]["mass_kg"] += mass_kg
        by_material[mat_name]["mass_lb"] += mass_lb
        by_material[mat_name]["volume_mm3"] += vol_mm3
        by_material[mat_name]["volume_in3"] += vol_in3

        total_mass_kg += mass_kg
        total_volume_mm3 += vol_mm3
        weighted_com_x += mass_kg * com.x
        weighted_com_y += mass_kg * com.y
        weighted_com_z += mass_kg * com.z

    if total_mass_kg > 0:
        com_mm = FreeCAD.Vector(
            weighted_com_x / total_mass_kg,
            weighted_com_y / total_mass_kg,
            weighted_com_z / total_mass_kg,
        )
    else:
        com_mm = FreeCAD.Vector(0, 0, 0)
        
    com_in = FreeCAD.Vector(com_mm.x / 25.4, com_mm.y / 25.4, com_mm.z / 25.4)
    total_mass_lb = total_mass_kg * 2.20462262
    total_volume_in3 = total_volume_mm3 / (25.4 ** 3)

    return {
        "total_mass_kg": total_mass_kg,
        "total_mass_lb": total_mass_lb,
        "total_volume_mm3": total_volume_mm3,
        "total_volume_in3": total_volume_in3,
        "center_of_mass_mm": com_mm,
        "center_of_mass_in": com_in,
        "items": items,
        "by_material": by_material,
    }

def format_mass_report(data_or_target, title="Physical Mass & Weight Engineering Report"):
    """
    Generates a formatted ASCII / Markdown report of mass and center of gravity properties.
    """
    if not isinstance(data_or_target, dict) or "total_mass_kg" not in data_or_target:
        data = get_mass_properties(data_or_target)
    else:
        data = data_or_target

    lines = []
    lines.append(f"================================================================================")
    lines.append(f" {title.upper()}")
    lines.append(f"================================================================================")
    lines.append(f" TOTAL MASS / WEIGHT:     {data['total_mass_lb']:.2f} lbs  ({data['total_mass_kg']:.3f} kg)")
    lines.append(f" TOTAL SOLID VOLUME:      {data['total_volume_in3']:.2f} in³ ({data['total_volume_mm3']/1e6:.3f} L)")
    lines.append(f" CENTER OF MASS (CoG):")
    lines.append(f"   - Metric (mm):         X = {data['center_of_mass_mm'].x:+.2f} mm, Y = {data['center_of_mass_mm'].y:+.2f} mm, Z = {data['center_of_mass_mm'].z:+.2f} mm")
    lines.append(f"   - Imperial (inches):   X = {data['center_of_mass_in'].x:+.2f} in, Y = {data['center_of_mass_in'].y:+.2f} in, Z = {data['center_of_mass_in'].z:+.2f} in")
    lines.append(f"--------------------------------------------------------------------------------")
    lines.append(f" MATERIAL SUMMARY BREAKDOWN:")
    lines.append(f" {'Material':<26} {'Parts':<7} {'Mass (lbs)':<12} {'Mass (kg)':<12} {'% Mass':<8}")
    lines.append(f" {'-'*26} {'-'*7} {'-'*12} {'-'*12} {'-'*8}")

    tot_m = data['total_mass_kg'] if data['total_mass_kg'] > 0 else 1.0
    for mat_name, m_info in sorted(data['by_material'].items(), key=lambda x: x[1]['mass_kg'], reverse=True):
        pct = (m_info['mass_kg'] / tot_m) * 100.0
        lines.append(
            f" {mat_name:<26} {m_info['count']:<7} {m_info['mass_lb']:<12.2f} {m_info['mass_kg']:<12.3f} {pct:>6.1f}%"
        )
    lines.append(f"================================================================================")
    return "\n".join(lines)

__all__ = [
    "get_materials_dir",
    "init_materials",
    "list_materials",
    "get_material",
    "apply_material",
    "get_mass_properties",
    "format_mass_report",
]
