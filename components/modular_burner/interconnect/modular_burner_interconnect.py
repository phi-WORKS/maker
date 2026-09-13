"""
Modular Burner Interconnect & Array Connection System
Standalone 3D Parametric CAD Module (Maker Component Library)

Explicitly models the complete mechanical, gas plumbing, flame bridging,
and ignition interconnection system linking two modular ceramic burner cassettes:
  1. Dual Stainless Angle Slide Rails (1" x 1" x 1/8") with M5 captive studs and slotted expansion holes
  2. Belleville disc spring washer stacks under knurled brass thumb nuts for continuous thermal clamping
  3. High-temperature ceramic fiber expansion gasket between cassettes (5mm gap)
  4. Formed 304 stainless steel perforated flame crossover channel bridge
  5. Precision 3/4" square gas distribution manifold rail with 3/8" flare inlet
  6. Twin laser-cut manifold standoff mounting brackets with ceramic thermal break isolator washers
  7. Dual calibrated brass hex orifice spuds (#60 drill @ 11 in W.C. LP) with exact coaxial alignment
  8. Calibrated 6mm primary air induction gap into venturi bellmouth horns
  9. Rotatable primary air shutter collars with adjustment thumbscrews
  10. Polished 304 SS radiant heat shield baffle plate protecting the gas manifold rail
  11. Silicone spark wire boots, high-voltage leads, and copper thermocouple sensing line
"""

import os
import sys
import math
import FreeCAD
import Part

from phi_works.maker.materials import apply_material

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
components_dir = os.path.abspath(os.path.join(script_dir, ".."))
if components_dir not in sys.path:
    sys.path.insert(0, components_dir)

from cassette.modular_ceramic_burner import create_modular_ceramic_burner_component

# ==============================================================================
# PARAMETRIC ENGINEERING DIMENSIONS (INTERCONNECT SYSTEM)
# ==============================================================================

# Cassette Geometry & Layout
CASING_W = 180.0              # Deep-drawn plenum width across X
CASING_L = 230.0              # Deep-drawn plenum length along Y
CASSETTE_GAP = 5.0            # Thermal expansion gap at X = 0
CASSETTE_PITCH_X = CASING_W + CASSETTE_GAP  # 185.0 mm center-to-center pitch
CASSETTE_SPAN_Y = CASING_L    # 230.0 mm span along Y

# Venturi & Gas Flow Coaxial Geometry
VENTURI_Z = 62.7              # Venturi centerline elevation
HORN_MOUTH_Y = -85.0          # Venturi bellmouth entrance Y coordinate
AIR_GAP = 6.0                 # Primary atmospheric air gap
ORIFICE_HEX = 11.0            # 7/16 in (11mm) brass hex body
ORIFICE_LEN = 20.0            # Overall spud length (hex + nozzle)
MANIFOLD_SIZE = 19.05         # 3/4 in square 6061-T6 aluminum rail
MANIFOLD_Y = HORN_MOUTH_Y - AIR_GAP - ORIFICE_LEN - MANIFOLD_SIZE / 2.0  # -120.525 mm
MANIFOLD_LEN = 360.0          # Manifold rail length across X

# Mechanical Slide Angle Rails (304 Stainless Steel)
RAIL_LEN = 380.0              # Total rail length across X
ANGLE_LEG = 25.4              # 1.0 in leg width
ANGLE_T = 3.175               # 1/8 in sheet thickness
RAIL_Z = 22.7 - ANGLE_T       # Flange elevation supporting cassette tabs
STUD_DIA = 5.0                # M5 captive threaded stud diameter
STUD_LEN = 25.0               # Stud height above rail horizontal leg
THUMB_NUT_OD = 14.0           # Knurled brass thumb nut outer diameter
THUMB_NUT_H = 10.0            # Thumb nut height
BELLEVILLE_OD = 12.0          # Conical Belleville disc spring washer OD
BELLEVILLE_H = 2.5            # Belleville spring stack height

# Flame Crossover Bridge
BRIDGE_W = 24.0               # Crossover bridge width across X
BRIDGE_L = 160.0              # Crossover bridge length along Y
BRIDGE_H = 10.0               # Arch height above radiant ceramic face
SLOT_PITCH = 15.0             # Perforation slot pitch along Y


def create_modular_burner_interconnect_component(doc, name="Modular_Burner_Interconnect", placement=None):
    """
    Builds the detailed modular burner connection assembly showcasing:
      - 2x Modular Ceramic Burner Cassettes (10,000 BTU each, coaxial venturis)
      - Front & rear 1" stainless angle slide rails with captive M5 studs & slotted expansion holes
      - Belleville disc spring washer stacks and knurled brass thumb nuts (tool-free thermal clamping)
      - Inter-cassette ceramic fiber thermal expansion gasket (5mm gap)
      - Perforated stainless flame crossover bridge spanning X = 0
      - Precision 3/4" gas manifold rail aligned coaxially with venturi horns
      - Twin standoff brackets with steatite ceramic thermal break isolator washers
      - 2x Machined brass hex orifice spuds with calibrated 6mm primary air gap
      - Polished 304 SS radiant heat shield baffle plate under the manifold
      - Silicone spark wire boots, ignition leads, and copper thermocouple sensing line
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Modular Burner Interconnect & Array Connection System"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Instantiate 2x Modular Ceramic Burner Cassettes (No Standalone Orifices)
    # --------------------------------------------------------------------------
    # Oriented with length along Y, venturis extending along -Y toward the gas manifold
    # Cassettes placed symmetrically at X = -CASSETTE_PITCH_X / 2 and +CASSETTE_PITCH_X / 2
    for i, offset_x in enumerate([-CASSETTE_PITCH_X / 2.0, CASSETTE_PITCH_X / 2.0], start=1):
        c_pos = FreeCAD.Vector(offset_x, 0, 0)
        c_placement = FreeCAD.Placement(c_pos, FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0))
        # include_orifice=False: Manifold rail provides the precisely aligned orifice spuds
        c_part = create_modular_ceramic_burner_component(doc, name=f"{name}_Cassette_{i}", placement=c_placement, include_orifice=False)
        grp.addObject(c_part)

    # --------------------------------------------------------------------------
    # 2. Dual Stainless Angle Slide Rails with Slotted Thermal Expansion Holes
    # --------------------------------------------------------------------------
    # Front angle rail at Y = +CASSETTE_SPAN_Y / 2.0
    # Rear angle rail at Y = -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG
    f_horiz = Part.makeBox(RAIL_LEN, ANGLE_LEG, ANGLE_T, FreeCAD.Vector(-RAIL_LEN / 2.0, CASSETTE_SPAN_Y / 2.0, RAIL_Z))
    f_vert = Part.makeBox(RAIL_LEN, ANGLE_T, ANGLE_LEG, FreeCAD.Vector(-RAIL_LEN / 2.0, CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG - ANGLE_T, RAIL_Z - ANGLE_LEG + ANGLE_T))
    front_angle = f_horiz.fuse(f_vert)

    r_horiz = Part.makeBox(RAIL_LEN, ANGLE_LEG, ANGLE_T, FreeCAD.Vector(-RAIL_LEN / 2.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG, RAIL_Z))
    r_vert = Part.makeBox(RAIL_LEN, ANGLE_T, ANGLE_LEG, FreeCAD.Vector(-RAIL_LEN / 2.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG, RAIL_Z - ANGLE_LEG + ANGLE_T))
    rear_angle = r_horiz.fuse(r_vert)

    # Cut 8.0mm x 5.5mm slotted expansion holes at cassette tab positions to allow thermal slip
    tab_x_positions = [
        -CASSETTE_PITCH_X / 2.0 - CASING_W / 4.0,
        -CASSETTE_PITCH_X / 2.0 + CASING_W / 4.0,
         CASSETTE_PITCH_X / 2.0 - CASING_W / 4.0,
         CASSETTE_PITCH_X / 2.0 + CASING_W / 4.0,
    ]
    for tx in tab_x_positions:
        # Front rail slot
        slot_f = Part.makeBox(8.0, 5.5, ANGLE_T + 4.0, FreeCAD.Vector(tx - 4.0, CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0 - 2.75, RAIL_Z - 2.0))
        front_angle = front_angle.cut(slot_f)
        # Rear rail slot
        slot_r = Part.makeBox(8.0, 5.5, ANGLE_T + 4.0, FreeCAD.Vector(tx - 4.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0 - 2.75, RAIL_Z - 2.0))
        rear_angle = rear_angle.cut(slot_r)

    # Frame chassis mounting holes at rail extremities
    for rx in [-RAIL_LEN / 2.0 + 15.0, RAIL_LEN / 2.0 - 15.0]:
        h_f = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(rx, CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0, RAIL_Z - 2.0), FreeCAD.Vector(0, 0, 1))
        h_r = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(rx, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0, RAIL_Z - 2.0), FreeCAD.Vector(0, 0, 1))
        front_angle = front_angle.cut(h_f)
        rear_angle = rear_angle.cut(h_r)

    slide_rails = front_angle.fuse(rear_angle)
    obj_rails = doc.addObject("Part::Feature", f"{name}_Slide_Angle_Rails")
    obj_rails.Label = "Dual 1in 304 SS Angle Slide Rails with Slotted Expansion Holes"
    obj_rails.Shape = slide_rails
    grp.addObject(obj_rails)
    apply_material(obj_rails, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 3. Captive M5 Studs, Belleville Spring Washer Packs & Knurled Brass Thumb Nuts
    # --------------------------------------------------------------------------
    studs = []
    springs = []
    nuts = []

    for tx in tab_x_positions:
        # Front row fasteners
        fy = CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0
        s_f = Part.makeCylinder(STUD_DIA / 2.0, STUD_LEN, FreeCAD.Vector(tx, fy, RAIL_Z), FreeCAD.Vector(0, 0, 1))
        studs.append(s_f)
        # Belleville disc spring stack (conical washer)
        b_f = Part.makeCone(BELLEVILLE_OD / 2.0, BELLEVILLE_OD / 2.0 - 1.0, BELLEVILLE_H, FreeCAD.Vector(tx, fy, RAIL_Z + ANGLE_T + 2.5), FreeCAD.Vector(0, 0, 1))
        springs.append(b_f)
        # Knurled brass thumb nut
        n_barrel_f = Part.makeCylinder(THUMB_NUT_OD / 2.0, THUMB_NUT_H, FreeCAD.Vector(tx, fy, RAIL_Z + ANGLE_T + 2.5 + BELLEVILLE_H), FreeCAD.Vector(0, 0, 1))
        n_collar_f = Part.makeCylinder(THUMB_NUT_OD / 2.0 + 1.5, 3.0, FreeCAD.Vector(tx, fy, RAIL_Z + ANGLE_T + 2.5 + BELLEVILLE_H + THUMB_NUT_H - 3.0), FreeCAD.Vector(0, 0, 1))
        nuts.append(n_barrel_f.fuse(n_collar_f))

        # Rear row fasteners
        ry = -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0
        s_r = Part.makeCylinder(STUD_DIA / 2.0, STUD_LEN, FreeCAD.Vector(tx, ry, RAIL_Z), FreeCAD.Vector(0, 0, 1))
        studs.append(s_r)
        b_r = Part.makeCone(BELLEVILLE_OD / 2.0, BELLEVILLE_OD / 2.0 - 1.0, BELLEVILLE_H, FreeCAD.Vector(tx, ry, RAIL_Z + ANGLE_T + 2.5), FreeCAD.Vector(0, 0, 1))
        springs.append(b_r)
        n_barrel_r = Part.makeCylinder(THUMB_NUT_OD / 2.0, THUMB_NUT_H, FreeCAD.Vector(tx, ry, RAIL_Z + ANGLE_T + 2.5 + BELLEVILLE_H), FreeCAD.Vector(0, 0, 1))
        n_collar_r = Part.makeCylinder(THUMB_NUT_OD / 2.0 + 1.5, 3.0, FreeCAD.Vector(tx, ry, RAIL_Z + ANGLE_T + 2.5 + BELLEVILLE_H + THUMB_NUT_H - 3.0), FreeCAD.Vector(0, 0, 1))
        nuts.append(n_barrel_r.fuse(n_collar_r))

    stud_shape = studs[0]
    for s in studs[1:]:
        stud_shape = stud_shape.fuse(s)
    obj_studs = doc.addObject("Part::Feature", f"{name}_Captive_Studs")
    obj_studs.Label = "M5 Stainless Steel Captive Threaded Mounting Studs (x8)"
    obj_studs.Shape = stud_shape
    grp.addObject(obj_studs)
    apply_material(obj_studs, "Steel-304Stainless")

    spring_shape = springs[0]
    for sp in springs[1:]:
        spring_shape = spring_shape.fuse(sp)
    obj_springs = doc.addObject("Part::Feature", f"{name}_Belleville_Springs")
    obj_springs.Label = "Belleville Disc Spring Packs (Thermal Expansion Clamping x8)"
    obj_springs.Shape = spring_shape
    grp.addObject(obj_springs)
    apply_material(obj_springs, "Steel-304Stainless")

    nut_shape = nuts[0]
    for n in nuts[1:]:
        nut_shape = nut_shape.fuse(n)
    obj_nuts = doc.addObject("Part::Feature", f"{name}_Knurled_Thumb_Nuts")
    obj_nuts.Label = "Knurled Brass Thumb Nuts (Tool-Free Quick Clamps x8)"
    obj_nuts.Shape = nut_shape
    grp.addObject(obj_nuts)
    apply_material(obj_nuts, "Brass-C360")

    # --------------------------------------------------------------------------
    # 4. Inter-Cassette Ceramic Fiber Thermal Expansion Gasket
    # --------------------------------------------------------------------------
    gasket_box = Part.makeBox(
        CASSETTE_GAP,
        CASSETTE_SPAN_Y - 10.0,
        32.0,
        FreeCAD.Vector(-CASSETTE_GAP / 2.0, -(CASSETTE_SPAN_Y - 10.0) / 2.0, 12.7)
    )
    obj_gasket = doc.addObject("Part::Feature", f"{name}_Thermal_Gasket")
    obj_gasket.Label = "Superwool 607 Ceramic Fiber Expansion Gasket (5mm Thermal Cushion)"
    obj_gasket.Shape = gasket_box
    grp.addObject(obj_gasket)
    apply_material(obj_gasket, "Ceramic-Cordierite")

    # --------------------------------------------------------------------------
    # 5. Formed 304 Stainless Steel Perforated Flame Crossover Bridge
    # --------------------------------------------------------------------------
    bridge_outer = Part.makeBox(BRIDGE_W, BRIDGE_L, BRIDGE_H, FreeCAD.Vector(-BRIDGE_W / 2.0, -BRIDGE_L / 2.0, -3.0))
    bridge_inner = Part.makeBox(BRIDGE_W - 3.0, BRIDGE_L - 3.0, BRIDGE_H, FreeCAD.Vector(-BRIDGE_W / 2.0 + 1.5, -BRIDGE_L / 2.0 + 1.5, -4.5))
    bridge_tunnel = bridge_outer.cut(bridge_inner)

    # Perforation slots for flame propagation
    for py in range(int(-BRIDGE_L / 2.0 + 15), int(BRIDGE_L / 2.0 - 10), int(SLOT_PITCH)):
        slot = Part.makeBox(BRIDGE_W + 4.0, 3.5, 4.0, FreeCAD.Vector(-BRIDGE_W / 2.0 - 2.0, py, BRIDGE_H - 5.0))
        bridge_tunnel = bridge_tunnel.cut(slot)

    foot_left = Part.makeBox(8.0, BRIDGE_L, 1.5, FreeCAD.Vector(-BRIDGE_W / 2.0 - 8.0, -BRIDGE_L / 2.0, -1.0))
    foot_right = Part.makeBox(8.0, BRIDGE_L, 1.5, FreeCAD.Vector(BRIDGE_W / 2.0, -BRIDGE_L / 2.0, -1.0))
    bridge_full = bridge_tunnel.fuse(foot_left).fuse(foot_right)

    obj_bridge = doc.addObject("Part::Feature", f"{name}_Flame_Crossover_Bridge")
    obj_bridge.Label = "Formed Perforated 304 SS Flame Crossover Bridge with Slip Relief"
    obj_bridge.Shape = bridge_full
    grp.addObject(obj_bridge)
    apply_material(obj_bridge, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 6. Gas Distribution Manifold Rail & 3/8" Flare Supply Inlet
    # --------------------------------------------------------------------------
    # Perfectly aligned at Z = VENTURI_Z (62.7mm) and Y = MANIFOLD_Y (-120.525mm)
    rail_main = Part.makeBox(
        MANIFOLD_LEN,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0, VENTURI_Z - MANIFOLD_SIZE / 2.0)
    )
    # Gas inlet fitting (3/8" SAE 45-deg brass flare) extending rearward (-Y) at center
    inlet_neck = Part.makeCylinder(
        6.35,
        28.0,
        FreeCAD.Vector(0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0, VENTURI_Z),
        FreeCAD.Vector(0, -1, 0)
    )
    inlet_hex = Part.makeCylinder(
        9.5,
        12.0,
        FreeCAD.Vector(0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0 - 16.0, VENTURI_Z),
        FreeCAD.Vector(0, -1, 0)
    )
    manifold_solid = rail_main.fuse(inlet_neck).fuse(inlet_hex)

    obj_manifold = doc.addObject("Part::Feature", f"{name}_Manifold_Rail")
    obj_manifold.Label = "3/4in Gas Distribution Manifold Rail with 3/8in Flare Inlet"
    obj_manifold.Shape = manifold_solid
    grp.addObject(obj_manifold)
    apply_material(obj_manifold, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 7. Twin Standoff Brackets with Steatite Ceramic Thermal Break Isolators
    # --------------------------------------------------------------------------
    standoffs = []
    isolators = []
    for bx in [-CASSETTE_PITCH_X / 2.0 - 45.0, CASSETTE_PITCH_X / 2.0 + 45.0]:
        # Steatite ceramic thermal barrier washer at bracket base (3mm thick)
        iso = Part.makeCylinder(8.0, 3.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0, RAIL_Z + ANGLE_T), FreeCAD.Vector(0, 0, 1))
        isolators.append(iso)

        # Laser-cut 304 SS bracket connecting rear angle rail to the manifold rail
        b_foot = Part.makeBox(16.0, 20.0, 3.0, FreeCAD.Vector(bx - 8.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0 - 10.0, RAIL_Z + ANGLE_T + 3.0))
        b_upright = Part.makeBox(
            3.0,
            abs(MANIFOLD_Y - (-CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0)),
            VENTURI_Z - RAIL_Z + MANIFOLD_SIZE / 2.0 + 5.0,
            FreeCAD.Vector(bx - 1.5, MANIFOLD_Y, RAIL_Z + ANGLE_T + 3.0)
        )
        b_clamp = Part.makeBox(
            16.0,
            MANIFOLD_SIZE + 6.0,
            MANIFOLD_SIZE + 6.0,
            FreeCAD.Vector(bx - 8.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0 - 3.0, VENTURI_Z - MANIFOLD_SIZE / 2.0 - 3.0)
        )
        b_hole = Part.makeBox(
            18.0,
            MANIFOLD_SIZE,
            MANIFOLD_SIZE,
            FreeCAD.Vector(bx - 9.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0, VENTURI_Z - MANIFOLD_SIZE / 2.0)
        )
        clamp_saddle = b_clamp.cut(b_hole)
        standoffs.append(b_foot.fuse(b_upright).fuse(clamp_saddle))

    standoff_solid = standoffs[0].fuse(standoffs[1])
    obj_standoffs = doc.addObject("Part::Feature", f"{name}_Manifold_Standoffs")
    obj_standoffs.Label = "304 SS Manifold Standoff Brackets (Laser-Cut)"
    obj_standoffs.Shape = standoff_solid
    grp.addObject(obj_standoffs)
    apply_material(obj_standoffs, "Steel-304Stainless")

    iso_solid = isolators[0].fuse(isolators[1])
    obj_isolators = doc.addObject("Part::Feature", f"{name}_Thermal_Break_Washers")
    obj_isolators.Label = "Steatite Ceramic Thermal Break Isolator Washers (Conductive Barrier)"
    obj_isolators.Shape = iso_solid
    grp.addObject(obj_isolators)
    apply_material(obj_isolators, "Ceramic-Cordierite")

    # --------------------------------------------------------------------------
    # 8. Dual Calibrated Brass Hex Orifice Spuds (#60 Drill, Exactly Coaxial)
    # --------------------------------------------------------------------------
    # Located at X = -CASSETTE_PITCH_X / 2.0 and +CASSETTE_PITCH_X / 2.0
    # Extending forward (+Y) from manifold front face toward venturi bellmouth horns
    spuds = []
    spud_start_y = MANIFOLD_Y + MANIFOLD_SIZE / 2.0  # -111.0 mm

    for sx in [-CASSETTE_PITCH_X / 2.0, CASSETTE_PITCH_X / 2.0]:
        s_hex = Part.makeCylinder(
            ORIFICE_HEX / 2.0,
            14.0,
            FreeCAD.Vector(sx, spud_start_y, VENTURI_Z),
            FreeCAD.Vector(0, 1, 0)
        )
        s_nozzle = Part.makeCone(
            4.0,
            2.5,
            ORIFICE_LEN - 14.0,
            FreeCAD.Vector(sx, spud_start_y + 14.0, VENTURI_Z),
            FreeCAD.Vector(0, 1, 0)
        )
        spuds.append(s_hex.fuse(s_nozzle))

    spud_shape = spuds[0].fuse(spuds[1])
    obj_spuds = doc.addObject("Part::Feature", f"{name}_Brass_Orifice_Spuds")
    obj_spuds.Label = "Dual Machined Brass Orifice Spuds (#60 Drill, 6mm Air Gap Coaxial)"
    obj_spuds.Shape = spud_shape
    grp.addObject(obj_spuds)
    apply_material(obj_spuds, "Brass-C360")

    # --------------------------------------------------------------------------
    # 9. Polished 304 SS Radiant Heat Shield Baffle Plate
    # --------------------------------------------------------------------------
    # Positioned horizontally between plenum top and manifold rail (Z = 50.0mm)
    # Deflects infrared radiation away from the aluminum gas rail
    baffle_box = Part.makeBox(
        340.0,
        50.0,
        1.2,
        FreeCAD.Vector(-170.0, MANIFOLD_Y - 10.0, 48.0)
    )
    # Clearance slots for standoff uprights
    for bx in [-CASSETTE_PITCH_X / 2.0 - 45.0, CASSETTE_PITCH_X / 2.0 + 45.0]:
        slot_b = Part.makeBox(8.0, 15.0, 4.0, FreeCAD.Vector(bx - 4.0, MANIFOLD_Y - 5.0, 46.0))
        baffle_box = baffle_box.cut(slot_b)

    obj_baffle = doc.addObject("Part::Feature", f"{name}_Radiant_Heat_Shield")
    obj_baffle.Label = "Polished 304 SS Radiant Heat Shield Baffle Plate (IR Deflector)"
    obj_baffle.Shape = baffle_box
    grp.addObject(obj_baffle)
    apply_material(obj_baffle, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 10. Silicone Spark Wire Boots & Thermocouple Safety Capillary Line
    # --------------------------------------------------------------------------
    boots = []
    leads = []
    for bx in [-CASSETTE_PITCH_X / 2.0 + 20.0, CASSETTE_PITCH_X / 2.0 - 20.0]:
        boot_vert = Part.makeCylinder(4.5, 18.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 8.0, 15.0), FreeCAD.Vector(0, 0, 1))
        boot_horiz = Part.makeCylinder(4.5, 20.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 8.0, 31.0), FreeCAD.Vector(0, 1, 0.2))
        boots.append(boot_vert.fuse(boot_horiz))
        wire_lead = Part.makeCylinder(2.2, 120.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 28.0, 35.0), FreeCAD.Vector(0, 1, 0.2))
        leads.append(wire_lead)

    tc_bulb = Part.makeCylinder(3.0, 22.0, FreeCAD.Vector(-CASSETTE_PITCH_X / 2.0 - 25.0, -CASSETTE_SPAN_Y / 4.0, 5.0), FreeCAD.Vector(0, 1, 0))
    tc_bracket = Part.makeBox(12.0, 15.0, 2.0, FreeCAD.Vector(-CASSETTE_PITCH_X / 2.0 - 31.0, -CASSETTE_SPAN_Y / 4.0 + 5.0, 6.0))
    tc_tube = Part.makeCylinder(1.8, 180.0, FreeCAD.Vector(-CASSETTE_PITCH_X / 2.0 - 25.0, -CASSETTE_SPAN_Y / 4.0 + 22.0, 5.0), FreeCAD.Vector(0, 1, 0.3))
    tc_assembly = tc_bulb.fuse(tc_bracket).fuse(tc_tube)

    harness_solid = boots[0].fuse(boots[1]).fuse(leads[0]).fuse(leads[1]).fuse(tc_assembly)
    obj_harness = doc.addObject("Part::Feature", f"{name}_Ignition_Safety_Leads")
    obj_harness.Label = "Silicone Spark Boots, HV Ignition Leads & Copper Thermocouple"
    obj_harness.Shape = harness_solid
    grp.addObject(obj_harness)
    apply_material(obj_harness, "Ceramic-Alumina")

    return grp


if __name__ == "__main__":
    doc = FreeCAD.newDocument("TestBurnerInterconnect")
    create_modular_burner_interconnect_component(doc)
    doc.recompute()
    print("Burner Interconnect build complete. Objects:", len(doc.Objects))
