import os
import sys
import math
import FreeCAD
import Part

# Ensure src directory is on sys.path for shared imports
maker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
src_dir = os.path.join(maker_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views

def set_vis(doc, obj, color):
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        if gui_d:
            g_obj = gui_d.getObject(obj.Name)
            if g_obj:
                g_obj.Visibility = True
                g_obj.ShapeColor = color
                g_obj.DisplayMode = "Flat Lines"

def build_v4():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
    sled_dir = os.path.dirname(script_dir)

    STEEL_DARK = (0.28, 0.30, 0.33, 0.0)      # 14-ga Hood & Skirts (Hot Rolled Steel)
    STEEL_BRIGHT = (0.55, 0.58, 0.62, 0.0)    # Skids, Frame, Clevis, Angle Iron
    BRASS = (0.85, 0.65, 0.20, 0.0)           # Valve & Brass Fittings
    HF_BLUE = (0.10, 0.35, 0.80, 0.0)         # Harbor Freight Handle Blue
    TORCH_BLACK = (0.15, 0.15, 0.15, 0.0)     # Torch Grip & Burner Head
    CHROME = (0.75, 0.78, 0.82, 0.0)          # Torch Wand Metal Shaft
    IGNITER_RED = (0.85, 0.15, 0.15, 0.0)     # Push-button Igniter
    PROPANE_GREEN = (0.12, 0.48, 0.22, 0.0)   # 1 lb Propane Cylinder
    TOWBAR_YELLOW = (0.88, 0.68, 0.12, 0.0)  # High-Vis Powdercoated Tow Bar

    v4_doc = FreeCAD.newDocument("caddy_v4")
    v4_doc.Label = "Flame Sled v4 - Subassembly Part Containers"

    # ==========================================
    # 0. SUBASSEMBLY PART CONTAINERS (v4)
    # ==========================================
    grp_hood = v4_doc.addObject("App::DocumentObjectGroup", "Hood_Subassembly")
    grp_hood.Label = "1. Pyramid Hood & Skid Subassembly"

    grp_frame = v4_doc.addObject("App::DocumentObjectGroup", "Overhead_Frame_Subassembly")
    grp_frame.Label = "2. Overhead Torch Mounting Frame"

    grp_torch = v4_doc.addObject("App::DocumentObjectGroup", "Harbor_Freight_Torch_Subassembly")
    grp_torch.Label = "3. Harbor Freight #91037 Torch Subassembly"

    grp_tow = v4_doc.addObject("App::DocumentObjectGroup", "Tow_Rigging_Subassembly")
    grp_tow.Label = "4. Forward Tow Rigging Subassembly"

    # ==========================================
    # 1. PARAMETRIC VARSET (dims)
    # ==========================================
    dims = v4_doc.addObject("App::VarSet", "dims")
    
    BASE_W = 457.2       # 18.0 in
    BASE_L = 457.2       # 18.0 in
    APEX_W = 101.6       # 4.0 in top apex opening
    APEX_L = 101.6       # 4.0 in top apex opening
    HOOD_H = 152.4       # 6.0 in vertical height
    SKIRT_H = 50.8       # 2.0 in vertical skirt extension
    SHEET_T = 1.905      # 14-gauge mild steel (0.075 in)
    GROUND_CLR = 12.7    # 0.5 in ground clearance
    VENT_W = 304.8       # 12.0 in rear vent width
    VENT_H = 38.1        # 1.5 in rear vent height

    SKID_W = 38.1        # 1.5 in wide flat bar
    SKID_T = 4.76        # 3/16 in thick
    SKID_TIP_L = 50.8    # 2.0 in turned-up tip length
    SKID_TIP_ANGLE = 30  # 30 degree tip angle

    TORCH_ANGLE = 35.0   # 35 deg incline from vertical
    NOZZLE_RECESS = 38.1 # Recessed into apex chamber

    TOWBAR_L = 1524.0    # 5.0 ft (60.0 in)
    TOWBAR_SQ = 19.05    # 3/4 in square tube
    STOP_ANGLE = 20.0    # 20 deg minimum tow bar rest tab angle
    CLEVIS_PIN_D = 9.525 # 3/8 in pin

    dims.addProperty("App::PropertyLength", "BaseWidth", "Dimensions", "Hood Base Width").BaseWidth = BASE_W
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Hood Base Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "ApexWidth", "Dimensions", "Top Apex Width").ApexWidth = APEX_W
    dims.addProperty("App::PropertyLength", "ApexLength", "Dimensions", "Top Apex Length").ApexLength = APEX_L
    dims.addProperty("App::PropertyLength", "HoodHeight", "Dimensions", "Pyramid Rise Height").HoodHeight = HOOD_H
    dims.addProperty("App::PropertyLength", "SkirtHeight", "Dimensions", "Vertical Skirt Height").SkirtHeight = SKIRT_H
    dims.addProperty("App::PropertyLength", "SheetThickness", "Dimensions", "14-ga Steel Thickness").SheetThickness = SHEET_T
    dims.addProperty("App::PropertyLength", "TowBarLength", "Dimensions", "Tow Bar Length").TowBarLength = TOWBAR_L

    Z_skirt_bot = GROUND_CLR
    Z_base = Z_skirt_bot + SKIRT_H
    Z_apex = Z_base + HOOD_H

    # ==========================================
    # 2. SUBASSEMBLY 1: HOOD & SKIDS
    # ==========================================
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

    skirt_outer = Part.makeBox(BASE_W, BASE_L, SKIRT_H, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_skirt_bot))
    skirt_inner = Part.makeBox(BASE_W - 2*SHEET_T, BASE_L - 2*SHEET_T, SKIRT_H + 0.2, FreeCAD.Vector(-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, Z_skirt_bot - 0.1))
    skirt_shell = skirt_outer.cut(skirt_inner)

    hood_full = pyramid_shell.fuse(skirt_shell)
    vent_box = Part.makeBox(VENT_W, SHEET_T * 4.0, VENT_H, FreeCAD.Vector(-VENT_W/2, BASE_L/2 - SHEET_T*2, Z_base - VENT_H))
    hood_with_vent = hood_full.cut(vent_box)

    flange_outer = Part.makeBox(BASE_W + 25.4, BASE_L + 25.4, 4.76, FreeCAD.Vector(-BASE_W/2 - 12.7, -BASE_L/2 - 12.7, Z_skirt_bot))
    flange_inner = Part.makeBox(BASE_W, BASE_L, 5.0, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_skirt_bot - 0.1))
    perimeter_flange = flange_outer.cut(flange_inner)

    hood_assembly = hood_with_vent.fuse(perimeter_flange)
    hood_obj = v4_doc.addObject("Part::Feature", "Pyramidal_Hood_Heat_Flange")
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

    gussets_obj = v4_doc.addObject("Part::Feature", "Corner_Gussets_AngleIron")
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

    skids_obj = v4_doc.addObject("Part::Feature", "Dual_Skid_Runners")
    skids_obj.Shape = dual_skids
    grp_hood.addObject(skids_obj)

    # ==========================================
    # 3. SUBASSEMBLY 2: OVERHEAD MOUNTING FRAME
    # ==========================================
    f_height = 80.0
    f_width = APEX_W + 50.0
    f_thick = 4.76
    leg_l = Part.makeBox(f_thick, APEX_L, f_height, FreeCAD.Vector(-f_width/2, -APEX_L/2, Z_apex))
    leg_r = Part.makeBox(f_thick, APEX_L, f_height, FreeCAD.Vector(f_width/2 - f_thick, -APEX_L/2, Z_apex))
    bridge = Part.makeBox(f_width, 38.1, f_thick, FreeCAD.Vector(-f_width/2, -19.05, Z_apex + f_height - f_thick))

    wand_lean_dir = FreeCAD.Vector(0, -math.sin(math.radians(TORCH_ANGLE)), math.cos(math.radians(TORCH_ANGLE)))

    clamp_sleeve = Part.makeCylinder(25.4, 60.0, FreeCAD.Vector(0, 10.0, Z_apex + f_height/2), wand_lean_dir)
    clamp_inner = Part.makeCylinder(19.05, 70.0, FreeCAD.Vector(0, 12.0, Z_apex + f_height/2 - 5.0), wand_lean_dir)
    sleeve_ring = clamp_sleeve.cut(clamp_inner)

    torch_frame_obj = v4_doc.addObject("Part::Feature", "Overhead_Torch_Mounting_Frame")
    torch_frame_obj.Shape = leg_l.fuse(leg_r).fuse(bridge).fuse(sleeve_ring)
    grp_frame.addObject(torch_frame_obj)

    # ==========================================
    # 4. SUBASSEMBLY 3: HARBOR FREIGHT TORCH 91037
    # ==========================================
    flame_dir = FreeCAD.Vector(0, math.sin(math.radians(TORCH_ANGLE)), math.cos(math.radians(TORCH_ANGLE)))
    nozzle_pos = FreeCAD.Vector(0, -30.0, Z_apex - NOZZLE_RECESS)
    
    bell_nozzle = Part.makeCone(38.1, 22.0, 100.0, nozzle_pos, flame_dir)
    bell_rim = Part.makeCylinder(39.0, 10.0, nozzle_pos, flame_dir)
    burner_head = bell_nozzle.fuse(bell_rim)

    wand_start = nozzle_pos + wand_lean_dir * 80.0
    wand_length = 500.0
    wand_shaft = Part.makeCylinder(9.525, wand_length, wand_start, wand_lean_dir)

    handle_start = wand_start + wand_lean_dir * wand_length
    handle_body = Part.makeCylinder(17.5, 180.0, handle_start, wand_lean_dir)
    grip_insert = Part.makeBox(20.0, 25.0, 120.0, FreeCAD.Vector(-10.0, handle_start.y - 12.0, handle_start.z + 30.0))
    squeeze_lever = Part.makeBox(6.0, 15.0, 100.0, FreeCAD.Vector(-3.0, handle_start.y - 25.0, handle_start.z + 20.0))
    
    brass_knob_pos = handle_start + wand_lean_dir * 160.0
    brass_knob = Part.makeCylinder(14.0, 20.0, brass_knob_pos + FreeCAD.Vector(0, 0, 15.0), FreeCAD.Vector(0, 0, 1))

    igniter_clamp_pos = wand_start + wand_lean_dir * 200.0
    igniter_housing = Part.makeBox(20.0, 30.0, 45.0, FreeCAD.Vector(-10.0, igniter_clamp_pos.y - 15.0, igniter_clamp_pos.z))
    igniter_button = Part.makeCylinder(6.0, 12.0, FreeCAD.Vector(0, igniter_clamp_pos.y - 20.0, igniter_clamp_pos.z + 20.0), FreeCAD.Vector(0, -1, 0))
    igniter_wire = Part.makeCylinder(2.5, 220.0, igniter_clamp_pos + FreeCAD.Vector(0, -10.0, 0), flame_dir)

    tank_pos = FreeCAD.Vector(-300.0, -200.0, 400.0)
    tank_body = Part.makeCylinder(47.6, 200.0, tank_pos, FreeCAD.Vector(0, 0, 1))
    tank_dome = Part.makeSphere(47.6, tank_pos + FreeCAD.Vector(0, 0, 200.0))
    tank_valve = Part.makeCylinder(10.0, 25.0, tank_pos + FreeCAD.Vector(0, 0, 240.0), FreeCAD.Vector(0, 0, 1))
    propane_tank = tank_body.fuse(tank_dome).fuse(tank_valve)

    burner_obj = v4_doc.addObject("Part::Feature", "HF_Burner_Head_Nozzle")
    burner_obj.Shape = burner_head
    grp_torch.addObject(burner_obj)

    wand_obj = v4_doc.addObject("Part::Feature", "Torch_Chrome_Wand_Shaft")
    wand_obj.Shape = wand_shaft
    grp_torch.addObject(wand_obj)

    handle_obj = v4_doc.addObject("Part::Feature", "HF_Blue_Torch_Handle")
    handle_obj.Shape = handle_body.fuse(grip_insert).fuse(squeeze_lever)
    grp_torch.addObject(handle_obj)

    brass_valve_obj = v4_doc.addObject("Part::Feature", "Brass_Flow_Control_Knob")
    brass_valve_obj.Shape = brass_knob
    grp_torch.addObject(brass_valve_obj)

    igniter_obj = v4_doc.addObject("Part::Feature", "Piezo_Igniter_Module")
    igniter_obj.Shape = igniter_housing.fuse(igniter_button).fuse(igniter_wire)
    grp_torch.addObject(igniter_obj)

    tank_obj = v4_doc.addObject("Part::Feature", "Propane_Cylinder_1lb")
    tank_obj.Shape = propane_tank
    grp_torch.addObject(tank_obj)

    # ==========================================
    # 5. SUBASSEMBLY 4: TOW RIGGING
    # ==========================================
    hitch_y = -BASE_L/2
    hitch_z = Z_skirt_bot + SKIRT_H / 2.0
    ear_spacing = 25.4
    ear_thick = 4.76
    ear_depth = 50.8
    ear_height = 50.8

    left_ear = Part.makeBox(ear_thick, ear_depth, ear_height, FreeCAD.Vector(-ear_spacing/2 - ear_thick, hitch_y - ear_depth, hitch_z - ear_height/2))
    right_ear = Part.makeBox(ear_thick, ear_depth, ear_height, FreeCAD.Vector(ear_spacing/2, hitch_y - ear_depth, hitch_z - ear_height/2))
    pin_center = FreeCAD.Vector(0, hitch_y - 30.0, hitch_z)
    clevis_pin = Part.makeCylinder(CLEVIS_PIN_D/2, ear_spacing + 2*ear_thick + 10.0, FreeCAD.Vector(-ear_spacing/2 - ear_thick - 5.0, hitch_y - 30.0, hitch_z), FreeCAD.Vector(1, 0, 0))
    stop_tab = Part.makeBox(ear_spacing + 2*ear_thick, 25.4, 25.4, FreeCAD.Vector(-ear_spacing/2 - ear_thick, hitch_y - ear_depth, hitch_z - ear_height/2 - 15.0))
    stop_tab.rotate(pin_center, FreeCAD.Vector(1, 0, 0), -STOP_ANGLE)

    hitch_obj = v4_doc.addObject("Part::Feature", "Front_Clevis_Hitch_With_StopTab")
    hitch_obj.Shape = left_ear.fuse(right_ear).fuse(stop_tab)
    grp_tow.addObject(hitch_obj)

    pin_obj = v4_doc.addObject("Part::Feature", "Clevis_Pin_38in")
    pin_obj.Shape = clevis_pin
    grp_tow.addObject(pin_obj)

    tow_angle = 35.0
    tow_dir = FreeCAD.Vector(0, -math.cos(math.radians(tow_angle)), math.sin(math.radians(tow_angle)))
    tow_bar_tube = Part.makeBox(TOWBAR_SQ, TOWBAR_SQ, TOWBAR_L, FreeCAD.Vector(-TOWBAR_SQ/2, -TOWBAR_SQ/2, 0))
    tow_bar_tube.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0), (90.0 - tow_angle))
    tow_bar_tube.translate(pin_center)

    handle_end_pos = pin_center + tow_dir * TOWBAR_L
    t_grip = Part.makeCylinder(12.7, 203.2, handle_end_pos + FreeCAD.Vector(-101.6, 0, 0), FreeCAD.Vector(1, 0, 0))

    towbar_obj = v4_doc.addObject("Part::Feature", "Forward_Rigid_Tow_Bar_5ft")
    towbar_obj.Shape = tow_bar_tube.fuse(t_grip)
    grp_tow.addObject(towbar_obj)

    # RECOMPUTE BEFORE GUI SETTINGS
    v4_doc.recompute()

    color_map = {
        hood_obj: STEEL_DARK,
        gussets_obj: STEEL_BRIGHT,
        skids_obj: STEEL_BRIGHT,
        torch_frame_obj: STEEL_BRIGHT,
        hitch_obj: STEEL_BRIGHT,
        pin_obj: STEEL_BRIGHT,
        burner_obj: TORCH_BLACK,
        wand_obj: CHROME,
        handle_obj: HF_BLUE,
        brass_valve_obj: BRASS,
        igniter_obj: IGNITER_RED,
        tank_obj: PROPANE_GREEN,
        towbar_obj: TOWBAR_YELLOW
    }

    for obj, color in color_map.items():
        set_vis(v4_doc, obj, color)

    # Save outputs
    fc_v4 = os.path.join(script_dir, "sled_v04.FCStd")
    png_v4 = os.path.join(script_dir, "sled_v04.png")
    v4_doc.saveAs(fc_v4)

    fc_root = os.path.join(sled_dir, "flame_sled.FCStd")
    v4_doc.saveAs(fc_root)

    if HAS_GUI:
        try:
            import FreeCADGui
            gui_d = FreeCADGui.getDocument(v4_doc.Name)
            if gui_d:
                base_prefix = os.path.join(script_dir, "sled_v04")
                export_orthogonal_views(gui_d, base_prefix, master_dir=sled_dir, model_prefix="flame_sled")
        except Exception as e:
            print(f"Render error: {e}")

    FreeCAD.closeDocument("caddy_v4")
    print(f"Built Version 4: {fc_v4} and {png_v4}")
    print(f"Master root file updated: {fc_root}")

if __name__ == "__main__":
    build_v4()
    sys.exit(0)
