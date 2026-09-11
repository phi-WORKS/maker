"""
Modular Burner Interconnect & Array Connection System
Standalone 3D Parametric CAD Module (Maker Component Library)

Explicitly models the complete mechanical, gas plumbing, flame bridging,
and ignition interconnection system linking modular ceramic burner cassettes:
  1. Dual Stainless Angle Slide Rails (1" x 1" x 1/8") with M5 captive studs
  2. Quick-swap knurled brass thumb nuts securing cassette slotted tabs
  3. High-temperature ceramic fiber expansion gasket between cassettes
  4. Formed 304 stainless steel perforated flame crossover channel bridge
  5. Rigid 3/4" square gas distribution manifold rail with 3/8" flare inlet
  6. Twin laser-cut manifold standoff mounting brackets
  7. Dual calibrated brass hex orifice spuds (#60 drill @ 11 in W.C. LP)
  8. Calibrated 6mm primary air induction gap into venturi bellmouth horns
  9. Rotatable primary air shutter collars with adjustment screws
  10. Silicone spark wire boots, high-voltage leads, and thermocouple probe
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

# Cassette Layout
CASSETTE_PITCH_X = 175.0      # Center-to-center pitch of the two 170mm-wide cassettes
CASSETTE_GAP = 5.0            # Thermal expansion gap at X = 0 (3-5 mm)
CASSETTE_SPAN_Y = 220.0       # Cassette length along Y (oriented 90-deg)

# Mechanical Slide Angle Rails (304 Stainless Steel)
RAIL_LEN = 380.0              # Total rail length across X (14.96 in)
ANGLE_LEG = 25.4              # 1.0 in leg width
ANGLE_T = 3.175               # 1/8 in sheet thickness
STUD_DIA = 5.0                # M5 captive threaded stud diameter
STUD_LEN = 25.0               # Stud height above rail horizontal leg
THUMB_NUT_OD = 14.0           # Knurled brass thumb nut outer diameter
THUMB_NUT_H = 10.0            # Thumb nut height

# Gas Manifold & Standoffs
MANIFOLD_SIZE = 19.05         # 3/4 in square tubing
MANIFOLD_LEN = 360.0          # Manifold rail length across X
MANIFOLD_Z = 68.0             # Manifold centerline elevation
MANIFOLD_Y = 118.0            # Manifold centerline position along Y
AIR_GAP = 6.0                 # Primary atmospheric air gap between nozzle and horn
ORIFICE_HEX = 11.0            # 7/16 in brass hex body
ORIFICE_PROJ = 24.0           # Orifice projection forward from manifold face

# Flame Crossover Bridge
BRIDGE_W = 24.0               # Crossover bridge width across X
BRIDGE_L = 160.0              # Crossover bridge length along Y
BRIDGE_H = 10.0               # Arch height above radiant ceramic face
SLOT_PITCH = 15.0             # Perforation slot pitch along Y


def create_modular_burner_interconnect_component(doc, name="Modular_Burner_Interconnect", placement=None):
    """
    Builds the detailed modular burner connection assembly showcasing:
      - 2x Modular Ceramic Burner Cassettes (10,000 BTU each)
      - Front & rear 1" stainless angle slide rails with captive M5 studs
      - 4x M5 knurled brass thumb nuts
      - Inter-cassette ceramic fiber thermal expansion gasket
      - Perforated stainless flame crossover tunnel
      - 3/4" gas manifold rail with twin standoff mounting brackets
      - 2x Machined brass hex orifice spuds with 6mm primary air gap
      - High-voltage spark wire boots and thermocouple safety sensor line
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Modular Burner Interconnect & Array Connection System"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Instantiate 2x Modular Ceramic Burner Cassettes
    # --------------------------------------------------------------------------
    # Rotated 90 deg so the 170 mm width is along X and 220 mm length is along Y
    # Venturis extend in the +Y direction toward the manifold rail
    rot_cassette = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), -90)

    for i, offset_x in enumerate([-CASSETTE_PITCH_X / 2.0, CASSETTE_PITCH_X / 2.0], start=1):
        c_pos = FreeCAD.Vector(offset_x, 0, 0)
        c_placement = FreeCAD.Placement(c_pos, rot_cassette)
        c_part = create_modular_ceramic_burner_component(doc, name=f"{name}_Cassette_{i}", placement=c_placement)
        grp.addObject(c_part)

    # --------------------------------------------------------------------------
    # 2. Dual Stainless Angle Slide Rails (Front & Rear Mounting Tray)
    # --------------------------------------------------------------------------
    # Front rail at Y = -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0
    # Rear rail at Y = +CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0
    # Horizontal flange supports cassette tabs at Z = 22.7 mm
    rail_z = 22.7 - ANGLE_T
    rails = []

    # Front Angle (Horizontal leg points +Y, vertical leg points -Z)
    f_horiz = Part.makeBox(RAIL_LEN, ANGLE_LEG, ANGLE_T, FreeCAD.Vector(-RAIL_LEN / 2.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG, rail_z))
    f_vert = Part.makeBox(RAIL_LEN, ANGLE_T, ANGLE_LEG, FreeCAD.Vector(-RAIL_LEN / 2.0, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG, rail_z - ANGLE_LEG + ANGLE_T))
    front_angle = f_horiz.fuse(f_vert)

    # Rear Angle (Horizontal leg points -Y, vertical leg points -Z)
    r_horiz = Part.makeBox(RAIL_LEN, ANGLE_LEG, ANGLE_T, FreeCAD.Vector(-RAIL_LEN / 2.0, CASSETTE_SPAN_Y / 2.0, rail_z))
    r_vert = Part.makeBox(RAIL_LEN, ANGLE_T, ANGLE_LEG, FreeCAD.Vector(-RAIL_LEN / 2.0, CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG - ANGLE_T, rail_z - ANGLE_LEG + ANGLE_T))
    rear_angle = r_horiz.fuse(r_vert)

    # Cut mounting bolt clearance holes at ends of angle rails
    for rx in [-RAIL_LEN / 2.0 + 15.0, RAIL_LEN / 2.0 - 15.0]:
        h_front = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(rx, -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0, rail_z - 2.0), FreeCAD.Vector(0, 0, 1))
        h_rear = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(rx, CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0, rail_z - 2.0), FreeCAD.Vector(0, 0, 1))
        front_angle = front_angle.cut(h_front)
        rear_angle = rear_angle.cut(h_rear)

    slide_rails = front_angle.fuse(rear_angle)
    obj_rails = doc.addObject("Part::Feature", f"{name}_Slide_Angle_Rails")
    obj_rails.Label = "Dual 1in 304 SS Angle Slide Rails (Quick-Swap Chassis Tray)"
    obj_rails.Shape = slide_rails
    grp.addObject(obj_rails)
    apply_material(obj_rails, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 3. Captive M5 Threaded Studs & Knurled Brass Thumb Nuts
    # --------------------------------------------------------------------------
    studs = []
    nuts = []
    # Stud locations match the 4 cassette tab positions
    tab_x_offsets = [
        -CASSETTE_PITCH_X / 2.0 - 170.0 / 4.0,
        -CASSETTE_PITCH_X / 2.0 + 170.0 / 4.0,
         CASSETTE_PITCH_X / 2.0 - 170.0 / 4.0,
         CASSETTE_PITCH_X / 2.0 + 170.0 / 4.0,
    ]

    for sx in tab_x_offsets:
        # Front row stud and nut
        sy_front = -CASSETTE_SPAN_Y / 2.0 - ANGLE_LEG / 2.0 + 2.0
        s_f = Part.makeCylinder(STUD_DIA / 2.0, STUD_LEN, FreeCAD.Vector(sx, sy_front, rail_z), FreeCAD.Vector(0, 0, 1))
        studs.append(s_f)
        n_barrel_f = Part.makeCylinder(THUMB_NUT_OD / 2.0, THUMB_NUT_H, FreeCAD.Vector(sx, sy_front, 25.2), FreeCAD.Vector(0, 0, 1))
        n_collar_f = Part.makeCylinder(THUMB_NUT_OD / 2.0 + 1.5, 3.0, FreeCAD.Vector(sx, sy_front, 25.2 + THUMB_NUT_H - 3.0), FreeCAD.Vector(0, 0, 1))
        nuts.append(n_barrel_f.fuse(n_collar_f))

        # Rear row stud and nut
        sy_rear = CASSETTE_SPAN_Y / 2.0 + ANGLE_LEG / 2.0 - 2.0
        s_r = Part.makeCylinder(STUD_DIA / 2.0, STUD_LEN, FreeCAD.Vector(sx, sy_rear, rail_z), FreeCAD.Vector(0, 0, 1))
        studs.append(s_r)
        n_barrel_r = Part.makeCylinder(THUMB_NUT_OD / 2.0, THUMB_NUT_H, FreeCAD.Vector(sx, sy_rear, 25.2), FreeCAD.Vector(0, 0, 1))
        n_collar_r = Part.makeCylinder(THUMB_NUT_OD / 2.0 + 1.5, 3.0, FreeCAD.Vector(sx, sy_rear, 25.2 + THUMB_NUT_H - 3.0), FreeCAD.Vector(0, 0, 1))
        nuts.append(n_barrel_r.fuse(n_collar_r))

    stud_shape = studs[0]
    for s in studs[1:]:
        stud_shape = stud_shape.fuse(s)
    obj_studs = doc.addObject("Part::Feature", f"{name}_Captive_Studs")
    obj_studs.Label = "M5 Stainless Steel Captive Threaded Mounting Studs (x8)"
    obj_studs.Shape = stud_shape
    grp.addObject(obj_studs)
    apply_material(obj_studs, "Steel-304Stainless")

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
    # Fills the 5 mm gap at X = 0 between the two steel plenum casings
    gasket_box = Part.makeBox(
        CASSETTE_GAP,
        CASSETTE_SPAN_Y - 10.0,
        32.0,
        FreeCAD.Vector(-CASSETTE_GAP / 2.0, -(CASSETTE_SPAN_Y - 10.0) / 2.0, 12.7)
    )
    obj_gasket = doc.addObject("Part::Feature", f"{name}_Thermal_Gasket")
    obj_gasket.Label = "High-Temp Ceramic Fiber Expansion Gasket (Vibration Cushion)"
    obj_gasket.Shape = gasket_box
    grp.addObject(obj_gasket)
    apply_material(obj_gasket, "Ceramic-Cordierite")

    # --------------------------------------------------------------------------
    # 5. Formed 304 Stainless Steel Perforated Flame Crossover Channel Bridge
    # --------------------------------------------------------------------------
    # Arch bridge centered at X = 0 spanning across the radiant face gap
    bridge_outer = Part.makeBox(
        BRIDGE_W,
        BRIDGE_L,
        BRIDGE_H,
        FreeCAD.Vector(-BRIDGE_W / 2.0, -BRIDGE_L / 2.0, -3.0)
    )
    bridge_inner = Part.makeBox(
        BRIDGE_W - 3.0,
        BRIDGE_L - 3.0,
        BRIDGE_H,
        FreeCAD.Vector(-BRIDGE_W / 2.0 + 1.5, -BRIDGE_L / 2.0 + 1.5, -4.5)
    )
    bridge_tunnel = bridge_outer.cut(bridge_inner)

    # Perforations along Y to allow flame front propagation and secondary air
    for py in range(int(-BRIDGE_L / 2.0 + 15), int(BRIDGE_L / 2.0 - 10), int(SLOT_PITCH)):
        slot = Part.makeBox(BRIDGE_W + 4.0, 3.5, 4.0, FreeCAD.Vector(-BRIDGE_W / 2.0 - 2.0, py, BRIDGE_H - 5.0))
        bridge_tunnel = bridge_tunnel.cut(slot)

    # Side mounting foot flanges clamping under tile retention bezels
    foot_left = Part.makeBox(8.0, BRIDGE_L, 1.5, FreeCAD.Vector(-BRIDGE_W / 2.0 - 8.0, -BRIDGE_L / 2.0, -1.0))
    foot_right = Part.makeBox(8.0, BRIDGE_L, 1.5, FreeCAD.Vector(BRIDGE_W / 2.0, -BRIDGE_L / 2.0, -1.0))
    bridge_full = bridge_tunnel.fuse(foot_left).fuse(foot_right)

    obj_bridge = doc.addObject("Part::Feature", f"{name}_Flame_Crossover_Bridge")
    obj_bridge.Label = "Formed Perforated 304 SS Flame Crossover Propagation Bridge"
    obj_bridge.Shape = bridge_full
    grp.addObject(obj_bridge)
    apply_material(obj_bridge, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 6. Gas Distribution Manifold Rail & 3/8" Flare Supply Inlet
    # --------------------------------------------------------------------------
    # 3/4" square rail mounted horizontally at Y = MANIFOLD_Y, Z = MANIFOLD_Z
    rail_main = Part.makeBox(
        MANIFOLD_LEN,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0, MANIFOLD_Z - MANIFOLD_SIZE / 2.0)
    )
    # Gas inlet fitting (3/8" SAE 45-deg brass flare) extending from rear (+Y)
    inlet_neck = Part.makeCylinder(
        6.35,
        28.0,
        FreeCAD.Vector(0, MANIFOLD_Y + MANIFOLD_SIZE / 2.0, MANIFOLD_Z),
        FreeCAD.Vector(0, 1, 0)
    )
    inlet_hex = Part.makeCylinder(
        9.5,
        12.0,
        FreeCAD.Vector(0, MANIFOLD_Y + MANIFOLD_SIZE / 2.0 + 8.0, MANIFOLD_Z),
        FreeCAD.Vector(0, 1, 0)
    )
    manifold_solid = rail_main.fuse(inlet_neck).fuse(inlet_hex)

    obj_manifold = doc.addObject("Part::Feature", f"{name}_Manifold_Rail")
    obj_manifold.Label = "3/4in Gas Distribution Manifold Rail with 3/8in Flare Inlet"
    obj_manifold.Shape = manifold_solid
    grp.addObject(obj_manifold)
    apply_material(obj_manifold, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 7. Twin Manifold Standoff Mounting Brackets (Laser-Cut Stainless)
    # --------------------------------------------------------------------------
    # Mounted from rear angle rail to hold manifold rail at exact standoff position
    standoffs = []
    for bx in [-CASSETTE_PITCH_X / 2.0 - 45.0, CASSETTE_PITCH_X / 2.0 + 45.0]:
        # Vertical riser plate
        b_plate = Part.makeBox(
            3.0,
            35.0,
            MANIFOLD_Z - rail_z + MANIFOLD_SIZE / 2.0 + 6.0,
            FreeCAD.Vector(bx - 1.5, CASSETTE_SPAN_Y / 2.0 + 5.0, rail_z)
        )
        # Clamp saddle around the 3/4" square rail
        b_saddle = Part.makeBox(
            12.0,
            MANIFOLD_SIZE + 6.0,
            MANIFOLD_SIZE + 6.0,
            FreeCAD.Vector(bx - 6.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0 - 3.0, MANIFOLD_Z - MANIFOLD_SIZE / 2.0 - 3.0)
        )
        b_hole = Part.makeBox(
            14.0,
            MANIFOLD_SIZE,
            MANIFOLD_SIZE,
            FreeCAD.Vector(bx - 7.0, MANIFOLD_Y - MANIFOLD_SIZE / 2.0, MANIFOLD_Z - MANIFOLD_SIZE / 2.0)
        )
        clamp = b_saddle.cut(b_hole)
        standoffs.append(b_plate.fuse(clamp))

    standoff_solid = standoffs[0].fuse(standoffs[1])
    obj_standoffs = doc.addObject("Part::Feature", f"{name}_Manifold_Standoffs")
    obj_standoffs.Label = "Precision Manifold Standoff Brackets (Laser-Cut 304 SS)"
    obj_standoffs.Shape = standoff_solid
    grp.addObject(obj_standoffs)
    apply_material(obj_standoffs, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 8. Calibrated Brass Hex Orifice Spuds (#60 Drill / 1/8" NPT)
    # --------------------------------------------------------------------------
    # Located at X = -CASSETTE_PITCH_X / 2.0 and +CASSETTE_PITCH_X / 2.0
    # Extending forward along -Y from manifold face toward venturi bellmouth horns
    spuds = []
    shutters = []

    for sx in [-CASSETTE_PITCH_X / 2.0, CASSETTE_PITCH_X / 2.0]:
        # Brass hex spud
        spud_y_start = MANIFOLD_Y - MANIFOLD_SIZE / 2.0
        s_hex = Part.makeCylinder(
            ORIFICE_HEX / 2.0,
            15.0,
            FreeCAD.Vector(sx, spud_y_start, MANIFOLD_Z),
            FreeCAD.Vector(0, -1, 0)
        )
        s_nozzle = Part.makeCone(
            4.5,
            2.5,
            ORIFICE_PROJ - 15.0,
            FreeCAD.Vector(sx, spud_y_start - 15.0, MANIFOLD_Z),
            FreeCAD.Vector(0, -1, 0)
        )
        spuds.append(s_hex.fuse(s_nozzle))

        # Rotatable Air Shutter Collar over venturi horn
        shutter_body = Part.makeCylinder(
            15.5,
            14.0,
            FreeCAD.Vector(sx, spud_y_start - ORIFICE_PROJ - AIR_GAP - 2.0, MANIFOLD_Z),
            FreeCAD.Vector(0, -1, 0)
        )
        shutter_slot = Part.makeBox(
            32.0,
            5.0,
            32.0,
            FreeCAD.Vector(sx - 16.0, spud_y_start - ORIFICE_PROJ - AIR_GAP - 10.0, MANIFOLD_Z - 16.0)
        )
        shutter_thumbscrew = Part.makeCylinder(
            3.0,
            8.0,
            FreeCAD.Vector(sx, spud_y_start - ORIFICE_PROJ - AIR_GAP - 8.0, MANIFOLD_Z + 15.0),
            FreeCAD.Vector(0, 0, 1)
        )
        shutters.append(shutter_body.cut(shutter_slot).fuse(shutter_thumbscrew))

    spud_shape = spuds[0].fuse(spuds[1])
    obj_spuds = doc.addObject("Part::Feature", f"{name}_Brass_Orifice_Spuds")
    obj_spuds.Label = "Dual Machined Brass Orifice Spuds (#60 Drill, 6mm Air Gap)"
    obj_spuds.Shape = spud_shape
    grp.addObject(obj_spuds)
    apply_material(obj_spuds, "Brass-C360")

    shutter_shape = shutters[0].fuse(shutters[1])
    obj_shutters = doc.addObject("Part::Feature", f"{name}_Air_Shutters")
    obj_shutters.Label = "Rotatable Air Shutter Collars with Locking Thumbscrews"
    obj_shutters.Shape = shutter_shape
    grp.addObject(obj_shutters)
    apply_material(obj_shutters, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 9. Silicone Spark Wire Boots & Thermocouple Safety Capillary Line
    # --------------------------------------------------------------------------
    # 90-degree silicone spark plug boots snapping onto the alumina electrodes
    boots = []
    leads = []
    for bx in [-CASSETTE_PITCH_X / 2.0 + 20.0, CASSETTE_PITCH_X / 2.0 - 20.0]:
        boot_vert = Part.makeCylinder(4.5, 18.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 8.0, 15.0), FreeCAD.Vector(0, 0, 1))
        boot_horiz = Part.makeCylinder(4.5, 20.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 8.0, 31.0), FreeCAD.Vector(0, 1, 0.2))
        boots.append(boot_vert.fuse(boot_horiz))
        # Flexible high-temp wire lead tracing back toward the manifold rail
        wire_lead = Part.makeCylinder(2.2, 120.0, FreeCAD.Vector(bx, -CASSETTE_SPAN_Y / 2.0 + 28.0, 35.0), FreeCAD.Vector(0, 1, 0.2))
        leads.append(wire_lead)

    # Copper thermocouple sensing bulb & capillary tube
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
