"""
Road Roaster 2W Modular Ceramic Burner Array Component
Standalone 3D Parametric CAD Module (Maker Component Library)

Engineered for the Road Roaster 2-Wheel Hand Truck Chassis:
  - Dual 10,000 BTU modular ceramic cassettes (20,000 BTU/hr total)
  - Common 3/4" square gas distribution manifold rail
  - Precision brass orifice spuds (#60 drill @ 11 in W.C. LP)
  - Perforated stainless steel flame crossover channel
  - Dual-lead electronic pulse spark wire harness
  - Thermoelectric safety thermocouple probe and lead
  - Low-profile 5052 aluminum reflector cowl (85 mm depth) with 30° flared skirt
  - Flat bar skid runners with 30° ski tips and suspension bridge brackets
"""

import os
import sys
import math
import FreeCAD
import Part

from phi_works.maker.materials import apply_material

# Import modular ceramic burner generator
script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
components_dir = os.path.abspath(os.path.join(script_dir, ".."))
if components_dir not in sys.path:
    sys.path.insert(0, components_dir)

from cassette.modular_ceramic_burner import create_modular_ceramic_burner_component

# ==============================================================================
# PARAMETRIC ENGINEERING DIMENSIONS (2W DUAL-ARRAY)
# ==============================================================================

# Array Layout: 2 Cassettes Side-by-Side along X
CASSETTE_PITCH_X = 175.0      # Center-to-center spacing along X
ARRAY_WIDTH = 355.0           # Active array width across X (13.98 in)
ARRAY_LENGTH = 230.0          # Active array length along Y (9.06 in)

# Low-Profile Reflector Cowl (5052 Aluminum)
COWL_OUTER_W = 380.0          # Outer cowl width (14.96 in - fits 15" hand truck sled)
COWL_OUTER_L = 320.0          # Outer cowl length (12.60 in)
COWL_DEPTH = 85.0             # Ultra low-profile depth (3.35 in vs Solaronics 8.75 in)
SKIRT_FLARE = 25.0            # 30-degree perimeter flare flange
SHEET_T = 1.6                 # 16-gauge (1.6 mm) aluminum sheet

# Gas Distribution Manifold Rail
MANIFOLD_SIZE = 19.05         # 3/4 in square tubing
MANIFOLD_LEN = 360.0          # Manifold rail length across X
FEED_INLET_R = 6.35           # 3/8 in flare inlet fitting radius

# Skid Runners
SKID_W = 25.4                 # 1.0 in flat bar width
SKID_T = 4.76                 # 3/16 in flat bar thickness
SKID_L = 360.0                # Total runner length


def create_modular_burner_array_2w_component(doc, name="Modular_Burner_Array_2W", placement=None):
    """
    Builds the 20,000 BTU dual-cassette modular burner array assembly for Road Roaster 2W.
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Road Roaster 2W Modular Burner Array (20,000 BTU)"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Instantiate 2x Modular Ceramic Burner Cassettes
    # --------------------------------------------------------------------------
    # Cassettes are rotated 90 deg so the 170 mm dimension is along X and 220 mm is along Y
    # Venturis point in the -Y direction toward the manifold rail
    rot_cassette = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 90)

    for i, offset_x in enumerate([-CASSETTE_PITCH_X / 2.0, CASSETTE_PITCH_X / 2.0], start=1):
        pos = FreeCAD.Vector(offset_x, 0, 0)
        c_placement = FreeCAD.Placement(pos, rot_cassette)
        c_part = create_modular_ceramic_burner_component(doc, name=f"{name}_Cassette_{i}", placement=c_placement)
        grp.addObject(c_part)

    # --------------------------------------------------------------------------
    # 2. Flame Crossover Channel Bridge (Stainless Steel)
    # --------------------------------------------------------------------------
    # Spans the gap between the two plaques at X = 0, Y from -90 to +90
    bridge_w = 20.0
    bridge_l = 180.0
    bridge_box = Part.makeBox(
        bridge_w,
        bridge_l,
        8.0,
        FreeCAD.Vector(-bridge_w / 2.0, -bridge_l / 2.0, -2.0)
    )
    # Perforated hollow flame propagation tunnel
    bridge_inner = Part.makeBox(
        bridge_w - 2.0,
        bridge_l - 2.0,
        7.0,
        FreeCAD.Vector(-bridge_w / 2.0 + 1.0, -bridge_l / 2.0 + 1.0, -2.5)
    )
    bridge_shell = bridge_box.cut(bridge_inner)

    obj_bridge = doc.addObject("Part::Feature", f"{name}_Flame_Crossover")
    obj_bridge.Label = "Perforated Stainless Flame Crossover Channel Bridge"
    obj_bridge.Shape = bridge_shell
    grp.addObject(obj_bridge)
    apply_material(obj_bridge, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 3. Gas Distribution Manifold Rail & Brass Feed Spuds
    # --------------------------------------------------------------------------
    # 3/4" square rail mounted horizontally along X at Y = -95.0, Z = 50.0
    manifold_y = -95.0
    manifold_z = 52.0

    rail_box = Part.makeBox(
        MANIFOLD_LEN,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0, manifold_y - MANIFOLD_SIZE / 2.0, manifold_z - MANIFOLD_SIZE / 2.0)
    )
    # Central gas supply inlet fitting (3/8" flare)
    inlet_pipe = Part.makeCylinder(
        FEED_INLET_R,
        28.0,
        FreeCAD.Vector(0, manifold_y - MANIFOLD_SIZE / 2.0 - 28.0, manifold_z),
        FreeCAD.Vector(0, 1, 0)
    )
    inlet_hex = Part.makeCylinder(
        8.0,
        10.0,
        FreeCAD.Vector(0, manifold_y - MANIFOLD_SIZE / 2.0 - 15.0, manifold_z),
        FreeCAD.Vector(0, 1, 0)
    )
    manifold_solid = rail_box.fuse(inlet_pipe).fuse(inlet_hex)

    obj_manifold = doc.addObject("Part::Feature", f"{name}_Gas_Manifold")
    obj_manifold.Label = "3/4in Gas Distribution Manifold Rail & Inlet Fitting"
    obj_manifold.Shape = manifold_solid
    grp.addObject(obj_manifold)
    apply_material(obj_manifold, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 4. Low-Profile Reflector Cowl (5052 Aluminum Sheet)
    # --------------------------------------------------------------------------
    # Outer sloping reflector cowl with flared perimeter skirt
    cowl_top_w = ARRAY_WIDTH + 15.0
    cowl_top_l = ARRAY_LENGTH + 45.0
    cowl_rim_w = COWL_OUTER_W
    cowl_rim_l = COWL_OUTER_L

    # Outer roof plate
    roof_plate = Part.makeBox(
        cowl_top_w,
        cowl_top_l,
        SHEET_T,
        FreeCAD.Vector(-cowl_top_w / 2.0, -cowl_top_l / 2.0 + 15.0, COWL_DEPTH)
    )
    # Outer flared skirt walls
    skirt_outer = Part.makeBox(
        cowl_rim_w,
        cowl_rim_l,
        COWL_DEPTH,
        FreeCAD.Vector(-cowl_rim_w / 2.0, -cowl_rim_l / 2.0 + 15.0, 0)
    )
    skirt_inner = Part.makeBox(
        cowl_rim_w - 2 * SHEET_T,
        cowl_rim_l - 2 * SHEET_T,
        COWL_DEPTH + 10.0,
        FreeCAD.Vector(-cowl_rim_w / 2.0 + SHEET_T, -cowl_rim_l / 2.0 + 15.0 + SHEET_T, -5.0)
    )
    cowl_skirt = skirt_outer.cut(skirt_inner)

    # Perimeter 30-degree flare flange
    flare_lip_w = cowl_rim_w + 2 * SKIRT_FLARE
    flare_lip_l = cowl_rim_l + 2 * SKIRT_FLARE
    flare_outer = Part.makeBox(
        flare_lip_w,
        flare_lip_l,
        SHEET_T,
        FreeCAD.Vector(-flare_lip_w / 2.0, -flare_lip_l / 2.0 + 15.0, 0)
    )
    flare_inner = Part.makeBox(
        cowl_rim_w,
        cowl_rim_l,
        SHEET_T + 2.0,
        FreeCAD.Vector(-cowl_rim_w / 2.0, -cowl_rim_l / 2.0 + 15.0, -1.0)
    )
    flare_flange = flare_outer.cut(flare_inner)

    cowl_body = roof_plate.fuse(cowl_skirt).fuse(flare_flange)

    obj_cowl = doc.addObject("Part::Feature", f"{name}_Reflector_Cowl")
    obj_cowl.Label = "Low-Profile 5052 Aluminum Reflector Cowl (85mm Profile)"
    obj_cowl.Shape = cowl_body
    grp.addObject(obj_cowl)
    apply_material(obj_cowl, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 5. Skid Runners & Suspension Mount Brackets (Steel A36)
    # --------------------------------------------------------------------------
    skids = []
    for sx in [-COWL_OUTER_W / 2.0 - SKID_W, COWL_OUTER_W / 2.0]:
        # Horizontal runner
        bar = Part.makeBox(
            SKID_W,
            SKID_L,
            SKID_T,
            FreeCAD.Vector(sx, -SKID_L / 2.0 + 15.0, -SKID_T)
        )
        # 30-degree front ski tip
        tip = Part.makeBox(
            SKID_W,
            50.0,
            SKID_T,
            FreeCAD.Vector(sx, SKID_L / 2.0 + 15.0, -SKID_T)
        )
        tip.rotate(FreeCAD.Vector(sx, SKID_L / 2.0 + 15.0, 0), FreeCAD.Vector(1, 0, 0), -25)
        # Suspension upright bracket ear
        ear = Part.makeBox(
            SKID_T,
            45.0,
            50.0,
            FreeCAD.Vector(sx + (SKID_W - SKID_T) / 2.0, -10.0, 0)
        )
        skids.append(bar.fuse(tip).fuse(ear))

    skid_shape = skids[0].fuse(skids[1])
    obj_skids = doc.addObject("Part::Feature", f"{name}_Skid_Runners")
    obj_skids.Label = "Ground Flat Bar Skid Runners & Swing-Arm Mounting Ears"
    obj_skids.Shape = skid_shape
    grp.addObject(obj_skids)
    apply_material(obj_skids, "Steel-A36")

    # --------------------------------------------------------------------------
    # 6. Ignition Wire Harness & Thermocouple Sensor Lead
    # --------------------------------------------------------------------------
    # High voltage pulse spark leads from manifold rail to each electrode
    spark_wires = []
    for sx in [-CASSETTE_PITCH_X / 2.0 + 10.0, CASSETTE_PITCH_X / 2.0 - 10.0]:
        w_lead = Part.makeCylinder(2.2, 75.0, FreeCAD.Vector(sx, manifold_y, manifold_z + 10.0), FreeCAD.Vector(0, 1, -0.4))
        spark_wires.append(w_lead)

    # Copper thermocouple tube running from Burner 1 along the manifold rail
    tc_tube = Part.makeCylinder(1.8, 140.0, FreeCAD.Vector(-CASSETTE_PITCH_X / 2.0 - 20.0, manifold_y + 10.0, 25.0), FreeCAD.Vector(1, 0, 0.2))

    harness_shape = spark_wires[0].fuse(spark_wires[1]).fuse(tc_tube)
    obj_harness = doc.addObject("Part::Feature", f"{name}_Ignition_Safety_Harness")
    obj_harness.Label = "Dual Spark High-Voltage Leads & Thermocouple Safety Conduit"
    obj_harness.Shape = harness_shape
    grp.addObject(obj_harness)
    apply_material(obj_harness, "Ceramic-Alumina")

    return grp


if __name__ == "__main__":
    doc = FreeCAD.newDocument("TestBurnerArray2W")
    create_modular_burner_array_2w_component(doc)
    doc.recompute()
    print("Test 2W Array build complete. Objects:", len(doc.Objects))
