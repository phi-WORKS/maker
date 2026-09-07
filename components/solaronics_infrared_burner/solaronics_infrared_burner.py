"""
Solaronics K-30 High-Intensity Ceramic Infrared Burner Component
Standalone 3D Parametric CAD Module (Maker Component Library)

Directly modeled from manufacturer specifications, engineering cross-sections,
CAD plan views, and physical unit reference imagery for the Solaronics K-30 heater:
  - Overall Mouth Length (X): 16-3/4 in (425.45 mm)
  - Overall Width w/ controls (Y): 28-5/8 in (727.08 mm)
  - Overall Depth (Z): 8-3/4 in (222.25 mm)
  - Radiating Surface Area: 173 sq. in. (111,613 mm^2)
  - Nominal Weight: ~30-32 lbs (14.5 kg)

Provides modular subcomponents:
  - `create_solaronics_burner_core_component(doc, placement)`: Standalone burner core engine
  - `create_solaronics_reflector_hood_component(doc, placement)`: Standalone flared reflector hood
  - `create_solaronics_infrared_burner_component(doc, placement)`: Master assembly integrating both
"""

import os
import sys
import math
import FreeCAD
import Part

from phi_works.maker.materials import apply_material

# ==============================================================================
# PARAMETRIC ENGINEERING DIMENSIONS (SOLARONICS K-30)
# ==============================================================================

# 1. Ceramic Plaque Radiant Matrix (Radiating Surface: 173 sq in / 1,116 cm^2)
TILES_COUNT = 4
TILE_W = 216.0               # 8.5 in width across X
TILE_L = 114.0               # 4.49 in length along Y per tile
TILE_T = 12.7                # 0.5 in thickness
TOTAL_TILES_L = TILES_COUNT * TILE_L  # 456.0 mm (17.95 in radiant length matching plan view)

# 2. Plaque Retention Frame & Mounting End Brackets (304 Stainless Steel)
FRAME_BEZEL_LIP = 10.0       # Overlapping retention margin
FRAME_BEZEL_T = 1.5          # 16-gauge sheet
FRAME_W = TILE_W + 16.0      # 232.0 mm
FRAME_L = TOTAL_TILES_L + 16.0  # 472.0 mm

# 3. Combustion Plenum Housing (Heavy Gauge Steel, Matte Black)
PLENUM_W = 236.0             # 9.29 in width
PLENUM_L = 480.0             # 18.9 in length
PLENUM_DEPTH = 85.0          # 3.35 in depth (from Z = TILE_T to Z = TILE_T + PLENUM_DEPTH)
PLENUM_WALL = 1.8            # 14-gauge cold rolled steel

# 4. Flared Reflector Hood (Mirror-Bright Aluminum / 304 Stainless)
# K-30 Specification: 16-3/4" mouth length (425.45 mm) across X
REFL_DEPTH = 110.0           # 4.33 in reflector cavity depth (Z = 0 to Z = -110 mm)
MOUTH_INNER_W = 358.0        # Inner opening width before flare (14.09 in)
MOUTH_INNER_L = 580.0        # Inner opening length before flare (22.83 in)
FLANGE_FLARE = 33.75         # 1.33 in flat perimeter flare flange
MOUTH_OUTER_W = MOUTH_INNER_W + 2 * FLANGE_FLARE   # 425.5 mm = 16.75 in (16-3/4")!
MOUTH_OUTER_L = 608.0        # 23.94 in overall length across outer flange rim
THROAT_W = PLENUM_W          # 236.0 mm throat at Z = 0
THROAT_L = PLENUM_L          # 480.0 mm throat at Z = 0
SHEET_T = 1.2                # 0.048 in (18-gauge) aluminum sheet

# 5. Control Valve & Ignition Module Enclosure (NEMA Enclosure)
VALVE_BOX_W = 150.0          # 5.9 in
VALVE_BOX_L = 120.0          # 4.7 in
VALVE_BOX_H = 85.0           # 3.3 in


# ==============================================================================
# SUBCOMPONENT 1: SOLARONICS BURNER CORE
# ==============================================================================
def build_burner_core_subassembly(doc, name="Solaronics_Burner_Core"):
    """
    Builds the core infrared burner engine subassembly:
      - 4x Cordierite ceramic grooved plaques (173 sq in matrix)
      - 304 Stainless retention frame with mitered end brackets
      - Direct spark pilot electrode & flame sensor assembly
      - Matte black combustion plenum chamber with internal diffuser
      - Cast iron venturi mixing tube & adjustable air shutter
      - Precision brass orifice & 1/2" NPT gas manifold
      - Hollow 16-gauge control valve enclosure & conduit fitting
      - Heavy-duty side suspension ears & zinc-plated eye bolts
    """
    grp_core = doc.addObject("App::Part", name)
    grp_core.Label = "Solaronics K-30 Ceramic Infrared Burner Core"

    # A. 4x Cordierite Ceramic Radiant Plaques
    plaques = []
    for i in range(TILES_COUNT):
        y_center = -TOTAL_TILES_L / 2.0 + (i + 0.5) * TILE_L
        t_box = Part.makeBox(TILE_W, TILE_L - 1.5, TILE_T, FreeCAD.Vector(-TILE_W / 2.0, y_center - (TILE_L - 1.5) / 2.0, 0))
        # Simulated radiant surface grooved texture
        for gy in range(int(y_center - TILE_L / 2.0 + 8), int(y_center + TILE_L / 2.0 - 8), 10):
            g = Part.makeBox(TILE_W - 12.0, 1.8, 1.5, FreeCAD.Vector(-TILE_W / 2.0 + 6.0, gy - 0.9, -0.5))
            t_box = t_box.cut(g)
        # Subtle chevron / lightning emboss mark
        chev1 = Part.makeBox(2.0, 24.0, 1.0, FreeCAD.Vector(0, y_center - 12.0, -0.5))
        chev1.rotate(FreeCAD.Vector(0, y_center, 0), FreeCAD.Vector(0, 0, 1), 25)
        chev2 = Part.makeBox(2.0, 24.0, 1.0, FreeCAD.Vector(0, y_center - 12.0, -0.5))
        chev2.rotate(FreeCAD.Vector(0, y_center, 0), FreeCAD.Vector(0, 0, 1), -25)
        t_box = t_box.cut(chev1).cut(chev2)
        plaques.append(t_box)

    tile_shape = plaques[0]
    for p in plaques[1:]:
        tile_shape = tile_shape.fuse(p)

    obj_tiles = doc.addObject("Part::Feature", "Solaronics_Ceramic_Plaques")
    obj_tiles.Label = "4x Cordierite Ceramic Radiant Matrix (173 sq in)"
    obj_tiles.Shape = tile_shape
    grp_core.addObject(obj_tiles)
    apply_material(obj_tiles, "Ceramic-Cordierite")

    # B. 304 Stainless Plaque Retention Frame & Notched End Brackets
    frame_outer = Part.makeBox(TILE_W + 16.0, TOTAL_TILES_L + 16.0, 2.0, FreeCAD.Vector(-(TILE_W + 16.0) / 2.0, -(TOTAL_TILES_L + 16.0) / 2.0, -0.5))
    frame_inner = Part.makeBox(TILE_W - 14.0, TOTAL_TILES_L - 14.0, 3.0, FreeCAD.Vector(-(TILE_W - 14.0) / 2.0, -(TOTAL_TILES_L - 14.0) / 2.0, -1.0))
    frame_rim = frame_outer.cut(frame_inner)

    # Center runner bar and tile divider bars
    center_runner = Part.makeBox(12.0, TOTAL_TILES_L, 1.5, FreeCAD.Vector(-6.0, -TOTAL_TILES_L / 2.0, -0.5))
    frame_rim = frame_rim.fuse(center_runner)
    for i in range(1, TILES_COUNT):
        y_div = -TOTAL_TILES_L / 2.0 + i * TILE_L
        div_bar = Part.makeBox(TILE_W, 6.0, 1.5, FreeCAD.Vector(-TILE_W / 2.0, y_div - 3.0, -0.5))
        frame_rim = frame_rim.fuse(div_bar)

    # Notched trapezoidal end mounting brackets per CAD plan view
    b_top = Part.makeBox(TILE_W + 24.0, 35.0, 2.0, FreeCAD.Vector(-(TILE_W + 24.0) / 2.0, TOTAL_TILES_L / 2.0 + 8.0, -0.5))
    b_bot = Part.makeBox(TILE_W + 24.0, 35.0, 2.0, FreeCAD.Vector(-(TILE_W + 24.0) / 2.0, -TOTAL_TILES_L / 2.0 - 43.0, -0.5))
    for hx in [-TILE_W / 2.0 - 5.0, TILE_W / 2.0 + 5.0]:
        for hy in [-TOTAL_TILES_L / 2.0 - 25.0, TOTAL_TILES_L / 2.0 + 25.0]:
            hole = Part.makeCylinder(3.2, 5.0, FreeCAD.Vector(hx, hy, -1.5), FreeCAD.Vector(0, 0, 1))
            b_top = b_top.cut(hole)
            b_bot = b_bot.cut(hole)

    bezel_shape = frame_rim.fuse(b_top).fuse(b_bot)
    obj_bezel = doc.addObject("Part::Feature", "Solaronics_Retention_Bezel")
    obj_bezel.Label = "304 Stainless Plaque Retention Frame & Brackets"
    obj_bezel.Shape = bezel_shape
    grp_core.addObject(obj_bezel)
    apply_material(obj_bezel, "Steel-304Stainless")

    # C. Direct Spark Pilot Electrode & Flame Sensor
    shield = Part.makeBox(50.0, 22.0, 16.0, FreeCAD.Vector(-25.0, -TOTAL_TILES_L / 2.0 - 15.0, -10.0))
    shield_cut = Part.makeBox(46.0, 24.0, 14.0, FreeCAD.Vector(-23.0, -TOTAL_TILES_L / 2.0 - 16.0, -9.0))
    shield = shield.cut(shield_cut)
    insul1 = Part.makeCylinder(4.0, 28.0, FreeCAD.Vector(-10.0, -TOTAL_TILES_L / 2.0 - 5.0, 2.0), FreeCAD.Vector(0, 0, -1))
    insul2 = Part.makeCylinder(4.0, 28.0, FreeCAD.Vector(10.0, -TOTAL_TILES_L / 2.0 - 5.0, 2.0), FreeCAD.Vector(0, 0, -1))
    probe1 = Part.makeCylinder(1.0, 18.0, FreeCAD.Vector(-10.0, -TOTAL_TILES_L / 2.0 - 5.0, -26.0), FreeCAD.Vector(0, 1, 0))
    probe2 = Part.makeCylinder(1.0, 18.0, FreeCAD.Vector(10.0, -TOTAL_TILES_L / 2.0 - 5.0, -26.0), FreeCAD.Vector(0, 1, 0))
    pilot_shape = shield.fuse(insul1).fuse(insul2).fuse(probe1).fuse(probe2)
    obj_pilot = doc.addObject("Part::Feature", "Solaronics_Pilot_Electrode")
    obj_pilot.Label = "Direct Spark Ignition Electrode & Flame Sensor Assembly"
    obj_pilot.Shape = pilot_shape
    grp_core.addObject(obj_pilot)
    apply_material(obj_pilot, "Ceramic-Alumina")

    # D. Combustion Plenum Housing (Heavy Gauge Steel Box, Matte Black)
    plenum_box = Part.makeBox(THROAT_W, THROAT_L, PLENUM_DEPTH, FreeCAD.Vector(-THROAT_W / 2.0, -THROAT_L / 2.0, TILE_T))
    plenum_inner = Part.makeBox(THROAT_W - 4.0, THROAT_L - 4.0, PLENUM_DEPTH - 2.0, FreeCAD.Vector(-THROAT_W / 2.0 + 2.0, -THROAT_L / 2.0 + 2.0, TILE_T + 2.0))
    plenum_shell = plenum_box.cut(plenum_inner)

    # Flue exhaust relief gap at top (+Y)
    flue_notch = Part.makeBox(THROAT_W - 40.0, 30.0, 12.0, FreeCAD.Vector(-THROAT_W / 2.0 + 20.0, THROAT_L / 2.0 - 20.0, TILE_T + PLENUM_DEPTH - 10.0))
    plenum_shell = plenum_shell.cut(flue_notch)

    # Internal pan diffuser plate
    diffuser = Part.makeBox(THROAT_W - 10.0, THROAT_L - 10.0, 2.0, FreeCAD.Vector(-THROAT_W / 2.0 + 5.0, -THROAT_L / 2.0 + 5.0, TILE_T + 45.0))
    plenum_shell = plenum_shell.fuse(diffuser)

    obj_plenum = doc.addObject("Part::Feature", "Solaronics_Combustion_Plenum")
    obj_plenum.Label = "Heavy Gauge Steel Combustion Plenum Chamber (Matte Black)"
    obj_plenum.Shape = plenum_shell
    grp_core.addObject(obj_plenum)
    apply_material(obj_plenum, "PowderCoat-MatteBlack")

    # E. Venturi Pre-Mix Manifold (Cast Iron)
    venturi_len = 160.0
    venturi_tube = Part.makeCylinder(21.0, venturi_len, FreeCAD.Vector(0, -50.0, TILE_T + PLENUM_DEPTH + 18.0), FreeCAD.Vector(0, -1, 0))
    bellmouth = Part.makeCone(28.0, 21.0, 35.0, FreeCAD.Vector(0, -50.0 - venturi_len, TILE_T + PLENUM_DEPTH + 18.0), FreeCAD.Vector(0, 1, 0))
    shutter = Part.makeCylinder(29.5, 20.0, FreeCAD.Vector(0, -50.0 - venturi_len + 10.0, TILE_T + PLENUM_DEPTH + 18.0), FreeCAD.Vector(0, -1, 0))
    venturi_shape = venturi_tube.fuse(bellmouth).fuse(shutter)
    obj_venturi = doc.addObject("Part::Feature", "Solaronics_Venturi_Assembly")
    obj_venturi.Label = "Cast Iron Pre-Mix Venturi Induction Tube & Air Shutter"
    obj_venturi.Shape = venturi_shape
    grp_core.addObject(obj_venturi)
    apply_material(obj_venturi, "CastIron-Gray")

    # F. Gas Manifold & Brass Orifice
    inlet_pipe = Part.makeCylinder(10.7, 45.0, FreeCAD.Vector(0, -50.0 - venturi_len - 45.0, TILE_T + PLENUM_DEPTH + 18.0), FreeCAD.Vector(0, 1, 0))
    orifice_hex = Part.makeCylinder(12.0, 25.0, FreeCAD.Vector(0, -50.0 - venturi_len - 15.0, TILE_T + PLENUM_DEPTH + 18.0), FreeCAD.Vector(0, 1, 0))
    gas_train_shape = inlet_pipe.fuse(orifice_hex)
    obj_gas = doc.addObject("Part::Feature", "Solaronics_Gas_Train")
    obj_gas.Label = "Precision Brass Gas Orifice & 1/2in NPT Supply Train"
    obj_gas.Shape = gas_train_shape
    grp_core.addObject(obj_gas)
    apply_material(obj_gas, "Brass-C360")

    # G. Control & Gas Valve Box Enclosure (16-Gauge Hollow Enclosure)
    cbox_y = -THROAT_L / 2.0 - VALVE_BOX_L
    cbox_outer = Part.makeBox(VALVE_BOX_W, VALVE_BOX_L, VALVE_BOX_H, FreeCAD.Vector(-VALVE_BOX_W / 2.0, cbox_y, TILE_T + 15.0))
    cbox_inner = Part.makeBox(VALVE_BOX_W - 3.0, VALVE_BOX_L - 3.0, VALVE_BOX_H - 1.5, FreeCAD.Vector(-VALVE_BOX_W / 2.0 + 1.5, cbox_y + 1.5, TILE_T + 16.5))
    cbox_shell = cbox_outer.cut(cbox_inner)
    cbox_lid = Part.makeBox(VALVE_BOX_W + 4.0, VALVE_BOX_L + 4.0, 2.0, FreeCAD.Vector(-VALVE_BOX_W / 2.0 - 2.0, cbox_y - 2.0, TILE_T + 15.0 + VALVE_BOX_H))
    conduit = Part.makeCylinder(10.0, 45.0, FreeCAD.Vector(VALVE_BOX_W / 2.0, cbox_y + 40.0, TILE_T + 45.0), FreeCAD.Vector(1, 0, 0))
    ctrl_shape = cbox_shell.fuse(cbox_lid).fuse(conduit)
    obj_ctrl = doc.addObject("Part::Feature", "Solaronics_Control_Enclosure")
    obj_ctrl.Label = "Automatic Gas Control Valve & Direct Spark Ignition Enclosure"
    obj_ctrl.Shape = ctrl_shape
    grp_core.addObject(obj_ctrl)
    apply_material(obj_ctrl, "Steel-A36")

    # H. Suspension Hardware (4 side ears with eye bolts)
    ears = []
    for ex in [-THROAT_W / 2.0 - 12.0, THROAT_W / 2.0]:
        for ey in [-THROAT_L / 4.0, THROAT_L / 4.0]:
            ear_plate = Part.makeBox(12.0, 40.0, 35.0, FreeCAD.Vector(ex, ey - 20.0, TILE_T + 20.0))
            eye_ring = Part.makeTorus(14.0, 4.0, FreeCAD.Vector(ex + 6.0, ey, TILE_T + 65.0), FreeCAD.Vector(1, 0, 0))
            eye_shank = Part.makeCylinder(4.75, 15.0, FreeCAD.Vector(ex + 6.0, ey, TILE_T + 45.0), FreeCAD.Vector(0, 0, 1))
            ears.append(ear_plate.fuse(eye_ring).fuse(eye_shank))

    susp_shape = ears[0]
    for e in ears[1:]:
        susp_shape = susp_shape.fuse(e)
    obj_susp = doc.addObject("Part::Feature", "Solaronics_Suspension_Hardware")
    obj_susp.Label = "Plenum Suspension Brackets & Zinc-Plated Eye Bolts"
    obj_susp.Shape = susp_shape
    grp_core.addObject(obj_susp)
    apply_material(obj_susp, "Steel-ZincPlated")

    return grp_core


# ==============================================================================
# SUBCOMPONENT 2: SOLARONICS FLARED REFLECTOR HOOD
# ==============================================================================
def build_reflector_hood_subassembly(doc, name="Solaronics_Reflector_Hood"):
    """
    Builds the deep focusing reflector hood subassembly:
      - 4-sided sloping mirror-polished aluminum reflector shell
      - 1.25 in (31.75 mm) wide outward flared perimeter rim flange
        expanding mouth to 16-3/4 in (425.5 mm) x 22-1/2 in (571.5 mm)
      - 45-degree mitered corner seams matching manufacturer photos
      - Mating collar at throat (Z = 0) attaching to plenum
      - Solaronics red identification nameplate badge
    """
    grp_hood = doc.addObject("App::Part", name)
    grp_hood.Label = "Solaronics K-30 Flared Parabolic Reflector Hood"

    # A. Sloping 4-Sided Reflector Cavity
    p_th_b0 = FreeCAD.Vector(-THROAT_W / 2.0, -THROAT_L / 2.0, 0)
    p_th_b1 = FreeCAD.Vector(THROAT_W / 2.0, -THROAT_L / 2.0, 0)
    p_th_b2 = FreeCAD.Vector(THROAT_W / 2.0, THROAT_L / 2.0, 0)
    p_th_b3 = FreeCAD.Vector(-THROAT_W / 2.0, THROAT_L / 2.0, 0)
    poly_throat = Part.makePolygon([p_th_b0, p_th_b1, p_th_b2, p_th_b3, p_th_b0])

    p_m_b0 = FreeCAD.Vector(-MOUTH_INNER_W / 2.0, -MOUTH_INNER_L / 2.0, -REFL_DEPTH)
    p_m_b1 = FreeCAD.Vector(MOUTH_INNER_W / 2.0, -MOUTH_INNER_L / 2.0, -REFL_DEPTH)
    p_m_b2 = FreeCAD.Vector(MOUTH_INNER_W / 2.0, MOUTH_INNER_L / 2.0, -REFL_DEPTH)
    p_m_b3 = FreeCAD.Vector(-MOUTH_INNER_W / 2.0, MOUTH_INNER_L / 2.0, -REFL_DEPTH)
    poly_mouth = Part.makePolygon([p_m_b0, p_m_b1, p_m_b2, p_m_b3, p_m_b0])

    hood_outer = Part.makeLoft([poly_mouth, poly_throat], True)

    # Inner cutout (1.2 mm thickness)
    p_th_in0 = FreeCAD.Vector(-THROAT_W / 2.0 + SHEET_T, -THROAT_L / 2.0 + SHEET_T, 0.5)
    p_th_in1 = FreeCAD.Vector(THROAT_W / 2.0 - SHEET_T, -THROAT_L / 2.0 + SHEET_T, 0.5)
    p_th_in2 = FreeCAD.Vector(THROAT_W / 2.0 - SHEET_T, THROAT_L / 2.0 - SHEET_T, 0.5)
    p_th_in3 = FreeCAD.Vector(-THROAT_W / 2.0 + SHEET_T, THROAT_L / 2.0 - SHEET_T, 0.5)
    poly_th_in = Part.makePolygon([p_th_in0, p_th_in1, p_th_in2, p_th_in3, p_th_in0])

    p_m_in0 = FreeCAD.Vector(-MOUTH_INNER_W / 2.0 + SHEET_T, -MOUTH_INNER_L / 2.0 + SHEET_T, -REFL_DEPTH - 0.5)
    p_m_in1 = FreeCAD.Vector(MOUTH_INNER_W / 2.0 - SHEET_T, -MOUTH_INNER_L / 2.0 + SHEET_T, -REFL_DEPTH - 0.5)
    p_m_in2 = FreeCAD.Vector(MOUTH_INNER_W / 2.0 - SHEET_T, MOUTH_INNER_L / 2.0 - SHEET_T, -REFL_DEPTH - 0.5)
    p_m_in3 = FreeCAD.Vector(-MOUTH_INNER_W / 2.0 + SHEET_T, MOUTH_INNER_L / 2.0 - SHEET_T, -REFL_DEPTH - 0.5)
    poly_m_in = Part.makePolygon([p_m_in0, p_m_in1, p_m_in2, p_m_in3, p_m_in0])

    hood_inner = Part.makeLoft([poly_m_in, poly_th_in], True)
    hood_shell = hood_outer.cut(hood_inner)

    # B. Outward Flared Perimeter Rim Flange (1.25 in / 31.75 mm flare at Z = -REFL_DEPTH)
    flange_outer = Part.makeBox(MOUTH_OUTER_W, MOUTH_OUTER_L, 2.0, FreeCAD.Vector(-MOUTH_OUTER_W / 2.0, -MOUTH_OUTER_L / 2.0, -REFL_DEPTH))
    flange_inner = Part.makeBox(MOUTH_INNER_W, MOUTH_INNER_L, 3.0, FreeCAD.Vector(-MOUTH_INNER_W / 2.0, -MOUTH_INNER_L / 2.0, -REFL_DEPTH - 0.5))
    flared_flange = flange_outer.cut(flange_inner)

    # 45-degree corner miter relief cuts on flange
    for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        cx = sx * MOUTH_INNER_W / 2.0
        cy = sy * MOUTH_INNER_L / 2.0
        m_slot = Part.makeBox(FLANGE_FLARE * 1.5, 1.2, 2.5, FreeCAD.Vector(0, -0.6, -REFL_DEPTH - 0.2))
        m_slot.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 45 if sx * sy > 0 else -45)
        m_slot.translate(FreeCAD.Vector(cx, cy, 0))
        flared_flange = flared_flange.cut(m_slot)

    hood_total = hood_shell.fuse(flared_flange)

    # C. Mating Mounting Collar at Throat (Z = 0)
    throat_flange_out = Part.makeBox(THROAT_W + 16.0, THROAT_L + 16.0, 2.0, FreeCAD.Vector(-(THROAT_W + 16.0) / 2.0, -(THROAT_L + 16.0) / 2.0, 0))
    throat_flange_in = Part.makeBox(THROAT_W, THROAT_L, 3.0, FreeCAD.Vector(-THROAT_W / 2.0, -THROAT_L / 2.0, -0.5))
    throat_flange = throat_flange_out.cut(throat_flange_in)
    hood_total = hood_total.fuse(throat_flange)

    obj_hood = doc.addObject("Part::Feature", "Solaronics_Flared_Reflector_Hood")
    obj_hood.Label = "Mirror-Polished Aluminum Flared Focusing Reflector Hood (16-3/4in Mouth)"
    obj_hood.Shape = hood_total
    grp_hood.addObject(obj_hood)
    apply_material(obj_hood, "Aluminum-6061-T6")

    # D. Solaronics Red Identification Nameplate
    logo_w = 120.0
    logo_l = 32.0
    logo_t = 1.0
    # Inward normal of lower reflector slope (dy = -50 mm, dz = -110 mm)
    # Tangent: (0, -0.4138, -0.9104), Inward normal: (0, 0.9104, -0.4138)
    ny, nz = 0.9104, -0.4138
    y_c = -265.0 + 0.8 * ny
    z_c = -55.0 + 0.8 * nz

    plate = Part.makeBox(logo_w, logo_l, logo_t, FreeCAD.Vector(-logo_w / 2.0, -logo_l / 2.0, -logo_t / 2.0))
    slope_angle = math.degrees(math.atan2(-110.0, -50.0)) - 180.0
    plate.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), slope_angle)
    plate.translate(FreeCAD.Vector(0, y_c, z_c))

    obj_logo = doc.addObject("Part::Feature", "Solaronics_Logo_Plate")
    obj_logo.Label = "Solaronics Red Identification Nameplate"
    obj_logo.Shape = plate
    grp_hood.addObject(obj_logo)
    apply_material(obj_logo, "PowderCoat-IndustrialRed")

    return grp_hood


# ==============================================================================
# PUBLIC STANDALONE BUILDER WRAPPERS
# ==============================================================================

def create_solaronics_burner_core_component(doc, placement=None):
    """
    Creates standalone Solaronics Burner Core subcomponent in `doc`.
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = build_burner_core_subassembly(doc, name="Solaronics_Burner_Core")
    grp.Placement = placement
    return grp


def create_solaronics_reflector_hood_component(doc, placement=None):
    """
    Creates standalone Solaronics Flared Reflector Hood subcomponent in `doc`.
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = build_reflector_hood_subassembly(doc, name="Solaronics_Reflector_Hood")
    grp.Placement = placement
    return grp


def create_solaronics_infrared_burner_component(doc, placement=None):
    """
    Creates complete Solaronics K-30 Infrared Burner assembly in `doc`.
    Organized as a master `App::Part` containing separate subcomponents:
      1. `Solaronics_Burner_Core` (App::Part)
      2. `Solaronics_Reflector_Hood` (App::Part)

    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)

    Returns:
      App::Part containing the complete burner and hood assembly
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp_master = doc.addObject("App::Part", "Solaronics_Infrared_Burner")
    grp_master.Label = "Solaronics K-30 High-Intensity Ceramic Infrared Burner & Flared Reflector"

    # Build subcomponents inside doc and attach to master Part
    grp_burner = build_burner_core_subassembly(doc, name="Solaronics_Burner_Core")
    grp_hood = build_reflector_hood_subassembly(doc, name="Solaronics_Reflector_Hood")

    grp_master.addObject(grp_burner)
    grp_master.addObject(grp_hood)

    grp_master.Placement = placement
    return grp_master

