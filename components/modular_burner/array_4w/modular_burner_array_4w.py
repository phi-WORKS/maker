"""
Road Roaster 4W Modular Ceramic Burner Array Component
Standalone 3D Parametric CAD Module (Maker Component Library)

Engineered for the Road Roaster 4-Wheel Commercial Platform Cart:
  - 4x 10,000 BTU modular ceramic cassettes in a 2x2 grid (40,000 BTU/hr total)
  - Active radiant surface: 232 sq in (34% larger than Solaronics K-30)
  - H-pattern dual gas distribution manifold rail with 3/8" flare inlet
  - Orthogonal stainless steel flame cross-lighting channel matrix
  - 4-outlet electronic pulse spark wire harness
  - Thermoelectric safety thermocouple sensor and valve mounting pad
  - Low-profile 5052 aluminum reflector cowl (90 mm profile, 30° flared skirt)
  - Heavy-duty 3/4" (19.05 mm) pivot axle hinge ears for 180° deck flip-back transit
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
# PARAMETRIC ENGINEERING DIMENSIONS (4W 2x2 GRID ARRAY)
# ==============================================================================

# 2x2 Grid Pitch: 2 Cassettes along X (220mm each) and 2 along Y (170mm each)
GRID_PITCH_X = 226.0          # Center-to-center pitch along X
GRID_PITCH_Y = 176.0          # Center-to-center pitch along Y

# Active Radiant Area: ~440 mm x 340 mm (17.32 in x 13.39 in = 232 sq in)
ARRAY_WIDTH = 452.0
ARRAY_LENGTH = 352.0

# Low-Profile Reflector Cowl (5052 Aluminum)
COWL_OUTER_W = 520.0          # 20.47 in width (fits cleanly within 24" cart deck)
COWL_OUTER_L = 420.0          # 16.54 in length (fits inside 18" front stow zone)
COWL_DEPTH = 90.0             # Ultra low-profile depth (3.54 in vs Solaronics 8.75 in)
SKIRT_FLARE = 30.0            # 30-degree perimeter flare flange
SHEET_T = 1.6                 # 16-gauge (1.6 mm) aluminum sheet

# Gas Manifold (H-pattern 3/4" square rail)
MANIFOLD_SIZE = 19.05         # 3/4 in square tubing
PIVOT_AXLE_DIA = 19.05        # 3/4 in (19.05 mm) continuous pivot axle bore
PIVOT_EAR_PROJ = 60.0         # Rearward hinge ear projection along +Y
PIVOT_EAR_H = 45.0            # Hinge ear height above cowl roof


def create_modular_burner_array_4w_component(doc, name="Modular_Burner_Array_4W", placement=None):
    """
    Builds the 40,000 BTU 4-cassette (2x2 grid) modular burner array assembly for Road Roaster 4W.
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Road Roaster 4W Modular Burner Array (40,000 BTU)"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Instantiate 4x Modular Ceramic Burner Cassettes (2x2 Grid)
    # --------------------------------------------------------------------------
    # Rows along Y: Front row at -GRID_PITCH_Y / 2, Rear row at +GRID_PITCH_Y / 2
    # Columns along X: Left col at -GRID_PITCH_X / 2, Right col at +GRID_PITCH_X / 2
    cassette_coords = [
        (-GRID_PITCH_X / 2.0, -GRID_PITCH_Y / 2.0, 0),  # Cassette 1 (Front Left)
        ( GRID_PITCH_X / 2.0, -GRID_PITCH_Y / 2.0, 0),  # Cassette 2 (Front Right)
        (-GRID_PITCH_X / 2.0,  GRID_PITCH_Y / 2.0, 0),  # Cassette 3 (Rear Left)
        ( GRID_PITCH_X / 2.0,  GRID_PITCH_Y / 2.0, 0),  # Cassette 4 (Rear Right)
    ]

    for i, (cx, cy, cz) in enumerate(cassette_coords, start=1):
        # Front row venturis point -Y, Rear row venturis point +Y (meeting at center manifold)
        if cy < 0:
            rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
        else:
            rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180)

        c_pos = FreeCAD.Vector(cx, cy, cz)
        c_placement = FreeCAD.Placement(c_pos, rot)
        c_part = create_modular_ceramic_burner_component(doc, name=f"{name}_Cassette_{i}", placement=c_placement)
        grp.addObject(c_part)

    # --------------------------------------------------------------------------
    # 2. Orthogonal (+) Stainless Flame Cross-Lighting Channels
    # --------------------------------------------------------------------------
    # Center X channel between front and rear pairs
    cx_bar = Part.makeBox(ARRAY_WIDTH - 20.0, 18.0, 8.0, FreeCAD.Vector(-(ARRAY_WIDTH - 20.0) / 2.0, -9.0, -2.0))
    # Center Y channel between left and right pairs
    cy_bar = Part.makeBox(18.0, ARRAY_LENGTH - 20.0, 8.0, FreeCAD.Vector(-9.0, -(ARRAY_LENGTH - 20.0) / 2.0, -2.0))
    cross_channels = cx_bar.fuse(cy_bar)

    obj_cross = doc.addObject("Part::Feature", f"{name}_Flame_Cross_Channels")
    obj_cross.Label = "Orthogonal Stainless Steel Flame Cross-Lighting Matrix"
    obj_cross.Shape = cross_channels
    grp.addObject(obj_cross)
    apply_material(obj_cross, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 3. H-Pattern Gas Distribution Manifold Rail
    # --------------------------------------------------------------------------
    # Center longitudinal runner along Y at X = 0, connecting to two lateral feeder rails
    center_rail = Part.makeBox(
        MANIFOLD_SIZE,
        GRID_PITCH_Y + 40.0,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-MANIFOLD_SIZE / 2.0, -(GRID_PITCH_Y + 40.0) / 2.0, COWL_DEPTH - 20.0)
    )
    front_feeder = Part.makeBox(
        ARRAY_WIDTH - 40.0,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-(ARRAY_WIDTH - 40.0) / 2.0, -GRID_PITCH_Y / 2.0 - 20.0, COWL_DEPTH - 20.0)
    )
    rear_feeder = Part.makeBox(
        ARRAY_WIDTH - 40.0,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-(ARRAY_WIDTH - 40.0) / 2.0, GRID_PITCH_Y / 2.0 + 20.0 - MANIFOLD_SIZE, COWL_DEPTH - 20.0)
    )
    # Gas inlet fitting with 3/8" flare connection
    inlet_pipe = Part.makeCylinder(
        6.35,
        35.0,
        FreeCAD.Vector(0, (GRID_PITCH_Y + 40.0) / 2.0, COWL_DEPTH - 20.0 + MANIFOLD_SIZE / 2.0),
        FreeCAD.Vector(0, 1, 0)
    )
    manifold_solid = center_rail.fuse(front_feeder).fuse(rear_feeder).fuse(inlet_pipe)

    obj_manifold = doc.addObject("Part::Feature", f"{name}_H_Gas_Manifold")
    obj_manifold.Label = "H-Pattern Balanced Gas Distribution Manifold Rail"
    obj_manifold.Shape = manifold_solid
    grp.addObject(obj_manifold)
    apply_material(obj_manifold, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 4. Low-Profile 5052 Aluminum Reflector Cowl
    # --------------------------------------------------------------------------
    cowl_top_w = ARRAY_WIDTH + 20.0
    cowl_top_l = ARRAY_LENGTH + 20.0
    cowl_rim_w = COWL_OUTER_W
    cowl_rim_l = COWL_OUTER_L

    # Roof plate
    roof_plate = Part.makeBox(
        cowl_top_w,
        cowl_top_l,
        SHEET_T,
        FreeCAD.Vector(-cowl_top_w / 2.0, -cowl_top_l / 2.0, COWL_DEPTH)
    )
    # Sloping skirt walls
    skirt_outer = Part.makeBox(
        cowl_rim_w,
        cowl_rim_l,
        COWL_DEPTH,
        FreeCAD.Vector(-cowl_rim_w / 2.0, -cowl_rim_l / 2.0, 0)
    )
    skirt_inner = Part.makeBox(
        cowl_rim_w - 2 * SHEET_T,
        cowl_rim_l - 2 * SHEET_T,
        COWL_DEPTH + 10.0,
        FreeCAD.Vector(-cowl_rim_w / 2.0 + SHEET_T, -cowl_rim_l / 2.0 + SHEET_T, -5.0)
    )
    cowl_skirt = skirt_outer.cut(skirt_inner)

    # Perimeter 30-degree flare flange
    flare_w = cowl_rim_w + 2 * SKIRT_FLARE
    flare_l = cowl_rim_l + 2 * SKIRT_FLARE
    flare_outer = Part.makeBox(
        flare_w,
        flare_l,
        SHEET_T,
        FreeCAD.Vector(-flare_w / 2.0, -flare_l / 2.0, 0)
    )
    flare_inner = Part.makeBox(
        cowl_rim_w,
        cowl_rim_l,
        SHEET_T + 2.0,
        FreeCAD.Vector(-cowl_rim_w / 2.0, -cowl_rim_l / 2.0, -1.0)
    )
    flare_flange = flare_outer.cut(flare_inner)

    cowl_body = roof_plate.fuse(cowl_skirt).fuse(flare_flange)

    obj_cowl = doc.addObject("Part::Feature", f"{name}_Reflector_Cowl")
    obj_cowl.Label = "Low-Profile 5052 Aluminum Reflector Cowl (90mm Profile)"
    obj_cowl.Shape = cowl_body
    grp.addObject(obj_cowl)
    apply_material(obj_cowl, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 5. Continuous Pivot Axle Hinge Ears (180° Flip-Back Hinge)
    # --------------------------------------------------------------------------
    # Twin 3/16" steel hinge brackets on rear skirt (+Y)
    hinge_ears = []
    for hx in [-COWL_OUTER_W / 4.0, COWL_OUTER_W / 4.0]:
        h_plate = Part.makeBox(
            6.0,
            PIVOT_EAR_PROJ,
            PIVOT_EAR_H,
            FreeCAD.Vector(hx - 3.0, COWL_OUTER_L / 2.0 - 10.0, COWL_DEPTH - 15.0)
        )
        # Axle bore hole for 3/4" continuous axle shaft
        h_hole = Part.makeCylinder(
            PIVOT_AXLE_DIA / 2.0 + 0.5,
            12.0,
            FreeCAD.Vector(hx - 6.0, COWL_OUTER_L / 2.0 + PIVOT_EAR_PROJ - 20.0, COWL_DEPTH + 15.0),
            FreeCAD.Vector(1, 0, 0)
        )
        h_ear = h_plate.cut(h_hole)
        hinge_ears.append(h_ear)

    hinge_solid = hinge_ears[0].fuse(hinge_ears[1])
    obj_hinge = doc.addObject("Part::Feature", f"{name}_Transit_Hinge_Ears")
    obj_hinge.Label = "Twin 3/4in Pivot Axle Hinge Ears (180-deg Flip-Back Mount)"
    obj_hinge.Shape = hinge_solid
    grp.addObject(obj_hinge)
    apply_material(obj_hinge, "Steel-A36")

    # --------------------------------------------------------------------------
    # 6. 4-Port Spark Wire Harness & Thermoelectric Safety Sensor
    # --------------------------------------------------------------------------
    spark_wires = []
    for cx, cy, _ in cassette_coords:
        s_lead = Part.makeCylinder(
            2.2,
            55.0,
            FreeCAD.Vector(cx, cy, COWL_DEPTH - 15.0),
            FreeCAD.Vector(0, 0, -1)
        )
        spark_wires.append(s_lead)

    # Thermocouple sensing lead from Burner 1 to rear valve mounting pad
    tc_lead = Part.makeCylinder(
        2.0,
        180.0,
        FreeCAD.Vector(-GRID_PITCH_X / 2.0, -GRID_PITCH_Y / 2.0, COWL_DEPTH - 10.0),
        FreeCAD.Vector(0, 1, 0.1)
    )
    # Brass safety valve mounting pad
    valve_pad = Part.makeBox(
        35.0,
        35.0,
        25.0,
        FreeCAD.Vector(-17.5, COWL_OUTER_L / 2.0 - 35.0, COWL_DEPTH + 2.0)
    )

    elec_solid = spark_wires[0].fuse(spark_wires[1]).fuse(spark_wires[2]).fuse(spark_wires[3]).fuse(tc_lead).fuse(valve_pad)

    obj_elec = doc.addObject("Part::Feature", f"{name}_Ignition_Safety_Train")
    obj_elec.Label = "4-Port Spark Ignition Leads, Thermocouple & Safety Valve Pad"
    obj_elec.Shape = elec_solid
    grp.addObject(obj_elec)
    apply_material(obj_elec, "Brass-C360")

    return grp


if __name__ == "__main__":
    doc = FreeCAD.newDocument("TestBurnerArray4W")
    create_modular_burner_array_4w_component(doc)
    doc.recompute()
    print("Test 4W Array build complete. Objects:", len(doc.Objects))
