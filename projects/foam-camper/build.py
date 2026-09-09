"""
Compact Foam Camper - Form Exploration & Compound Curve Modeling
Project: Ultralight Towable Rigid Foam Insulation Camper Shell Studies
Dimensions: 12'-0" (3,658 mm) Length x 6'-6" (1,981 mm) Width x 5'-9" (1,750 mm) Height

Explores three distinct solid form modeling methodologies:
  1. Form A: Dual-Axis Carved Aero Capsule (Orthogonal Sketch Pad & Pocket Intersection)
  2. Form B: Multi-Chine Faceted Hull (Kerf-Scored Developable Rigid Foam Study)
  3. Form C: Multi-Station Arched Loft (Organic Cross-Section Rib Loft)
"""

import os
import sys
import math
import shutil
import FreeCAD
import Part
import Sketcher

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import (
    init_materials,
    apply_material,
    get_mass_properties,
    format_mass_report,
)
from phi_works.maker.skeleton import create_varset


def make_trailer_bed_wire(length, width, x_offset=0.0, y_offset=0.0):
    """Generates a reference wire of the 12' x 6.5' trailer bed with hitch tongue and axle line."""
    p1 = FreeCAD.Vector(x_offset, y_offset - width / 2.0, 0)
    p2 = FreeCAD.Vector(x_offset + length, y_offset - width / 2.0, 0)
    p3 = FreeCAD.Vector(x_offset + length, y_offset + width / 2.0, 0)
    p4 = FreeCAD.Vector(x_offset, y_offset + width / 2.0, 0)
    
    edges = [
        Part.makeLine(p1, p2),
        Part.makeLine(p2, p3),
        Part.makeLine(p3, p4),
        Part.makeLine(p4, p1),
    ]
    # Tongue coupler triangle extending 900mm in front of bed
    pt_coupler = FreeCAD.Vector(x_offset - 900.0, y_offset, 0)
    edges.append(Part.makeLine(FreeCAD.Vector(x_offset, y_offset - width / 4.0, 0), pt_coupler))
    edges.append(Part.makeLine(FreeCAD.Vector(x_offset, y_offset + width / 4.0, 0), pt_coupler))

    # Axle centerline reference (typical 60/40 weight balance: ~60% of length from hitch)
    axle_x = x_offset + (length * 0.60)
    edges.append(Part.makeLine(FreeCAD.Vector(axle_x, y_offset - width / 2.0 - 150, 0),
                               FreeCAD.Vector(axle_x, y_offset + width / 2.0 + 150, 0)))
    return Part.Compound(edges)


def create_form_a_carved(length, width, height):
    """
    Form A: Dual-Axis Carved Aero Capsule (Orthogonal Sketch Pad & Pocket Intersection).
    - Elevation Profile: Aerodynamic teardrop with curved bullet-nose and gentle Kamm-tail taper.
    - Plan Profile: Aerodynamic boat-tail planform (curved prow, max beam at shoulder, tapering to rear).
    - Shoulder Roll: 200mm fillet along top perimeter creating compound curvature across all axes.
    """
    # 1. Elevation Profile in XZ
    p_floor_start = FreeCAD.Vector(180, 0, 0)
    p_floor_end   = FreeCAD.Vector(length, 0, 0)
    p_transom_top = FreeCAD.Vector(length, 0, 480)
    p_tail_upper  = FreeCAD.Vector(3000, 0, 1420)
    p_roof_apex   = FreeCAD.Vector(1200, 0, height)
    p_windshield  = FreeCAD.Vector(400, 0, 1400)
    p_nose_tip    = FreeCAD.Vector(0, 0, 650)
    p_chin_curve  = FreeCAD.Vector(60, 0, 250)

    edges_elev = []
    edges_elev.append(Part.makeLine(p_floor_end, p_floor_start))
    edges_elev.append(Part.BSplineCurve([p_floor_start, p_chin_curve, p_nose_tip, p_windshield, p_roof_apex]).toShape())
    edges_elev.append(Part.BSplineCurve([p_roof_apex, p_tail_upper, p_transom_top]).toShape())
    edges_elev.append(Part.makeLine(p_transom_top, p_floor_end))

    wire_elev = Part.Wire(edges_elev)
    face_elev = Part.Face(wire_elev)
    solid_elev = face_elev.extrude(FreeCAD.Vector(0, width * 1.5, 0))
    solid_elev.translate(FreeCAD.Vector(0, -(width * 1.5) / 2.0, 0))

    # 2. Plan Profile in XY
    w_half_max  = width / 2.0
    w_half_nose = width * 0.32
    w_half_rear = width * 0.38

    q_nose_tip = FreeCAD.Vector(0, 0, 0)
    q_nose_r   = FreeCAD.Vector(250, -w_half_nose, 0)
    q_shldr_r  = FreeCAD.Vector(1300, -w_half_max, 0)
    q_rear_r   = FreeCAD.Vector(length, -w_half_rear, 0)
    q_rear_l   = FreeCAD.Vector(length, w_half_rear, 0)
    q_shldr_l  = FreeCAD.Vector(1300, w_half_max, 0)
    q_nose_l   = FreeCAD.Vector(250, w_half_nose, 0)

    edges_plan = []
    edges_plan.append(Part.BSplineCurve([q_nose_tip, q_nose_r, q_shldr_r, q_rear_r]).toShape())
    edges_plan.append(Part.makeLine(q_rear_r, q_rear_l))
    edges_plan.append(Part.BSplineCurve([q_rear_l, q_shldr_l, q_nose_l, q_nose_tip]).toShape())

    wire_plan = Part.Wire(edges_plan)
    face_plan = Part.Face(wire_plan)
    solid_plan = face_plan.extrude(FreeCAD.Vector(0, 0, height * 1.4))

    # 3. Intersection
    body = solid_elev.common(solid_plan)

    # 4. Shoulder Roll: Blend top perimeter edges with 180mm compound fillet
    fillet_edges = []
    for edge in body.Edges:
        bb = edge.BoundBox
        if bb.ZMin > height * 0.65 and bb.XMax < length - 30:
            fillet_edges.append(edge)

    try:
        if fillet_edges:
            body = body.makeFillet(180.0, fillet_edges)
    except Exception as e:
        print(f"Note: Fillet applied partially or skipped: {e}")

    return body


def create_form_b_faceted(length, width, height):
    """
    Form B: Multi-Chine Faceted Hull (Kerf-Scored Rigid Foam Study).
    - Faceted cross-sections along 4 key stations:
      - Station 0: Nose wedge (X = 0 mm)
      - Station 1: Shoulder peak (X = 1100 mm)
      - Station 2: Mid-body (X = 2400 mm)
      - Station 3: Rear transom (X = 3658 mm)
    - Each station profile has 8 discrete faceted segments:
      Plinth (vertical), Tumblehome chine 1 (12 deg), Shoulder chine 2 (28 deg), Roof crown facet (45 deg / top).
    - Ruled lofting produces developable flat facets tailored for scored foam.
    """
    def make_station_faceted_wire(x_pos, w_max, h_max, plinth_h, h_crown):
        w_half = w_max / 2.0
        w_ch1  = w_half * 0.94
        w_ch2  = w_half * 0.78
        w_roof = w_half * 0.45

        z_plinth = plinth_h
        z_ch1    = plinth_h + (h_crown - plinth_h) * 0.42
        z_ch2    = plinth_h + (h_crown - plinth_h) * 0.78
        z_top    = h_crown

        pts = [
            FreeCAD.Vector(x_pos, -w_half, 0),
            FreeCAD.Vector(x_pos, -w_half, z_plinth),
            FreeCAD.Vector(x_pos, -w_ch1,  z_ch1),
            FreeCAD.Vector(x_pos, -w_ch2,  z_ch2),
            FreeCAD.Vector(x_pos, -w_roof, z_top),
            FreeCAD.Vector(x_pos,  w_roof, z_top),
            FreeCAD.Vector(x_pos,  w_ch2,  z_ch2),
            FreeCAD.Vector(x_pos,  w_ch1,  z_ch1),
            FreeCAD.Vector(x_pos,  w_half, z_plinth),
            FreeCAD.Vector(x_pos,  w_half, 0),
        ]
        edges = []
        for i in range(len(pts) - 1):
            edges.append(Part.makeLine(pts[i], pts[i+1]))
        edges.append(Part.makeLine(pts[-1], pts[0]))
        return Part.Wire(edges)

    w0 = make_station_faceted_wire(0.0,    width * 0.65, 1100.0, 300.0, 1100.0)
    w1 = make_station_faceted_wire(1100.0, width,        height, 480.0, height)
    w2 = make_station_faceted_wire(2400.0, width * 0.94, height * 0.94, 450.0, height * 0.94)
    w3 = make_station_faceted_wire(length, width * 0.76, 750.0,  250.0, 750.0)

    body = Part.makeLoft([w0, w1, w2, w3], True, True)
    return body


def create_form_c_lofted(length, width, height):
    """
    Form C: Multi-Station Arched Loft (Continuous Organic Cross-Section Loft).
    - Station 0 (X = 0 mm): Bow nose arch (W = 1300 mm, H = 1050 mm)
    - Station 1 (X = 1100 mm): Full cabin crown (W = 1981 mm, H = 1750 mm)
    - Station 2 (X = 2400 mm): Mid-cabin arch (W = 1880 mm, H = 1620 mm)
    - Station 3 (X = 3658 mm): Rear Kamm-tail arch (W = 1500 mm, H = 900 mm)
    """
    def make_station_arch_wire(x_pos, w_max, h_max, tumblehome_ratio=0.88):
        w_half = w_max / 2.0
        w_top  = w_half * tumblehome_ratio

        p_bot_r   = FreeCAD.Vector(x_pos, -w_half, 0)
        p_mid_r   = FreeCAD.Vector(x_pos, -w_half, h_max * 0.50)
        p_shldr_r = FreeCAD.Vector(x_pos, -w_top,  h_max * 0.88)
        p_apex    = FreeCAD.Vector(x_pos, 0,       h_max)
        p_shldr_l = FreeCAD.Vector(x_pos,  w_top,  h_max * 0.88)
        p_mid_l   = FreeCAD.Vector(x_pos,  w_half, h_max * 0.50)
        p_bot_l   = FreeCAD.Vector(x_pos,  w_half, 0)

        edges = []
        edges.append(Part.makeLine(p_bot_l, p_bot_r))
        edges.append(Part.makeLine(p_bot_r, p_mid_r))
        edges.append(Part.BSplineCurve([p_mid_r, p_shldr_r, p_apex, p_shldr_l, p_mid_l]).toShape())
        edges.append(Part.makeLine(p_mid_l, p_bot_l))
        return Part.Wire(edges)

    s0 = make_station_arch_wire(0.0,    width * 0.66, 1050.0, tumblehome_ratio=0.75)
    s1 = make_station_arch_wire(1100.0, width,        height, tumblehome_ratio=0.84)
    s2 = make_station_arch_wire(2400.0, width * 0.94, height * 0.92, tumblehome_ratio=0.86)
    s3 = make_station_arch_wire(length, width * 0.74, 900.0,  tumblehome_ratio=0.90)

    body = Part.makeLoft([s0, s1, s2, s3], True, False)
    return body


def build_foam_camper():
    init_materials()
    doc_base_name = "foam_camper"
    fcstd_path = os.path.join(script_dir, "foam-camper.FCStd")

    doc = FreeCAD.newDocument(doc_base_name)
    doc.Label = "Compact Foam Camper v0.1.0 (12' x 6.5' Solid Form Explorations)"

    # Parametric Dimensions VarSet
    vars_dict = {
        "CamperLength": 3658.0,      # 12'-0"
        "CamperWidth": 1981.0,       # 6'-6"
        "CamperHeight": 1750.0,      # 5'-9"
        "FoamThickness": 50.8,       # 2.0" XPS rigid foam
        "AxleStation": 2194.8,       # 60% rearward axle line
        "DisplaySpacing": 3200.0,    # Lateral spacing between comparison models
    }
    varset = create_varset(doc, "Vars", "Camper Parameters", vars_dict)

    L = varset.CamperLength.Value
    W = varset.CamperWidth.Value
    H = varset.CamperHeight.Value
    spacing = varset.DisplaySpacing.Value

    # =========================================================================
    # FORM A: DUAL-AXIS CARVED AERO CAPSULE (Centered at Y = 0)
    # =========================================================================
    grp_a = doc.addObject("App::DocumentObjectGroup", "Form_A_Carved_Aero")
    grp_a.Label = "Form A: Carved Aero Capsule (Pad & Pocket Intersection)"

    shape_a = create_form_a_carved(L, W, H)
    feat_a = doc.addObject("Part::Feature", "Solid_Form_A")
    feat_a.Label = "Form A: Solid Aero Envelope"
    feat_a.Shape = shape_a
    apply_material(feat_a, "Polymer-XPS-Foam")
    grp_a.addObject(feat_a)

    bed_wire_a = make_trailer_bed_wire(L, W, 0.0, 0.0)
    bed_feat_a = doc.addObject("Part::Feature", "Trailer_Bed_Outline_A")
    bed_feat_a.Label = "Trailer Bed Reference A (12' x 6.5')"
    bed_feat_a.Shape = bed_wire_a
    grp_a.addObject(bed_feat_a)

    # =========================================================================
    # FORM B: MULTI-CHINE FACETED HULL (Offset to Y = +spacing)
    # =========================================================================
    grp_b = doc.addObject("App::DocumentObjectGroup", "Form_B_Faceted_Chine")
    grp_b.Label = "Form B: Multi-Chine Faceted Hull (Kerf-Scored Foam Study)"

    shape_b = create_form_b_faceted(L, W, H)
    shape_b.translate(FreeCAD.Vector(0, spacing, 0))
    feat_b = doc.addObject("Part::Feature", "Solid_Form_B")
    feat_b.Label = "Form B: Solid Faceted Envelope"
    feat_b.Shape = shape_b
    apply_material(feat_b, "Polymer-XPS-Foam")
    grp_b.addObject(feat_b)

    bed_wire_b = make_trailer_bed_wire(L, W, 0.0, spacing)
    bed_feat_b = doc.addObject("Part::Feature", "Trailer_Bed_Outline_B")
    bed_feat_b.Label = "Trailer Bed Reference B (12' x 6.5')"
    bed_feat_b.Shape = bed_wire_b
    grp_b.addObject(bed_feat_b)

    # =========================================================================
    # FORM C: MULTI-STATION ARCHED LOFT (Offset to Y = -spacing)
    # =========================================================================
    grp_c = doc.addObject("App::DocumentObjectGroup", "Form_C_Lofted_Organic")
    grp_c.Label = "Form C: Multi-Station Arched Loft (Continuous Organic Shell)"

    shape_c = create_form_c_lofted(L, W, H)
    shape_c.translate(FreeCAD.Vector(0, -spacing, 0))
    feat_c = doc.addObject("Part::Feature", "Solid_Form_C")
    feat_c.Label = "Form C: Solid Lofted Envelope"
    feat_c.Shape = shape_c
    apply_material(feat_c, "Polymer-XPS-Foam")
    grp_c.addObject(feat_c)

    bed_wire_c = make_trailer_bed_wire(L, W, 0.0, -spacing)
    bed_feat_c = doc.addObject("Part::Feature", "Trailer_Bed_Outline_C")
    bed_feat_c.Label = "Trailer Bed Reference C (12' x 6.5')"
    bed_feat_c.Shape = bed_wire_c
    grp_c.addObject(bed_feat_c)

    doc.recompute()

    # Log Volume and Weight Metrics
    print("\n" + "="*80)
    print(" COMPACT FOAM CAMPER: 3D SOLID FORM VOLUME & WEIGHT ANALYSIS")
    print("="*80)
    vol_a_m3 = shape_a.Volume / 1e9
    vol_b_m3 = shape_b.Volume / 1e9
    vol_c_m3 = shape_c.Volume / 1e9
    print(f" Form A (Carved Aero):     Volume = {vol_a_m3:6.2f} m³ ({vol_a_m3 * 35.3147:5.1f} cu.ft)")
    print(f" Form B (Faceted Chine):   Volume = {vol_b_m3:6.2f} m³ ({vol_b_m3 * 35.3147:5.1f} cu.ft)")
    print(f" Form C (Lofted Organic):  Volume = {vol_c_m3:6.2f} m³ ({vol_c_m3 * 35.3147:5.1f} cu.ft)")
    print(f" XPS Foam Density: 32 kg/m³ (~2.0 lb/cu.ft)")
    print("="*80 + "\n")

    doc.saveAs(fcstd_path)
    print(f"Saved master model to: {fcstd_path}")

    # =========================================================================
    # HIGH-RESOLUTION VISUAL RENDERS
    # =========================================================================
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        FreeCADGui.updateGui()

        # Archive milestone thumbnail to changelog/
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)

        # 1. Master comparison showcase (all 3 forms visible side-by-side)
        prefix_master = os.path.join(script_dir, "foam-camper")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_master,
            width=1920,
            height=1080
        )
        print("Generated master comparison renders (foam-camper.png)")

        # Copy milestone render
        src_master = f"{prefix_master}.png"
        dst_master = os.path.join(changelog_dir, "v0.1.0.png")
        if os.path.exists(src_master):
            shutil.copyfile(src_master, dst_master)

        # Helper to set visibility on gui objects
        def set_group_visible(grp, visible):
            g_obj = gui_doc.getObject(grp.Name)
            if g_obj:
                g_obj.Visibility = visible
            for child in getattr(grp, "Group", []):
                c_obj = gui_doc.getObject(child.Name)
                if c_obj:
                    c_obj.Visibility = visible

        # 2. Form A Isolated Renders
        set_group_visible(grp_b, False)
        set_group_visible(grp_c, False)
        set_group_visible(grp_a, True)
        prefix_a = os.path.join(script_dir, "form_a_carved")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_a,
            width=1920,
            height=1080
        )
        print("Generated Form A renders (form_a_carved.png)")

        # 3. Form B Isolated Renders
        set_group_visible(grp_a, False)
        set_group_visible(grp_c, False)
        set_group_visible(grp_b, True)
        prefix_b = os.path.join(script_dir, "form_b_faceted")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_b,
            width=1920,
            height=1080
        )
        print("Generated Form B renders (form_b_faceted.png)")

        # 4. Form C Isolated Renders
        set_group_visible(grp_a, False)
        set_group_visible(grp_b, False)
        set_group_visible(grp_c, True)
        prefix_c = os.path.join(script_dir, "form_c_lofted")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_c,
            width=1920,
            height=1080
        )
        print("Generated Form C renders (form_c_lofted.png)")

        # Restore visibility for clean master save
        set_group_visible(grp_a, True)
        set_group_visible(grp_b, True)
        set_group_visible(grp_c, True)
        doc.save()

    FreeCAD.closeDocument(doc.Name)
    print("Build complete!")


if __name__ == "__main__":
    build_foam_camper()
    os._exit(0)
