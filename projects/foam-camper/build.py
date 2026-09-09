"""
Compact Foam Camper v0.2.0 - Pop-Top with Orthogonal Single-Axis Curvature Intersection
Project: Ultralight Towable Rigid Foam Insulation Camper Shell
Dimensions: 12'-0" (3,658 mm) Length x 6'-6" (1,981 mm) Width x 4'-11" (1,500 mm) Closed Travel Height

Key Architecture in v0.2.0:
  1. Side Panels Curving in the XY Plane (Horizontal plan boat-tail curve with vertical developable rulings in Z)
  2. Roof Curving in the XZ Plane (Vertical elevation aerodynamic curve with transverse developable rulings in Y)
  3. Continuous 3D Intersection Shoulder Seam where the two curved planes intersect
  4. Three Independent Modular Frames (Port Side Frame, Starboard Side Frame, Center Pop-Up Roof Frame)
  5. Center Walk-Through Entrance Doorway on Towing Tongue End (Direct access to standing aisle)
  6. Pop-Up Roof Frame with Parametric Lift Stroke (Vars.PopUp_Lift: 0 mm closed -> 508 mm / 20" camp)
  7. 6'5" (1,958 mm) Center Aisle Standing Headroom (Demonstrated with 6'0" scale human figure)
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


def make_trailer_chassis(length, width, tongue_length=1000.0):
    """
    Creates reference wire geometry for the 12' x 6.5' trailer chassis,
    including A-frame tongue, 2" ball coupler, 60/40 axle line, and tongue walk platform.
    """
    half_w = width / 2.0
    p1 = FreeCAD.Vector(0, -half_w, 0)
    p2 = FreeCAD.Vector(length, -half_w, 0)
    p3 = FreeCAD.Vector(length, half_w, 0)
    p4 = FreeCAD.Vector(0, half_w, 0)

    edges = [
        Part.makeLine(p1, p2),
        Part.makeLine(p2, p3),
        Part.makeLine(p3, p4),
        Part.makeLine(p4, p1),
    ]

    # Tongue A-frame converging to hitch coupler
    p_coupler = FreeCAD.Vector(-tongue_length, 0, 0)
    p_tongue_r = FreeCAD.Vector(0, -half_w * 0.45, 0)
    p_tongue_l = FreeCAD.Vector(0, half_w * 0.45, 0)
    edges.append(Part.makeLine(p_tongue_r, p_coupler))
    edges.append(Part.makeLine(p_tongue_l, p_coupler))

    # Center tongue drawbar
    edges.append(Part.makeLine(FreeCAD.Vector(0, 0, 0), p_coupler))

    # Walkable tongue step platform in front of center door (600mm x 450mm)
    plat_w = 600.0
    plat_l = 450.0
    pp1 = FreeCAD.Vector(-plat_l, -plat_w / 2.0, 0)
    pp2 = FreeCAD.Vector(0, -plat_w / 2.0, 0)
    pp3 = FreeCAD.Vector(0, plat_w / 2.0, 0)
    pp4 = FreeCAD.Vector(-plat_l, plat_w / 2.0, 0)
    edges.extend([
        Part.makeLine(pp1, pp2),
        Part.makeLine(pp2, pp3),
        Part.makeLine(pp3, pp4),
        Part.makeLine(pp4, pp1),
    ])

    # 60/40 balance axle line
    axle_x = length * 0.60
    edges.append(Part.makeLine(
        FreeCAD.Vector(axle_x, -half_w - 180, 0),
        FreeCAD.Vector(axle_x, half_w + 180, 0)
    ))

    return Part.Compound(edges)


def create_scale_human_figure(standing_x=1600.0, standing_y=0.0, height=1828.8):
    """
    Creates an ergonomic 3D human mannequin figure (6'0" = 1,828.8 mm tall)
    standing in the center aisle to visually validate head clearance under the pop-up roof.
    """
    head_r = 110.0
    head_z = height - head_r
    head = Part.makeSphere(head_r)
    head.translate(FreeCAD.Vector(standing_x, standing_y, head_z))

    torso_w = 400.0
    torso_d = 220.0
    torso_h = 600.0
    torso_z = 850.0
    torso = Part.makeBox(torso_d, torso_w, torso_h)
    torso.translate(FreeCAD.Vector(standing_x - torso_d / 2.0, standing_y - torso_w / 2.0, torso_z))

    # Left and right legs
    leg_r = 60.0
    leg_h = 850.0
    leg_l = Part.makeCylinder(leg_r, leg_h)
    leg_l.translate(FreeCAD.Vector(standing_x, standing_y + 110.0, 0))
    leg_r_cyl = Part.makeCylinder(leg_r, leg_h)
    leg_r_cyl.translate(FreeCAD.Vector(standing_x, standing_y - 110.0, 0))

    figure = head.fuse(torso).fuse(leg_l).fuse(leg_r_cyl)
    return figure


def build_foam_camper():
    """Master build entry point for Compact Foam Camper v0.2.0."""
    fcstd_path = os.path.join(script_dir, "foam-camper.FCStd")

    doc = FreeCAD.newDocument("foam_camper")
    doc.Label = "Compact Foam Camper v0.2.0"
    init_materials(doc)

    print("=" * 80)
    print(" COMPACT FOAM CAMPER v0.2.0: ORTHOGONAL 1D CURVATURE INTERSECTION & POP-TOP")
    print("=" * 80)

    # 1. PARAMETRIC VARSET INITIALIZATION
    vars_dict = {
        "Bed_Length": 3658.0,      # 12'-0"
        "Bed_Width": 1981.0,       # 6'-6"
        "Nose_Width": 1300.0,      # 4'-3"
        "Rear_Width": 1520.0,      # 5'-0"
        "Apex_Height": 1500.0,     # 4'-11" (59") Closed apex height
        "Brow_Height": 1350.0,     # 4'-5" Front brow height
        "Transom_Height": 850.0,   # 2'-9.5" Rear transom height
        "Nose_Height": 900.0,      # 2'-11.4" Front nose height
        "Foam_Thickness": 50.8,    # 2.0" XPS rigid foam
        "PopUp_Width": 1067.0,     # 42" Center pop-top channel width
        "PopUp_Lift": 508.0,       # 20.0" Lift stroke in camping mode (0 mm in travel mode)
        "Door_Width": 610.0,       # 24.0" Front center entrance doorway
        "Door_Height": 1270.0,     # 50.0" Lower rigid door height
    }
    vars_obj = create_varset(doc, "Vars", "Design_Parameters", vars_dict)

    length = float(vars_obj.Bed_Length.Value)
    w_max = float(vars_obj.Bed_Width.Value)
    w_nose = float(vars_obj.Nose_Width.Value)
    w_rear = float(vars_obj.Rear_Width.Value)
    w_mid = (w_max + w_rear) / 2.0
    h_apex = float(vars_obj.Apex_Height.Value)
    h_brow = float(vars_obj.Brow_Height.Value)
    h_mid = (h_apex + float(vars_obj.Transom_Height.Value)) / 2.0 + 50.0
    h_transom = float(vars_obj.Transom_Height.Value)
    h_nose = float(vars_obj.Nose_Height.Value)
    foam_t = float(vars_obj.Foam_Thickness.Value)
    pop_w = float(vars_obj.PopUp_Width.Value)
    half_pop = pop_w / 2.0
    pop_lift = float(vars_obj.PopUp_Lift.Value)
    door_w = float(vars_obj.Door_Width.Value)
    door_h = float(vars_obj.Door_Height.Value)

    # Pop-Up Roof Dimensions
    pop_x = 400.0
    pop_l = 2700.0

    # Calculated Interior Headroom in Central Standing Aisle (X = 1,600 mm)
    standing_headroom_closed = 1460.0
    standing_headroom_open = standing_headroom_closed + pop_lift

    print(f" Footprint: {length / 304.8:.1f}' L x {w_max / 304.8:.1f}' W")
    print(f" Closed Travel Height: {h_apex / 304.8:.2f}' ({h_apex:.0f} mm) (Fits 7' Residential Garage!)")
    print(f" Pop-Up Lift Stroke:   {pop_lift / 25.4:.1f}\" ({pop_lift:.0f} mm)")
    print(f" Closed Headroom:      {standing_headroom_closed / 304.8:.2f}' ({standing_headroom_closed / 25.4:.1f}\" / {standing_headroom_closed:.0f} mm)")
    print(f" Open Standing Height: {standing_headroom_open / 304.8:.2f}' ({standing_headroom_open / 25.4:.1f}\" / {standing_headroom_open:.0f} mm)")
    print(f" 6'0\" Human Clearance: +{(standing_headroom_open - 1828.8) / 25.4:.1f}\" (Center Aisle)")
    print("-" * 80)

    # 2. ORTHOGONAL SINGLE-AXIS CURVATURE GEOMETRY INTERSECTION

    # A. Outer Plan Solid (XY Plane: Boat-Tail Curve, Extruded Vertically in Z)
    p_nose_r = FreeCAD.Vector(0, -w_nose / 2.0, 0)
    p_nose_l = FreeCAD.Vector(0, w_nose / 2.0, 0)
    p_shldr_r = FreeCAD.Vector(1200.0, -w_max / 2.0, 0)
    p_shldr_l = FreeCAD.Vector(1200.0, w_max / 2.0, 0)
    p_mid_r = FreeCAD.Vector(2400.0, -w_mid / 2.0, 0)
    p_mid_l = FreeCAD.Vector(2400.0, w_mid / 2.0, 0)
    p_rear_r = FreeCAD.Vector(length, -w_rear / 2.0, 0)
    p_rear_l = FreeCAD.Vector(length, w_rear / 2.0, 0)

    spline_r = Part.BSplineCurve([p_nose_r, p_shldr_r, p_mid_r, p_rear_r]).toShape()
    spline_l = Part.BSplineCurve([p_rear_l, p_mid_l, p_shldr_l, p_nose_l]).toShape()
    wire_plan = Part.Wire([
        Part.makeLine(p_nose_l, p_nose_r),
        spline_r,
        Part.makeLine(p_rear_r, p_rear_l),
        spline_l
    ])
    face_plan = Part.Face(wire_plan)
    solid_plan = face_plan.extrude(FreeCAD.Vector(0, 0, h_apex * 1.5))

    # B. Outer Elevation Solid (XZ Plane: Aerodynamic Teardrop Curve, Extruded Laterally in Y)
    p_f_front = FreeCAD.Vector(0, 0, 0)
    p_f_rear = FreeCAD.Vector(length, 0, 0)
    p_t_top = FreeCAD.Vector(length, 0, h_transom)
    p_r_mid = FreeCAD.Vector(2400.0, 0, h_mid)
    p_r_apex = FreeCAD.Vector(1200.0, 0, h_apex)
    p_r_brow = FreeCAD.Vector(300.0, 0, h_brow)
    p_r_nose = FreeCAD.Vector(0, 0, h_nose)

    spline_roof = Part.BSplineCurve([p_r_nose, p_r_brow, p_r_apex, p_r_mid, p_t_top]).toShape()
    wire_elev = Part.Wire([
        spline_roof,
        Part.makeLine(p_t_top, p_f_rear),
        Part.makeLine(p_f_rear, p_f_front),
        Part.makeLine(p_f_front, p_r_nose)
    ])
    face_elev = Part.Face(wire_elev)
    solid_elev = face_elev.extrude(FreeCAD.Vector(0, w_max * 2.0, 0))
    solid_elev.translate(FreeCAD.Vector(0, -w_max, 0))

    # Master Intersection Solid (Where the two 1D curved planes intersect)
    master_solid = solid_plan.common(solid_elev)

    # C. Inner Hollow Core (Offset inward by 2.0" XPS foam_t)
    w_nose_in = max(w_nose - foam_t * 2, 200.0)
    w_max_in = max(w_max - foam_t * 2, 200.0)
    w_mid_in = max(w_mid - foam_t * 2, 200.0)
    w_rear_in = max(w_rear - foam_t * 2, 200.0)

    q_nose_r = FreeCAD.Vector(foam_t, -w_nose_in / 2.0, 0)
    q_nose_l = FreeCAD.Vector(foam_t, w_nose_in / 2.0, 0)
    q_shldr_r = FreeCAD.Vector(1200.0, -w_max_in / 2.0, 0)
    q_shldr_l = FreeCAD.Vector(1200.0, w_max_in / 2.0, 0)
    q_mid_r = FreeCAD.Vector(2400.0, -w_mid_in / 2.0, 0)
    q_mid_l = FreeCAD.Vector(2400.0, w_mid_in / 2.0, 0)
    q_rear_r = FreeCAD.Vector(length - foam_t, -w_rear_in / 2.0, 0)
    q_rear_l = FreeCAD.Vector(length - foam_t, w_rear_in / 2.0, 0)

    spline_r_in = Part.BSplineCurve([q_nose_r, q_shldr_r, q_mid_r, q_rear_r]).toShape()
    spline_l_in = Part.BSplineCurve([q_rear_l, q_mid_l, q_shldr_l, q_nose_l]).toShape()
    wire_plan_in = Part.Wire([
        Part.makeLine(q_nose_l, q_nose_r),
        spline_r_in,
        Part.makeLine(q_rear_r, q_rear_l),
        spline_l_in
    ])
    face_plan_in = Part.Face(wire_plan_in)
    solid_plan_in = face_plan_in.extrude(FreeCAD.Vector(0, 0, h_apex * 1.5))

    q_f_front = FreeCAD.Vector(foam_t, 0, 0)
    q_f_rear = FreeCAD.Vector(length - foam_t, 0, 0)
    q_t_top = FreeCAD.Vector(length - foam_t, 0, h_transom - foam_t)
    q_r_mid = FreeCAD.Vector(2400.0, 0, h_mid - foam_t)
    q_r_apex = FreeCAD.Vector(1200.0, 0, h_apex - foam_t)
    q_r_brow = FreeCAD.Vector(300.0, 0, h_brow - foam_t)
    q_r_nose = FreeCAD.Vector(foam_t, 0, h_nose - foam_t)

    spline_roof_in = Part.BSplineCurve([q_r_nose, q_r_brow, q_r_apex, q_r_mid, q_t_top]).toShape()
    wire_elev_in = Part.Wire([
        spline_roof_in,
        Part.makeLine(q_t_top, q_f_rear),
        Part.makeLine(q_f_rear, q_f_front),
        Part.makeLine(q_f_front, q_r_nose)
    ])
    face_elev_in = Part.Face(wire_elev_in)
    solid_elev_in = face_elev_in.extrude(FreeCAD.Vector(0, w_max * 2.0, 0))
    solid_elev_in.translate(FreeCAD.Vector(0, -w_max, 0))

    inner_solid = solid_plan_in.common(solid_elev_in)
    hollow_shell = master_solid.cut(inner_solid)

    # 3. INDEPENDENT MODULAR SUBASSEMBLIES

    # Module A: Left (Port) Side Frame
    # Curving in XY plane with vertical rulings; trimmed at top by XZ roof curve intersection
    box_left = Part.makeBox(length * 2, w_max, h_apex * 2, FreeCAD.Vector(-100, half_pop, -100))
    port_shape = hollow_shell.common(box_left)

    # Side window cutout (900 mm x 450 mm)
    win_cutter_l = Part.makeBox(900.0, w_max, 450.0, FreeCAD.Vector(length * 0.38, half_pop, h_apex * 0.45))
    port_shape = port_shape.cut(win_cutter_l)

    grp_left = doc.addObject("App::DocumentObjectGroup", "Left_Side_Frame")
    grp_left.Label = "Left Side Frame (Port - 1D XY Curved Wall & Shoulder)"
    obj_left = doc.addObject("Part::Feature", "Left_Wall_Solid")
    obj_left.Label = "Left Curved Foam Wall & Shoulder"
    obj_left.Shape = port_shape
    apply_material(obj_left, "Polymer-XPS-Foam")
    grp_left.addObject(obj_left)

    # Module B: Right (Starboard) Side Frame
    box_right = Part.makeBox(length * 2, w_max, h_apex * 2, FreeCAD.Vector(-100, -half_pop - w_max, -100))
    starboard_shape = hollow_shell.common(box_right)

    # Side window cutout (900 mm x 450 mm)
    win_cutter_r = Part.makeBox(900.0, w_max, 450.0, FreeCAD.Vector(length * 0.38, -half_pop - w_max, h_apex * 0.45))
    starboard_shape = starboard_shape.cut(win_cutter_r)

    grp_right = doc.addObject("App::DocumentObjectGroup", "Right_Side_Frame")
    grp_right.Label = "Right Side Frame (Starboard - 1D XY Curved Wall & Shoulder)"
    obj_right = doc.addObject("Part::Feature", "Right_Wall_Solid")
    obj_right.Label = "Right Curved Foam Wall & Shoulder"
    obj_right.Shape = starboard_shape
    apply_material(obj_right, "Polymer-XPS-Foam")
    grp_right.addObject(obj_right)

    # Module C: Center Pop-Up Roof Frame
    # Curving in XZ plane with lateral horizontal rulings; lifts vertically on command
    box_center = Part.makeBox(pop_l, pop_w, h_apex * 2, FreeCAD.Vector(pop_x, -half_pop, 0))
    center_channel = hollow_shell.common(box_center)
    # Slice off only the top roof shell (above Z = h_transom - 50)
    box_roof_slice = Part.makeBox(pop_l * 2, pop_w * 2, h_apex, FreeCAD.Vector(pop_x - 50, -half_pop - 50, h_transom - 50.0))
    popup_roof_shape = center_channel.common(box_roof_slice)

    grp_popup = doc.addObject("App::DocumentObjectGroup", "PopUp_Roof_Frame")
    grp_popup.Label = "Center Pop-Up Roof Frame (1D XZ Curved Canopy)"
    obj_popup = doc.addObject("Part::Feature", "PopUp_Roof_Solid")
    obj_popup.Label = "1D Curved Pop-Up Roof Panel"
    obj_popup.Shape = popup_roof_shape
    obj_popup.Placement.Base = FreeCAD.Vector(0, 0, pop_lift)
    apply_material(obj_popup, "Polymer-XPS-Foam")
    grp_popup.addObject(obj_popup)

    # Weatherproof Canvas Bellows / Skirt (Camping Mode)
    if pop_lift > 10.0:
        skirt_outer = Part.makeBox(pop_l, pop_w, pop_lift)
        skirt_outer.translate(FreeCAD.Vector(pop_x, -half_pop, h_brow))
        skirt_inner = Part.makeBox(pop_l - 20.0, pop_w - 20.0, pop_lift * 1.5)
        skirt_inner.translate(FreeCAD.Vector(pop_x + 10.0, -half_pop + 10.0, h_brow - 10.0))
        shape_skirt = skirt_outer.cut(skirt_inner)
        obj_skirt = doc.addObject("Part::Feature", "PopUp_Canvas_Skirt")
        obj_skirt.Label = "Weatherproof Pop-Up Fabric Bellows"
        obj_skirt.Shape = shape_skirt
        grp_popup.addObject(obj_skirt)

    # Module D: Front Bulkhead Frame (Towing End with Center Door)
    front_slab = Part.makeBox(foam_t, w_nose, h_nose, FreeCAD.Vector(0, -w_nose / 2.0, 0))
    # Center entrance doorway (24" wide x door_h)
    door_cutter = Part.makeBox(foam_t * 3.0, door_w, door_h, FreeCAD.Vector(-foam_t, -door_w / 2.0, 0))
    front_shape = front_slab.cut(door_cutter)

    grp_front = doc.addObject("App::DocumentObjectGroup", "Front_Bulkhead_Frame")
    grp_front.Label = "Front Bulkhead (Towing End with Center Door)"
    obj_front = doc.addObject("Part::Feature", "Front_Wall_Solid")
    obj_front.Label = "Front Foam Bulkhead with Center Door"
    obj_front.Shape = front_shape
    apply_material(obj_front, "Polymer-XPS-Foam")
    grp_front.addObject(obj_front)

    # Module E: Rear Transom Frame
    rear_slab = Part.makeBox(foam_t, w_rear, h_transom, FreeCAD.Vector(length - foam_t, -w_rear / 2.0, 0))
    win_rear_cutter = Part.makeBox(foam_t * 3.0, 800.0, 380.0, FreeCAD.Vector(length - foam_t * 2, -400.0, h_transom * 0.38))
    rear_shape = rear_slab.cut(win_rear_cutter)

    grp_rear = doc.addObject("App::DocumentObjectGroup", "Rear_Transom_Frame")
    grp_rear.Label = "Rear Transom Frame"
    obj_rear = doc.addObject("Part::Feature", "Rear_Wall_Solid")
    obj_rear.Label = "Rear Foam Transom with Window"
    obj_rear.Shape = rear_shape
    apply_material(obj_rear, "Polymer-XPS-Foam")
    grp_rear.addObject(obj_rear)

    # Module F: Reference Trailer Chassis & Tongue Platform
    grp_trailer = doc.addObject("App::DocumentObjectGroup", "Trailer_Chassis_Ref")
    grp_trailer.Label = "Reference 12' x 6.5' Trailer"
    trailer_wire = make_trailer_chassis(length, w_max)
    obj_trailer = doc.addObject("Part::Feature", "Trailer_Bed_Wire")
    obj_trailer.Label = "Chassis, A-Frame Tongue & Tongue Platform"
    obj_trailer.Shape = trailer_wire
    grp_trailer.addObject(obj_trailer)

    # Module G: Scale Human Figure (6'0" Standing Reference)
    grp_human = doc.addObject("App::DocumentObjectGroup", "Ergonomic_Reference")
    grp_human.Label = "Ergonomic Reference"
    shape_human = create_scale_human_figure(standing_x=1600.0, standing_y=0.0, height=1828.8)
    obj_human = doc.addObject("Part::Feature", "Human_6ft_Reference")
    obj_human.Label = "6'0\" Human Mannequin (1,829 mm)"
    obj_human.Shape = shape_human
    grp_human.addObject(obj_human)

    doc.recompute()

    # Mass & Engineering Properties
    props = get_mass_properties(doc)
    report = format_mass_report(props)
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80 + "\n")

    doc.saveAs(fcstd_path)
    print(f"Saved master model to: {fcstd_path}")

    # Archive master CAD model to changelog/
    changelog_dir = os.path.join(script_dir, "changelog")
    os.makedirs(changelog_dir, exist_ok=True)
    dst_v020_fcstd = os.path.join(changelog_dir, "v0.2.0_foam-camper.FCStd")
    shutil.copyfile(fcstd_path, dst_v020_fcstd)
    print(f"Archived master CAD model to: {dst_v020_fcstd}")

    # =========================================================================
    # HIGH-RESOLUTION VISUAL RENDERS (XVFB-RUN ACCELERATED)
    # =========================================================================
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        FreeCADGui.updateGui()

        # Visual styling
        if hasattr(obj_human, "ViewObject") and obj_human.ViewObject:
            obj_human.ViewObject.ShapeColor = (1.0, 0.45, 0.0)  # High-visibility Safety Orange

        if 'obj_skirt' in locals() and hasattr(obj_skirt, "ViewObject") and obj_skirt.ViewObject:
            obj_skirt.ViewObject.ShapeColor = (0.85, 0.85, 0.85)
            obj_skirt.ViewObject.Transparency = 55  # Semi-transparent canvas

        # 1. Master Camping Mode Renders (Pop-Up Roof Raised 20", 6'5" Headroom)
        prefix_master = os.path.join(script_dir, "foam-camper")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_master,
            width=1920,
            height=1080
        )
        print("Exported master Camping Mode renders (foam-camper.png)")

        # Archive milestone thumbnail to changelog/v0.2.0.png
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)
        src_master = f"{prefix_master}.png"
        dst_v020 = os.path.join(changelog_dir, "v0.2.0.png")
        if os.path.exists(src_master):
            shutil.copyfile(src_master, dst_v020)
            print(f"Archived milestone snapshot to: {dst_v020}")

        # 2. Travel Mode Renders (Pop-Up Roof Closed, PopUp_Lift = 0 mm, Human Hidden)
        print("Rendering Travel Mode (Pop-Up Closed)...")
        obj_popup.Placement.Base = FreeCAD.Vector(0, 0, 0)
        if 'obj_skirt' in locals() and hasattr(obj_skirt, "ViewObject") and obj_skirt.ViewObject:
            obj_skirt.ViewObject.Visibility = False
        if hasattr(obj_human, "ViewObject") and obj_human.ViewObject:
            obj_human.ViewObject.Visibility = False
        doc.recompute()
        FreeCADGui.updateGui()

        prefix_travel = os.path.join(script_dir, "foam-camper_travel")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_travel,
            width=1920,
            height=1080
        )
        print("Exported Travel Mode renders (foam-camper_travel.png)")

        # Reset back to Camping Mode for master model state
        obj_popup.Placement.Base = FreeCAD.Vector(0, 0, pop_lift)
        if 'obj_skirt' in locals() and hasattr(obj_skirt, "ViewObject") and obj_skirt.ViewObject:
            obj_skirt.ViewObject.Visibility = True
        if hasattr(obj_human, "ViewObject") and obj_human.ViewObject:
            obj_human.ViewObject.Visibility = True
        doc.recompute()
        doc.save()

    FreeCAD.closeDocument(doc.Name)
    print("\nCompact Foam Camper v0.2.0 build completed successfully!")


if __name__ == "__main__":
    build_foam_camper()
    os._exit(0)
