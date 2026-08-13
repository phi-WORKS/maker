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
from phi_works.maker.components import (
    create_torch_component,
    create_propane_cylinder_component,
    create_propane_harness_component,
)

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
def build_hood_subassembly(doc, grp_hood, dims):
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

    wand_lean_dir = FreeCAD.Vector(0, -math.sin(math.radians(TORCH_ANGLE)), math.cos(math.radians(TORCH_ANGLE)))

    clamp_sleeve = Part.makeCylinder(25.4, 60.0, FreeCAD.Vector(0, 10.0, Z_apex + f_height/2), wand_lean_dir)
    clamp_inner = Part.makeCylinder(19.05, 70.0, FreeCAD.Vector(0, 12.0, Z_apex + f_height/2 - 5.0), wand_lean_dir)
    sleeve_ring = clamp_sleeve.cut(clamp_inner)

    torch_frame_obj = doc.addObject("Part::Feature", "Overhead_Torch_Mounting_Frame")
    torch_frame_obj.Shape = leg_l.fuse(leg_r).fuse(bridge).fuse(sleeve_ring)
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

    nozzle_pos = FreeCAD.Vector(0, -30.0, Z_apex - NOZZLE_RECESS)
    torch_grp = create_torch_component(doc, insertion_point=nozzle_pos, lean_angle_deg=35.0, flame_angle_deg=35.0)
    
    # Move torch component objects into grp_torch subassembly
    for obj in torch_grp.Group:
        grp_torch.addObject(obj)

    return torch_grp

# ==========================================
# 4. SUBASSEMBLY BUILDER 4: TOW RIGGING
# ==========================================
def build_tow_rigging_subassembly(doc, grp_tow, dims):
    BASE_L = dims.BaseLength.Value
    SKIRT_H = dims.SkirtHeight.Value
    GROUND_CLR = 12.7
    TOWBAR_L = dims.TowBarLength.Value
    TOWBAR_SQ = 19.05    # 3/4 in square tube
    STOP_ANGLE = 20.0    # 20 deg minimum tow bar rest tab angle
    CLEVIS_PIN_D = 9.525 # 3/8 in pin

    Z_skirt_bot = GROUND_CLR
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

    hitch_obj = doc.addObject("Part::Feature", "Front_Clevis_Hitch_With_StopTab")
    hitch_obj.Shape = left_ear.fuse(right_ear).fuse(stop_tab)
    grp_tow.addObject(hitch_obj)

    pin_obj = doc.addObject("Part::Feature", "Clevis_Pin_38in")
    pin_obj.Shape = clevis_pin
    grp_tow.addObject(pin_obj)

    tow_angle = 35.0
    tow_dir = FreeCAD.Vector(0, -math.cos(math.radians(tow_angle)), math.sin(math.radians(tow_angle)))
    tow_bar_tube = Part.makeBox(TOWBAR_SQ, TOWBAR_SQ, TOWBAR_L, FreeCAD.Vector(-TOWBAR_SQ/2, -TOWBAR_SQ/2, 0))
    tow_bar_tube.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0), (90.0 - tow_angle))
    tow_bar_tube.translate(pin_center)

    handle_end_pos = pin_center + tow_dir * TOWBAR_L
    t_grip = Part.makeCylinder(12.7, 203.2, handle_end_pos + FreeCAD.Vector(-101.6, 0, 0), FreeCAD.Vector(1, 0, 0))

    towbar_obj = doc.addObject("Part::Feature", "Forward_Rigid_Tow_Bar_5ft")
    towbar_obj.Shape = tow_bar_tube.fuse(t_grip)
    grp_tow.addObject(towbar_obj)

    return hitch_obj, pin_obj, towbar_obj, pin_center, tow_dir

# ==========================================
# 5. SUBASSEMBLY BUILDER 5: PROPANE HARNESS & TANK
# ==========================================
def build_propane_harness_subassembly(doc, grp_harness, pin_center, tow_dir):
    # Mount harness at L = 1100 mm along tow bar
    harness_dist = 1100.0
    harness_base_pos = pin_center + tow_dir * harness_dist

    # Rotation matching tow bar angle
    rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 35.0)
    harness_placement = FreeCAD.Placement(harness_base_pos, rot)

    harness_grp = create_propane_harness_component(doc, placement=harness_placement)
    for obj in harness_grp.Group:
        grp_harness.addObject(obj)

    # Seat 1 lb Cylinder inside harness
    cylinder_base_pos = harness_base_pos + FreeCAD.Vector(0, -math.sin(math.radians(35.0))*2.0, math.cos(math.radians(35.0))*2.0)
    cylinder_placement = FreeCAD.Placement(cylinder_base_pos, rot)
    
    cylinder_grp = create_propane_cylinder_component(doc, placement=cylinder_placement)
    for obj in cylinder_grp.Group:
        grp_harness.addObject(obj)

    # Flexible High-Pressure Propane Line Hose
    # Route from cylinder valve to torch handle control knob
    valve_top_pos = cylinder_base_pos + FreeCAD.Vector(0, -math.sin(math.radians(35.0))*198.0, math.cos(math.radians(35.0))*198.0)
    torch_knob_pos = FreeCAD.Vector(0, -330.0, 520.0)

    hose_path = Part.makeCylinder(4.0, (torch_knob_pos - valve_top_pos).Length, valve_top_pos, (torch_knob_pos - valve_top_pos).normalize())
    hose_obj = doc.addObject("Part::Feature", "High_Pressure_Propane_Extension_Hose")
    hose_obj.Shape = hose_path
    grp_harness.addObject(hose_obj)

    return harness_grp, cylinder_grp, hose_obj

# ==========================================
# MAIN ORCHESTRATOR FUNCTION: build()
# ==========================================
def build():
    STEEL_DARK = (0.28, 0.30, 0.33, 0.0)      # 14-ga Hood & Skirts
    STEEL_BRIGHT = (0.55, 0.58, 0.62, 0.0)    # Skids, Frame, Clevis, Angle Iron
    BRASS = (0.85, 0.65, 0.20, 0.0)           # Valve & Brass Fittings
    HF_BLUE = (0.10, 0.35, 0.80, 0.0)         # Harbor Freight Handle Blue
    TORCH_BLACK = (0.15, 0.15, 0.15, 0.0)     # Torch Grip & Burner Head
    CHROME = (0.75, 0.78, 0.82, 0.0)          # Torch Wand Metal Shaft
    IGNITER_RED = (0.85, 0.15, 0.15, 0.0)     # Push-button Igniter
    PROPANE_GREEN = (0.12, 0.48, 0.22, 0.0)   # 1 lb Propane Cylinder
    TOWBAR_YELLOW = (0.88, 0.68, 0.12, 0.0)  # High-Vis Powdercoated Tow Bar
    HARNESS_MATTE = (0.18, 0.18, 0.18, 0.0)   # Black Powdercoat Cage
    HOSE_BLACK = (0.08, 0.08, 0.08, 0.0)      # Rubber Extension Hose

    model = FreeCAD.newDocument("road_roaster")
    model.Label = "Road Roaster v0.4.0 - Onboard Propane Harness & Imported Components"

    # 0. SUBASSEMBLY PART CONTAINERS (v0.4.0)
    grp_hood = model.addObject("App::DocumentObjectGroup", "Hood_Subassembly")
    grp_hood.Label = "1. Pyramid Hood & Skid Subassembly"

    grp_frame = model.addObject("App::DocumentObjectGroup", "Overhead_Frame_Subassembly")
    grp_frame.Label = "2. Overhead Torch Mounting Frame"

    grp_torch = model.addObject("App::DocumentObjectGroup", "Harbor_Freight_Torch_Subassembly")
    grp_torch.Label = "3. Harbor Freight #91037 Torch Subassembly"

    grp_harness = model.addObject("App::DocumentObjectGroup", "Propane_Harness_Subassembly")
    grp_harness.Label = "4. Propane Bottle Harness & Tank Subassembly"

    grp_tow = model.addObject("App::DocumentObjectGroup", "Tow_Rigging_Subassembly")
    grp_tow.Label = "5. Forward Tow Rigging Subassembly"

    # 1. PARAMETRIC VARSET (dims)
    dims = model.addObject("App::VarSet", "dims")
    
    BASE_W = 457.2       # 18.0 in
    BASE_L = 457.2       # 18.0 in
    APEX_W = 101.6       # 4.0 in top apex opening
    APEX_L = 101.6       # 4.0 in top apex opening
    HOOD_H = 152.4       # 6.0 in vertical height
    SKIRT_H = 50.8       # 2.0 in vertical skirt extension
    SHEET_T = 1.905      # 14-gauge mild steel (0.075 in)
    TOWBAR_L = 1524.0    # 5.0 ft (60.0 in)

    dims.addProperty("App::PropertyLength", "BaseWidth", "Dimensions", "Hood Base Width").BaseWidth = BASE_W
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Hood Base Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "ApexWidth", "Dimensions", "Top Apex Width").ApexWidth = APEX_W
    dims.addProperty("App::PropertyLength", "ApexLength", "Dimensions", "Top Apex Length").ApexLength = APEX_L
    dims.addProperty("App::PropertyLength", "HoodHeight", "Dimensions", "Pyramid Rise Height").HoodHeight = HOOD_H
    dims.addProperty("App::PropertyLength", "SkirtHeight", "Dimensions", "Vertical Skirt Height").SkirtHeight = SKIRT_H
    dims.addProperty("App::PropertyLength", "SheetThickness", "Dimensions", "14-ga Steel Thickness").SheetThickness = SHEET_T
    dims.addProperty("App::PropertyLength", "TowBarLength", "Dimensions", "Tow Bar Length").TowBarLength = TOWBAR_L

    # 2. BUILD SUBASSEMBLIES
    hood_obj, gussets_obj, skids_obj = build_hood_subassembly(model, grp_hood, dims)
    torch_frame_obj = build_overhead_frame_subassembly(model, grp_frame, dims)
    torch_grp = build_torch_subassembly(model, grp_torch, dims)
    hitch_obj, pin_obj, towbar_obj, pin_center, tow_dir = build_tow_rigging_subassembly(model, grp_tow, dims)
    harness_grp, cylinder_grp, hose_obj = build_propane_harness_subassembly(model, grp_harness, pin_center, tow_dir)

    model.recompute()

    # Apply Visual Colors
    color_map = {
        hood_obj: STEEL_DARK,
        gussets_obj: STEEL_BRIGHT,
        skids_obj: STEEL_BRIGHT,
        torch_frame_obj: STEEL_BRIGHT,
        hitch_obj: STEEL_BRIGHT,
        pin_obj: STEEL_BRIGHT,
        towbar_obj: TOWBAR_YELLOW,
        hose_obj: HOSE_BLACK
    }

    for obj, color in color_map.items():
        set_vis(model, obj, color)

    # Save outputs
    fc_file = os.path.join(script_dir, "sled_v0.4.0.FCStd")
    png_file = os.path.join(script_dir, "sled_v0.4.0.png")
    model.saveAs(fc_file)

    if HAS_GUI:
        try:
            import FreeCADGui
            gui_d = FreeCADGui.getDocument(model.Name)
            if gui_d:
                base_prefix = os.path.join(script_dir, "sled_v0.4.0")
                export_orthogonal_views(gui_d, base_prefix)
        except Exception as e:
            print(f"Render error: {e}")

    FreeCAD.closeDocument("road_roaster")
    print(f"Built Version 0.4.0: {fc_file} and {png_file}")

if __name__ == "__main__":
    build()
    sys.exit(0)
