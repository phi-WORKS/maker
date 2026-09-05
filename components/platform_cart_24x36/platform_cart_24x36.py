"""
Commercial 24" x 36" Platform Cart Component (Dolly Chassis)
Standalone 3D Parametric CAD Module

Modeled after standard commercial heavy-duty steel/aluminum platform trucks:
- Deck: 24.0" (609.6 mm) wide x 36.0" (914.4 mm) long with diamond non-skid plate relief
- Perimeter skirt downturn (1.75" / 45 mm) with 1.5" radiused corners
- 4 heavy-duty molded rubber corner bumpers with recessed socket fasteners
- Under-deck longitudinal channels and cross stringers (1000+ lb capacity)
- 4-wheel running gear with 5.0" (127.0 mm) diameter wheels:
  - 2 Front rigid stamped steel casters
  - 2 Rear 360-deg swivel casters with integrated foot brake lock levers
  - Heavy-duty yellow hub cores with black industrial treaded rubber tires
- Handle: 1.25" OD tubular steel push handle rising 29.0" (736.6 mm) above the deck
  - 2 horizontal reinforcement/accessory cross rails
  - Folding base hinge brackets with foot-release cross bar
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

def set_obj_visuals(doc, obj, color):
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        if gui_d:
            g_obj = gui_d.getObject(obj.Name)
            if g_obj:
                g_obj.Visibility = True
                g_obj.ShapeColor = color
                g_obj.DisplayMode = "Flat Lines"

def create_platform_cart_component(doc, placement=None):
    """
    Creates the Commercial 24" x 36" Platform Cart in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing cart subassemblies
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp_root = doc.addObject("App::DocumentObjectGroup", "Platform_Cart_24x36")
    grp_root.Label = "Commercial 24x36 Platform Cart (5in Wheels, 29in Handle)"

    grp_deck = doc.addObject("App::DocumentObjectGroup", "Cart_Deck_Subassembly")
    grp_deck.Label = "1. Deck & Frame Subassembly (24x36in Diamond Plate)"

    grp_gear = doc.addObject("App::DocumentObjectGroup", "Cart_Running_Gear")
    grp_gear.Label = "2. Running Gear (5in Yellow-Hub Wheels & Casters)"

    grp_handle = doc.addObject("App::DocumentObjectGroup", "Cart_Push_Handle")
    grp_handle.Label = "3. Push Handle Subassembly (29in Height, Folding Base)"

    grp_root.addObject(grp_deck)
    grp_root.addObject(grp_gear)
    grp_root.addObject(grp_handle)

    # ==========================================================================
    # COLOR PALETTE
    # ==========================================================================
    DECK_ALUM = (0.78, 0.80, 0.83, 0.0)       # Diamond-Plate Aluminum / Zinc Deck
    DIAMOND_LIP = (0.84, 0.86, 0.88, 0.0)     # Embossed Diamond Plate Ribs
    FRAME_STEEL = (0.38, 0.40, 0.44, 0.0)     # Under-Deck Structural Channel Steel
    BUMPER_BLACK = (0.15, 0.15, 0.16, 0.0)    # Molded Impact Rubber Corner Bumpers
    BUMPER_BOLT = (0.45, 0.65, 0.90, 0.0)     # Blue Anodized / Zinc Center Fasteners
    CASTER_STEEL = (0.75, 0.78, 0.82, 0.0)    # Zinc-Plated Stamped Caster Brackets
    WHEEL_YELLOW = (0.92, 0.72, 0.08, 0.0)    # High-Visibility Yellow Hub Core
    TIRE_BLACK = (0.12, 0.12, 0.13, 0.0)      # Solid Rubber Tread
    AXLE_BOLT = (0.82, 0.84, 0.86, 0.0)       # Grade 5 Axle Bolts & Nuts
    HANDLE_CHROME = (0.86, 0.88, 0.91, 0.0)   # Chrome / Polished Stainless Tubing
    HINGE_STEEL = (0.68, 0.70, 0.74, 0.0)     # Heavy Gauge Folding Hinge Hardware
    BRAKE_PEDAL = (0.70, 0.72, 0.76, 0.0)     # Caster Foot Lock Pedal

    # ==========================================================================
    # PARAMETRIC DIMENSIONS
    # ==========================================================================
    DECK_W = 609.6              # 24.0 in width along X
    DECK_L = 914.4              # 36.0 in length along Y
    DECK_SKIRT_H = 45.0         # 1.77 in perimeter skirt height
    DECK_TOP_Z = 175.0          # Top surface of deck from ground (~6.9 in)
    DECK_BOT_Z = DECK_TOP_Z - DECK_SKIRT_H  # Bottom of skirt at Z = 130.0 mm
    CORNER_R = 38.1             # 1.5 in corner fillet radius
    SHEET_T = 3.175             # 1/8 in aluminum sheet deck

    WHEEL_DIA = 127.0           # 5.0 in wheel outer diameter
    WHEEL_R = WHEEL_DIA / 2.0   # 63.5 mm (2.5 in)
    WHEEL_W = 35.0              # 1.38 in tread face width
    AXLE_Z = WHEEL_R            # 63.5 mm from ground
    HUB_DIA = 65.0              # Hub center diameter
    HUB_W = 40.0                # Hub width across bearings

    CASTER_TOP_Z = DECK_BOT_Z   # Mounting plate underside of deck frame (Z = 130 mm)
    TRACK_X = 220.0             # Caster lateral centerlines (X = ±220 mm)
    WHEELBASE_Y = 320.0         # Front casters Y = -320 mm, Rear casters Y = +320 mm

    HANDLE_H = 736.6            # Exactly 29.0 in user specified handle height above deck
    HANDLE_TUBE_OD = 31.75      # 1.25 in OD tubular steel
    R_tube = HANDLE_TUBE_OD / 2.0
    HANDLE_W = 480.0            # Center-to-center upright width
    HANDLE_Y = DECK_L / 2.0 - 45.0  # Inset from rear edge (Y = +412.2 mm)

    # --------------------------------------------------------------------------
    # 1. DECK PLATE & PERIMETER SKIRT WITH ROUNDED CORNERS
    # --------------------------------------------------------------------------
    # Outer rounded rectangle profile
    dx = DECK_W / 2.0 - CORNER_R
    dy = DECK_L / 2.0 - CORNER_R

    # Central core boxes
    box_x = Part.makeBox(DECK_W - 2*CORNER_R, DECK_L, DECK_SKIRT_H,
                         FreeCAD.Vector(-dx, -DECK_L/2.0, DECK_BOT_Z))
    box_y = Part.makeBox(DECK_W, DECK_L - 2*CORNER_R, DECK_SKIRT_H,
                         FreeCAD.Vector(-DECK_W/2.0, -dy, DECK_BOT_Z))
    deck_solid = box_x.fuse(box_y)

    # 4 Corner rounded cylinders
    c_fl = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(-dx, -dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_fr = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(dx, -dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_rl = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(-dx, dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_rr = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(dx, dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    deck_solid = deck_solid.fuse(c_fl).fuse(c_fr).fuse(c_rl).fuse(c_rr)

    # Hollow out bottom to create 3.2 mm wall skirt downturn
    inner_w = DECK_W - 2*SHEET_T
    inner_l = DECK_L - 2*SHEET_T
    inner_r = max(CORNER_R - SHEET_T, 2.0)
    idx = inner_w / 2.0 - inner_r
    idy = inner_l / 2.0 - inner_r

    ibox_x = Part.makeBox(inner_w - 2*inner_r, inner_l, DECK_SKIRT_H - SHEET_T + 1.0,
                          FreeCAD.Vector(-idx, -inner_l/2.0, DECK_BOT_Z - 0.5))
    ibox_y = Part.makeBox(inner_w, inner_l - 2*inner_r, DECK_SKIRT_H - SHEET_T + 1.0,
                          FreeCAD.Vector(-inner_w/2.0, -idy, DECK_BOT_Z - 0.5))
    inner_core = ibox_x.fuse(ibox_y)

    ic_fl = Part.makeCylinder(inner_r, DECK_SKIRT_H - SHEET_T + 1.0, FreeCAD.Vector(-idx, -idy, DECK_BOT_Z - 0.5), FreeCAD.Vector(0, 0, 1))
    ic_fr = Part.makeCylinder(inner_r, DECK_SKIRT_H - SHEET_T + 1.0, FreeCAD.Vector(idx, -idy, DECK_BOT_Z - 0.5), FreeCAD.Vector(0, 0, 1))
    ic_rl = Part.makeCylinder(inner_r, DECK_SKIRT_H - SHEET_T + 1.0, FreeCAD.Vector(-idx, idy, DECK_BOT_Z - 0.5), FreeCAD.Vector(0, 0, 1))
    ic_rr = Part.makeCylinder(inner_r, DECK_SKIRT_H - SHEET_T + 1.0, FreeCAD.Vector(idx, idy, DECK_BOT_Z - 0.5), FreeCAD.Vector(0, 0, 1))
    inner_core = inner_core.fuse(ic_fl).fuse(ic_fr).fuse(ic_rl).fuse(ic_rr)

    deck_shell = deck_solid.cut(inner_core)

    # Diamond plate raised traction ribs on top surface (embossed non-skid relief)
    rib_solids = []
    num_ribs_y = 11
    num_ribs_x = 7
    pitch_y = (DECK_L - 100.0) / (num_ribs_y - 1)
    pitch_x = (DECK_W - 80.0) / (num_ribs_x - 1)
    for iy in range(num_ribs_y):
        ry = -DECK_L/2.0 + 50.0 + iy * pitch_y
        for ix in range(num_ribs_x):
            rx = -DECK_W/2.0 + 40.0 + ix * pitch_x
            angle = 45.0 if (ix + iy) % 2 == 0 else -45.0
            rib = Part.makeBox(22.0, 4.5, 1.2, FreeCAD.Vector(-11.0, -2.25, DECK_TOP_Z))
            rib.rotate(FreeCAD.Vector(0, 0, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1), angle)
            rib.translate(FreeCAD.Vector(rx, ry, 0))
            rib_solids.append(rib)

    all_ribs = rib_solids[0]
    for r in rib_solids[1:]:
        all_ribs = all_ribs.fuse(r)

    # --------------------------------------------------------------------------
    # 2. UNDER-DECK STRUCTURAL STEEL REINFORCING CHANNELS
    # --------------------------------------------------------------------------
    CH_W = 40.0
    CH_H = 30.0
    CH_L = DECK_L - 40.0
    chan_left = Part.makeBox(CH_W, CH_L, CH_H, FreeCAD.Vector(-TRACK_X - CH_W/2.0, -CH_L/2.0, DECK_BOT_Z))
    chan_right = Part.makeBox(CH_W, CH_L, CH_H, FreeCAD.Vector(TRACK_X - CH_W/2.0, -CH_L/2.0, DECK_BOT_Z))

    STR_W = DECK_W - 40.0
    STR_L = 40.0
    str_front = Part.makeBox(STR_W, STR_L, CH_H, FreeCAD.Vector(-STR_W/2.0, -WHEELBASE_Y - STR_L/2.0, DECK_BOT_Z))
    str_mid   = Part.makeBox(STR_W, STR_L, CH_H, FreeCAD.Vector(-STR_W/2.0, -STR_L/2.0, DECK_BOT_Z))
    str_rear  = Part.makeBox(STR_W, STR_L, CH_H, FreeCAD.Vector(-STR_W/2.0, WHEELBASE_Y - STR_L/2.0, DECK_BOT_Z))

    under_frame = chan_left.fuse(chan_right).fuse(str_front).fuse(str_mid).fuse(str_rear)

    # --------------------------------------------------------------------------
    # 3. MOLDED RUBBER CORNER BUMPERS WITH FASTENERS (4 CORNERS)
    # --------------------------------------------------------------------------
    bumpers = []
    bumper_bolts = []
    BUMP_THICK = 10.0
    BUMP_H = DECK_SKIRT_H + 4.0
    BUMP_LEG = 65.0
    BUMP_Z = DECK_BOT_Z - 2.0

    corner_positions = [
        (-DECK_W/2.0, -DECK_L/2.0, 1, 1),    # Front-Left
        (DECK_W/2.0, -DECK_L/2.0, -1, 1),    # Front-Right
        (-DECK_W/2.0, DECK_L/2.0, 1, -1),    # Rear-Left
        (DECK_W/2.0, DECK_L/2.0, -1, -1),    # Rear-Right
    ]

    for cx, cy, sx, sy in corner_positions:
        b_x = Part.makeBox(BUMP_LEG, BUMP_THICK, BUMP_H,
                           FreeCAD.Vector(cx if sx > 0 else cx - BUMP_LEG,
                                          cy - BUMP_THICK if sy > 0 else cy,
                                          BUMP_Z))
        b_y = Part.makeBox(BUMP_THICK, BUMP_LEG, BUMP_H,
                           FreeCAD.Vector(cx - BUMP_THICK if sx > 0 else cx,
                                          cy if sy > 0 else cy - BUMP_LEG,
                                          BUMP_Z))
        cap_r = CORNER_R + BUMP_THICK
        c_cap = Part.makeCylinder(cap_r, BUMP_H,
                                  FreeCAD.Vector(cx + sx * CORNER_R, cy + sy * CORNER_R, BUMP_Z),
                                  FreeCAD.Vector(0, 0, 1))
        cutter = Part.makeBox(cap_r * 2, cap_r * 2, BUMP_H + 2.0,
                              FreeCAD.Vector(cx if sx < 0 else cx - 2*cap_r,
                                             cy if sy < 0 else cy - 2*cap_r,
                                             BUMP_Z - 1.0))
        c_quarter = c_cap.cut(cutter)
        bumper_unit = b_x.fuse(b_y).fuse(c_quarter)
        bumpers.append(bumper_unit)

        bz = BUMP_Z + BUMP_H / 2.0
        bolt_y = Part.makeCylinder(4.5, 12.0,
                                   FreeCAD.Vector(cx + sx * 35.0, cy - sy * 4.0, bz),
                                   FreeCAD.Vector(0, sy, 0))
        bolt_x = Part.makeCylinder(4.5, 12.0,
                                   FreeCAD.Vector(cx - sx * 4.0, cy + sy * 35.0, bz),
                                   FreeCAD.Vector(sx, 0, 0))
        bumper_bolts.append(bolt_y.fuse(bolt_x))

    all_bumpers = bumpers[0]
    for b in bumpers[1:]:
        all_bumpers = all_bumpers.fuse(b)

    all_bumper_bolts = bumper_bolts[0]
    for bb in bumper_bolts[1:]:
        all_bumper_bolts = all_bumper_bolts.fuse(bb)

    # --------------------------------------------------------------------------
    # 4. RUNNING GEAR: 5" WHEELS & HEAVY-DUTY CASTER ASSEMBLIES
    # --------------------------------------------------------------------------
    def make_wheel_assembly(center_pos, axis_dir):
        cx, cy, cz = center_pos.x, center_pos.y, center_pos.z
        norm_dir = axis_dir.normalize()

        tire_cyl = Part.makeCylinder(WHEEL_R, WHEEL_W,
                                     FreeCAD.Vector(cx - norm_dir.x * WHEEL_W/2.0,
                                                    cy - norm_dir.y * WHEEL_W/2.0,
                                                    cz - norm_dir.z * WHEEL_W/2.0),
                                     norm_dir)
        tire_inner = Part.makeCylinder(HUB_DIA/2.0, WHEEL_W + 2.0,
                                       FreeCAD.Vector(cx - norm_dir.x * (WHEEL_W/2.0 + 1.0),
                                                      cy - norm_dir.y * (WHEEL_W/2.0 + 1.0),
                                                      cz - norm_dir.z * (WHEEL_W/2.0 + 1.0)),
                                       norm_dir)
        tire_solid = tire_cyl.cut(tire_inner)

        hub_solid = Part.makeCylinder(HUB_DIA/2.0, HUB_W,
                                      FreeCAD.Vector(cx - norm_dir.x * HUB_W/2.0,
                                                     cy - norm_dir.y * HUB_W/2.0,
                                                     cz - norm_dir.z * HUB_W/2.0),
                                      norm_dir)
        axle_bore = Part.makeCylinder(6.35, HUB_W + 10.0,
                                      FreeCAD.Vector(cx - norm_dir.x * (HUB_W/2.0 + 5.0),
                                                     cy - norm_dir.y * (HUB_W/2.0 + 5.0),
                                                     cz - norm_dir.z * (HUB_W/2.0 + 5.0)),
                                      norm_dir)
        hub_solid = hub_solid.cut(axle_bore)

        bolt_len = HUB_W + 35.0
        axle_rod = Part.makeCylinder(6.0, bolt_len,
                                     FreeCAD.Vector(cx - norm_dir.x * bolt_len/2.0,
                                                    cy - norm_dir.y * bolt_len/2.0,
                                                    cz - norm_dir.z * bolt_len/2.0),
                                     norm_dir)
        hex_head = Part.makeCylinder(10.0, 8.0,
                                     FreeCAD.Vector(cx - norm_dir.x * (bolt_len/2.0),
                                                    cy - norm_dir.y * (bolt_len/2.0),
                                                    cz - norm_dir.z * (bolt_len/2.0)),
                                     norm_dir)
        hex_nut = Part.makeCylinder(10.0, 8.0,
                                    FreeCAD.Vector(cx + norm_dir.x * (bolt_len/2.0 - 8.0),
                                                   cy + norm_dir.y * (bolt_len/2.0 - 8.0),
                                                   cz + norm_dir.z * (bolt_len/2.0 - 8.0)),
                                    norm_dir)
        axle_solid = axle_rod.fuse(hex_head).fuse(hex_nut)

        return tire_solid, hub_solid, axle_solid

    all_tires = []
    all_hubs = []
    all_axles = []
    all_brackets = []
    all_brakes = []

    PLATE_W = 85.0
    PLATE_L = 100.0
    PLATE_T = 4.0
    FORK_T = 3.5

    # A. Front Rigid Casters
    for x_c in [-TRACK_X, TRACK_X]:
        w_center = FreeCAD.Vector(x_c, -WHEELBASE_Y, AXLE_Z)
        tire, hub, axle = make_wheel_assembly(w_center, FreeCAD.Vector(1, 0, 0))
        all_tires.append(tire)
        all_hubs.append(hub)
        all_axles.append(axle)

        top_plate = Part.makeBox(PLATE_W, PLATE_L, PLATE_T,
                                 FreeCAD.Vector(x_c - PLATE_W/2.0, -WHEELBASE_Y - PLATE_L/2.0, CASTER_TOP_Z - PLATE_T))
        
        for bx in [-28.0, 28.0]:
            for by in [-35.0, 35.0]:
                b_head = Part.makeCylinder(4.5, 5.0,
                                           FreeCAD.Vector(x_c + bx, -WHEELBASE_Y + by, CASTER_TOP_Z - PLATE_T - 5.0),
                                           FreeCAD.Vector(0, 0, 1))
                top_plate = top_plate.fuse(b_head)

        leg_spacing = HUB_W + 10.0
        leg_l = Part.makeBox(FORK_T, 45.0, CASTER_TOP_Z - PLATE_T - AXLE_Z + 15.0,
                             FreeCAD.Vector(x_c - leg_spacing/2.0 - FORK_T, -WHEELBASE_Y - 22.5, AXLE_Z - 15.0))
        leg_r = Part.makeBox(FORK_T, 45.0, CASTER_TOP_Z - PLATE_T - AXLE_Z + 15.0,
                             FreeCAD.Vector(x_c + leg_spacing/2.0, -WHEELBASE_Y - 22.5, AXLE_Z - 15.0))
        rigid_bracket = top_plate.fuse(leg_l).fuse(leg_r)
        all_brackets.append(rigid_bracket)

    # B. Rear Swivel Casters with Brake Lever
    SWIVEL_TRAIL = 25.0
    for x_c in [-TRACK_X, TRACK_X]:
        swivel_center_y = WHEELBASE_Y
        wheel_center_y = swivel_center_y + SWIVEL_TRAIL
        w_center = FreeCAD.Vector(x_c, wheel_center_y, AXLE_Z)
        tire, hub, axle = make_wheel_assembly(w_center, FreeCAD.Vector(1, 0, 0))
        all_tires.append(tire)
        all_hubs.append(hub)
        all_axles.append(axle)

        top_plate = Part.makeBox(PLATE_W, PLATE_L, PLATE_T,
                                 FreeCAD.Vector(x_c - PLATE_W/2.0, swivel_center_y - PLATE_L/2.0, CASTER_TOP_Z - PLATE_T))
        swivel_race = Part.makeCylinder(36.0, 8.0,
                                        FreeCAD.Vector(x_c, swivel_center_y, CASTER_TOP_Z - PLATE_T - 8.0),
                                        FreeCAD.Vector(0, 0, 1))
        leg_spacing = HUB_W + 10.0
        fork_crown = Part.makeBox(leg_spacing + 2*FORK_T, 50.0, 6.0,
                                  FreeCAD.Vector(x_c - leg_spacing/2.0 - FORK_T, swivel_center_y - 25.0, CASTER_TOP_Z - PLATE_T - 14.0))

        dy = SWIVEL_TRAIL
        dz = (CASTER_TOP_Z - PLATE_T - 14.0) - AXLE_Z
        arm_h = math.hypot(dy, dz) + 20.0
        angle = math.degrees(math.atan2(dy, dz))

        arm_l = Part.makeBox(FORK_T, 40.0, arm_h,
                             FreeCAD.Vector(x_c - leg_spacing/2.0 - FORK_T, swivel_center_y - 20.0, AXLE_Z - 10.0))
        arm_l.rotate(FreeCAD.Vector(x_c, swivel_center_y, CASTER_TOP_Z - PLATE_T - 14.0), FreeCAD.Vector(1, 0, 0), -angle)

        arm_r = Part.makeBox(FORK_T, 40.0, arm_h,
                             FreeCAD.Vector(x_c + leg_spacing/2.0, swivel_center_y - 20.0, AXLE_Z - 10.0))
        arm_r.rotate(FreeCAD.Vector(x_c, swivel_center_y, CASTER_TOP_Z - PLATE_T - 14.0), FreeCAD.Vector(1, 0, 0), -angle)

        swivel_bracket = top_plate.fuse(swivel_race).fuse(fork_crown).fuse(arm_l).fuse(arm_r)
        all_brackets.append(swivel_bracket)

        brake_tab = Part.makeBox(leg_spacing + 8.0, 35.0, 3.0,
                                 FreeCAD.Vector(x_c - (leg_spacing + 8.0)/2.0, wheel_center_y + 20.0, AXLE_Z + 25.0))
        brake_tab.rotate(FreeCAD.Vector(x_c, wheel_center_y + 20.0, AXLE_Z + 25.0), FreeCAD.Vector(1, 0, 0), 30.0)
        paddle = Part.makeBox(30.0, 20.0, 4.0,
                              FreeCAD.Vector(x_c - 15.0, wheel_center_y + 42.0, AXLE_Z + 40.0))
        brake_assembly = brake_tab.fuse(paddle)
        all_brakes.append(brake_assembly)

    compound_tires = all_tires[0]
    for t in all_tires[1:]:
        compound_tires = compound_tires.fuse(t)

    compound_hubs = all_hubs[0]
    for h in all_hubs[1:]:
        compound_hubs = compound_hubs.fuse(h)

    compound_axles = all_axles[0]
    for a in all_axles[1:]:
        compound_axles = compound_axles.fuse(a)

    compound_brackets = all_brackets[0]
    for b in all_brackets[1:]:
        compound_brackets = compound_brackets.fuse(b)

    compound_brakes = all_brakes[0].fuse(all_brakes[1])

    # --------------------------------------------------------------------------
    # 5. PUSH HANDLE SUBASSEMBLY (29.0" ABOVE DECK, 2 CROSS RAILS, FOLDING BASE)
    # --------------------------------------------------------------------------
    Z_HANDLE_APEX = DECK_TOP_Z + HANDLE_H
    R_HANDLE_CORNER = 65.0

    Z_upright_top = Z_HANDLE_APEX - R_HANDLE_CORNER
    Z_hinge_bot = DECK_TOP_Z + 15.0

    tube_l = Part.makeCylinder(R_tube, Z_upright_top - Z_hinge_bot,
                               FreeCAD.Vector(-HANDLE_W/2.0, HANDLE_Y, Z_hinge_bot),
                               FreeCAD.Vector(0, 0, 1))
    tube_r = Part.makeCylinder(R_tube, Z_upright_top - Z_hinge_bot,
                               FreeCAD.Vector(HANDLE_W/2.0, HANDLE_Y, Z_hinge_bot),
                               FreeCAD.Vector(0, 0, 1))

    grip_w = HANDLE_W - 2 * R_HANDLE_CORNER
    top_grip = Part.makeCylinder(R_tube, grip_w,
                                 FreeCAD.Vector(-grip_w/2.0, HANDLE_Y, Z_HANDLE_APEX),
                                 FreeCAD.Vector(1, 0, 0))

    torus_l = Part.makeTorus(R_HANDLE_CORNER, R_tube,
                             FreeCAD.Vector(-HANDLE_W/2.0 + R_HANDLE_CORNER, HANDLE_Y, Z_upright_top),
                             FreeCAD.Vector(0, 1, 0))
    cut_l = Part.makeBox(2*R_HANDLE_CORNER + 20.0, 2*HANDLE_TUBE_OD + 10.0, 2*R_HANDLE_CORNER + 20.0,
                         FreeCAD.Vector(-HANDLE_W/2.0 + R_HANDLE_CORNER - 5.0,
                                        HANDLE_Y - HANDLE_TUBE_OD - 5.0,
                                        Z_upright_top - 2*R_HANDLE_CORNER - 10.0))
    cut_l2 = Part.makeBox(2*R_HANDLE_CORNER + 20.0, 2*HANDLE_TUBE_OD + 10.0, 2*R_HANDLE_CORNER + 20.0,
                          FreeCAD.Vector(-HANDLE_W/2.0 + R_HANDLE_CORNER - 5.0,
                                         HANDLE_Y - HANDLE_TUBE_OD - 5.0,
                                         Z_upright_top - 5.0))
    corner_l = torus_l.cut(cut_l).cut(cut_l2)

    torus_r = Part.makeTorus(R_HANDLE_CORNER, R_tube,
                             FreeCAD.Vector(HANDLE_W/2.0 - R_HANDLE_CORNER, HANDLE_Y, Z_upright_top),
                             FreeCAD.Vector(0, 1, 0))
    cut_r = Part.makeBox(2*R_HANDLE_CORNER + 20.0, 2*HANDLE_TUBE_OD + 10.0, 2*R_HANDLE_CORNER + 20.0,
                         FreeCAD.Vector(HANDLE_W/2.0 - 3*R_HANDLE_CORNER - 15.0,
                                        HANDLE_Y - HANDLE_TUBE_OD - 5.0,
                                        Z_upright_top - 2*R_HANDLE_CORNER - 10.0))
    cut_r2 = Part.makeBox(2*R_HANDLE_CORNER + 20.0, 2*HANDLE_TUBE_OD + 10.0, 2*R_HANDLE_CORNER + 20.0,
                          FreeCAD.Vector(HANDLE_W/2.0 - 3*R_HANDLE_CORNER - 15.0,
                                         HANDLE_Y - HANDLE_TUBE_OD - 5.0,
                                         Z_upright_top - 5.0))
    corner_r = torus_r.cut(cut_r).cut(cut_r2)

    R_cross = 12.7
    cross_rail_span = HANDLE_W - HANDLE_TUBE_OD
    z_rail_1 = DECK_TOP_Z + 240.0
    cross_1 = Part.makeCylinder(R_cross, cross_rail_span,
                                FreeCAD.Vector(-cross_rail_span/2.0, HANDLE_Y, z_rail_1),
                                FreeCAD.Vector(1, 0, 0))
    z_rail_2 = DECK_TOP_Z + 480.0
    cross_2 = Part.makeCylinder(R_cross, cross_rail_span,
                                FreeCAD.Vector(-cross_rail_span/2.0, HANDLE_Y, z_rail_2),
                                FreeCAD.Vector(1, 0, 0))

    handle_tubing = tube_l.fuse(tube_r).fuse(top_grip).fuse(corner_l).fuse(corner_r).fuse(cross_1).fuse(cross_2)

    hinge_parts = []
    for x_h in [-HANDLE_W/2.0, HANDLE_W/2.0]:
        h_side1 = Part.makeBox(4.0, 60.0, 50.0,
                               FreeCAD.Vector(x_h - 18.0, HANDLE_Y - 30.0, DECK_TOP_Z))
        h_side2 = Part.makeBox(4.0, 60.0, 50.0,
                               FreeCAD.Vector(x_h + 14.0, HANDLE_Y - 30.0, DECK_TOP_Z))
        p_pin = Part.makeCylinder(6.0, 42.0,
                                  FreeCAD.Vector(x_h - 21.0, HANDLE_Y, DECK_TOP_Z + 25.0),
                                  FreeCAD.Vector(1, 0, 0))
        hinge_parts.append(h_side1.fuse(h_side2).fuse(p_pin))

    foot_bar_span = HANDLE_W - 36.0
    foot_bar = Part.makeCylinder(8.0, foot_bar_span,
                                 FreeCAD.Vector(-foot_bar_span/2.0, HANDLE_Y - 18.0, DECK_TOP_Z + 35.0),
                                 FreeCAD.Vector(1, 0, 0))
    foot_pedal = Part.makeBox(60.0, 25.0, 6.0,
                              FreeCAD.Vector(-30.0, HANDLE_Y - 35.0, DECK_TOP_Z + 32.0))
    hinges_solid = hinge_parts[0].fuse(hinge_parts[1]).fuse(foot_bar).fuse(foot_pedal)

    # ==========================================================================
    # APPLY TRANSFORMATION PLACEMENT (IF PROVIDED)
    # ==========================================================================
    if placement is not None:
        deck_shell.Placement = placement.multiply(deck_shell.Placement)
        all_ribs.Placement = placement.multiply(all_ribs.Placement)
        under_frame.Placement = placement.multiply(under_frame.Placement)
        all_bumpers.Placement = placement.multiply(all_bumpers.Placement)
        all_bumper_bolts.Placement = placement.multiply(all_bumper_bolts.Placement)
        compound_tires.Placement = placement.multiply(compound_tires.Placement)
        compound_hubs.Placement = placement.multiply(compound_hubs.Placement)
        compound_axles.Placement = placement.multiply(compound_axles.Placement)
        compound_brackets.Placement = placement.multiply(compound_brackets.Placement)
        compound_brakes.Placement = placement.multiply(compound_brakes.Placement)
        handle_tubing.Placement = placement.multiply(handle_tubing.Placement)
        hinges_solid.Placement = placement.multiply(hinges_solid.Placement)

    # ==========================================================================
    # CREATE FREECAD DOCUMENT OBJECTS & MATERIALS
    # ==========================================================================
    # 1. Deck
    obj_deck = doc.addObject("Part::Feature", "Platform_Deck_Plate")
    obj_deck.Label = "24x36in Aluminum Diamond-Plate Deck & Skirt"
    obj_deck.Shape = deck_shell
    grp_deck.addObject(obj_deck)
    apply_material(obj_deck, "Aluminum-6061-T6")

    obj_ribs = doc.addObject("Part::Feature", "Deck_Traction_Ribs")
    obj_ribs.Label = "Deck Diamond Non-Skid Traction Grid"
    obj_ribs.Shape = all_ribs
    grp_deck.addObject(obj_ribs)
    apply_material(obj_ribs, "Aluminum-6061-T6")

    obj_frame = doc.addObject("Part::Feature", "Under_Deck_Frame_Channels")
    obj_frame.Label = "Under-Deck Structural Steel C-Channels & Stringers"
    obj_frame.Shape = under_frame
    grp_deck.addObject(obj_frame)
    apply_material(obj_frame, "Steel-A36")

    obj_bumpers = doc.addObject("Part::Feature", "Corner_Rubber_Bumpers")
    obj_bumpers.Label = "Molded Impact Rubber Corner Bumpers (4 Corners)"
    obj_bumpers.Shape = all_bumpers
    grp_deck.addObject(obj_bumpers)
    apply_material(obj_bumpers, "Rubber-Solid")

    obj_b_bolts = doc.addObject("Part::Feature", "Corner_Bumper_Fasteners")
    obj_b_bolts.Label = "Corner Bumper Recessed Fastener Hardware"
    obj_b_bolts.Shape = all_bumper_bolts
    grp_deck.addObject(obj_b_bolts)
    apply_material(obj_b_bolts, "Steel-ZincPlated")

    # 2. Running Gear
    obj_tires = doc.addObject("Part::Feature", "Caster_Rubber_Tires")
    obj_tires.Label = "5.0in Heavy-Duty Solid Rubber Tread Tires"
    obj_tires.Shape = compound_tires
    grp_gear.addObject(obj_tires)
    apply_material(obj_tires, "Rubber-Solid")

    obj_hubs = doc.addObject("Part::Feature", "Caster_Wheel_Hubs")
    obj_hubs.Label = "Industrial Yellow Caster Hub Cores & Bearings"
    obj_hubs.Shape = compound_hubs
    grp_gear.addObject(obj_hubs)
    apply_material(obj_hubs, "Polyurethane")

    obj_axles = doc.addObject("Part::Feature", "Caster_Axle_Hardware")
    obj_axles.Label = "Zinc-Plated 1/2in Caster Axle Bolts & Nuts"
    obj_axles.Shape = compound_axles
    grp_gear.addObject(obj_axles)
    apply_material(obj_axles, "Steel-ZincPlated")

    obj_brackets = doc.addObject("Part::Feature", "Caster_Mounting_Brackets")
    obj_brackets.Label = "Stamped Steel Casters (2 Front Rigid, 2 Rear Swivel)"
    obj_brackets.Shape = compound_brackets
    grp_gear.addObject(obj_brackets)
    apply_material(obj_brackets, "Steel-ZincPlated")

    obj_brakes = doc.addObject("Part::Feature", "Rear_Caster_Foot_Brakes")
    obj_brakes.Label = "Rear Swivel Caster Foot Lock Brake Levers"
    obj_brakes.Shape = compound_brakes
    grp_gear.addObject(obj_brakes)
    apply_material(obj_brakes, "Steel-ZincPlated")

    # 3. Handle
    obj_handle = doc.addObject("Part::Feature", "Tubular_Push_Handle")
    obj_handle.Label = "29in Tubular Steel Push Handle (Dual Cross Rails)"
    obj_handle.Shape = handle_tubing
    grp_handle.addObject(obj_handle)
    apply_material(obj_handle, "Steel-304Stainless")

    obj_hinges = doc.addObject("Part::Feature", "Handle_Folding_Hinges")
    obj_hinges.Label = "Folding Base Hinge Brackets & Foot Release Bar"
    obj_hinges.Shape = hinges_solid
    grp_handle.addObject(obj_hinges)
    apply_material(obj_hinges, "Steel-ZincPlated")

    return grp_root
