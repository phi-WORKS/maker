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

# ==============================================================================
# SUBASSEMBLY 1: FORWARD DIRECTIONAL RADIANT CERAMIC INFRARED SLED
# ==============================================================================
def build_radiant_sled_subassembly(doc, grp_sled, dims):
    """
    Builds the outer protective steel sled housing, perimeter ground skirts,
    dual skid runners with turned-up tips, suspension bridge, and imports
    the Solaronics Ceramic Infrared Burner module positioned compactly in front
    of the hand truck chassis.
    """
    SLED_W = dims.SledWidth.Value
    SLED_L = dims.SledLength.Value
    SLED_H = dims.SledHeight.Value
    SKIRT_H = dims.SkirtHeight.Value
    SHEET_T = dims.SheetThickness.Value
    GROUND_CLR = dims.GroundClearance.Value
    SLED_Y = dims.SledCenterY.Value
    
    # Sled Colors
    STEEL_HOOD = (0.32, 0.34, 0.38, 0.0)      # 14-gauge Hot-Rolled Steel Sled Cowl
    SKID_STEEL = (0.70, 0.72, 0.75, 0.0)      # Machined Ground Skid Runners
    BRIDGE_STEEL = (0.28, 0.30, 0.33, 0.0)    # Top Suspension Bridge Tower
    
    Z_skirt_bot = GROUND_CLR
    Z_base = Z_skirt_bot + SKIRT_H
    Z_top = Z_base + SLED_H
    
    # 1. Outer Steel Sled Cowl & Perimeter Skirts (Centered at Y = SLED_Y)
    cowl_outer = Part.makeBox(SLED_W, SLED_L, SLED_H + SKIRT_H, FreeCAD.Vector(-SLED_W/2, SLED_Y - SLED_L/2, Z_skirt_bot))
    cowl_inner = Part.makeBox(SLED_W - 2*SHEET_T, SLED_L - 2*SHEET_T, SLED_H + SKIRT_H + 2.0, FreeCAD.Vector(-SLED_W/2 + SHEET_T, SLED_Y - SLED_L/2 + SHEET_T, Z_skirt_bot - 1.0))
    cowl_shell = cowl_outer.cut(cowl_inner)
    
    # Front Heat Draft Vent (Slots at front face Y = SLED_Y - SLED_L/2)
    vent_w = SLED_W - 60.0
    vent_h = 35.0
    vent_cut = Part.makeBox(vent_w, 20.0, vent_h, FreeCAD.Vector(-vent_w/2, SLED_Y - SLED_L/2 - 10.0, Z_base + 10.0))
    cowl_shell = cowl_shell.cut(vent_cut)
    
    # Top Intake / Venturi Exhaust Cutout (for burner manifold breathing)
    top_vent_w = 160.0
    top_vent_l = 180.0
    top_vent_cut = Part.makeBox(top_vent_w, top_vent_l, 20.0, FreeCAD.Vector(-top_vent_w/2, SLED_Y + 20.0, Z_top - 10.0))
    cowl_shell = cowl_shell.cut(top_vent_cut)
    
    # 2. Continuous Ground Skid Runners (1.5" x 3/16" Flat Bar with 30° Ski Tips)
    SKID_W = 38.1
    SKID_T = 4.76
    SKID_TIP_L = 50.8
    SKID_X = SLED_W/2 - SKID_W/2
    
    # Left & Right Main Skid Bars
    skid_l_flat = Part.makeBox(SKID_W, SLED_L, SKID_T, FreeCAD.Vector(-SKID_X - SKID_W/2, SLED_Y - SLED_L/2, Z_skirt_bot - SKID_T))
    skid_r_flat = Part.makeBox(SKID_W, SLED_L, SKID_T, FreeCAD.Vector(SKID_X - SKID_W/2, SLED_Y - SLED_L/2, Z_skirt_bot - SKID_T))
    
    # Front Turned-Up Ski Tips
    tip_fl = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(-SKID_X - SKID_W/2, SLED_Y - SLED_L/2 - SKID_TIP_L, Z_skirt_bot - SKID_T))
    tip_fl.rotate(FreeCAD.Vector(-SKID_X, SLED_Y - SLED_L/2, Z_skirt_bot - SKID_T), FreeCAD.Vector(1, 0, 0), -30.0)
    
    tip_fr = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(SKID_X - SKID_W/2, SLED_Y - SLED_L/2 - SKID_TIP_L, Z_skirt_bot - SKID_T))
    tip_fr.rotate(FreeCAD.Vector(SKID_X, SLED_Y - SLED_L/2, Z_skirt_bot - SKID_T), FreeCAD.Vector(1, 0, 0), -30.0)
    
    # Rear Turned-Up Ski Tips
    tip_rl = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(-SKID_X - SKID_W/2, SLED_Y + SLED_L/2, Z_skirt_bot - SKID_T))
    tip_rl.rotate(FreeCAD.Vector(-SKID_X, SLED_Y + SLED_L/2, Z_skirt_bot - SKID_T), FreeCAD.Vector(1, 0, 0), 30.0)
    
    tip_rr = Part.makeBox(SKID_W, SKID_TIP_L, SKID_T, FreeCAD.Vector(SKID_X - SKID_W/2, SLED_Y + SLED_L/2, Z_skirt_bot - SKID_T))
    tip_rr.rotate(FreeCAD.Vector(SKID_X, SLED_Y + SLED_L/2, Z_skirt_bot - SKID_T), FreeCAD.Vector(1, 0, 0), 30.0)
    
    skids_shape = skid_l_flat.fuse(skid_r_flat).fuse(tip_fl).fuse(tip_fr).fuse(tip_rl).fuse(tip_rr)
    
    # 3. Top Suspension Bridge & Tilt-Latch Catch Tower (At rear of sled cowl)
    bridge_w = SLED_W + 10.0
    bridge_plate = Part.makeBox(bridge_w, 60.0, 4.76, FreeCAD.Vector(-bridge_w/2, SLED_Y + SLED_L/2 - 60.0, Z_top))
    tower_h = 75.0
    catch_tower = Part.makeBox(40.0, 30.0, tower_h, FreeCAD.Vector(-20.0, SLED_Y + SLED_L/2 - 45.0, Z_top))
    catch_pin = Part.makeCylinder(6.0, 50.0, FreeCAD.Vector(-25.0, SLED_Y + SLED_L/2 - 30.0, Z_top + tower_h - 15.0), FreeCAD.Vector(1, 0, 0))
    bridge_shape = bridge_plate.fuse(catch_tower).fuse(catch_pin)
    
    # Add Document Objects
    obj_cowl = doc.addObject("Part::Feature", "Radiant_Sled_Outer_Cowl")
    obj_cowl.Label = "14-Gauge Steel Protective Radiant Sled Cowl & Skirts"
    obj_cowl.Shape = cowl_shell
    grp_sled.addObject(obj_cowl)
    set_vis(doc, obj_cowl, STEEL_HOOD)
    
    obj_skids = doc.addObject("Part::Feature", "Radiant_Sled_Skid_Runners")
    obj_skids.Label = "Continuous Flat Bar Skid Runners with 30-deg Ski Tips"
    obj_skids.Shape = skids_shape
    grp_sled.addObject(obj_skids)
    set_vis(doc, obj_skids, SKID_STEEL)
    
    obj_bridge = doc.addObject("Part::Feature", "Radiant_Sled_Suspension_Bridge")
    obj_bridge.Label = "Sled Suspension Bridge & Transit Latch Catch Tower"
    obj_bridge.Shape = bridge_shape
    grp_sled.addObject(obj_bridge)
    set_vis(doc, obj_bridge, BRIDGE_STEEL)
    
    # 4. Import Standalone Solaronics Ceramic Infrared Burner Component
    burner_pos = FreeCAD.Vector(0, SLED_Y, Z_skirt_bot + 45.0)
    burner_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 0)
    burner_grp = import_component(doc, "solaronics_infrared_burner", placement=FreeCAD.Placement(burner_pos, burner_rot))
    if burner_grp:
        grp_sled.addObject(burner_grp)

# ==============================================================================
# SUBASSEMBLY 2: COMMON-AXIS TRIANGULAR SLED SUSPENSION & TRANSIT LATCH
# ==============================================================================
def build_suspension_linkage_subassembly(doc, grp_susp, dims):
    """
    Builds the triangular suspension straps linking the sled directly to the
    COMMON WHEEL AXLE (pivoting on the axle shaft inside the frame trusses),
    matching the triangular truss geometry of the vintage hand truck frame.
    """
    SLED_W = dims.SledWidth.Value
    SLED_L = dims.SledLength.Value
    SLED_Y = dims.SledCenterY.Value
    AXLE_Y = dims.AxleY.Value
    AXLE_Z = dims.AxleZ.Value
    
    STRAP_T = 4.76      # 3/16 in steel strap
    STRAP_W = 25.4      # 1.0 in wide strap
    SLEEVE_OD = 25.4    # 1.0 in OD axle pivot bushing
    SLEEVE_LEN = 25.0
    
    LINKAGE_STEEL = (0.45, 0.48, 0.52, 0.0)
    LATCH_GOLD = (0.85, 0.65, 0.15, 0.0)
    
    # Common Axle Mounting: Sled triangular straps mount directly onto the axle shaft
    # at X = ±145 mm (inboard of the hand truck uprights X = ±158.75 mm and frame trusses X = ±175 mm)
    x_arm_positions = [-145.0, 145.0]
    
    # Target Sled Mount Coordinates:
    # Lower mount at rear sled chassis: (x_arm, SLED_Y + SLED_L/2 - 20 mm, Z = 50 mm)
    # Upper mount at sled bridge tower: (x_arm, SLED_Y + SLED_L/2 - 45 mm, Z = 193.5 mm)
    y_target_low = SLED_Y + SLED_L/2 - 20.0
    z_target_low = 50.0
    y_target_up = SLED_Y + SLED_L/2 - 45.0
    z_target_up = 193.5
    
    def make_strap_yz(y1, z1, y2, z2, width, thickness, x_center):
        dy = y2 - y1
        dz = z2 - z1
        L = math.hypot(dy, dz)
        if L == 0:
            return None
        ny = -dz / L * (width / 2.0)
        nz = dy / L * (width / 2.0)
        v1 = FreeCAD.Vector(0, y1 + ny, z1 + nz)
        v2 = FreeCAD.Vector(0, y2 + ny, z2 + nz)
        v3 = FreeCAD.Vector(0, y2 - ny, z2 - nz)
        v4 = FreeCAD.Vector(0, y1 - ny, z1 - nz)
        poly = Part.makePolygon([v1, v2, v3, v4, v1])
        face = Part.Face(poly)
        solid = face.extrude(FreeCAD.Vector(thickness, 0, 0))
        solid.translate(FreeCAD.Vector(x_center - thickness/2.0, 0, 0))
        return solid
    
    triangular_straps = []
    
    for x_a in x_arm_positions:
        # 1. Axle Pivot Sleeve Bushing (Rotates directly on the 5/8" continuous axle shaft)
        sleeve = Part.makeCylinder(SLEEVE_OD/2, SLEEVE_LEN,
                                   FreeCAD.Vector(x_a - SLEEVE_LEN/2, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
        
        # 2. Lower Forward Strut: Axle (AXLE_Y, AXLE_Z) -> Sled Lower Chassis (y_target_low, z_target_low)
        strut_low = make_strap_yz(AXLE_Y, AXLE_Z, y_target_low, z_target_low, STRAP_W, STRAP_T, x_a)
        
        # 3. Upper Forward Strut: Axle (AXLE_Y, AXLE_Z) -> Sled Bridge Tower (y_target_up, z_target_up)
        strut_up = make_strap_yz(AXLE_Y, AXLE_Z, y_target_up, z_target_up, STRAP_W, STRAP_T, x_a)
        
        # 4. Vertical Stiffener Web / Gusset Plate (Rigidifying the triangle)
        gusset_h = abs(z_target_up - z_target_low) - 20.0
        gusset = Part.makeBox(STRAP_T, STRAP_W, gusset_h,
                              FreeCAD.Vector(x_a - STRAP_T/2, y_target_low - STRAP_W, z_target_low + 10.0))
        
        # 5. Pivot attachment pin bosses at sled
        pin_low = Part.makeCylinder(6.35, 20.0, FreeCAD.Vector(x_a - 10.0, y_target_low, z_target_low), FreeCAD.Vector(1, 0, 0))
        pin_up = Part.makeCylinder(6.35, 20.0, FreeCAD.Vector(x_a - 10.0, y_target_up, z_target_up), FreeCAD.Vector(1, 0, 0))
        
        arm_side = sleeve.fuse(strut_low).fuse(strut_up).fuse(gusset).fuse(pin_low).fuse(pin_up)
        triangular_straps.append(arm_side)
    
    triangular_arms_compound = triangular_straps[0].fuse(triangular_straps[1])
    
    # 6. Foot-Release Upright Transit Tilt Snap Latch
    # Mounted to the lower horizontal cross-strap at Z = 292 mm, Y = 0
    # Reaches forward to latch onto the catch pin on the sled bridge tower at Y = SLED_Y + SLED_L/2 - 30 mm
    latch_y_catch = SLED_Y + SLED_L/2 - 30.0
    latch_len = abs(latch_y_catch) + 30.0
    latch_bar = Part.makeBox(15.0, latch_len, 6.0, FreeCAD.Vector(-7.5, -latch_len + 15.0, 260.0))
    latch_pedal = Part.makeBox(50.0, 35.0, 6.0, FreeCAD.Vector(-25.0, -10.0, 285.0))
    latch_hook = Part.makeCylinder(8.0, 25.0, FreeCAD.Vector(-12.5, latch_y_catch, 260.0), FreeCAD.Vector(1, 0, 0))
    latch_shape = latch_bar.fuse(latch_pedal).fuse(latch_hook)
    
    obj_arms = doc.addObject("Part::Feature", "Axle_Triangular_Sled_Straps")
    obj_arms.Label = "Axle-Mounted Triangular Sled Suspension Straps (Common Pivot Axis)"
    obj_arms.Shape = triangular_arms_compound
    grp_susp.addObject(obj_arms)
    set_vis(doc, obj_arms, LINKAGE_STEEL)
    
    obj_latch = doc.addObject("Part::Feature", "Transit_Tilt_Snap_Latch")
    obj_latch.Label = "Foot-Release Upright Vacuum Tilt Snap Latch"
    obj_latch.Shape = latch_shape
    grp_susp.addObject(obj_latch)
    set_vis(doc, obj_latch, LATCH_GOLD)

# ==============================================================================
# SUBASSEMBLY 3: PROPANE FUEL TRAIN & TANK-MOUNTED ROTARY FLOW VALVE
# ==============================================================================
def build_gas_train_subassembly(doc, grp_gas, dims):
    """
    Mounts the propane cylinder and quick-release harness solidly to the vintage
    hand truck frame, models the integrated rotating flow control valve & 11" W.C. regulator
    directly atop the tank, and routes the flexible gas hose to the burner manifold.
    """
    SLED_Y = dims.SledCenterY.Value
    
    HOSE_BLACK = (0.12, 0.12, 0.14, 0.0)      # Flexible 350 PSI Gas Hose
    REG_ZINC = (0.60, 0.62, 0.65, 0.0)        # 11" W.C. Low Pressure LP Regulator
    VALVE_BRASS = (0.85, 0.65, 0.20, 0.0)     # Brass Flow Control Rotary Valve & Knob
    WIRE_ORANGE = (0.95, 0.40, 0.05, 0.0)     # Silicone Spark Ignition Wire
    MOUNT_STEEL = (0.35, 0.38, 0.42, 0.0)     # Steel Frame Clamping Brackets
    
    # 1. Mount Propane Bottle Harness & 1 lb Cylinder BEHIND the vertical supports
    # Positioned in the right bay (X = +80 mm), behind middle horizontal cross strap (Strap 2: Z in [533.4, 558.8 mm])
    # Cylinder centered at X = +80.0 mm, Y = +75.4 mm, seated at Z = 460.0 mm
    cyl_pos = FreeCAD.Vector(80.0, 75.4, 460.0)
    cyl_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), -90) # Open cage facing rearward to operator
    cyl_grp = import_component(doc, "propane_cylinder_1lb", placement=FreeCAD.Placement(cyl_pos, cyl_rot))
    if cyl_grp:
        grp_gas.addObject(cyl_grp)
        
    harn_pos = FreeCAD.Vector(80.0, 75.4, 460.0)
    harn_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), -90)
    harn_grp = import_component(doc, "propane_harness", placement=FreeCAD.Placement(harn_pos, harn_rot))
    if harn_grp:
        grp_gas.addObject(harn_grp)
        
    # 2. Structural Clamping Straps connecting Harness directly to Hand Truck Horizontal Cross-Strap
    # Middle cross-strap (Strap 2) is at Z in [533.4, 558.8 mm], thickness in [12.7, 17.46 mm]
    # Clamping bracket wraps around Strap 2 with front and rear clamping jaws:
    bkt_w = 50.0        # Width along X
    bkt_t = 4.76        # 3/16 in steel flat bar
    
    # Rear clamp plate welded to harness spine (flush against rear of cross-strap at Y = 17.46 mm)
    rear_plate = Part.makeBox(bkt_w, bkt_t, 45.0, FreeCAD.Vector(80.0 - bkt_w/2, 17.46, 523.0))
    
    # Upper clamp lip hooking over top edge of Strap 2 (Z = 558.8 mm)
    lip_top = Part.makeBox(bkt_w, 14.22, bkt_t, FreeCAD.Vector(80.0 - bkt_w/2, 8.0, 558.8))
    
    # Lower clamp lip hooking under bottom edge of Strap 2 (Z = 533.4 mm)
    lip_bot = Part.makeBox(bkt_w, 14.22, bkt_t, FreeCAD.Vector(80.0 - bkt_w/2, 8.0, 528.64))
    
    # Front retention plate sandwiching the cross strap (Y in [8.0, 12.76 mm])
    front_plate = Part.makeBox(bkt_w, bkt_t, 45.0, FreeCAD.Vector(80.0 - bkt_w/2, 8.0, 523.0))
    
    # Through-clamping bolt heads
    bolt1 = Part.makeCylinder(5.0, 18.0, FreeCAD.Vector(65.0, 7.0, 546.0), FreeCAD.Vector(0, 1, 0))
    bolt2 = Part.makeCylinder(5.0, 18.0, FreeCAD.Vector(95.0, 7.0, 546.0), FreeCAD.Vector(0, 1, 0))
    
    # Side stabilizer tab reaching to right vertical pipe (X = 158.75 mm)
    tab_len = 158.75 - (80.0 + bkt_w/2)
    stab_tab = Part.makeBox(tab_len, bkt_t, 25.4, FreeCAD.Vector(80.0 + bkt_w/2, 12.7, 533.4))
    
    harness_clamps_solid = rear_plate.fuse(lip_top).fuse(lip_bot).fuse(front_plate).fuse(bolt1).fuse(bolt2).fuse(stab_tab)
    
    obj_mount = doc.addObject("Part::Feature", "Propane_Harness_Strap_Clamps")
    obj_mount.Label = "Propane Harness Horizontal Cross-Strap Clamping Brackets"
    obj_mount.Shape = harness_clamps_solid
    grp_gas.addObject(obj_mount)
    set_vis(doc, obj_mount, MOUNT_STEEL)
    
    # 3. Tank-Mounted Rotating Flow Control Valve & Integrated 11" W.C. Regulator
    valve_neck = Part.makeCylinder(10.0, 25.0, FreeCAD.Vector(80.0, 75.4, 650.0), FreeCAD.Vector(0, 0, 1))
    reg_body = Part.makeCylinder(24.0, 18.0, FreeCAD.Vector(80.0, 75.4, 675.0), FreeCAD.Vector(0, 0, 1))
    dial_knob = Part.makeCylinder(15.0, 12.0, FreeCAD.Vector(80.0, 75.4, 693.0), FreeCAD.Vector(0, 0, 1))
    dial_indicator = Part.makeBox(4.0, 14.0, 6.0, FreeCAD.Vector(78.0, 63.4, 696.0))
    piezo_btn = Part.makeCylinder(5.0, 10.0, FreeCAD.Vector(80.0, 89.4, 680.0), FreeCAD.Vector(0, 1, 0))
    
    valve_assembly_shape = valve_neck.fuse(reg_body).fuse(dial_knob).fuse(dial_indicator).fuse(piezo_btn)
    
    obj_valve = doc.addObject("Part::Feature", "Tank_Mounted_Regulator_Valve")
    obj_valve.Label = "Tank-Mounted Rotary Flow Control Valve & 11in Regulator"
    obj_valve.Shape = valve_assembly_shape
    grp_gas.addObject(obj_valve)
    set_vis(doc, obj_valve, VALVE_BRASS)
    
    # 4. Smooth B-Spline Flexible Gas Hose traveling down Center Support Pipe
    # Originates at regulator, curves over to center spine pipe, travels vertically down,
    # and curves forward through the open bay directly to the Solaronics burner gas connector
    p_reg = FreeCAD.Vector(70.0, 75.4, 675.0)
    p_burner_inlet = FreeCAD.Vector(0.0, SLED_Y + 259.3, 92.9)
    
    hose_pts = [
        p_reg,
        FreeCAD.Vector(35.0, 48.0, 630.0),
        FreeCAD.Vector(8.0, 26.0, 570.0),
        FreeCAD.Vector(8.0, 26.0, 420.0),
        FreeCAD.Vector(8.0, 26.0, 280.0),
        FreeCAD.Vector(6.0, 22.0, 160.0),
        FreeCAD.Vector(0.0, 5.0, 110.0),
        FreeCAD.Vector(0.0, -18.0, 95.0),
        p_burner_inlet
    ]
    
    spline_h = Part.BSplineCurve()
    spline_h.interpolate(hose_pts)
    wire_h = Part.Wire([Part.Edge(spline_h)])
    circ_h = Part.makeCircle(4.76, hose_pts[0], spline_h.tangent(0.0)[0])
    face_h = Part.Face(Part.Wire([circ_h]))
    flexible_gas_hose = wire_h.makePipe(face_h)
    
    # Brass crimp ferrule fittings at hose ends
    ferrule_top = Part.makeCylinder(6.5, 18.0, FreeCAD.Vector(70.0, 75.4, 665.0), spline_h.tangent(0.0)[0])
    ferrule_bot = Part.makeCylinder(6.5, 18.0, FreeCAD.Vector(0.0, SLED_Y + 259.3 - 10.0, 92.9), FreeCAD.Vector(0, 1, 0))
    flexible_gas_hose = flexible_gas_hose.fuse(ferrule_top).fuse(ferrule_bot)
    
    # 5. High-Voltage Silicone Spark Igniter Wire traveling down Center Support Pipe
    # Originates at piezo push-button, joins center spine pipe alongside hose,
    # travels down center support, and curves forward into burner ceramic matrix
    p_piezo = FreeCAD.Vector(75.0, 89.4, 675.0)
    p_spark_dest = FreeCAD.Vector(-65.25, SLED_Y - 84.3, 90.4)
    
    spark_pts = [
        p_piezo,
        FreeCAD.Vector(35.0, 55.0, 630.0),
        FreeCAD.Vector(-8.0, 26.0, 570.0),
        FreeCAD.Vector(-8.0, 26.0, 420.0),
        FreeCAD.Vector(-8.0, 26.0, 280.0),
        FreeCAD.Vector(-8.0, 22.0, 160.0),
        FreeCAD.Vector(-15.0, 5.0, 110.0),
        FreeCAD.Vector(-35.0, -100.0, 100.0),
        FreeCAD.Vector(-55.0, -250.0, 95.0),
        p_spark_dest
    ]
    
    spline_w = Part.BSplineCurve()
    spline_w.interpolate(spark_pts)
    wire_w = Part.Wire([Part.Edge(spline_w)])
    circ_w = Part.makeCircle(2.0, spark_pts[0], spline_w.tangent(0.0)[0])
    face_w = Part.Face(Part.Wire([circ_w]))
    flexible_spark_wire = wire_w.makePipe(face_w)
    
    # 6. Center Support Cable & Hose Retention Clips (Zip-Ties / P-Clips)
    # Wrapping around the 1.0" OD center spine pipe at Z = 540 mm and Z = 300 mm
    clip_1 = Part.makeTorus(14.5, 2.5, FreeCAD.Vector(0.0, 16.0, 540.0), FreeCAD.Vector(0, 0, 1))
    clip_2 = Part.makeTorus(14.5, 2.5, FreeCAD.Vector(0.0, 16.0, 300.0), FreeCAD.Vector(0, 0, 1))
    clips_shape = clip_1.fuse(clip_2)
    
    obj_clips = doc.addObject("Part::Feature", "Center_Spine_Hose_Clips")
    obj_clips.Label = "Center Support Pipe Hose & Wire Retention Clips"
    obj_clips.Shape = clips_shape
    grp_gas.addObject(obj_clips)
    set_vis(doc, obj_clips, MOUNT_STEEL)
    
    obj_hose = doc.addObject("Part::Feature", "Flexible_Gas_Feed_Hose")
    obj_hose.Label = "Flexible 3/8in Reinforced LP Gas Hose (Center Support Routed)"
    obj_hose.Shape = flexible_gas_hose
    grp_gas.addObject(obj_hose)
    set_vis(doc, obj_hose, HOSE_BLACK)
    
    obj_spark = doc.addObject("Part::Feature", "Flexible_Spark_Ignition_Wire")
    obj_spark.Label = "High-Voltage Silicone Spark Ignition Wire (Center Support Routed)"
    obj_spark.Shape = flexible_spark_wire
    grp_gas.addObject(obj_spark)
    set_vis(doc, obj_spark, WIRE_ORANGE)

# ==============================================================================
# MASTER ASSEMBLY BUILD FUNCTION
# ==============================================================================
def build_road_roaster():
    doc_name = "road_roaster"
    doc = FreeCAD.newDocument(doc_name)
    
    # Parametric VarSet (Accurate Physical Datum & Sled Dimensions)
    dims = doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "SledWidth", "Dimensions", "Outer Sled Cowl Width").SledWidth = 381.0       # 15.0 in
    dims.addProperty("App::PropertyLength", "SledLength", "Dimensions", "Outer Sled Cowl Length").SledLength = 457.2     # 18.0 in
    dims.addProperty("App::PropertyLength", "SledHeight", "Dimensions", "Outer Sled Cowl Height").SledHeight = 130.0     # 5.12 in
    dims.addProperty("App::PropertyLength", "SkirtHeight", "Dimensions", "Ground Skirt Height").SkirtHeight = 50.8       # 2.0 in
    dims.addProperty("App::PropertyLength", "GroundClearance", "Dimensions", "Ground Clearance").GroundClearance = 12.7  # 0.5 in
    dims.addProperty("App::PropertyDistance", "SledCenterY", "Dimensions", "Forward Sled Center Position").SledCenterY = -300.0 # Snug forward stance
    dims.addProperty("App::PropertyLength", "SheetThickness", "Dimensions", "14-Ga Sheet Steel").SheetThickness = 1.905  # 0.075 in
    dims.addProperty("App::PropertyLength", "AxleY", "Dimensions", "Axle Y Position").AxleY = 120.65                    # 4.75 in from side rail
    dims.addProperty("App::PropertyLength", "AxleZ", "Dimensions", "Axle Z Position").AxleZ = 120.65                    # 4.75 in from floor
    dims.addProperty("App::PropertyLength", "WheelDiameter", "Dimensions", "Wheel Diameter").WheelDiameter = 241.3      # 9.5 in wheels
    dims.addProperty("App::PropertyFloat", "BurnerBTU", "Thermal", "Radiant Heat Rating").BurnerBTU = 60000.0
    
    print("Building Road Roaster v0.7.0 (Vintage Hand Truck + Common-Axis Triangular Sled Suspension)...")
    
    # 1. Master Containers
    grp_chassis = doc.addObject("App::DocumentObjectGroup", "Commercial_HandTruck_Chassis")
    grp_chassis.Label = "1. Vintage Hand Truck Chassis (U-Frame, Triangular Axle Trusses, 9.5in Wheels)"
    
    grp_sled = doc.addObject("App::DocumentObjectGroup", "Solaronics_Infrared_Sled")
    grp_sled.Label = "2. Forward Directional Radiant Ceramic Infrared Sled & Ground Skids"
    
    grp_susp = doc.addObject("App::DocumentObjectGroup", "Suspension_Linkage")
    grp_susp.Label = "3. Common-Axis Triangular Sled Suspension Straps & Transit Tilt Latch"
    
    grp_gas = doc.addObject("App::DocumentObjectGroup", "Propane_Gas_Train")
    grp_gas.Label = "4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve"
    
    # 2. Import Hand Truck Chassis
    hand_truck_grp = import_component(doc, "commercial_hand_truck", placement=FreeCAD.Placement())
    if hand_truck_grp:
        grp_chassis.addObject(hand_truck_grp)
        
    # 3. Build Subassemblies
    build_radiant_sled_subassembly(doc, grp_sled, dims)
    build_suspension_linkage_subassembly(doc, grp_susp, dims)
    build_gas_train_subassembly(doc, grp_gas, dims)
    
    doc.recompute()
    
    fcstd_path = os.path.join(script_dir, "road-roaster.FCStd")
    doc.saveAs(fcstd_path)
    print(f"Saved master Road Roaster assembly: {fcstd_path}")
    
    # 4. Render Orthogonal & Isometric PNG Views
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, "road-roaster")
        export_orthogonal_views(gui_doc, base_prefix, model_prefix="road-roaster")
        
    FreeCAD.closeDocument(doc.Name)
    print("Road Roaster v0.7.0 build and render complete.")

if __name__ == "__main__":
    build_road_roaster()
    sys.exit(0)
