"""
Commercial 24" x 36" Platform Cart Component (Dolly Chassis)
FreeCAD 1.1 Assembly Workbench Parametric CAD Module

Modeled after standard commercial heavy-duty steel/aluminum platform trucks:
- Deck: 24.0" (609.6 mm) wide x 36.0" (914.4 mm) long with diamond non-skid plate relief
- Perimeter skirt downturn (1.75" / 45 mm) with 1.5" radiused corners
- 4 heavy-duty molded rubber corner bumpers with recessed socket fasteners
- Under-deck longitudinal channels and cross stringers (1000+ lb capacity)
- 4-wheel running gear with standalone COTS 5.0" plate casters:
  - 2 Front rigid casters (caster_rigid_5in)
  - 2 Rear 360-deg swivel casters with integrated foot brake lock levers (caster_swivel_5in)
  - High-visibility yellow hub cores with black solid rubber tires
- Handle: 1.25" OD tubular steel push handle rising 29.0" (736.6 mm) above the deck
  - 2 horizontal reinforcement cross rails
  - Folding base hinge brackets with foot-release cross bar
"""

import os
import sys
import math
import FreeCAD
import Part
try:
    import FreeCADGui
    HAS_GUI = bool(getattr(FreeCAD, "GuiUp", False))
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.materials import (
    init_materials,
    apply_material,
)
from phi_works.maker.components import import_component
from phi_works.maker.assembly import (
    create_assembly,
    create_exploded_view,
    add_exploded_step,
)


def create_platform_cart_component(doc, placement=None):
    """
    Creates the Commercial 24" x 36" Platform Cart in `doc` using FreeCAD 1.1 Assembly.

    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)

    Returns:
      Assembly::AssemblyObject root container
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    assy = create_assembly(doc, "Platform_Cart_24x36", "Commercial 24x36 Platform Cart (5in Casters, 29in Handle)")

    grp_deck = doc.addObject("App::DocumentObjectGroup", "Cart_Deck_Subassembly")
    grp_deck.Label = "1. Deck & Frame Subassembly (24x36in Diamond Plate)"

    grp_gear = doc.addObject("App::DocumentObjectGroup", "Cart_Running_Gear")
    grp_gear.Label = "2. Running Gear (5in COTS Rigid & Swivel Casters)"

    grp_handle = doc.addObject("App::DocumentObjectGroup", "Cart_Push_Handle")
    grp_handle.Label = "3. Push Handle Subassembly (29in Height, Folding Base)"

    assy.addObject(grp_deck)
    assy.addObject(grp_gear)
    assy.addObject(grp_handle)

    # ==========================================================================
    # PARAMETRIC DIMENSIONS
    # ==========================================================================
    DECK_W = 609.6              # 24.0 in width along X
    DECK_L = 914.4              # 36.0 in length along Y
    DECK_SKIRT_H = 45.0         # 1.77 in perimeter skirt height
    CASTER_H = 150.0            # 5.0" commercial caster overall height to mounting plate
    DECK_BOT_Z = CASTER_H       # Underside of deck rests directly on caster top plate (150 mm)
    DECK_TOP_Z = DECK_BOT_Z + DECK_SKIRT_H  # Top surface of deck: 195.0 mm (~7.7 in)
    CORNER_R = 38.1             # 1.5 in corner fillet radius
    SHEET_T = 3.175             # 1/8 in aluminum sheet deck

    TRACK_X = 220.0             # Caster lateral centerlines (X = ±220 mm)
    WHEELBASE_Y = 320.0         # Front casters Y = -320 mm, Rear casters Y = +320 mm

    HANDLE_H = 736.6            # Exactly 29.0 in handle height above deck
    HANDLE_TUBE_OD = 31.75      # 1.25 in OD tubular steel
    R_tube = HANDLE_TUBE_OD / 2.0
    HANDLE_W = 480.0            # Center-to-center upright width
    HANDLE_Y = DECK_L / 2.0 - 45.0  # Inset from rear edge (Y = +412.2 mm)

    # --------------------------------------------------------------------------
    # 1. DECK PLATE & PERIMETER SKIRT WITH ROUNDED CORNERS
    # --------------------------------------------------------------------------
    dx = DECK_W / 2.0 - CORNER_R
    dy = DECK_L / 2.0 - CORNER_R

    box_x = Part.makeBox(DECK_W - 2*CORNER_R, DECK_L, DECK_SKIRT_H,
                         FreeCAD.Vector(-dx, -DECK_L/2.0, DECK_BOT_Z))
    box_y = Part.makeBox(DECK_W, DECK_L - 2*CORNER_R, DECK_SKIRT_H,
                         FreeCAD.Vector(-DECK_W/2.0, -dy, DECK_BOT_Z))
    deck_solid = box_x.fuse(box_y)

    c_fl = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(-dx, -dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_fr = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(dx, -dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_rl = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(-dx, dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    c_rr = Part.makeCylinder(CORNER_R, DECK_SKIRT_H, FreeCAD.Vector(dx, dy, DECK_BOT_Z), FreeCAD.Vector(0, 0, 1))
    deck_solid = deck_solid.fuse(c_fl).fuse(c_fr).fuse(c_rl).fuse(c_rr)

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

    # Diamond plate raised traction ribs on top surface
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
    # 4. PUSH HANDLE SUBASSEMBLY (29.0" ABOVE DECK, 2 CROSS RAILS, FOLDING BASE)
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

    # 2. Handle
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

    # 3. Import Standalone COTS Running Gear Components
    p_fl = FreeCAD.Placement(FreeCAD.Vector(-TRACK_X, -WHEELBASE_Y, 0), FreeCAD.Rotation())
    p_fr = FreeCAD.Placement(FreeCAD.Vector(TRACK_X, -WHEELBASE_Y, 0), FreeCAD.Rotation())
    p_rl = FreeCAD.Placement(FreeCAD.Vector(-TRACK_X, WHEELBASE_Y, 0), FreeCAD.Rotation())
    p_rr = FreeCAD.Placement(FreeCAD.Vector(TRACK_X, WHEELBASE_Y, 0), FreeCAD.Rotation())

    if placement is not None:
        p_fl = placement.multiply(p_fl)
        p_fr = placement.multiply(p_fr)
        p_rl = placement.multiply(p_rl)
        p_rr = placement.multiply(p_rr)

    caster_fl = import_component(doc, "caster_rigid_5in", placement=p_fl, label="Front Left Rigid Caster (5in)", as_link=True)
    caster_fr = import_component(doc, "caster_rigid_5in", placement=p_fr, label="Front Right Rigid Caster (5in)", as_link=True)
    caster_rl = import_component(doc, "caster_swivel_5in", placement=p_rl, label="Rear Left Swivel Caster (5in Brake)", as_link=True)
    caster_rr = import_component(doc, "caster_swivel_5in", placement=p_rr, label="Rear Right Swivel Caster (5in Brake)", as_link=True)

    grp_gear.addObject(caster_fl)
    grp_gear.addObject(caster_fr)
    grp_gear.addObject(caster_rl)
    grp_gear.addObject(caster_rr)

    # 4. Programmatic Exploded View
    exp_view = create_exploded_view(doc, assy, "ExplodedView_RunningGear", "Running Gear & Handle Exploded View")
    add_exploded_step(doc, exp_view, caster_fl, FreeCAD.Vector(-30, -60, -70), label="Explode FL Caster")
    add_exploded_step(doc, exp_view, caster_fr, FreeCAD.Vector(30, -60, -70), label="Explode FR Caster")
    add_exploded_step(doc, exp_view, caster_rl, FreeCAD.Vector(-30, 60, -70), label="Explode RL Caster")
    add_exploded_step(doc, exp_view, caster_rr, FreeCAD.Vector(30, 60, -70), label="Explode RR Caster")
    add_exploded_step(doc, exp_view, obj_handle, FreeCAD.Vector(0, 0, 100), label="Explode Push Handle")

    doc.recompute()
    return assy
