"""
Compact Foam Camper - Egg-Crate Plywood Buck Generator
Project: Rigid Internal Interlocking Buck for Scored XPS Foam Bending
Sized for 12' x 6.5' Camper Shell with 2.0" (50.8 mm) Inward Foam Thickness Offset

Features:
  - 5 Transverse Interlocking Bulkhead Ribs (3/4" CDX Plywood)
  - 3 Longitudinal Interlocking Stringers (Ridge Spine + Left/Right Shoulder Stringers)
  - Self-Squaring Half-Lap Interlocking Slots (19.5 mm / 0.77" width)
  - Central Interior Access / Weight Reduction Openings
  - Ghosted Transparent Outer Foam Shell Reference Overlay
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


def make_rib_face(x_pos, w_outer, h_outer, t_foam, slot_depth=120.0, t_ply=19.05, is_galley=False):
    """
    Creates a 2D transverse rib face with 2.0" inward offset from outer shell,
    interior crawl-through opening, and 3 half-lap slots cut down from the top.
    """
    w_rib_half = max((w_outer / 2.0) - t_foam, 200.0)
    h_rib = max(h_outer - t_foam, 300.0)
    w_top = w_rib_half * 0.84

    # Outer rib profile points in YZ plane
    p_bot_r   = FreeCAD.Vector(0, -w_rib_half, 0)
    p_mid_r   = FreeCAD.Vector(0, -w_rib_half, h_rib * 0.50)
    p_shldr_r = FreeCAD.Vector(0, -w_top,      h_rib * 0.88)
    p_apex    = FreeCAD.Vector(0, 0,           h_rib)
    p_shldr_l = FreeCAD.Vector(0,  w_top,      h_rib * 0.88)
    p_mid_l   = FreeCAD.Vector(0,  w_rib_half, h_rib * 0.50)
    p_bot_l   = FreeCAD.Vector(0,  w_rib_half, 0)

    edges_outer = [
        Part.makeLine(p_bot_l, p_bot_r),
        Part.makeLine(p_bot_r, p_mid_r),
        Part.BSplineCurve([p_mid_r, p_shldr_r, p_apex, p_shldr_l, p_mid_l]).toShape(),
        Part.makeLine(p_mid_l, p_bot_l),
    ]
    wire_outer = Part.Wire(edges_outer)
    face_outer = Part.Face(wire_outer)

    # Interior Crawl-Through / Weight Reduction Opening
    # If galley bulkhead, smaller pass-through / storage cutout
    wall_border = 140.0 if not is_galley else 250.0
    w_hole_half = max(w_rib_half - wall_border, 100.0)
    h_hole = max(h_rib - wall_border - 60.0, 150.0)

    q_bot_r   = FreeCAD.Vector(0, -w_hole_half, 80.0)
    q_shldr_r = FreeCAD.Vector(0, -w_hole_half * 0.80, h_hole * 0.80)
    q_apex    = FreeCAD.Vector(0, 0, h_hole)
    q_shldr_l = FreeCAD.Vector(0,  w_hole_half * 0.80, h_hole * 0.80)
    q_bot_l   = FreeCAD.Vector(0,  w_hole_half, 80.0)

    edges_hole = [
        Part.makeLine(q_bot_l, q_bot_r),
        Part.makeLine(q_bot_r, q_shldr_r),
        Part.BSplineCurve([q_shldr_r, q_apex, q_shldr_l]).toShape(),
        Part.makeLine(q_shldr_l, q_bot_l),
    ]
    wire_hole = Part.Wire(edges_hole)
    face_hole = Part.Face(wire_hole)

    rib_face = face_outer.cut(face_hole)

    # 3 Top Half-Lap Slots (Center Y=0, Left Y=+550, Right Y=-550)
    solid_rib = rib_face.extrude(FreeCAD.Vector(t_ply, 0, 0))
    solid_rib.translate(FreeCAD.Vector(x_pos - t_ply / 2.0, 0, 0))

    slot_w = t_ply + 0.5
    slot_box_ctr = Part.makeBox(slot_w * 2, slot_w, slot_depth * 1.5,
                                FreeCAD.Vector(x_pos - slot_w, -slot_w / 2.0, h_rib - slot_depth))
    solid_rib = solid_rib.cut(slot_box_ctr)

    y_shldr = min(550.0, w_rib_half * 0.70)
    h_at_shldr = h_rib * 0.90
    slot_box_l = Part.makeBox(slot_w * 2, slot_w, slot_depth * 1.5,
                              FreeCAD.Vector(x_pos - slot_w, y_shldr - slot_w / 2.0, h_at_shldr - slot_depth))
    slot_box_r = Part.makeBox(slot_w * 2, slot_w, slot_depth * 1.5,
                              FreeCAD.Vector(x_pos - slot_w, -y_shldr - slot_w / 2.0, h_at_shldr - slot_depth))
    solid_rib = solid_rib.cut(slot_box_l)
    solid_rib = solid_rib.cut(slot_box_r)

    return solid_rib


def make_stringer(y_pos, x_start, x_end, rib_stations, h_profile_fn, slot_depth=120.0, t_ply=19.05, stringer_depth=180.0):
    """
    Creates a longitudinal interlocking stringer with upward-facing half-lap slots
    at each rib station.
    """
    pts_top = []
    pts_bot = []
    step = 50.0
    x_curr = x_start
    while x_curr <= x_end:
        h_top = h_profile_fn(x_curr, y_pos)
        pts_top.append(FreeCAD.Vector(x_curr, 0, h_top))
        pts_bot.append(FreeCAD.Vector(x_curr, 0, max(h_top - stringer_depth, 0)))
        x_curr += step
    if pts_top[-1].x < x_end:
        h_top = h_profile_fn(x_end, y_pos)
        pts_top.append(FreeCAD.Vector(x_end, 0, h_top))
        pts_bot.append(FreeCAD.Vector(x_end, 0, max(h_top - stringer_depth, 0)))

    edges = []
    edges.append(Part.makeLine(pts_bot[0], pts_top[0]))
    edges.append(Part.BSplineCurve(pts_top).toShape())
    edges.append(Part.makeLine(pts_top[-1], pts_bot[-1]))
    pts_bot.reverse()
    edges.append(Part.BSplineCurve(pts_bot).toShape())

    wire = Part.Wire(edges)
    face = Part.Face(wire)
    solid = face.extrude(FreeCAD.Vector(0, t_ply, 0))
    solid.translate(FreeCAD.Vector(0, y_pos - t_ply / 2.0, 0))

    slot_w = t_ply + 0.5
    for x_rib in rib_stations:
        h_top = h_profile_fn(x_rib, y_pos)
        h_slot_bot = h_top - stringer_depth
        slot_cutter = Part.makeBox(slot_w, t_ply * 2, stringer_depth - slot_depth + 5.0,
                                   FreeCAD.Vector(x_rib - slot_w / 2.0, y_pos - t_ply, h_slot_bot))
        solid = solid.cut(slot_cutter)

    return solid


def build_buck():
    init_materials()
    doc_name = "camper_buck"
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Camper Fabrication Buck (Interlocking 3/4in Plywood Egg-Crate Jig)"

    L = 3658.0          # 12'-0"
    W = 1981.0          # 6'-6"
    H = 1750.0          # 5'-9"
    T_FOAM = 50.8       # 2.0" XPS Foam
    T_PLY = 19.05       # 3/4" CDX Plywood

    vars_dict = {
        "CamperLength": L,
        "CamperWidth": W,
        "CamperHeight": H,
        "FoamThickness": T_FOAM,
        "PlywoodThickness": T_PLY,
        "SlotDepth": 100.0,
        "StringerDepth": 180.0,
    }
    varset = create_varset(doc, "Vars", "Buck Parameters", vars_dict)

    stations = [
        {"name": "Rib_0_Nose",     "x": 60.0,   "w": W * 0.68, "h": 1080.0, "is_galley": False, "label": "Station 0: Nose Rib"},
        {"name": "Rib_1_Shoulder", "x": 1100.0, "w": W,        "h": H,      "is_galley": False, "label": "Station 1: Peak Shoulder Rib"},
        {"name": "Rib_2_MidCabin", "x": 1800.0, "w": W * 0.98, "h": 1720.0, "is_galley": False, "label": "Station 2: Mid-Cabin Rib"},
        {"name": "Rib_3_Galley",   "x": 2500.0, "w": W * 0.92, "h": 1580.0, "is_galley": True,  "label": "Station 3: Galley Bulkhead (Permanent)"},
        {"name": "Rib_4_Transom",  "x": 3580.0, "w": W * 0.74, "h": 920.0,  "is_galley": False, "label": "Station 4: Rear Transom Rib"},
    ]
    x_station_list = [s["x"] for s in stations]

    def get_buck_crown_height(x, y):
        if x <= 1100.0:
            u = max(x, 0) / 1100.0
            h_ctr = 1080.0 + (H - 1080.0) * math.sin(u * math.pi / 2.0)
        else:
            u = (x - 1100.0) / (L - 1100.0)
            h_ctr = H - (H - 920.0) * (u ** 1.35)

        camber_drop = (abs(y) / (W / 2.0)) ** 2 * 140.0
        return max(h_ctr - camber_drop - T_FOAM, 200.0)

    # 1. Transverse Ribs Container
    grp_ribs = doc.addObject("App::DocumentObjectGroup", "Transverse_Ribs")
    grp_ribs.Label = "1. Transverse Plywood Ribs (Egg-Crate Bulkheads)"

    for s in stations:
        rib_shape = make_rib_face(s["x"], s["w"], s["h"], T_FOAM,
                                  slot_depth=varset.SlotDepth.Value,
                                  t_ply=T_PLY,
                                  is_galley=s["is_galley"])
        feat_rib = doc.addObject("Part::Feature", s["name"])
        feat_rib.Label = s["label"]
        feat_rib.Shape = rib_shape
        apply_material(feat_rib, "Wood-PlywoodSheathing")
        grp_ribs.addObject(feat_rib)

    # 2. Longitudinal Stringers Container
    grp_stringers = doc.addObject("App::DocumentObjectGroup", "Longitudinal_Stringers")
    grp_stringers.Label = "2. Longitudinal Interlocking Stringers"

    # Ridge Spine
    spine_shape = make_stringer(0.0, stations[0]["x"], stations[-1]["x"], x_station_list,
                                get_buck_crown_height,
                                slot_depth=varset.SlotDepth.Value,
                                t_ply=T_PLY,
                                stringer_depth=varset.StringerDepth.Value)
    feat_spine = doc.addObject("Part::Feature", "Stringer_Center_Spine")
    feat_spine.Label = "Centerline Ridge Spine (Y = 0)"
    feat_spine.Shape = spine_shape
    apply_material(feat_spine, "Wood-PlywoodSheathing")
    grp_stringers.addObject(feat_spine)

    # Left & Right Shoulder Stringers
    y_sh = 550.0
    str_l_shape = make_stringer(y_sh, stations[0]["x"], stations[-1]["x"], x_station_list,
                                get_buck_crown_height,
                                slot_depth=varset.SlotDepth.Value,
                                t_ply=T_PLY,
                                stringer_depth=varset.StringerDepth.Value)
    feat_str_l = doc.addObject("Part::Feature", "Stringer_Left_Shoulder")
    feat_str_l.Label = "Left Shoulder Stringer (Y = +550 mm)"
    feat_str_l.Shape = str_l_shape
    apply_material(feat_str_l, "Wood-PlywoodSheathing")
    grp_stringers.addObject(feat_str_l)

    str_r_shape = make_stringer(-y_sh, stations[0]["x"], stations[-1]["x"], x_station_list,
                                get_buck_crown_height,
                                slot_depth=varset.SlotDepth.Value,
                                t_ply=T_PLY,
                                stringer_depth=varset.StringerDepth.Value)
    feat_str_r = doc.addObject("Part::Feature", "Stringer_Right_Shoulder")
    feat_str_r.Label = "Right Shoulder Stringer (Y = -550 mm)"
    feat_str_r.Shape = str_r_shape
    apply_material(feat_str_r, "Wood-PlywoodSheathing")
    grp_stringers.addObject(feat_str_r)

    # 3. Outer Foam Shell Reference Overlay
    grp_shell = doc.addObject("App::DocumentObjectGroup", "Foam_Shell_Overlay")
    grp_shell.Label = "3. Outer Foam Shell Reference (Ghosted Overlay)"

    s_wires = []
    for s in stations:
        w_half = s["w"] / 2.0
        w_top = w_half * 0.84
        h = s["h"]
        p1 = FreeCAD.Vector(s["x"], -w_half, 0)
        p2 = FreeCAD.Vector(s["x"], -w_half, h * 0.50)
        p3 = FreeCAD.Vector(s["x"], -w_top,  h * 0.88)
        p4 = FreeCAD.Vector(s["x"], 0,       h)
        p5 = FreeCAD.Vector(s["x"],  w_top,  h * 0.88)
        p6 = FreeCAD.Vector(s["x"],  w_half, h * 0.50)
        p7 = FreeCAD.Vector(s["x"],  w_half, 0)
        edges = [
            Part.makeLine(p7, p1),
            Part.makeLine(p1, p2),
            Part.BSplineCurve([p2, p3, p4, p5, p6]).toShape(),
            Part.makeLine(p6, p7),
        ]
        s_wires.append(Part.Wire(edges))

    shell_solid = Part.makeLoft(s_wires, True, False)
    feat_shell = doc.addObject("Part::Feature", "Ghost_Foam_Shell")
    feat_shell.Label = "2.0in Outer Foam Shell Envelope"
    feat_shell.Shape = shell_solid
    apply_material(feat_shell, "Polymer-XPS-Foam")
    grp_shell.addObject(feat_shell)

    doc.recompute()

    # Log Mass Report
    print("\n" + "="*80)
    print(" COMPACT FOAM CAMPER: PLYWOOD BUCK MASS & MATERIAL REPORT")
    print("="*80)
    rep_ribs = get_mass_properties(grp_ribs)
    rep_str = get_mass_properties(grp_stringers)
    total_ply_mass_lb = rep_ribs["total_mass_lb"] + rep_str["total_mass_lb"]
    total_ply_mass_kg = rep_ribs["total_mass_kg"] + rep_str["total_mass_kg"]
    print(f" Transverse Bulkheads (5 Ribs): {rep_ribs['total_mass_lb']:6.1f} lbs ({rep_ribs['total_mass_kg']:5.1f} kg)")
    print(f" Longitudinal Stringers (3 Spines): {rep_str['total_mass_lb']:6.1f} lbs ({rep_str['total_mass_kg']:5.1f} kg)")
    print(f" TOTAL EGG-CRATE BUCK WEIGHT:   {total_ply_mass_lb:6.1f} lbs ({total_ply_mass_kg:5.1f} kg)")
    print(f" Plywood Density: 600 kg/m³ (37.5 lb/cu.ft)")
    print("="*80 + "\n")

    doc.saveAs(fcstd_path)
    print(f"Saved buck master model to: {fcstd_path}")

    # Renders
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        FreeCADGui.updateGui()

        g_shell = gui_doc.getObject(feat_shell.Name)
        if g_shell:
            g_shell.Transparency = 75

        # 1. Complete Assembly View (Buck inside Ghost Shell)
        prefix_assembly = os.path.join(script_dir, "camper_buck_with_shell")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_assembly,
            width=1920,
            height=1080
        )
        print("Generated buck with ghost shell renders")

        # 2. Isolated Buck Skeleton View (Shell Hidden)
        if g_shell:
            g_shell.Visibility = False
        prefix_buck = os.path.join(script_dir, "camper_buck")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_buck,
            width=1920,
            height=1080
        )
        print("Generated isolated buck renders (camper_buck.png)")

        if g_shell:
            g_shell.Visibility = True
        doc.save()

    FreeCAD.closeDocument(doc.Name)
    print("Buck build complete!")


if __name__ == "__main__":
    build_buck()
    os._exit(0)
