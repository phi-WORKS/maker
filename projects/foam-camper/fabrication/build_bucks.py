"""
Compact Foam Camper v0.3.0 - Multi-Buck Fabrication & Assembly Suite
phi-WORKS Maker Framework (projects/foam-camper/fabrication/build_bucks.py)

Generates parametric 3D CAD fabrication bucks for the modular,
single-axis 1D developable curved camper shell:
  1. Master Egg-Crate Assembly Buck (camper_assembly_buck.FCStd / camper_buck.FCStd)
     - Full 12' x 6.5' chassis-mounted interlocking egg-crate jig
     - 24" center walk-through doorway at Station 0
     - Left & Right shoulder stringers at Y = +/- 533.5 mm (pop-top aperture & 3D shoulder seam)
     - 5 Transverse Bulkheads (Station 0 Nose to Station 4 Transom)
     - Ghosted 2.0" XPS outer shell overlay
  2. Pop-Up Roof Canopy Form Buck (roof_canopy_buck.FCStd)
     - Standalone bench-top forming buck for the 42" x 106" 1D XZ curved pop-up roof canopy
     - 3 longitudinal profile formers + 4 transverse interlocking cross-ties
     - Clamped curved foam panel overlay
  3. Side Wall Planform Bending Jig (side_wall_buck.FCStd)
     - Curved shop template for pre-curving the vertically scored 2.0" XPS side panels
     - Baseplate with boat-tail XY contour + vertical clamp uprights
"""

import os
import sys
import math
import shutil
import FreeCAD
import Part

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views
from phi_works.maker.materials import (
    init_materials,
    apply_material,
    get_mass_properties,
    format_mass_report,
)
from phi_works.maker.skeleton import create_varset


def build_geometry_solids(L, W, W_nose, W_rear, H_apex, H_brow, H_mid, H_transom, H_nose, T_FOAM):
    """
    Builds the outer master shell solid, the inner cavity solid (offset by T_FOAM),
    and the hollow shell for reference overlays.
    """
    w_mid = (W + W_rear) / 2.0

    # Outer Plan Solid (XY Boat-Tail Curve, Extruded in Z)
    p_nose_r = FreeCAD.Vector(0, -W_nose / 2.0, 0)
    p_nose_l = FreeCAD.Vector(0, W_nose / 2.0, 0)
    p_shldr_r = FreeCAD.Vector(1200.0, -W / 2.0, 0)
    p_shldr_l = FreeCAD.Vector(1200.0, W / 2.0, 0)
    p_mid_r = FreeCAD.Vector(2400.0, -w_mid / 2.0, 0)
    p_mid_l = FreeCAD.Vector(2400.0, w_mid / 2.0, 0)
    p_rear_r = FreeCAD.Vector(L, -W_rear / 2.0, 0)
    p_rear_l = FreeCAD.Vector(L, W_rear / 2.0, 0)

    spline_r = Part.BSplineCurve([p_nose_r, p_shldr_r, p_mid_r, p_rear_r]).toShape()
    spline_l = Part.BSplineCurve([p_rear_l, p_mid_l, p_shldr_l, p_nose_l]).toShape()
    wire_plan = Part.Wire([
        Part.makeLine(p_nose_l, p_nose_r),
        spline_r,
        Part.makeLine(p_rear_r, p_rear_l),
        spline_l
    ])
    face_plan = Part.Face(wire_plan)
    solid_plan = face_plan.extrude(FreeCAD.Vector(0, 0, H_apex * 1.5))

    # Outer Elevation Solid (XZ Teardrop Curve, Extruded in Y)
    p_f_front = FreeCAD.Vector(0, 0, 0)
    p_f_rear = FreeCAD.Vector(L, 0, 0)
    p_t_top = FreeCAD.Vector(L, 0, H_transom)
    p_r_mid = FreeCAD.Vector(2400.0, 0, H_mid)
    p_r_apex = FreeCAD.Vector(1200.0, 0, H_apex)
    p_r_brow = FreeCAD.Vector(300.0, 0, H_brow)
    p_r_nose = FreeCAD.Vector(0, 0, H_nose)

    spline_roof = Part.BSplineCurve([p_r_nose, p_r_brow, p_r_apex, p_r_mid, p_t_top]).toShape()
    wire_elev = Part.Wire([
        spline_roof,
        Part.makeLine(p_t_top, p_f_rear),
        Part.makeLine(p_f_rear, p_f_front),
        Part.makeLine(p_f_front, p_r_nose)
    ])
    face_elev = Part.Face(wire_elev)
    solid_elev = face_elev.extrude(FreeCAD.Vector(0, W * 2.0, 0))
    solid_elev.translate(FreeCAD.Vector(0, -W, 0))

    master_outer = solid_plan.common(solid_elev)

    # Inner Plan Solid (Offset inward by T_FOAM)
    w_nose_in = max(W_nose - T_FOAM * 2, 200.0)
    w_max_in = max(W - T_FOAM * 2, 200.0)
    w_mid_in = max(w_mid - T_FOAM * 2, 200.0)
    w_rear_in = max(W_rear - T_FOAM * 2, 200.0)

    q_nose_r = FreeCAD.Vector(T_FOAM, -w_nose_in / 2.0, 0)
    q_nose_l = FreeCAD.Vector(T_FOAM, w_nose_in / 2.0, 0)
    q_shldr_r = FreeCAD.Vector(1200.0, -w_max_in / 2.0, 0)
    q_shldr_l = FreeCAD.Vector(1200.0, w_max_in / 2.0, 0)
    q_mid_r = FreeCAD.Vector(2400.0, -w_mid_in / 2.0, 0)
    q_mid_l = FreeCAD.Vector(2400.0, w_mid_in / 2.0, 0)
    q_rear_r = FreeCAD.Vector(L - T_FOAM, -w_rear_in / 2.0, 0)
    q_rear_l = FreeCAD.Vector(L - T_FOAM, w_rear_in / 2.0, 0)

    spline_r_in = Part.BSplineCurve([q_nose_r, q_shldr_r, q_mid_r, q_rear_r]).toShape()
    spline_l_in = Part.BSplineCurve([q_rear_l, q_mid_l, q_shldr_l, q_nose_l]).toShape()
    wire_plan_in = Part.Wire([
        Part.makeLine(q_nose_l, q_nose_r),
        spline_r_in,
        Part.makeLine(q_rear_r, q_rear_l),
        spline_l_in
    ])
    face_plan_in = Part.Face(wire_plan_in)
    solid_plan_in = face_plan_in.extrude(FreeCAD.Vector(0, 0, H_apex * 1.5))

    # Inner Elevation Solid (Offset inward by T_FOAM)
    q_f_front = FreeCAD.Vector(T_FOAM, 0, 0)
    q_f_rear = FreeCAD.Vector(L - T_FOAM, 0, 0)
    q_t_top = FreeCAD.Vector(L - T_FOAM, 0, H_transom - T_FOAM)
    q_r_mid = FreeCAD.Vector(2400.0, 0, H_mid - T_FOAM)
    q_r_apex = FreeCAD.Vector(1200.0, 0, H_apex - T_FOAM)
    q_r_brow = FreeCAD.Vector(300.0, 0, H_brow - T_FOAM)
    q_r_nose = FreeCAD.Vector(T_FOAM, 0, H_nose - T_FOAM)

    spline_roof_in = Part.BSplineCurve([q_r_nose, q_r_brow, q_r_apex, q_r_mid, q_t_top]).toShape()
    wire_elev_in = Part.Wire([
        spline_roof_in,
        Part.makeLine(q_t_top, q_f_rear),
        Part.makeLine(q_f_rear, q_f_front),
        Part.makeLine(q_f_front, q_r_nose)
    ])
    face_elev_in = Part.Face(wire_elev_in)
    solid_elev_in = face_elev_in.extrude(FreeCAD.Vector(0, W * 2.0, 0))
    solid_elev_in.translate(FreeCAD.Vector(0, -W, 0))

    inner_solid = solid_plan_in.common(solid_elev_in)
    hollow_shell = master_outer.cut(inner_solid)

    return master_outer, inner_solid, hollow_shell


def build_master_assembly_buck():
    """
    Generates the master 12' x 6.5' interlocking plywood egg-crate assembly buck
    featuring the 24" center walk-through door and shoulder stringers.
    """
    print("\n" + "=" * 80)
    print(" 1. GENERATING MASTER ASSEMBLY BUCK (camper_assembly_buck.FCStd)")
    print("=" * 80)

    doc = FreeCAD.newDocument("camper_assembly_buck")
    doc.Label = "Camper Master Assembly Buck (12ft Interlocking Egg-Crate Jig)"
    init_materials(doc)

    L = 3658.0          # 12'-0"
    W = 1981.0          # 6'-6"
    W_nose = 1300.0
    W_rear = 1520.0
    H_apex = 1500.0
    H_brow = 1350.0
    H_mid = (H_apex + 850.0) / 2.0 + 50.0
    H_transom = 850.0
    H_nose = 900.0
    T_FOAM = 50.8
    T_PLY = 19.05
    POP_W = 1067.0
    HALF_POP = POP_W / 2.0
    DOOR_W = 610.0
    DOOR_H = 1270.0
    SLOT_W = T_PLY + 0.5
    SLOT_D = 100.0

    vars_dict = {
        "Camper_Length": L,
        "Camper_Width": W,
        "Apex_Height": H_apex,
        "Foam_Thickness": T_FOAM,
        "Plywood_Thickness": T_PLY,
        "PopUp_Width": POP_W,
        "Door_Width": DOOR_W,
        "Slot_Depth": SLOT_D,
    }
    create_varset(doc, "Vars", "Buck_Parameters", vars_dict)

    master_outer, inner_solid, hollow_shell = build_geometry_solids(
        L, W, W_nose, W_rear, H_apex, H_brow, H_mid, H_transom, H_nose, T_FOAM
    )

    stations = [
        {"name": "Rib_0_Nose",     "x": 60.0,   "label": "Station 0: Nose Rib (Door Walk-Through)", "is_door": True},
        {"name": "Rib_1_Shoulder", "x": 1200.0, "label": "Station 1: Shoulder Apex Rib (Max Width)", "is_door": False},
        {"name": "Rib_2_MidCabin", "x": 2000.0, "label": "Station 2: Mid-Cabin Rib", "is_door": False},
        {"name": "Rib_3_Galley",   "x": 2700.0, "label": "Station 3: Galley / Pop-Top End Bulkhead", "is_door": False, "is_galley": True},
        {"name": "Rib_4_Transom",  "x": 3580.0, "label": "Station 4: Rear Transom Rib", "is_door": False, "is_transom": True},
    ]

    # Transverse Ribs Container
    grp_ribs = doc.addObject("App::DocumentObjectGroup", "Transverse_Ribs")
    grp_ribs.Label = "1. Transverse Plywood Ribs (3/4in CDX)"

    for s in stations:
        x = s["x"]
        slab_box = Part.makeBox(T_PLY, W * 2, H_apex * 2, FreeCAD.Vector(x - T_PLY / 2.0, -W, 0))
        rib = inner_solid.common(slab_box)
        bb = rib.BoundBox

        if s.get("is_door"):
            door_box = Part.makeBox(T_PLY * 2, DOOR_W, DOOR_H + 100.0, FreeCAD.Vector(x - T_PLY, -DOOR_W / 2.0, 0))
            rib = rib.cut(door_box)
        elif s.get("is_transom"):
            win_box = Part.makeBox(T_PLY * 2, 800.0, 400.0, FreeCAD.Vector(x - T_PLY, -400.0, bb.ZLength * 0.30))
            rib = rib.cut(win_box)
        else:
            w_cut = max(bb.YLength - 300.0, 400.0)
            h_cut = max(bb.ZLength - 250.0, 400.0)
            crawl_box = Part.makeBox(T_PLY * 2, w_cut, h_cut, FreeCAD.Vector(x - T_PLY, -w_cut / 2.0, 100.0))
            rib = rib.cut(crawl_box)

        # Half-lap slots cut down from the top edge for the shoulder stringers
        slot_l = Part.makeBox(T_PLY * 2, SLOT_W, SLOT_D * 1.5, FreeCAD.Vector(x - T_PLY, HALF_POP - SLOT_W / 2.0, bb.ZMax - SLOT_D))
        slot_r = Part.makeBox(T_PLY * 2, SLOT_W, SLOT_D * 1.5, FreeCAD.Vector(x - T_PLY, -HALF_POP - SLOT_W / 2.0, bb.ZMax - SLOT_D))
        rib = rib.cut(slot_l).cut(slot_r)

        feat = doc.addObject("Part::Feature", s["name"])
        feat.Label = s["label"]
        feat.Shape = rib
        apply_material(feat, "Wood-PlywoodSheathing")
        grp_ribs.addObject(feat)

    # Longitudinal Stringers Container
    grp_str = doc.addObject("App::DocumentObjectGroup", "Longitudinal_Stringers")
    grp_str.Label = "2. Longitudinal Shoulder Stringers (Y = +/- 533.5 mm)"

    for side_sign, str_name, str_lbl in [
        (1, "Stringer_Left_Shoulder", "Left Shoulder Stringer (Y = +533.5 mm)"),
        (-1, "Stringer_Right_Shoulder", "Right Shoulder Stringer (Y = -533.5 mm)")
    ]:
        y_pos = side_sign * HALF_POP
        slab_str = Part.makeBox(L * 2, T_PLY, H_apex * 2, FreeCAD.Vector(-100, y_pos - T_PLY / 2.0, 0))
        str_raw = inner_solid.common(slab_str)
        str_shape = str_raw

        # Lightweighting cutouts between stations
        for i in range(len(stations) - 1):
            x1 = stations[i]["x"] + 80.0
            x2 = stations[i+1]["x"] - 80.0
            if x2 > x1 + 100.0:
                bb_reg = inner_solid.common(Part.makeBox(x2 - x1, 100, H_apex * 2, FreeCAD.Vector(x1, y_pos - 50, 0))).BoundBox
                cut_h = max(bb_reg.ZMin + bb_reg.ZLength - 180.0, 100.0)
                light_cutter = Part.makeBox(x2 - x1, T_PLY * 2, cut_h, FreeCAD.Vector(x1, y_pos - T_PLY, 0))
                str_shape = str_shape.cut(light_cutter)

        # Half-lap upward slots at each station
        for s in stations:
            x_st = s["x"]
            bb_st = inner_solid.common(Part.makeBox(T_PLY * 2, 100, H_apex * 2, FreeCAD.Vector(x_st - T_PLY, y_pos - 50, 0))).BoundBox
            z_top = bb_st.ZMax
            slot_up = Part.makeBox(SLOT_W, T_PLY * 2, z_top - SLOT_D + 5.0, FreeCAD.Vector(x_st - SLOT_W / 2.0, y_pos - T_PLY, 0))
            str_shape = str_shape.cut(slot_up)

        feat_str = doc.addObject("Part::Feature", str_name)
        feat_str.Label = str_lbl
        feat_str.Shape = str_shape
        apply_material(feat_str, "Wood-PlywoodSheathing")
        grp_str.addObject(feat_str)

    # Ghosted Outer Foam Shell Reference Overlay
    grp_shell = doc.addObject("App::DocumentObjectGroup", "Foam_Shell_Overlay")
    grp_shell.Label = "3. Outer Foam Shell Reference (Ghosted Overlay)"

    shell_ref = hollow_shell
    d_cut = Part.makeBox(T_FOAM * 3, DOOR_W, DOOR_H, FreeCAD.Vector(-T_FOAM, -DOOR_W / 2.0, 0))
    win_l = Part.makeBox(900.0, W, 450.0, FreeCAD.Vector(L * 0.38, HALF_POP, H_apex * 0.45))
    win_r = Part.makeBox(900.0, W, 450.0, FreeCAD.Vector(L * 0.38, -HALF_POP - W, H_apex * 0.45))
    shell_ref = shell_ref.cut(d_cut).cut(win_l).cut(win_r)

    feat_shell = doc.addObject("Part::Feature", "Ghost_Foam_Shell")
    feat_shell.Label = "2.0in Scored XPS Outer Shell (Reference)"
    feat_shell.Shape = shell_ref
    apply_material(feat_shell, "Polymer-XPS-Foam")
    grp_shell.addObject(feat_shell)

    doc.recompute()

    # Mass Properties
    rep_ribs = get_mass_properties(grp_ribs)
    rep_str = get_mass_properties(grp_str)
    tot_ply_lb = rep_ribs["total_mass_lb"] + rep_str["total_mass_lb"]
    tot_ply_kg = rep_ribs["total_mass_kg"] + rep_str["total_mass_kg"]
    print(f" Bulkhead Ribs (5 Stations):   {rep_ribs['total_mass_lb']:5.1f} lbs ({rep_ribs['total_mass_kg']:4.1f} kg)")
    print(f" Shoulder Stringers (2 Rails):  {rep_str['total_mass_lb']:5.1f} lbs ({rep_str['total_mass_kg']:4.1f} kg)")
    print(f" TOTAL MASTER ASSEMBLY BUCK:    {tot_ply_lb:5.1f} lbs ({tot_ply_kg:4.1f} kg)")
    print(f" Plywood Sheet Requirement:     ~2.8 sheets of 3/4\" CDX Plywood")
    print("-" * 80)

    # Save document
    fcstd_path = os.path.join(script_dir, "camper_assembly_buck.FCStd")
    doc.saveAs(fcstd_path)
    print(f" Saved master assembly buck: {fcstd_path}")

    legacy_path = os.path.join(script_dir, "camper_buck.FCStd")
    shutil.copy2(fcstd_path, legacy_path)

    gui_doc = FreeCADGui.getDocument(doc.Name) if HAS_GUI else None
    if gui_doc:
        # Render 1: Buck alone (shell hidden)
        feat_shell.ViewObject.Visibility = False
        doc.recompute()
        FreeCADGui.updateGui()
        prefix_buck = os.path.join(script_dir, "camper_assembly_buck")
        export_orthogonal_views(gui_doc, base_prefix=prefix_buck, width=1920, height=1080, bg_type="Transparent")
        for suffix in ["", "_top", "_bottom", "_front", "_back", "_left", "_right"]:
            src_png = os.path.join(script_dir, f"camper_assembly_buck{suffix}.png")
            dst_png = os.path.join(script_dir, f"camper_buck{suffix}.png")
            if os.path.exists(src_png):
                shutil.copy2(src_png, dst_png)

        # Render 2: Buck with Ghost Shell
        feat_shell.ViewObject.Visibility = True
        feat_shell.ViewObject.Transparency = 75
        doc.recompute()
        FreeCADGui.updateGui()
        prefix_with_shell = os.path.join(script_dir, "camper_assembly_buck_with_shell")
        export_orthogonal_views(gui_doc, base_prefix=prefix_with_shell, width=1920, height=1080, bg_type="Transparent")
        for suffix in ["", "_top", "_bottom", "_front", "_back", "_left", "_right"]:
            src_png = os.path.join(script_dir, f"camper_assembly_buck_with_shell{suffix}.png")
            dst_png = os.path.join(script_dir, f"camper_buck_with_shell{suffix}.png")
            if os.path.exists(src_png):
                shutil.copy2(src_png, dst_png)

    FreeCAD.closeDocument(doc.Name)
    print(" Master Assembly Buck complete!\n")


def build_roof_canopy_buck():
    """
    Generates the standalone bench-top forming buck for bending and gluing
    the 42" x 106" 1D XZ curved pop-up roof canopy.
    """
    print("\n" + "=" * 80)
    print(" 2. GENERATING POP-UP ROOF CANOPY FORM BUCK (roof_canopy_buck.FCStd)")
    print("=" * 80)

    doc = FreeCAD.newDocument("roof_canopy_buck")
    doc.Label = "Pop-Up Roof Canopy Form Buck (1D XZ Arched Bench Jig)"
    init_materials(doc)

    L = 3658.0
    W = 1981.0
    W_nose = 1300.0
    W_rear = 1520.0
    H_apex = 1500.0
    H_brow = 1350.0
    H_mid = (H_apex + 850.0) / 2.0 + 50.0
    H_transom = 850.0
    H_nose = 900.0
    T_FOAM = 50.8
    T_PLY = 19.05
    POP_W = 1067.0
    HALF_POP = POP_W / 2.0
    POP_X = 400.0
    POP_L = 2700.0
    SLOT_W = T_PLY + 0.5
    SLOT_D = 80.0
    Z_BASE = 600.0

    vars_dict = {
        "Canopy_Length": POP_L,
        "Canopy_Width": POP_W,
        "Foam_Thickness": T_FOAM,
        "Plywood_Thickness": T_PLY,
        "Base_Height": Z_BASE,
        "Slot_Depth": SLOT_D,
    }
    create_varset(doc, "Vars", "Roof_Buck_Parameters", vars_dict)

    # Inner elevation wire
    q_f_front = FreeCAD.Vector(T_FOAM, 0, 0)
    q_f_rear = FreeCAD.Vector(L - T_FOAM, 0, 0)
    q_t_top = FreeCAD.Vector(L - T_FOAM, 0, H_transom - T_FOAM)
    q_r_mid = FreeCAD.Vector(2400.0, 0, H_mid - T_FOAM)
    q_r_apex = FreeCAD.Vector(1200.0, 0, H_apex - T_FOAM)
    q_r_brow = FreeCAD.Vector(300.0, 0, H_brow - T_FOAM)
    q_r_nose = FreeCAD.Vector(T_FOAM, 0, H_nose - T_FOAM)

    spline_roof_in = Part.BSplineCurve([q_r_nose, q_r_brow, q_r_apex, q_r_mid, q_t_top]).toShape()
    wire_elev_in = Part.Wire([
        spline_roof_in,
        Part.makeLine(q_t_top, q_f_rear),
        Part.makeLine(q_f_rear, q_f_front),
        Part.makeLine(q_f_front, q_r_nose)
    ])
    face_elev_in = Part.Face(wire_elev_in)
    solid_roof_slab = face_elev_in.extrude(FreeCAD.Vector(0, POP_W * 2, 0))
    solid_roof_slab.translate(FreeCAD.Vector(0, -POP_W, 0))

    # Bounded to pop-up length
    pop_box = Part.makeBox(POP_L, POP_W * 2, H_apex * 2, FreeCAD.Vector(POP_X, -POP_W, 0))
    roof_pop_inner = solid_roof_slab.common(pop_box)

    base_cut_box = Part.makeBox(POP_L * 2, POP_W * 2, Z_BASE, FreeCAD.Vector(POP_X - 100, -POP_W, 0))

    # 3 Longitudinal Arched Formers
    y_formers = [420.0, 0.0, -420.0]
    x_ties = [POP_X + 120.0, 1200.0, 2000.0, POP_X + POP_L - 120.0]

    grp_formers = doc.addObject("App::DocumentObjectGroup", "Longitudinal_Formers")
    grp_formers.Label = "1. Longitudinal Arched Formers (3/4in CDX)"

    for idx, y_f in enumerate(y_formers):
        slab_f = Part.makeBox(POP_L, T_PLY, H_apex * 2, FreeCAD.Vector(POP_X, y_f - T_PLY / 2.0, 0))
        former = roof_pop_inner.common(slab_f).cut(base_cut_box)

        # Half-lap slots cut down from the top edge
        for xt in x_ties:
            bb_t = former.common(Part.makeBox(T_PLY * 2, 100, H_apex * 2, FreeCAD.Vector(xt - T_PLY, y_f - 50, 0))).BoundBox
            slot_down = Part.makeBox(SLOT_W, T_PLY * 2, SLOT_D, FreeCAD.Vector(xt - SLOT_W / 2.0, y_f - T_PLY, bb_t.ZMax - SLOT_D))
            former = former.cut(slot_down)

        feat = doc.addObject("Part::Feature", f"Roof_Former_{idx}")
        feat.Label = f"Roof Former {idx+1} (Y = {y_f:+.0f} mm)"
        feat.Shape = former
        apply_material(feat, "Wood-PlywoodSheathing")
        grp_formers.addObject(feat)

    # 4 Transverse Cross-Ties
    grp_ties = doc.addObject("App::DocumentObjectGroup", "Transverse_Ties")
    grp_ties.Label = "2. Transverse Interlocking Cross-Ties"

    for idx, xt in enumerate(x_ties):
        slab_tie = Part.makeBox(T_PLY, POP_W - 40.0, H_apex * 2, FreeCAD.Vector(xt - T_PLY / 2.0, -HALF_POP + 20.0, 0))
        tie = roof_pop_inner.common(slab_tie).cut(base_cut_box)

        # Half-lap upward slots at y_formers
        for y_f in y_formers:
            bb_y = tie.common(Part.makeBox(100, T_PLY * 2, H_apex * 2, FreeCAD.Vector(xt - 50, y_f - T_PLY, 0))).BoundBox
            slot_up = Part.makeBox(T_PLY * 2, SLOT_W, bb_y.ZMax - SLOT_D + 5.0 - Z_BASE, FreeCAD.Vector(xt - T_PLY, y_f - SLOT_W / 2.0, Z_BASE))
            tie = tie.cut(slot_up)

        feat_tie = doc.addObject("Part::Feature", f"Cross_Tie_{idx}")
        feat_tie.Label = f"Cross-Tie {idx+1} (X = {xt:.0f} mm)"
        feat_tie.Shape = tie
        apply_material(feat_tie, "Wood-PlywoodSheathing")
        grp_ties.addObject(feat_tie)

    # Foam Canopy Reference Overlay
    p_f_front = FreeCAD.Vector(0, 0, 0)
    p_f_rear = FreeCAD.Vector(L, 0, 0)
    p_t_top = FreeCAD.Vector(L, 0, H_transom)
    p_r_mid = FreeCAD.Vector(2400.0, 0, H_mid)
    p_r_apex = FreeCAD.Vector(1200.0, 0, H_apex)
    p_r_brow = FreeCAD.Vector(300.0, 0, H_brow)
    p_r_nose = FreeCAD.Vector(0, 0, H_nose)
    spline_roof_out = Part.BSplineCurve([p_r_nose, p_r_brow, p_r_apex, p_r_mid, p_t_top]).toShape()
    wire_roof_out = Part.Wire([
        spline_roof_out,
        Part.makeLine(p_t_top, p_f_rear),
        Part.makeLine(p_f_rear, p_f_front),
        Part.makeLine(p_f_front, p_r_nose)
    ])
    solid_out = Part.Face(wire_roof_out).extrude(FreeCAD.Vector(0, POP_W, 0))
    solid_out.translate(FreeCAD.Vector(0, -HALF_POP, 0))
    canopy_foam = solid_out.cut(solid_roof_slab).common(pop_box)

    grp_foam = doc.addObject("App::DocumentObjectGroup", "Foam_Canopy_Ref")
    grp_foam.Label = "3. Clamped Foam Canopy Overlay"
    feat_foam = doc.addObject("Part::Feature", "Clamped_Roof_Canopy")
    feat_foam.Label = "42in x 106in Curved 2.0in XPS Foam Canopy"
    feat_foam.Shape = canopy_foam
    apply_material(feat_foam, "Polymer-XPS-Foam")
    grp_foam.addObject(feat_foam)

    doc.recompute()

    rep_f = get_mass_properties(grp_formers)
    rep_t = get_mass_properties(grp_ties)
    tot_roof_lb = rep_f["total_mass_lb"] + rep_t["total_mass_lb"]
    tot_roof_kg = rep_f["total_mass_kg"] + rep_t["total_mass_kg"]
    print(f" Longitudinal Formers (3 rails): {rep_f['total_mass_lb']:5.1f} lbs ({rep_f['total_mass_kg']:4.1f} kg)")
    print(f" Transverse Cross-Ties (4 ties): {rep_t['total_mass_lb']:5.1f} lbs ({rep_t['total_mass_kg']:4.1f} kg)")
    print(f" TOTAL ROOF CANOPY BUCK:         {tot_roof_lb:5.1f} lbs ({tot_roof_kg:4.1f} kg)")
    print("-" * 80)

    # Save document
    fcstd_path = os.path.join(script_dir, "roof_canopy_buck.FCStd")
    doc.saveAs(fcstd_path)
    print(f" Saved roof canopy buck: {fcstd_path}")

    gui_doc = FreeCADGui.getDocument(doc.Name) if HAS_GUI else None
    if gui_doc:
        feat_foam.ViewObject.Transparency = 50
        doc.recompute()
        FreeCADGui.updateGui()
        prefix = os.path.join(script_dir, "roof_canopy_buck")
        export_orthogonal_views(gui_doc, base_prefix=prefix, width=1920, height=1080, bg_type="Transparent")

    FreeCAD.closeDocument(doc.Name)
    print(" Roof Canopy Form Buck complete!\n")


def build_side_wall_buck():
    """
    Generates the side wall planform bending template jig
    for pre-curving the vertically kerfed 2.0" XPS side panels.
    """
    print("\n" + "=" * 80)
    print(" 3. GENERATING SIDE WALL PLANFORM BENDING JIG (side_wall_buck.FCStd)")
    print("=" * 80)

    doc = FreeCAD.newDocument("side_wall_buck")
    doc.Label = "Side Wall Planform Bending Jig (1D XY Boat-Tail Shop Form)"
    init_materials(doc)

    L = 3658.0
    W = 1981.0
    W_nose = 1300.0
    W_rear = 1520.0
    w_mid = (W + W_rear) / 2.0
    T_FOAM = 50.8
    T_PLY = 19.05
    H_STANCHION = 1200.0

    w_nose_in = max(W_nose - T_FOAM * 2, 200.0)
    w_max_in = max(W - T_FOAM * 2, 200.0)
    w_mid_in = max(w_mid - T_FOAM * 2, 200.0)
    w_rear_in = max(W_rear - T_FOAM * 2, 200.0)

    vars_dict = {
        "Camper_Length": L,
        "Max_Width": W,
        "Foam_Thickness": T_FOAM,
        "Plywood_Thickness": T_PLY,
        "Stanchion_Height": H_STANCHION,
    }
    create_varset(doc, "Vars", "Side_Jig_Parameters", vars_dict)

    # Inner boat-tail curve for port side (Y > 0)
    q_nose = FreeCAD.Vector(T_FOAM, w_nose_in / 2.0, 0)
    q_shldr = FreeCAD.Vector(1200.0, w_max_in / 2.0, 0)
    q_mid = FreeCAD.Vector(2400.0, w_mid_in / 2.0, 0)
    q_rear = FreeCAD.Vector(L - T_FOAM, w_rear_in / 2.0, 0)
    spline_inner = Part.BSplineCurve([q_nose, q_shldr, q_mid, q_rear]).toShape()

    # Outer boat-tail curve for port side
    p_nose = FreeCAD.Vector(0, W_nose / 2.0, 0)
    p_shldr = FreeCAD.Vector(1200.0, W / 2.0, 0)
    p_mid = FreeCAD.Vector(2400.0, w_mid / 2.0, 0)
    p_rear = FreeCAD.Vector(L, W_rear / 2.0, 0)
    spline_outer = Part.BSplineCurve([p_nose, p_shldr, p_mid, p_rear]).toShape()

    # Base Template Plate: 220 mm wide strip following the inner curve
    w_plate = 220.0
    p1 = FreeCAD.Vector(T_FOAM, (w_nose_in / 2.0) - w_plate, 0)
    p2 = FreeCAD.Vector(1200.0, (w_max_in / 2.0) - w_plate, 0)
    p3 = FreeCAD.Vector(2400.0, (w_mid_in / 2.0) - w_plate, 0)
    p4 = FreeCAD.Vector(L - T_FOAM, (w_rear_in / 2.0) - w_plate, 0)
    spline_plate_in = Part.BSplineCurve([p4, p3, p2, p1]).toShape()

    wire_plate = Part.Wire([
        spline_inner,
        Part.makeLine(q_rear, p4),
        spline_plate_in,
        Part.makeLine(p1, q_nose)
    ])
    base_plate = Part.Face(wire_plate).extrude(FreeCAD.Vector(0, 0, T_PLY))

    grp_base = doc.addObject("App::DocumentObjectGroup", "Base_Template")
    grp_base.Label = "1. Curved Sole Base Plate (3/4in Plywood)"
    feat_base = doc.addObject("Part::Feature", "Curved_Sole_Plate")
    feat_base.Label = "Boat-Tail Planform Sole Plate"
    feat_base.Shape = base_plate
    apply_material(feat_base, "Wood-PlywoodSheathing")
    grp_base.addObject(feat_base)

    # Upright Clamp Stanchions (6 vertical posts spaced along the curve)
    grp_posts = doc.addObject("App::DocumentObjectGroup", "Clamp_Stanchions")
    grp_posts.Label = "2. Vertical Clamp Stanchions (2x4 / Gussets)"

    x_posts = [150.0, 800.0, 1500.0, 2200.0, 2900.0, 3550.0]
    post_w = 89.0   # 2x4 3.5"
    post_t = 38.0   # 2x4 1.5"

    for idx, xp in enumerate(x_posts):
        sl = base_plate.common(Part.makeBox(1.0, 2000, 100, FreeCAD.Vector(xp, 0, 0)))
        y_contact = sl.BoundBox.YMax

        post_box = Part.makeBox(post_w, post_t, H_STANCHION,
                                FreeCAD.Vector(xp - post_w / 2.0, y_contact - post_t, T_PLY))
        feat_post = doc.addObject("Part::Feature", f"Stanchion_{idx}")
        feat_post.Label = f"Vertical Clamp Post {idx+1} (X = {xp:.0f} mm)"
        feat_post.Shape = post_box
        apply_material(feat_post, "Wood-SoftwoodPine")
        grp_posts.addObject(feat_post)

    # Clamped Foam Panel Reference
    wire_foam_strip = Part.Wire([
        spline_outer,
        Part.makeLine(p_rear, q_rear),
        Part.BSplineCurve([q_rear, q_mid, q_shldr, q_nose]).toShape(),
        Part.makeLine(q_nose, p_nose)
    ])
    clamped_foam = Part.Face(wire_foam_strip).extrude(FreeCAD.Vector(0, 0, H_STANCHION - 100.0))
    clamped_foam.translate(FreeCAD.Vector(0, 0, T_PLY))

    grp_foam = doc.addObject("App::DocumentObjectGroup", "Clamped_Side_Wall")
    grp_foam.Label = "3. Clamped Scored Foam Wall Overlay"
    feat_foam = doc.addObject("Part::Feature", "Clamped_Foam_Wall")
    feat_foam.Label = "Curved 2.0in XPS Side Panel (Pre-Forming)"
    feat_foam.Shape = clamped_foam
    apply_material(feat_foam, "Polymer-XPS-Foam")
    grp_foam.addObject(feat_foam)

    doc.recompute()

    rep_base = get_mass_properties(grp_base)
    rep_posts = get_mass_properties(grp_posts)
    tot_jig_lb = rep_base["total_mass_lb"] + rep_posts["total_mass_lb"]
    print(f" Sole Base Plate:         {rep_base['total_mass_lb']:5.1f} lbs")
    print(f" Vertical Clamp Posts:    {rep_posts['total_mass_lb']:5.1f} lbs")
    print(f" TOTAL SIDE WALL JIG:     {tot_jig_lb:5.1f} lbs")
    print("-" * 80)

    # Save document
    fcstd_path = os.path.join(script_dir, "side_wall_buck.FCStd")
    doc.saveAs(fcstd_path)
    print(f" Saved side wall buck: {fcstd_path}")

    gui_doc = FreeCADGui.getDocument(doc.Name) if HAS_GUI else None
    if gui_doc:
        feat_foam.ViewObject.Transparency = 50
        doc.recompute()
        FreeCADGui.updateGui()
        prefix = os.path.join(script_dir, "side_wall_buck")
        export_orthogonal_views(gui_doc, base_prefix=prefix, width=1920, height=1080, bg_type="Transparent")

    FreeCAD.closeDocument(doc.Name)
    print(" Side Wall Planform Bending Jig complete!\n")


def main():
    print("=" * 80)
    print(" COMPACT FOAM CAMPER v0.3.0: COMPLETE FABRICATION BUCK SUITE BUILDER")
    print("=" * 80)

    build_master_assembly_buck()
    build_roof_canopy_buck()
    build_side_wall_buck()

    print("=" * 80)
    print(" ALL FABRICATION BUCKS GENERATED AND RENDERED SUCCESSFULLY!")
    print("=" * 80)
    os._exit(0)


if __name__ == "__main__":
    main()
