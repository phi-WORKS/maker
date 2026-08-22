import os
import sys
import math
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
from phi_works.maker.components import import_component

def set_vis(doc, obj, color):
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        if gui_d:
            g_obj = gui_d.getObject(obj.Name)
            if g_obj:
                g_obj.Visibility = True
                g_obj.ShapeColor = color
                g_obj.DisplayMode = "Flat Lines"

# ==========================================
# 1. SUBASSEMBLY BUILDER 1: HOOD & SKIDS
# ==========================================
def build_hood_subassembly(doc, grp_hood, dims, axle_y):
    BASE_W = dims.BaseWidth.Value
    BASE_L = dims.BaseLength.Value
    APEX_W = dims.ApexWidth.Value
    APEX_L = dims.ApexLength.Value
    HOOD_H = dims.HoodHeight.Value
    SKIRT_H = dims.SkirtHeight.Value
    SHEET_T = dims.SheetThickness.Value
    GROUND_CLR = 12.7    # 0.5 in ground clearance
    VENT_W = 304.8       # 12.0 in rear vent width
    VENT_H = 38.1        # 1.5 in rear vent height

    SKID_W = 38.1        # 1.5 in wide flat bar
    SKID_T = 4.76        # 3/16 in thick
    SKID_TIP_L = 50.8    # 2.0 in turned-up tip length
    SKID_TIP_ANGLE = 30  # 30 degree tip angle

    Z_skirt_bot = GROUND_CLR
    Z_base = Z_skirt_bot + SKIRT_H
    Z_apex = Z_base + HOOD_H

    # Pyramid Shell
    p_b0 = FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_base)
    p_b1 = FreeCAD.Vector(BASE_W/2, -BASE_L/2, Z_base)
    p_b2 = FreeCAD.Vector(BASE_W/2, BASE_L/2, Z_base)
    p_b3 = FreeCAD.Vector(-BASE_W/2, BASE_L/2, Z_base)

    p_a0 = FreeCAD.Vector(-APEX_W/2, -APEX_L/2, Z_apex)
    p_a1 = FreeCAD.Vector(APEX_W/2, -APEX_L/2, Z_apex)
    p_a2 = FreeCAD.Vector(APEX_W/2, APEX_L/2, Z_apex)
    p_a3 = FreeCAD.Vector(-APEX_W/2, APEX_L/2, Z_apex)

    pyr_outer = Part.makeLoft([
        Part.makePolygon([p_b0, p_b1, p_b2, p_b3, p_b0]),
        Part.makePolygon([p_a0, p_a1, p_a2, p_a3, p_a0])
    ], True)

    p_in_b0 = FreeCAD.Vector(-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, Z_base - 0.1)
    p_in_b1 = FreeCAD.Vector(BASE_W/2 - SHEET_T, -BASE_L/2 + SHEET_T, Z_base - 0.1)
    p_in_b2 = FreeCAD.Vector(BASE_W/2 - SHEET_T, BASE_L/2 - SHEET_T, Z_base - 0.1)
    p_in_b3 = FreeCAD.Vector(-BASE_W/2 + SHEET_T, BASE_L/2 - SHEET_T, Z_base - 0.1)

    p_in_a0 = FreeCAD.Vector(-APEX_W/2 + SHEET_T, -APEX_L/2 + SHEET_T, Z_apex + 0.1)
    p_in_a1 = FreeCAD.Vector(APEX_W/2 - SHEET_T, -APEX_L/2 + SHEET_T, Z_apex + 0.1)
    p_in_a2 = FreeCAD.Vector(APEX_W/2 - SHEET_T, APEX_L/2 - SHEET_T, Z_apex + 0.1)
    p_in_a3 = FreeCAD.Vector(-APEX_W/2 + SHEET_T, APEX_L/2 - SHEET_T, Z_apex + 0.1)

    pyr_inner = Part.makeLoft([
        Part.makePolygon([p_in_b0, p_in_b1, p_in_b2, p_in_b3, p_in_b0]),
        Part.makePolygon([p_in_a0, p_in_a1, p_in_a2, p_in_a3, p_in_a0])
    ], True)

    pyramid_shell = pyr_outer.cut(pyr_inner)

    # Skirt Box Shell
    skirt_outer = Part.makeBox(BASE_W, BASE_L, SKIRT_H, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_skirt_bot))
    skirt_inner = Part.makeBox(BASE_W - 2*SHEET_T, BASE_L - 2*SHEET_T, SKIRT_H + 0.2, FreeCAD.Vector(-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, Z_skirt_bot - 0.1))
    skirt_shell = skirt_outer.cut(skirt_inner)

    hood_full = pyramid_shell.fuse(skirt_shell)
    vent_box = Part.makeBox(VENT_W, SHEET_T * 4.0, VENT_H, FreeCAD.Vector(-VENT_W/2, BASE_L/2 - SHEET_T*2, Z_base - VENT_H))
    hood_with_vent = hood_full.cut(vent_box)

    # Perimeter Flange
    flange_outer = Part.makeBox(BASE_W + 25.4, BASE_L + 25.4, 4.76, FreeCAD.Vector(-BASE_W/2 - 12.7, -BASE_L/2 - 12.7, Z_skirt_bot))
    flange_inner = Part.makeBox(BASE_W, BASE_L, 5.0, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_skirt_bot - 0.1))
    perimeter_flange = flange_outer.cut(flange_inner)

    # Rear Cantilevered Axle Extension Arms extending back to axle_y (+280 mm)
    arm_w = 40.0
    arm_l = axle_y - (BASE_L/2 - 50.0) + 25.0
    arm_t = 4.76
    arm_left = Part.makeBox(arm_w, arm_l, arm_t, FreeCAD.Vector(-BASE_W/2 - arm_w, BASE_L/2 - 50.0, Z_skirt_bot))
    arm_right = Part.makeBox(arm_w, arm_l, arm_t, FreeCAD.Vector(BASE_W/2, BASE_L/2 - 50.0, Z_skirt_bot))
    
    # Dual Upright Pivot Ears for U-Handle & Axle Pins at axle_y
    ear_h = 65.0
    ear_l = 40.0
    ear_t = 4.76
    ear_l1 = Part.makeBox(ear_t, ear_l, ear_h, FreeCAD.Vector(-BASE_W/2 - 15.0 - ear_t, axle_y - ear_l/2, Z_skirt_bot))
    ear_l2 = Part.makeBox(ear_t, ear_l, ear_h, FreeCAD.Vector(-BASE_W/2 - 35.0, axle_y - ear_l/2, Z_skirt_bot))
    ear_r1 = Part.makeBox(ear_t, ear_l, ear_h, FreeCAD.Vector(BASE_W/2 + 15.0, axle_y - ear_l/2, Z_skirt_bot))
    ear_r2 = Part.makeBox(ear_t, ear_l, ear_h, FreeCAD.Vector(BASE_W/2 + 35.0 - ear_t, axle_y - ear_l/2, Z_skirt_bot))

    hood_assembly = hood_with_vent.fuse(perimeter_flange).fuse(arm_left).fuse(arm_right).fuse(ear_l1).fuse(ear_l2).fuse(ear_r1).fuse(ear_r2)
    hood_obj = doc.addObject("Part::Feature", "Pyramidal_Hood_Heat_Flange")
    hood_obj.Shape = hood_assembly
    grp_hood.addObject(hood_obj)

    # Corner Gussets
    gusset_shapes = []
    g_size = 100.0
    g_thick = 3.175
    corners = [
        (-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, 1, 1),
        (BASE_W/2 - SHEET_T, -BASE_L/2 + SHEET_T, -1, 1),
        (BASE_W/2 - SHEET_T, BASE_L/2 - SHEET_T, -1, -1),
        (-BASE_W/2 + SHEET_T, BASE_L/2 - SHEET_T, 1, -1)
    ]
    for cx, cy, dx, dy in corners:
        gp1 = FreeCAD.Vector(cx, cy, Z_base)
        gp2 = FreeCAD.Vector(cx + dx * g_size, cy, Z_base)
        gp3 = FreeCAD.Vector(cx, cy + dy * g_size, Z_base)
        g_face = Part.Face(Part.makePolygon([gp1, gp2, gp3, gp1]))
        g_solid = g_face.extrude(FreeCAD.Vector(0, 0, g_thick))
        gusset_shapes.append(g_solid)

    all_gussets = gusset_shapes[0]
    for g in gusset_shapes[1:]:
        all_gussets = all_gussets.fuse(g)

    gussets_obj = doc.addObject("Part::Feature", "Corner_Gussets_AngleIron")
    gussets_obj.Shape = all_gussets
    grp_hood.addObject(gussets_obj)

    # Dual Skids
    def make_skid_runner(x_pos):
        main_bar = Part.makeBox(SKID_W, BASE_L, SKID_T, FreeCAD.Vector(x_pos - SKID_W/2, -BASE_L/2, 0))
        front_tip_box = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(x_pos - SKID_W/2, -BASE_L/2 - SKID_TIP_L, 0))
        front_tip_box.rotate(FreeCAD.Vector(x_pos, -BASE_L/2, 0), FreeCAD.Vector(1, 0, 0), -SKID_TIP_ANGLE)
        rear_tip_box = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(x_pos - SKID_W/2, BASE_L/2, 0))
        rear_tip_box.rotate(FreeCAD.Vector(x_pos, BASE_L/2, 0), FreeCAD.Vector(1, 0, 0), SKID_TIP_ANGLE)
        return main_bar.fuse(front_tip_box).fuse(rear_tip_box)

    left_skid = make_skid_runner(-BASE_W/2 + SKID_W/2)
    right_skid = make_skid_runner(BASE_W/2 - SKID_W/2)
    dual_skids = left_skid.fuse(right_skid)

    skids_obj = doc.addObject("Part::Feature", "Dual_Skid_Runners")
    skids_obj.Shape = dual_skids
    grp_hood.addObject(skids_obj)

    return hood_obj, gussets_obj, skids_obj

# ==========================================
# 2. SUBASSEMBLY BUILDER 2: OVERHEAD MOUNTING FRAME
# ==========================================
def build_overhead_frame_subassembly(doc, grp_frame, dims):
    APEX_W = dims.ApexWidth.Value
    APEX_L = dims.ApexLength.Value
    HOOD_H = dims.HoodHeight.Value
    SKIRT_H = dims.SkirtHeight.Value
    GROUND_CLR = 12.7
    TORCH_ANGLE = 35.0

    Z_apex = GROUND_CLR + SKIRT_H + HOOD_H

    f_height = 80.0
    f_width = APEX_W + 50.0
    f_thick = 4.76
    leg_l = Part.makeBox(f_thick, APEX_L, f_height, FreeCAD.Vector(-f_width/2, -APEX_L/2, Z_apex))
    leg_r = Part.makeBox(f_thick, APEX_L, f_height, FreeCAD.Vector(f_width/2 - f_thick, -APEX_L/2, Z_apex))
    bridge = Part.makeBox(f_width, 38.1, f_thick, FreeCAD.Vector(-f_width/2, -19.05, Z_apex + f_height - f_thick))

    # Wand leans towards rear (+Y) where handle, tank, and operator are located
    wand_lean_dir = FreeCAD.Vector(0, math.sin(math.radians(TORCH_ANGLE)), math.cos(math.radians(TORCH_ANGLE)))

    clamp_sleeve = Part.makeCylinder(25.4, 60.0, FreeCAD.Vector(0, -10.0, Z_apex + f_height/2), wand_lean_dir)
    clamp_inner = Part.makeCylinder(19.05, 70.0, FreeCAD.Vector(0, -12.0, Z_apex + f_height/2 - 5.0), wand_lean_dir)
    sleeve_ring = clamp_sleeve.cut(clamp_inner)

    # Rear Latch Catch Tower (for Upright Vacuum Snap Catch towards +Y)
    latch_catch_bracket = Part.makeBox(38.1, 25.4, 40.0, FreeCAD.Vector(-19.05, APEX_L/2, Z_apex + f_height - 40.0))
    catch_slot = Part.makeBox(40.0, 10.0, 15.0, FreeCAD.Vector(-20.0, APEX_L/2 + 10.0, Z_apex + f_height - 25.0))
    catch_body = latch_catch_bracket.cut(catch_slot)

    torch_frame_obj = doc.addObject("Part::Feature", "Overhead_Torch_Mounting_Frame")
    torch_frame_obj.Shape = leg_l.fuse(leg_r).fuse(bridge).fuse(sleeve_ring).fuse(catch_body)
    grp_frame.addObject(torch_frame_obj)

    return torch_frame_obj

# ==========================================
# 3. SUBASSEMBLY BUILDER 3: HARBOR FREIGHT TORCH
# ==========================================
def build_torch_subassembly(doc, grp_torch, dims):
    HOOD_H = dims.HoodHeight.Value
    SKIRT_H = dims.SkirtHeight.Value
    GROUND_CLR = 12.7
    NOZZLE_RECESS = 38.1
    Z_apex = GROUND_CLR + SKIRT_H + HOOD_H

    # Nozzle centered in hood opening, wand leaning towards +Y (operator/handle side)
    nozzle_pos = FreeCAD.Vector(0, 30.0, Z_apex - NOZZLE_RECESS)
    torch_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180)
    torch_placement = FreeCAD.Placement(nozzle_pos, torch_rot)
    torch_grp = import_component(doc, "torch_hf91037", placement=torch_placement, group_label="Harbor Freight Torch #91037 Component")
    
    for obj in torch_grp.Group:
        grp_torch.addObject(obj)

    return torch_grp

# ==========================================
# 4. SUBASSEMBLY BUILDER 4: DUAL STEEL WHEELS & AXLES
# ==========================================
def build_wheels_subassembly(doc, grp_wheels, dims, axle_y):
    BASE_W = dims.BaseWidth.Value
    WHEEL_DIA = dims.WheelDiameter.Value
    WHEEL_R = WHEEL_DIA / 2.0
    AXLE_Y = axle_y
    AXLE_Z = WHEEL_R # Axle center aligned so wheel bottom is at Z = 0 (ground level)

    left_wheel_x = -BASE_W/2 - 55.0
    right_wheel_x = BASE_W/2 + 55.0

    # Import Left Wheel (Bracket-less solid wheel)
    placement_left = FreeCAD.Placement(FreeCAD.Vector(left_wheel_x, AXLE_Y, AXLE_Z), FreeCAD.Rotation())
    left_wheel_grp = import_component(doc, "steel_caster_wheel", placement=placement_left, group_label="Left 4\" Solid Steel Wheel")
    for obj in left_wheel_grp.Group:
        grp_wheels.addObject(obj)

    # Import Right Wheel (Bracket-less solid wheel)
    placement_right = FreeCAD.Placement(FreeCAD.Vector(right_wheel_x, AXLE_Y, AXLE_Z), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180))
    right_wheel_grp = import_component(doc, "steel_caster_wheel", placement=placement_right, group_label="Right 4\" Solid Steel Wheel")
    for obj in right_wheel_grp.Group:
        grp_wheels.addObject(obj)

    # Dual Axle Pivot Pins connecting through side chassis ears
    pin_d = 12.7
    pin_l = 80.0
    pin_left = Part.makeCylinder(pin_d/2, pin_l, FreeCAD.Vector(-BASE_W/2 - 70.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    pin_right = Part.makeCylinder(pin_d/2, pin_l, FreeCAD.Vector(BASE_W/2 - 10.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    pins_solid = pin_left.fuse(pin_right)

    pins_obj = doc.addObject("Part::Feature", "Chassis_Pivot_Axle_Pins")
    pins_obj.Shape = pins_solid
    grp_wheels.addObject(pins_obj)

    return left_wheel_grp, right_wheel_grp, pins_obj, FreeCAD.Vector(0, AXLE_Y, AXLE_Z)

# ==========================================
# 5. SUBASSEMBLY BUILDER 5: U-HANDLE & TILT LATCH
# ==========================================
def build_handle_frame_subassembly(doc, grp_handle, dims, axle_center):
    BASE_W = dims.BaseWidth.Value
    HANDLE_L = dims.HandleLength.Value
    HANDLE_W = dims.HandleWidth.Value
    HANDLE_SQ = 19.05   # 3/4" square steel tube (0.75 in)
    HANDLE_ANGLE = 40.0 # 40 deg upright ergonomic angle leaning towards rear (+Y)

    AXLE_Y = axle_center.y
    AXLE_Z = axle_center.z

    # Direction vector of U-handle pointing rearward-upward (+Y, +Z) toward operator
    handle_dir = FreeCAD.Vector(0, math.sin(math.radians(HANDLE_ANGLE)), math.cos(math.radians(HANDLE_ANGLE)))

    # Left & Right Upright Tubes
    left_x = -HANDLE_W/2
    right_x = HANDLE_W/2

    # Prototype vertical tube oriented along handle_dir (-HANDLE_ANGLE around X rotates +Z toward +Y)
    tube_proto = Part.makeBox(HANDLE_SQ, HANDLE_SQ, HANDLE_L, FreeCAD.Vector(-HANDLE_SQ/2, -HANDLE_SQ/2, 0))
    tube_proto.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0), -HANDLE_ANGLE)

    tube_left = tube_proto.copy()
    tube_left.translate(FreeCAD.Vector(left_x, AXLE_Y, AXLE_Z))

    tube_right = tube_proto.copy()
    tube_right.translate(FreeCAD.Vector(right_x, AXLE_Y, AXLE_Z))

    # Top Ergonomic Crossbar Handle & Rubber Grips directly spanning across the tops of the verticals
    top_pos = FreeCAD.Vector(0, AXLE_Y, AXLE_Z) + handle_dir * HANDLE_L
    crossbar_w = HANDLE_W + 100.0
    top_crossbar = Part.makeCylinder(12.7, crossbar_w, top_pos + FreeCAD.Vector(-crossbar_w/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    grip_left = Part.makeCylinder(15.8, 120.0, top_pos + FreeCAD.Vector(-crossbar_w/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    grip_right = Part.makeCylinder(15.8, 120.0, top_pos + FreeCAD.Vector(crossbar_w/2 - 120.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    top_assembly = top_crossbar.fuse(grip_left).fuse(grip_right)

    # Middle Cross-Brace (Directly connected between verticals, mounting spine for 1 lb Propane Tank)
    mid_pos = FreeCAD.Vector(0, AXLE_Y, AXLE_Z) + handle_dir * 650.0
    mid_brace = Part.makeBox(HANDLE_W, 38.1, 4.76, FreeCAD.Vector(-HANDLE_W/2, -19.05, -2.38))
    mid_brace.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -HANDLE_ANGLE)
    mid_brace.translate(mid_pos)

    # Lower Cross-Brace (Directly connected between verticals, striker for Upright-Vacuum Tilt Latch)
    low_pos = FreeCAD.Vector(0, AXLE_Y, AXLE_Z) + handle_dir * 280.0
    low_brace = Part.makeBox(HANDLE_W, 25.4, 4.76, FreeCAD.Vector(-HANDLE_W/2, -12.7, -2.38))
    low_brace.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -HANDLE_ANGLE)
    low_brace.translate(low_pos)

    # Dual Lower Pivot Eye Clevis Ends (connecting to axle pins)
    clevis_l = Part.makeCylinder(15.0, HANDLE_SQ + 6.0, FreeCAD.Vector(left_x - (HANDLE_SQ+6)/2, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    clevis_r = Part.makeCylinder(15.0, HANDLE_SQ + 6.0, FreeCAD.Vector(right_x - (HANDLE_SQ+6)/2, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))

    u_frame_solid = tube_left.fuse(tube_right).fuse(top_assembly).fuse(mid_brace).fuse(low_brace).fuse(clevis_l).fuse(clevis_r)

    handle_obj = doc.addObject("Part::Feature", "HandTruck_U_Frame_Handle")
    handle_obj.Shape = u_frame_solid
    grp_handle.addObject(handle_obj)

    # Upright Vacuum Style Snap Tilt-Back Latch
    # Latch link locking handle low_brace to overhead frame catch tower
    latch_body = Part.makeBox(25.4, 160.0, 12.7, FreeCAD.Vector(-12.7, low_pos.y - 160.0, low_pos.z))
    latch_hook = Part.makeBox(35.0, 25.0, 25.4, FreeCAD.Vector(-17.5, low_pos.y - 160.0, low_pos.z - 10.0))
    foot_pedal_tab = Part.makeBox(60.0, 30.0, 6.35, FreeCAD.Vector(-30.0, low_pos.y - 50.0, low_pos.z + 12.7))
    latch_solid = latch_body.fuse(latch_hook).fuse(foot_pedal_tab)

    latch_obj = doc.addObject("Part::Feature", "Tilt_Back_Vacuum_Snap_Latch")
    latch_obj.Shape = latch_solid
    grp_handle.addObject(latch_obj)

    return handle_obj, latch_obj, mid_pos, handle_dir

# ==========================================
# 6. SUBASSEMBLY BUILDER 6: PROPANE HARNESS & FUEL
# ==========================================
def build_propane_subassembly(doc, grp_fuel, mid_pos, handle_dir):
    # Mount harness on middle crossbar of U-handle (leaning towards +Y)
    rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -40.0)
    harness_placement = FreeCAD.Placement(mid_pos + FreeCAD.Vector(0, 10.0, 10.0), rot)

    harness_grp = import_component(doc, "propane_harness", placement=harness_placement, group_label="Propane Bottle Harness Component")
    for obj in harness_grp.Group:
        grp_fuel.addObject(obj)

    # Seat 1 lb Cylinder inside harness
    cylinder_base_pos = mid_pos + FreeCAD.Vector(0, math.sin(math.radians(40.0))*2.0 + 10.0, math.cos(math.radians(40.0))*2.0 + 10.0)
    cylinder_placement = FreeCAD.Placement(cylinder_base_pos, rot)
    
    cylinder_grp = import_component(doc, "propane_cylinder_1lb", placement=cylinder_placement, group_label="1 lb Propane Cylinder Component")
    for obj in cylinder_grp.Group:
        grp_fuel.addObject(obj)

    # Flexible High-Pressure Propane Line Hose routing to Torch Wand
    valve_top_pos = cylinder_base_pos + FreeCAD.Vector(0, math.sin(math.radians(40.0))*198.0, math.cos(math.radians(40.0))*198.0)
    torch_knob_pos = FreeCAD.Vector(0, 250.0, 480.0)

    hose_path = Part.makeCylinder(4.0, (torch_knob_pos - valve_top_pos).Length, valve_top_pos, (torch_knob_pos - valve_top_pos).normalize())
    hose_obj = doc.addObject("Part::Feature", "High_Pressure_Propane_Extension_Hose")
    hose_obj.Shape = hose_path
    grp_fuel.addObject(hose_obj)

    return harness_grp, cylinder_grp, hose_obj

# ==========================================
# MAIN ORCHESTRATOR FUNCTION: build()
# ==========================================
def build():
    STEEL_DARK = (0.28, 0.30, 0.33, 0.0)      # 14-ga Hood & Skirts
    STEEL_BRIGHT = (0.55, 0.58, 0.62, 0.0)    # Skids, Frame, Gussets, Pins
    TOWBAR_YELLOW = (0.90, 0.70, 0.10, 0.0)  # High-Vis Powdercoated U-Handle Frame
    LATCH_RED = (0.85, 0.20, 0.20, 0.0)       # Foot Pedal Snap Latch
    HOSE_BLACK = (0.08, 0.08, 0.08, 0.0)      # High-Pressure Rubber Hose

    model = FreeCAD.newDocument("road_roaster")
    model.Label = "Road Roaster - Upright Vacuum Tilt-Back Thermal Sled"

    # 0. SUBASSEMBLY PART CONTAINERS
    grp_hood = model.addObject("App::DocumentObjectGroup", "Hood_Subassembly")
    grp_hood.Label = "1. Pyramid Hood & Skid Subassembly"

    grp_frame = model.addObject("App::DocumentObjectGroup", "Overhead_Frame_Subassembly")
    grp_frame.Label = "2. Overhead Torch Mounting Frame"

    grp_torch = model.addObject("App::DocumentObjectGroup", "Harbor_Freight_Torch_Subassembly")
    grp_torch.Label = "3. Harbor Freight #91037 Torch Subassembly"

    grp_wheels = model.addObject("App::DocumentObjectGroup", "Dual_Wheels_Subassembly")
    grp_wheels.Label = "4. Dual Metal Wheel & Axle Subassembly"

    grp_handle = model.addObject("App::DocumentObjectGroup", "HandTruck_Handle_Subassembly")
    grp_handle.Label = "5. Dual-Pivot U-Handle & Tilt Latch Subassembly"

    grp_fuel = model.addObject("App::DocumentObjectGroup", "Propane_Fuel_Subassembly")
    grp_fuel.Label = "6. Propane Bottle Harness & Tank Subassembly"

    # 1. PARAMETRIC VARSET (dims)
    dims = model.addObject("App::VarSet", "dims")
    
    BASE_W = 457.2       # 18.0 in
    BASE_L = 457.2       # 18.0 in
    APEX_W = 101.6       # 4.0 in top apex opening
    APEX_L = 101.6       # 4.0 in top apex opening
    HOOD_H = 152.4       # 6.0 in vertical height
    SKIRT_H = 50.8       # 2.0 in vertical skirt extension
    SHEET_T = 1.905      # 14-gauge mild steel (0.075 in)
    WHEEL_DIA = 101.6    # 4.0 in metal wheel diameter
    TRACK_W = 533.4      # 21.0 in wheel track width
    HANDLE_L = 1219.2    # 48.0 in upright handle length
    HANDLE_W = 482.6     # 19.0 in U-handle frame width

    dims.addProperty("App::PropertyLength", "BaseWidth", "Dimensions", "Hood Base Width").BaseWidth = BASE_W
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Hood Base Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "ApexWidth", "Dimensions", "Top Apex Width").ApexWidth = APEX_W
    dims.addProperty("App::PropertyLength", "ApexLength", "Dimensions", "Top Apex Length").ApexLength = APEX_L
    dims.addProperty("App::PropertyLength", "HoodHeight", "Dimensions", "Pyramid Rise Height").HoodHeight = HOOD_H
    dims.addProperty("App::PropertyLength", "SkirtHeight", "Dimensions", "Vertical Skirt Height").SkirtHeight = SKIRT_H
    dims.addProperty("App::PropertyLength", "SheetThickness", "Dimensions", "14-ga Steel Thickness").SheetThickness = SHEET_T
    dims.addProperty("App::PropertyLength", "WheelDiameter", "Dimensions", "Caster Wheel Diameter").WheelDiameter = WHEEL_DIA
    dims.addProperty("App::PropertyLength", "TrackWidth", "Dimensions", "Wheel Track Width").TrackWidth = TRACK_W
    dims.addProperty("App::PropertyLength", "HandleLength", "Dimensions", "U-Handle Frame Length").HandleLength = HANDLE_L
    dims.addProperty("App::PropertyLength", "HandleWidth", "Dimensions", "U-Handle Frame Width").HandleWidth = HANDLE_W

    # Wheels and handle pivot set back behind the rear of the sled
    AXLE_Y = 280.0  # Set back behind the sled rear edge (BASE_L/2 = 228.6 mm)

    # 2. BUILD SUBASSEMBLIES
    hood_obj, gussets_obj, skids_obj = build_hood_subassembly(model, grp_hood, dims, AXLE_Y)
    torch_frame_obj = build_overhead_frame_subassembly(model, grp_frame, dims)
    torch_grp = build_torch_subassembly(model, grp_torch, dims)
    left_wheel_grp, right_wheel_grp, pins_obj, axle_center = build_wheels_subassembly(model, grp_wheels, dims, AXLE_Y)
    handle_obj, latch_obj, mid_pos, handle_dir = build_handle_frame_subassembly(model, grp_handle, dims, axle_center)
    harness_grp, cylinder_grp, hose_obj = build_propane_subassembly(model, grp_fuel, mid_pos, handle_dir)

    model.recompute()

    # Apply Visual Colors
    color_map = {
        hood_obj: STEEL_DARK,
        gussets_obj: STEEL_BRIGHT,
        skids_obj: STEEL_BRIGHT,
        torch_frame_obj: STEEL_BRIGHT,
        pins_obj: STEEL_BRIGHT,
        handle_obj: TOWBAR_YELLOW,
        latch_obj: LATCH_RED,
        hose_obj: HOSE_BLACK
    }

    for obj, color in color_map.items():
        set_vis(model, obj, color)

    # Save outputs
    fc_file = os.path.join(script_dir, "road-roaster.FCStd")
    png_file = os.path.join(script_dir, "road-roaster.png")
    model.saveAs(fc_file)

    if HAS_GUI:
        try:
            import FreeCADGui
            gui_d = FreeCADGui.getDocument(model.Name)
            if gui_d:
                base_prefix = os.path.join(script_dir, "road-roaster")
                export_orthogonal_views(gui_d, base_prefix)
        except Exception as e:
            print(f"Render error: {e}")

    FreeCAD.closeDocument("road_roaster")
    print(f"Successfully created Road Roaster v0.5.0 master model & multi-view renders in {script_dir}")

if __name__ == "__main__":
    build()
    sys.exit(0)
