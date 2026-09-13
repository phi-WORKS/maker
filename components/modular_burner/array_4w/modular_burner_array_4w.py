"""
Road Roaster 4W Modular Ceramic Burner Array (40,000 BTU)
Standalone 3D Parametric CAD Assembly Module (Maker Component Library)

Optimized 4-cassette (2x2 grid) radiant thermal engine for the 4-wheel platform cart:
  1. 4x Modular Ceramic Infrared Burner Cassettes (10,000 BTU each, 40,000 BTU / 11.72 kW total)
  2. 232 sq in active radiant area (+34% larger than Solaronics K-30)
  3. Central Balanced Gas Distribution Manifold Rail (3/4" square) with 4 coaxial brass orifice spuds
  4. Symmetrical inward-facing venturis with exact 6mm primary air induction gaps
  5. Steatite ceramic thermal break isolators and polished 304 SS radiant heat shield baffle
  6. Orthogonal (+) stainless steel flame cross-lighting matrix linking all 4 quadrants
  7. Low-profile 5052 aluminum reflector cowl (90mm depth, 60% lower profile than Solaronics)
  8. Top primary air ventilation window showcasing the precision central gas distribution train
  9. Twin continuous 3/4" pivot axle hinge ears for 180° flip-back stowage onto 24" x 36" cart deck
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

# Burner Grid Geometry: 2 Columns along X, 2 Rows along Y
CASING_W = 180.0              # Deep-drawn plenum width across X
CASING_L = 230.0              # Deep-drawn plenum length along Y
GAP_X = 5.0                   # Thermal expansion gap between left and right columns
PITCH_X = CASING_W + GAP_X    # 185.0 mm center-to-center pitch along X
PITCH_Y = 250.0               # Center-to-center pitch along Y (front at -125mm, rear at +125mm)

# Active Radiant Dimensions: 2x 170mm width (340mm) x 2x 220mm length (440mm) = 232 sq in
ARRAY_WIDTH = 2 * CASING_W + GAP_X   # 365.0 mm active width
ARRAY_LENGTH = 2 * CASING_L + 20.0   # 480.0 mm active length

# Venturi & Gas Flow Coaxial Geometry
VENTURI_Z = 62.7              # Exact venturi centerline elevation
MANIFOLD_SIZE = 19.05         # 3/4 in square 6061-T6 aluminum rail
MANIFOLD_LEN = 380.0          # Manifold rail length across X
AIR_GAP = 6.0                 # Primary atmospheric air entrainment gap
ORIFICE_HEX = 11.0            # 7/16 in brass hex body
# Distance from manifold face (9.525mm) to venturi horn mouth (40.0mm) = 30.475mm
# Orifice length = 30.475 - AIR_GAP = 24.475 mm
ORIFICE_LEN = 24.475
ORIFICE_TIP_Y = 40.0 - AIR_GAP  # 34.0 mm

# Low-Profile Reflector Cowl (5052 Aluminum)
COWL_OUTER_W = 430.0          # Outer cowl width (fits within 24" cart deck)
COWL_OUTER_L = 550.0          # Outer cowl length (fits within 18" front stow zone)
COWL_DEPTH = 90.0             # Ultra low-profile depth (3.54 in vs Solaronics 8.75 in)
SKIRT_FLARE = 25.0            # Perimeter flare flange
SHEET_T = 1.6                 # 16-gauge (1.6 mm) aluminum sheet

# Transit Hinge Mounting Ears
PIVOT_AXLE_DIA = 19.05        # 3/4 in continuous pivot axle bore
PIVOT_EAR_PROJ = 55.0         # Rearward hinge ear projection along +Y
PIVOT_EAR_H = 45.0            # Hinge ear height above cowl roof


def create_modular_burner_array_4w_component(doc, name="Modular_Burner_Array_4W", placement=None):
    """
    Builds the complete 40,000 BTU 4-cassette (2x2 grid) modular burner array for Road Roaster 4W.
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Road Roaster 4W Modular Burner Array (40,000 BTU)"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Instantiate 4x Modular Ceramic Burner Cassettes (2x2 Grid)
    # --------------------------------------------------------------------------
    # Front row: Y = -PITCH_Y / 2 (-125mm), Rotated 180° so venturis point +Y toward Y = 0
    # Rear row:  Y = +PITCH_Y / 2 (+125mm), Rotated 0° so venturis point -Y toward Y = 0
    cassette_placements = [
        ("Cassette_1", -PITCH_X / 2.0, -PITCH_Y / 2.0, 180),  # Front Left
        ("Cassette_2",  PITCH_X / 2.0, -PITCH_Y / 2.0, 180),  # Front Right
        ("Cassette_3", -PITCH_X / 2.0,  PITCH_Y / 2.0,   0),  # Rear Left
        ("Cassette_4",  PITCH_X / 2.0,  PITCH_Y / 2.0,   0),  # Rear Right
    ]

    for cname, cx, cy, rot_z in cassette_placements:
        pos = FreeCAD.Vector(cx, cy, 0)
        rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), rot_z)
        c_part = create_modular_ceramic_burner_component(doc, name=f"{name}_{cname}", placement=FreeCAD.Placement(pos, rot), include_orifice=False)
        grp.addObject(c_part)

    # --------------------------------------------------------------------------
    # 2. Central Balanced Gas Distribution Manifold Rail & 3/8" Flare Inlet
    # --------------------------------------------------------------------------
    # Single transverse rail centered at Y = 0, Z = VENTURI_Z (62.7mm)
    rail_solid = Part.makeBox(
        MANIFOLD_LEN,
        MANIFOLD_SIZE,
        MANIFOLD_SIZE,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0, -MANIFOLD_SIZE / 2.0, VENTURI_Z - MANIFOLD_SIZE / 2.0)
    )
    # Gas supply inlet fitting (3/8" SAE flare) entering from the left end (-X)
    inlet_pipe = Part.makeCylinder(
        6.35,
        35.0,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0, 0, VENTURI_Z),
        FreeCAD.Vector(-1, 0, 0)
    )
    inlet_hex = Part.makeCylinder(
        9.5,
        14.0,
        FreeCAD.Vector(-MANIFOLD_LEN / 2.0 - 20.0, 0, VENTURI_Z),
        FreeCAD.Vector(-1, 0, 0)
    )
    manifold_solid = rail_solid.fuse(inlet_pipe).fuse(inlet_hex)

    obj_manifold = doc.addObject("Part::Feature", f"{name}_Central_Gas_Manifold")
    obj_manifold.Label = "Central Balanced Gas Distribution Manifold Rail (3/4in Aluminum)"
    obj_manifold.Shape = manifold_solid
    grp.addObject(obj_manifold)
    apply_material(obj_manifold, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 3. 4x Precision Brass Hex Orifice Spuds (#60 Drill, Coaxial Alignment)
    # --------------------------------------------------------------------------
    # 2 South-facing spuds at X = ±PITCH_X / 2 firing into front venturis
    # 2 North-facing spuds at X = ±PITCH_X / 2 firing into rear venturis
    spuds = []
    col_x_positions = [-PITCH_X / 2.0, PITCH_X / 2.0]

    for ox in col_x_positions:
        # South-facing orifice spud (projects along -Y)
        s_hex_s = Part.makeCylinder(ORIFICE_HEX / 2.0, 16.0, FreeCAD.Vector(ox, -MANIFOLD_SIZE / 2.0, VENTURI_Z), FreeCAD.Vector(0, -1, 0))
        s_nozzle_s = Part.makeCone(4.0, 2.5, ORIFICE_LEN - 16.0, FreeCAD.Vector(ox, -MANIFOLD_SIZE / 2.0 - 16.0, VENTURI_Z), FreeCAD.Vector(0, -1, 0))
        spuds.append(s_hex_s.fuse(s_nozzle_s))

        # North-facing orifice spud (projects along +Y)
        s_hex_n = Part.makeCylinder(ORIFICE_HEX / 2.0, 16.0, FreeCAD.Vector(ox, MANIFOLD_SIZE / 2.0, VENTURI_Z), FreeCAD.Vector(0, 1, 0))
        s_nozzle_n = Part.makeCone(4.0, 2.5, ORIFICE_LEN - 16.0, FreeCAD.Vector(ox, MANIFOLD_SIZE / 2.0 + 16.0, VENTURI_Z), FreeCAD.Vector(0, 1, 0))
        spuds.append(s_hex_n.fuse(s_nozzle_n))

    spud_shape = spuds[0]
    for sp in spuds[1:]:
        spud_shape = spud_shape.fuse(sp)

    obj_spuds = doc.addObject("Part::Feature", f"{name}_Brass_Orifices")
    obj_spuds.Label = "4x Machined Brass Hex Orifice Spuds (#60 Drill, 6mm Air Gap)"
    obj_spuds.Shape = spud_shape
    grp.addObject(obj_spuds)
    apply_material(obj_spuds, "Brass-C360")

    # --------------------------------------------------------------------------
    # 4. Manifold Standoff Brackets with Steatite Ceramic Thermal Break Isolators
    # --------------------------------------------------------------------------
    standoffs = []
    isolators = []
    rail_z = 22.7 - 3.175
    for bx in [-PITCH_X / 2.0 - 55.0, PITCH_X / 2.0 + 55.0]:
        iso = Part.makeCylinder(8.0, 3.0, FreeCAD.Vector(bx, -15.0, rail_z + 3.175), FreeCAD.Vector(0, 0, 1))
        isolators.append(iso)
        b_foot = Part.makeBox(16.0, 30.0, 3.0, FreeCAD.Vector(bx - 8.0, -15.0, rail_z + 6.175))
        b_upright = Part.makeBox(3.0, 16.0, VENTURI_Z - rail_z + MANIFOLD_SIZE / 2.0 + 5.0, FreeCAD.Vector(bx - 1.5, -8.0, rail_z + 6.175))
        b_clamp = Part.makeBox(16.0, MANIFOLD_SIZE + 6.0, MANIFOLD_SIZE + 6.0, FreeCAD.Vector(bx - 8.0, -MANIFOLD_SIZE / 2.0 - 3.0, VENTURI_Z - MANIFOLD_SIZE / 2.0 - 3.0))
        b_hole = Part.makeBox(18.0, MANIFOLD_SIZE, MANIFOLD_SIZE, FreeCAD.Vector(bx - 9.0, -MANIFOLD_SIZE / 2.0, VENTURI_Z - MANIFOLD_SIZE / 2.0))
        standoffs.append(b_foot.fuse(b_upright).fuse(b_clamp.cut(b_hole)))

    obj_standoffs = doc.addObject("Part::Feature", f"{name}_Manifold_Standoffs")
    obj_standoffs.Label = "304 SS Central Manifold Standoff Brackets"
    obj_standoffs.Shape = standoffs[0].fuse(standoffs[1])
    grp.addObject(obj_standoffs)
    apply_material(obj_standoffs, "Steel-304Stainless")

    obj_iso = doc.addObject("Part::Feature", f"{name}_Thermal_Isolators")
    obj_iso.Label = "Steatite Ceramic Thermal Break Isolator Washers"
    obj_iso.Shape = isolators[0].fuse(isolators[1])
    grp.addObject(obj_iso)
    apply_material(obj_iso, "Ceramic-Cordierite")

    # --------------------------------------------------------------------------
    # 5. Polished 304 SS Radiant Heat Shield Baffle Plate
    # --------------------------------------------------------------------------
    # Horizontal deflector plate positioned between plenum tops and the central gas rail
    baffle_box = Part.makeBox(360.0, 70.0, 1.2, FreeCAD.Vector(-180.0, -35.0, 48.0))
    obj_baffle = doc.addObject("Part::Feature", f"{name}_Radiant_Baffle")
    obj_baffle.Label = "Polished 304 SS Central Radiant Heat Shield Baffle Plate"
    obj_baffle.Shape = baffle_box
    grp.addObject(obj_baffle)
    apply_material(obj_baffle, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 6. Orthogonal (+) Stainless Steel Flame Cross-Lighting Matrix
    # --------------------------------------------------------------------------
    # Center X channel linking left and right pairs
    cx_bar = Part.makeBox(ARRAY_WIDTH - 20.0, 20.0, 8.0, FreeCAD.Vector(-(ARRAY_WIDTH - 20.0) / 2.0, -10.0, -2.0))
    # Center Y channel linking front and rear pairs
    cy_bar = Part.makeBox(20.0, ARRAY_LENGTH - 40.0, 8.0, FreeCAD.Vector(-10.0, -(ARRAY_LENGTH - 40.0) / 2.0, -2.0))
    cross_channels = cx_bar.fuse(cy_bar)

    obj_cross = doc.addObject("Part::Feature", f"{name}_Flame_Cross_Matrix")
    obj_cross.Label = "Orthogonal 304 SS Flame Cross-Lighting Cruciform Matrix"
    obj_cross.Shape = cross_channels
    grp.addObject(obj_cross)
    apply_material(obj_cross, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 7. Low-Profile Reflector Cowl with Central Primary Air Window (5052 Aluminum)
    # --------------------------------------------------------------------------
    cowl_top_w = ARRAY_WIDTH + 20.0
    cowl_top_l = ARRAY_LENGTH + 30.0
    cowl_rim_w = COWL_OUTER_W
    cowl_rim_l = COWL_OUTER_L

    # Roof plate with central chimney cutout over the manifold and air induction zone
    roof_plate = Part.makeBox(cowl_top_w, cowl_top_l, SHEET_T, FreeCAD.Vector(-cowl_top_w / 2.0, -cowl_top_l / 2.0, COWL_DEPTH))
    vent_window = Part.makeBox(280.0, 85.0, SHEET_T + 4.0, FreeCAD.Vector(-140.0, -42.5, COWL_DEPTH - 2.0))
    roof_plate = roof_plate.cut(vent_window)

    # Sloping skirt walls
    skirt_outer = Part.makeBox(cowl_rim_w, cowl_rim_l, COWL_DEPTH, FreeCAD.Vector(-cowl_rim_w / 2.0, -cowl_rim_l / 2.0, 0))
    skirt_inner = Part.makeBox(cowl_rim_w - 2 * SHEET_T, cowl_rim_l - 2 * SHEET_T, COWL_DEPTH + 10.0, FreeCAD.Vector(-cowl_rim_w / 2.0 + SHEET_T, -cowl_rim_l / 2.0 + SHEET_T, -5.0))
    cowl_skirt = skirt_outer.cut(skirt_inner)

    # Perimeter 30-degree flare flange
    flare_lip_w = cowl_rim_w + 2 * SKIRT_FLARE
    flare_lip_l = cowl_rim_l + 2 * SKIRT_FLARE
    flare_outer = Part.makeBox(flare_lip_w, flare_lip_l, SHEET_T, FreeCAD.Vector(-flare_lip_w / 2.0, -flare_lip_l / 2.0, 0))
    flare_inner = Part.makeBox(cowl_rim_w - 10.0, cowl_rim_l - 10.0, SHEET_T + 2.0, FreeCAD.Vector(-(cowl_rim_w - 10.0) / 2.0, -(cowl_rim_l - 10.0) / 2.0, -1.0))
    cowl_flare = flare_outer.cut(flare_inner)

    cowl_solid = roof_plate.fuse(cowl_skirt).fuse(cowl_flare)
    obj_cowl = doc.addObject("Part::Feature", f"{name}_Reflector_Cowl")
    obj_cowl.Label = "Low-Profile 5052 Aluminum Reflector Cowl (90mm Depth)"
    obj_cowl.Shape = cowl_solid
    grp.addObject(obj_cowl)
    apply_material(obj_cowl, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 8. Twin Continuous 3/4" Pivot Axle Hinge Ears (180° Flip-Back Mount)
    # --------------------------------------------------------------------------
    ears = []
    rear_cowl_edge_y = cowl_top_l / 2.0
    for ex in [-120.0, 120.0]:
        ear_body = Part.makeBox(
            8.0,
            PIVOT_EAR_PROJ,
            PIVOT_EAR_H,
            FreeCAD.Vector(ex - 4.0, rear_cowl_edge_y - 15.0, COWL_DEPTH - 10.0)
        )
        axle_hole = Part.makeCylinder(
            PIVOT_AXLE_DIA / 2.0 + 0.5,
            16.0,
            FreeCAD.Vector(ex - 8.0, rear_cowl_edge_y + PIVOT_EAR_PROJ - 22.0, COWL_DEPTH + PIVOT_EAR_H - 18.0),
            FreeCAD.Vector(1, 0, 0)
        )
        ears.append(ear_body.cut(axle_hole))

    hinge_solid = ears[0].fuse(ears[1])
    obj_hinge = doc.addObject("Part::Feature", f"{name}_Transit_Hinge_Ears")
    obj_hinge.Label = "Twin 3/4in Continuous Pivot Axle Hinge Ears (180-deg Flip-Back Mount)"
    obj_hinge.Shape = hinge_solid
    grp.addObject(obj_hinge)
    apply_material(obj_hinge, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 9. Pulse Spark Ignition Leads & Thermocouple Safety Harness
    # --------------------------------------------------------------------------
    leads = []
    for sx, sy in [(-PITCH_X / 2.0 + 20.0, -PITCH_Y / 2.0), (PITCH_X / 2.0 - 20.0, -PITCH_Y / 2.0),
                   (-PITCH_X / 2.0 + 20.0,  PITCH_Y / 2.0), (PITCH_X / 2.0 - 20.0,  PITCH_Y / 2.0)]:
        boot = Part.makeCylinder(4.5, 18.0, FreeCAD.Vector(sx, sy - 8.0, 15.0), FreeCAD.Vector(0, 0, 1))
        wire = Part.makeCylinder(2.0, 60.0, FreeCAD.Vector(sx, sy - 8.0, 31.0), FreeCAD.Vector(0, 1 if sy < 0 else -1, 0.4))
        leads.append(boot.fuse(wire))

    tc_lead = Part.makeCylinder(2.2, 120.0, FreeCAD.Vector(-PITCH_X / 2.0 - 20.0, -PITCH_Y / 2.0 + 30.0, 8.0), FreeCAD.Vector(0, 1, 0.3))
    safety_solid = leads[0].fuse(leads[1]).fuse(leads[2]).fuse(leads[3]).fuse(tc_lead)

    obj_safety = doc.addObject("Part::Feature", f"{name}_Ignition_Safety_Train")
    obj_safety.Label = "4-Port Spark Ignition Leads & Thermocouple Safety Line"
    obj_safety.Shape = safety_solid
    grp.addObject(obj_safety)
    apply_material(obj_safety, "Ceramic-Alumina")

    return grp


if __name__ == "__main__":
    doc = FreeCAD.newDocument("TestBurnerArray4W")
    create_modular_burner_array_4w_component(doc)
    doc.recompute()
    print("Burner Array 4W build complete. Objects:", len(doc.Objects))
