"""
Road Roaster 4 - Master Assembly Build Script
Project: 4-Wheel Commercial Platform Dolly Architecture for Ceramic Infrared Weed Eradication

Full Integrated Assembly:
1. Commercial 24" x 36" Platform Cart (5in Running Gear, 29in Handle with dual cross rails)
2. 20 lb Propane Fuel Train & Deck Retention Ring (seated in rear zone near handle)
3. Handle-Mounted Auxiliary Spot Torch Wand (Harbor Freight #91037) & 2.5 Gal Water Safety Reservoir
4. Front Cantilevered Radiant Ceramic Burner Assembly with 180° Flip-Back Transit Hinge & Height Adjustment

Builds road-roaster-4.FCStd and exports 7 standard orthogonal and isometric PNG renders.
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

from phi_works.maker.render import export_orthogonal_views, save_model, close_model
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

# ==============================================================================
# SUBASSEMBLY 1: FRONT CANTILEVERED RADIANT BURNER & 180° FLIP HINGE
# ==============================================================================
def build_front_cantilever_burner_subassembly(doc, grp_burner, dims):
    """
    Builds the front cantilevered radiant ceramic burner assembly:
    - Deck mounting brackets bolted to the front lip of the platform cart
    - 180° flip pivot hinge with dual cantilever square-tube arms
    - Threaded turnbuckle height-adjustment linkage (0.5" to 2.5" ground clearance)
    - Protective 14-gauge steel burner cowl with perimeter heat skirts
    - Solaronics ceramic infrared radiant burner engine hovering above pavement
    - Flexible LP gas supply loop
    """
    DECK_W = dims.DeckWidth.Value
    DECK_L = dims.DeckLength.Value
    DECK_TOP_Z = dims.DeckHeight.Value
    
    BURNER_W = dims.BurnerWidth.Value
    BURNER_L = dims.BurnerLength.Value
    BURNER_H = dims.BurnerHeight.Value
    HOVER_Z = dims.HoverClearance.Value
    BURNER_Y = dims.BurnerCenterY.Value
    
    # Colors
    COWL_STEEL = (0.32, 0.34, 0.38, 0.0)      # 14-Gauge Hot-Rolled Steel Cowl
    ARM_STEEL = (0.42, 0.45, 0.48, 0.0)       # Square Tube Cantilever Arms
    HINGE_ZINC = (0.75, 0.78, 0.82, 0.0)      # Heavy Zinc-Plated Hinge Brackets
    TURNBUCKLE_BRASS = (0.85, 0.65, 0.20, 0.0)# Turnbuckle Adjustment Hardware
    HOSE_BLACK = (0.12, 0.12, 0.14, 0.0)      # Flexible High-Temp LP Gas Hose
    
    FRONT_LIP_Y = -DECK_L / 2.0  # Y = -457.2 mm
    
    # --------------------------------------------------------------------------
    # 1. Front Deck Hinge Brackets (Bolted to Front Deck Skirt)
    # --------------------------------------------------------------------------
    # Left & right pivot bracket assemblies at X = ±180 mm
    hinge_parts = []
    arm_x_positions = [-180.0, 180.0]
    PIVOT_Y = FRONT_LIP_Y - 15.0
    PIVOT_Z = DECK_TOP_Z + 25.0
    
    for x_h in arm_x_positions:
        # Base deck mounting pad bolted through deck
        pad = Part.makeBox(40.0, 65.0, 6.0, FreeCAD.Vector(x_h - 20.0, FRONT_LIP_Y, DECK_TOP_Z))
        # Vertical twin hinge ear uprights
        ear1 = Part.makeBox(6.0, 45.0, 45.0, FreeCAD.Vector(x_h - 22.0, FRONT_LIP_Y - 25.0, DECK_TOP_Z))
        ear2 = Part.makeBox(6.0, 45.0, 45.0, FreeCAD.Vector(x_h + 16.0, FRONT_LIP_Y - 25.0, DECK_TOP_Z))
        # Pivot pin through ears
        pin = Part.makeCylinder(6.0, 50.0, FreeCAD.Vector(x_h - 25.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
        hinge_parts.append(pad.fuse(ear1).fuse(ear2).fuse(pin))
        
    hinge_brackets_solid = hinge_parts[0].fuse(hinge_parts[1])
    
    # --------------------------------------------------------------------------
    # 2. Dual Cantilever Arms (1.5" Square Tubing with 180° Flip Pivot)
    # --------------------------------------------------------------------------
    ARM_TUBE = 38.1  # 1.5 in square tube
    arm_solids = []
    
    for x_a in arm_x_positions:
        # Pivot sleeve cylinder rotating around hinge pin
        sleeve = Part.makeCylinder(12.0, 32.0, FreeCAD.Vector(x_a - 16.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
        
        # Main cantilever beam extending from pivot (Y=PIVOT_Y, Z=PIVOT_Z) forward
        # to burner cowl attachment point at (Y=BURNER_Y + BURNER_L/2, Z=HOVER_Z + BURNER_H - 10)
        target_y = BURNER_Y + BURNER_L / 2.0
        target_z = HOVER_Z + BURNER_H - 10.0
        
        dy = target_y - PIVOT_Y
        dz = target_z - PIVOT_Z
        arm_len = math.hypot(dy, dz)
        angle = math.degrees(math.atan2(dz, dy))
        
        arm_beam = Part.makeBox(ARM_TUBE, arm_len, ARM_TUBE, FreeCAD.Vector(x_a - ARM_TUBE/2.0, 0, -ARM_TUBE/2.0))
        # Rotate arm to angle in YZ plane
        arm_beam.rotate(FreeCAD.Vector(x_a, 0, 0), FreeCAD.Vector(1, 0, 0), -(180.0 - angle))
        arm_beam.translate(FreeCAD.Vector(0, PIVOT_Y, PIVOT_Z))
        
        # Cowl attachment clevis plate at front end
        clevis = Part.makeBox(ARM_TUBE + 10.0, 35.0, 45.0, FreeCAD.Vector(x_a - (ARM_TUBE+10)/2.0, target_y - 20.0, target_z - 20.0))
        
        arm_solids.append(sleeve.fuse(arm_beam).fuse(clevis))
        
    cantilever_arms_solid = arm_solids[0].fuse(arm_solids[1])
    
    # --------------------------------------------------------------------------
    # 3. Threaded Turnbuckle Height-Adjustment Linkage
    # --------------------------------------------------------------------------
    # Strut connecting deck mast to cantilever arm to set and lock burner height
    turnbuckle_parts = []
    for x_t in arm_x_positions:
        # Mast tower on deck
        mast = Part.makeBox(30.0, 25.0, 80.0, FreeCAD.Vector(x_t - 15.0, FRONT_LIP_Y + 30.0, DECK_TOP_Z))
        # Turnbuckle barrel
        tb_cyl = Part.makeCylinder(10.0, 90.0, FreeCAD.Vector(x_t, FRONT_LIP_Y + 25.0, DECK_TOP_Z + 75.0),
                                   FreeCAD.Vector(0, -0.85, -0.52).normalize())
        # Hex adjustment nut
        tb_nut = Part.makeCylinder(14.0, 20.0, FreeCAD.Vector(x_t, FRONT_LIP_Y - 10.0, DECK_TOP_Z + 55.0),
                                   FreeCAD.Vector(0, -0.85, -0.52).normalize())
        turnbuckle_parts.append(mast.fuse(tb_cyl).fuse(tb_nut))
        
    turnbuckle_solid = turnbuckle_parts[0].fuse(turnbuckle_parts[1])
    
    # --------------------------------------------------------------------------
    # 4. 14-Gauge Steel Protective Burner Cowl & Skirts (Centered at Y = BURNER_Y)
    # --------------------------------------------------------------------------
    SHEET_T = 1.9  # 14-gauge steel
    cowl_outer = Part.makeBox(BURNER_W, BURNER_L, BURNER_H,
                              FreeCAD.Vector(-BURNER_W/2.0, BURNER_Y - BURNER_L/2.0, HOVER_Z))
    cowl_inner = Part.makeBox(BURNER_W - 2*SHEET_T, BURNER_L - 2*SHEET_T, BURNER_H + 2.0,
                              FreeCAD.Vector(-BURNER_W/2.0 + SHEET_T, BURNER_Y - BURNER_L/2.0 + SHEET_T, HOVER_Z - 1.0))
    cowl_shell = cowl_outer.cut(cowl_inner)
    
    # Front Heat Draft Vent Slots
    vent_w = BURNER_W - 80.0
    vent_h = 30.0
    vent_cut = Part.makeBox(vent_w, 20.0, vent_h,
                            FreeCAD.Vector(-vent_w/2.0, BURNER_Y - BURNER_L/2.0 - 10.0, HOVER_Z + 40.0))
    cowl_shell = cowl_shell.cut(vent_cut)
    
    # Top Intake / Exhaust Cutout for venturi manifold breathing
    top_vent = Part.makeBox(150.0, 180.0, 20.0,
                            FreeCAD.Vector(-75.0, BURNER_Y - 30.0, HOVER_Z + BURNER_H - 10.0))
    cowl_shell = cowl_shell.cut(top_vent)
    
    # --------------------------------------------------------------------------
    # 5. Flexible LP Gas Feed Hose Loop
    # --------------------------------------------------------------------------
    # Hose routed from deck manifold, looping through pivot center, to burner inlet
    p1 = FreeCAD.Vector(0.0, FRONT_LIP_Y + 50.0, DECK_TOP_Z + 20.0)
    p2 = FreeCAD.Vector(0.0, FRONT_LIP_Y - 15.0, PIVOT_Z + 30.0)
    p3 = FreeCAD.Vector(0.0, (FRONT_LIP_Y + BURNER_Y)/2.0, HOVER_Z + BURNER_H + 35.0)
    p4 = FreeCAD.Vector(0.0, BURNER_Y + 120.0, HOVER_Z + BURNER_H - 10.0)
    
    spline_h = Part.BSplineCurve()
    spline_h.interpolate([p1, p2, p3, p4])
    wire_h = Part.Wire([Part.Edge(spline_h)])
    circ_h = Part.makeCircle(6.0, p1, spline_h.tangent(0.0)[0])
    face_h = Part.Face(Part.Wire([circ_h]))
    hose_solid = wire_h.makePipe(face_h)
    
    # Document Objects
    obj_hinges = doc.addObject("Part::Feature", "Burner_Deck_Hinge_Brackets")
    obj_hinges.Label = "Front Deck 180-deg Flip Hinge Brackets & Pivot Pins"
    obj_hinges.Shape = hinge_brackets_solid
    grp_burner.addObject(obj_hinges)
    set_vis(doc, obj_hinges, HINGE_ZINC)
    
    obj_arms = doc.addObject("Part::Feature", "Burner_Cantilever_Arms")
    obj_arms.Label = "Cantilever Square-Tube Arms (180-deg Flip & Height Adjust)"
    obj_arms.Shape = cantilever_arms_solid
    grp_burner.addObject(obj_arms)
    set_vis(doc, obj_arms, ARM_STEEL)
    
    obj_tb = doc.addObject("Part::Feature", "Turnbuckle_Height_Adjuster")
    obj_tb.Label = "Threaded Turnbuckle Height Adjustment Struts"
    obj_tb.Shape = turnbuckle_solid
    grp_burner.addObject(obj_tb)
    set_vis(doc, obj_tb, TURNBUCKLE_BRASS)
    
    obj_cowl = doc.addObject("Part::Feature", "Burner_Sled_Cowl")
    obj_cowl.Label = "14-Gauge Protective Burner Sled Cowl & Heat Skirts"
    obj_cowl.Shape = cowl_shell
    grp_burner.addObject(obj_cowl)
    set_vis(doc, obj_cowl, COWL_STEEL)
    
    obj_hose = doc.addObject("Part::Feature", "Burner_Flexible_Gas_Loop")
    obj_hose.Label = "Flexible Reinforced LP Gas Hose Supply Loop"
    obj_hose.Shape = hose_solid
    grp_burner.addObject(obj_hose)
    set_vis(doc, obj_hose, HOSE_BLACK)
    
    # --------------------------------------------------------------------------
    # 6. Import Standalone Solaronics Ceramic Infrared Burner Component
    # --------------------------------------------------------------------------
    burner_pos = FreeCAD.Vector(0, BURNER_Y, HOVER_Z + 45.0)
    burner_grp = import_component(doc, "solaronics_infrared_burner", placement=FreeCAD.Placement(burner_pos, FreeCAD.Rotation()))
    if burner_grp:
        grp_burner.addObject(burner_grp)

# ==============================================================================
# SUBASSEMBLY 2: 20 LB PROPANE FUEL TRAIN & DECK CLAMP
# ==============================================================================
def build_fuel_train_subassembly(doc, grp_fuel, dims):
    """
    Mounts the standard 20 lb propane cylinder solidly to the rear deck of the cart,
    adds a heavy-duty welded floor ring retention bracket, and models the dual manifold tee.
    """
    DECK_TOP_Z = dims.DeckHeight.Value
    TANK_X = dims.TankCenterX.Value  # +75.0 mm (Right-rear zone)
    TANK_Y = dims.TankCenterY.Value  # +220.0 mm
    
    TANK_STEEL = (0.35, 0.38, 0.42, 0.0)      # Heavy Steel Mounting Ring
    VALVE_BRASS = (0.85, 0.65, 0.20, 0.0)     # Brass Dual Manifold Tee
    HOSE_BLACK = (0.12, 0.12, 0.14, 0.0)      # Flexible Gas Hose
    
    # 1. Import 20 lb Propane Cylinder Component
    tank_pos = FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z)
    tank_grp = import_component(doc, "propane_cylinder_20lb", placement=FreeCAD.Placement(tank_pos, FreeCAD.Rotation()))
    if tank_grp:
        grp_fuel.addObject(tank_grp)
        
    # 2. Welded Deck Retention Ring & Quick-Release Clamp
    FOOT_R = 101.6
    RING_T = 6.0
    ring_outer = Part.makeCylinder(FOOT_R + 8.0, 35.0, FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1))
    ring_inner = Part.makeCylinder(FOOT_R + 2.0, 40.0, FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z - 1.0), FreeCAD.Vector(0, 0, 1))
    deck_ring = ring_outer.cut(ring_inner)
    
    # 3 Mounting bolt tabs anchored through deck channels
    tabs = []
    for ang in [30, 150, 270]:
        t_box = Part.makeBox(35.0, 40.0, 6.0, FreeCAD.Vector(-17.5, FOOT_R + 5.0, DECK_TOP_Z))
        t_box.rotate(FreeCAD.Vector(0, 0, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1), ang)
        t_box.translate(FreeCAD.Vector(TANK_X, TANK_Y, 0))
        tabs.append(t_box)
        
    retention_collar = deck_ring.fuse(tabs[0]).fuse(tabs[1]).fuse(tabs[2])
    
    # 3. Dual-Port Brass Manifold Tee at Regulator Outlet
    # Seated atop the 20 lb cylinder regulator
    Z_reg = DECK_TOP_Z + 480.0
    tee_body = Part.makeBox(35.0, 30.0, 35.0, FreeCAD.Vector(TANK_X - 17.5, TANK_Y + 65.0, Z_reg))
    port_front = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(TANK_X, TANK_Y + 65.0, Z_reg + 17.5), FreeCAD.Vector(0, -1, 0))
    port_side = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(TANK_X + 17.5, TANK_Y + 80.0, Z_reg + 17.5), FreeCAD.Vector(1, 0, 0))
    tee_assembly = tee_body.fuse(port_front).fuse(port_side)
    
    obj_ring = doc.addObject("Part::Feature", "Tank_Deck_Retention_Ring")
    obj_ring.Label = "20 lb Propane Foot-Ring Deck Retention Clamp"
    obj_ring.Shape = retention_collar
    grp_fuel.addObject(obj_ring)
    set_vis(doc, obj_ring, TANK_STEEL)
    
    obj_tee = doc.addObject("Part::Feature", "Dual_Manifold_Gas_Tee")
    obj_tee.Label = "Brass Dual-Outlet Regulator Distribution Manifold Tee"
    obj_tee.Shape = tee_assembly
    grp_fuel.addObject(obj_tee)
    set_vis(doc, obj_tee, VALVE_BRASS)

# ==============================================================================
# SUBASSEMBLY 3: AUXILIARY SPOT TORCH WAND & WATER SAFETY RESERVOIR
# ==============================================================================
def build_auxiliary_safety_subassembly(doc, grp_aux, dims):
    """
    Mounts the Harbor Freight spot torch wand to the push handle cross rails (hanging vertically in a stirrup),
    and places a dedicated 2.5 gallon blue water safety canister at the rear of the cart next to the propane tank.
    """
    DECK_TOP_Z = dims.DeckHeight.Value
    DECK_L = dims.DeckLength.Value
    HANDLE_Y = DECK_L / 2.0 - 45.0  # Y = +412.2 mm
    
    WATER_BLUE = (0.10, 0.42, 0.85, 0.0)      # Vivid Safety Water Blue Tank
    PUMP_BLACK = (0.15, 0.15, 0.16, 0.0)      # Molded Poly Pump Plunger & Hose
    BRACKET_STEEL = (0.45, 0.48, 0.52, 0.0)   # Quick-Release Steel Brackets
    
    # --------------------------------------------------------------------------
    # 1. 2.5-Gallon Blue Pressurized Water Safety Reservoir (Rear Deck, Beside Gas Tank)
    # --------------------------------------------------------------------------
    # Seated at X = -170 mm, Y = +220 mm (side-by-side with 20 lb propane cylinder at rear)
    WATER_X = dims.WaterCenterX.Value  # -170.0 mm
    WATER_Y = dims.TankCenterY.Value   # +220.0 mm
    WATER_R = 90.0    # 7.1 in diameter
    WATER_H = 340.0   # 13.4 in height
    
    tank_cyl = Part.makeCylinder(WATER_R, WATER_H, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1))
    top_dome = Part.makeCone(WATER_R, 40.0, 45.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z + WATER_H), FreeCAD.Vector(0, 0, 1))
    pump_handle = Part.makeBox(120.0, 30.0, 25.0, FreeCAD.Vector(WATER_X - 60.0, WATER_Y - 15.0, DECK_TOP_Z + WATER_H + 45.0))
    spray_hose = Part.makeTorus(WATER_R + 15.0, 6.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z + WATER_H / 2.0), FreeCAD.Vector(0, 0, 1))
    water_canister_solid = tank_cyl.fuse(top_dome).fuse(pump_handle).fuse(spray_hose)
    
    # Deck cradle bracket for water tank
    cradle_base = Part.makeBox(200.0, 200.0, 6.0, FreeCAD.Vector(WATER_X - 100.0, WATER_Y - 100.0, DECK_TOP_Z))
    cradle_lip = Part.makeCylinder(WATER_R + 5.0, 35.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1))
    cradle_inner = Part.makeCylinder(WATER_R + 1.0, 40.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z - 1.0), FreeCAD.Vector(0, 0, 1))
    cradle_solid = cradle_base.fuse(cradle_lip.cut(cradle_inner))
    
    # --------------------------------------------------------------------------
    # 2. Auxiliary Spot Torch Wand (Harbor Freight #91037) in Vertical Stirrup
    # --------------------------------------------------------------------------
    # The axis of the wand tube is mounted STRICTLY VERTICAL along (0, 0, -1).
    # Supported by a drop-in stirrup loop on the upper cross rail (Z = 655 mm),
    # with a lower guide saddle on the lower cross rail (Z = 415 mm).
    # Handle is at the very top (Z = 875 mm) for immediate grab-and-go access,
    # and the burner bell hangs straight down at Z ~ 95 mm.
    TORCH_X = 200.0
    TORCH_Y = HANDLE_Y + 28.0
    TORCH_Z = DECK_TOP_Z + 700.0  # Base of handle at Z = 875.0 mm
    
    z_rail_upper = DECK_TOP_Z + 480.0  # 655.0 mm
    z_rail_lower = DECK_TOP_Z + 240.0  # 415.0 mm
    
    # A. Upper Stirrup Holster Hoop (Clamped to upper cross rail Z = 655 mm)
    clamp_top = Part.makeBox(35.0, 24.0, 22.0, FreeCAD.Vector(TORCH_X - 17.5, HANDLE_Y - 12.0, z_rail_upper - 11.0))
    bore_top = Part.makeCylinder(12.7, 40.0, FreeCAD.Vector(TORCH_X - 20.0, HANDLE_Y, z_rail_upper), FreeCAD.Vector(1, 0, 0))
    clamp_top = clamp_top.cut(bore_top)
    
    arm_top = Part.makeBox(12.0, TORCH_Y - HANDLE_Y, 8.0, FreeCAD.Vector(TORCH_X - 6.0, HANDLE_Y, z_rail_upper - 4.0))
    
    loop_outer = Part.makeCylinder(22.0, 22.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_upper - 11.0), FreeCAD.Vector(0, 0, 1))
    loop_inner = Part.makeCylinder(15.0, 26.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_upper - 13.0), FreeCAD.Vector(0, 0, 1))
    stirrup_top_loop = loop_outer.cut(loop_inner)
    
    # B. Lower Guide Stirrup Saddle (Clamped to lower cross rail Z = 415 mm)
    clamp_bot = Part.makeBox(35.0, 24.0, 20.0, FreeCAD.Vector(TORCH_X - 17.5, HANDLE_Y - 12.0, z_rail_lower - 10.0))
    bore_bot = Part.makeCylinder(12.7, 40.0, FreeCAD.Vector(TORCH_X - 20.0, HANDLE_Y, z_rail_lower), FreeCAD.Vector(1, 0, 0))
    clamp_bot = clamp_bot.cut(bore_bot)
    
    arm_bot = Part.makeBox(10.0, TORCH_Y - HANDLE_Y, 6.0, FreeCAD.Vector(TORCH_X - 5.0, HANDLE_Y, z_rail_lower - 3.0))
    
    saddle_out = Part.makeCylinder(18.0, 18.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_lower - 9.0), FreeCAD.Vector(0, 0, 1))
    saddle_in = Part.makeCylinder(11.0, 22.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_lower - 11.0), FreeCAD.Vector(0, 0, 1))
    stirrup_bot_saddle = saddle_out.cut(saddle_in)
    
    stirrups_solid = clamp_top.fuse(arm_top).fuse(stirrup_top_loop).fuse(clamp_bot).fuse(arm_bot).fuse(stirrup_bot_saddle)
    
    # Import Harbor Freight torch component with tube axis strictly vertical (bell pointing DOWN)
    torch_pos = FreeCAD.Vector(TORCH_X, TORCH_Y, TORCH_Z)
    torch_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 180)
    torch_grp = import_component(doc, "torch_hf91037", placement=FreeCAD.Placement(torch_pos, torch_rot))
    if torch_grp:
        grp_aux.addObject(torch_grp)
        
    # Flexible gas supply hose from regulator manifold tee to torch handle inlet
    p_tee = FreeCAD.Vector(dims.TankCenterX.Value + 42.5, dims.TankCenterY.Value + 80.0, DECK_TOP_Z + 497.5)
    p_torch_in = FreeCAD.Vector(TORCH_X, TORCH_Y - 10.0, TORCH_Z)
    p_mid = FreeCAD.Vector((dims.TankCenterX.Value + 42.5 + TORCH_X)/2.0 + 15.0, HANDLE_Y - 10.0, (DECK_TOP_Z + 497.5 + TORCH_Z)/2.0 + 20.0)
    
    spline_t = Part.BSplineCurve()
    spline_t.interpolate([p_tee, p_mid, p_torch_in])
    wire_t = Part.Wire([Part.Edge(spline_t)])
    circ_t = Part.makeCircle(4.76, p_tee, spline_t.tangent(0.0)[0])
    face_t = Part.Face(Part.Wire([circ_t]))
    torch_supply_hose = wire_t.makePipe(face_t)
        
    obj_water = doc.addObject("Part::Feature", "Water_Safety_Reservoir")
    obj_water.Label = "2.5 Gal Pressurized Blue Water Safety Spray Tank"
    obj_water.Shape = water_canister_solid
    grp_aux.addObject(obj_water)
    set_vis(doc, obj_water, WATER_BLUE)
    
    obj_cradle = doc.addObject("Part::Feature", "Water_Tank_Deck_Cradle")
    obj_cradle.Label = "Water Safety Tank Quick-Lock Deck Cradle"
    obj_cradle.Shape = cradle_solid
    grp_aux.addObject(obj_cradle)
    set_vis(doc, obj_cradle, BRACKET_STEEL)
    
    obj_stirrups = doc.addObject("Part::Feature", "Torch_Handle_Stirrup_Holster")
    obj_stirrups.Label = "Quick-Draw Torch Handle Stirrup Loop & Guide Saddle"
    obj_stirrups.Shape = stirrups_solid
    grp_aux.addObject(obj_stirrups)
    set_vis(doc, obj_stirrups, BRACKET_STEEL)

    obj_t_hose = doc.addObject("Part::Feature", "Torch_Auxiliary_Gas_Hose")
    obj_t_hose.Label = "Auxiliary Spot Torch Flexible Gas Hose"
    obj_t_hose.Shape = torch_supply_hose
    grp_aux.addObject(obj_t_hose)
    set_vis(doc, obj_t_hose, (0.12, 0.12, 0.14, 0.0))

# ==============================================================================
# MASTER ASSEMBLY BUILD FUNCTION
# ==============================================================================
def build_road_roaster_4w():
    doc_name = "road-roaster-4w"
    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture)"

    # ==========================================================================
    # PARAMETRIC DATUM VARSET
    # ==========================================================================
    dims = doc.addObject("App::VarSet", "dims")
    # Platform Cart Dimensions
    dims.addProperty("App::PropertyLength", "DeckWidth", "Dimensions", "Platform Deck Width").DeckWidth = 609.6         # 24.0 in
    dims.addProperty("App::PropertyLength", "DeckLength", "Dimensions", "Platform Deck Length").DeckLength = 914.4       # 36.0 in
    dims.addProperty("App::PropertyLength", "DeckHeight", "Dimensions", "Deck Top Surface from Ground").DeckHeight = 175.0 # 6.89 in
    dims.addProperty("App::PropertyLength", "HandleHeight", "Dimensions", "Push Handle Height above Deck").HandleHeight = 736.6 # 29.0 in
    dims.addProperty("App::PropertyLength", "WheelDiameter", "Dimensions", "Caster Wheel Diameter").WheelDiameter = 127.0 # 5.0 in
    
    # Cantilever Burner Geometry
    dims.addProperty("App::PropertyLength", "BurnerWidth", "Burner", "Burner Cowl Width").BurnerWidth = 381.0          # 15.0 in
    dims.addProperty("App::PropertyLength", "BurnerLength", "Burner", "Burner Cowl Length").BurnerLength = 457.2        # 18.0 in
    dims.addProperty("App::PropertyLength", "BurnerHeight", "Burner", "Burner Cowl Height").BurnerHeight = 120.0        # 4.72 in
    dims.addProperty("App::PropertyDistance", "BurnerCenterY", "Burner", "Cantilever Forward Position").BurnerCenterY = -720.0 # Forward of front bumper
    dims.addProperty("App::PropertyLength", "HoverClearance", "Burner", "Operating Ground Hover Clearance").HoverClearance = 25.4 # 1.0 in
    dims.addProperty("App::PropertyFloat", "BurnerBTU", "Thermal", "Radiant Heat Rating").BurnerBTU = 60000.0
    
    # Fuel & Safety Systems (Rear Deck Side-by-Side)
    dims.addProperty("App::PropertyDistance", "TankCenterY", "Fuel", "20 lb Tank Deck Y Position").TankCenterY = 220.0   # Rear deck zone
    dims.addProperty("App::PropertyDistance", "TankCenterX", "Fuel", "20 lb Tank Lateral Position").TankCenterX = 75.0  # Right-rear zone
    dims.addProperty("App::PropertyDistance", "WaterCenterX", "Safety", "Water Tank Lateral Position").WaterCenterX = -170.0 # Left-rear zone

    print("Building Road Roaster 4W v0.1.0 (Commercial 24x36 Platform Cart + 20lb Propane + Cantilever 180° Flip Burner)...")

    # ==========================================================================
    # SUBASSEMBLY CONTAINERS
    # ==========================================================================
    grp_cart = doc.addObject("App::DocumentObjectGroup", "Chassis_Platform_Cart")
    grp_cart.Label = "1. Commercial 24x36 Platform Cart Foundation (5in Running Gear, 29in Handle)"

    grp_burner = doc.addObject("App::DocumentObjectGroup", "Front_Cantilever_Burner")
    grp_burner.Label = "2. Front Cantilevered Radiant Ceramic Burner & 180-deg Flip Hinge"

    grp_fuel = doc.addObject("App::DocumentObjectGroup", "Fuel_System_20lb")
    grp_fuel.Label = "3. 20lb Propane Tank Mounting & Primary Gas Train"

    grp_aux = doc.addObject("App::DocumentObjectGroup", "Auxiliary_Torch_Safety")
    grp_aux.Label = "4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir"

    # ==========================================================================
    # 1. IMPORT COMMERCIAL 24x36 PLATFORM CART FOUNDATION
    # ==========================================================================
    cart_comp = import_component(doc, "platform_cart_24x36", placement=FreeCAD.Placement())
    if cart_comp:
        grp_cart.addObject(cart_comp)

    # ==========================================================================
    # 2. BUILD SUBASSEMBLIES
    # ==========================================================================
    build_front_cantilever_burner_subassembly(doc, grp_burner, dims)
    build_fuel_train_subassembly(doc, grp_fuel, dims)
    build_auxiliary_safety_subassembly(doc, grp_aux, dims)

    doc.recompute()

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    # Export 7 Multi-View Perspective PNG Renders
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

        # Archive milestone thumbnail to changelog/
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)
        home_src = os.path.join(script_dir, f"{doc_name}.png")
        home_dst = os.path.join(changelog_dir, "v0.1.0.png")
        if os.path.exists(home_src):
            shutil.copyfile(home_src, home_dst)
            print(f"Archived milestone render to changelog: {home_dst}")

    # Save Master CAD Model with framed Perspective Isometric home view
    save_model(doc, fcstd_path, camera_type="Perspective")

    # Cleanly close document to release locks and avoid stray backup files
    close_model(doc.Name)
    print("Road Roaster 4W v0.1.0 build complete.")

if __name__ == "__main__":
    build_road_roaster_4w()
    os._exit(0)
