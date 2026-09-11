"""
Modular Commodity Ceramic Infrared Burner Cassette Component
Standalone 3D Parametric CAD Module (Maker Component Library)

Models a standard mass-market commodity infrared ceramic plaque cassette
(standard HD220 format: 220 mm x 170 mm x 60 mm, nominal 10,000 BTU/hr @ 11 in W.C. LP).

Engineered for modular array assembly:
  - Cordierite honeycomb micro-pore ceramic radiant tile (1,600°F - 1,800°F)
  - 304 Stainless steel protective wire mesh face screen
  - Deep-drawn 304 SS / aluminized combustion plenum chamber
  - Atmospheric pre-mix venturi tube with adjustable primary air shutter
  - Precision brass hex orifice spud (#60 drill = 0.040 in / 1.016 mm)
  - Alumina ceramic spark ignition electrode and thermocouple mounting clip
  - Quick-swap slotted perimeter mounting tabs with knurled brass thumb nuts
"""

import os
import sys
import math
import FreeCAD
import Part

from phi_works.maker.materials import apply_material

# ==============================================================================
# PARAMETRIC ENGINEERING DIMENSIONS (HD220 FORMAT)
# ==============================================================================

# 1. Ceramic Plaque Dimensions (Nominal 10,000 BTU/hr / 2.93 kW)
TILE_W = 200.0               # Active radiant width across X (7.87 in)
TILE_L = 145.0               # Active radiant length along Y (5.71 in)
TILE_T = 12.7                # Standard cordierite tile thickness (0.50 in)

# 2. Plenum Housing & Flanges (304 Stainless Steel)
CASING_W = 220.0             # Overall cassette body width (8.66 in)
CASING_L = 170.0             # Overall cassette body length (6.69 in)
PLENUM_DEPTH = 38.0          # Plenum chamber depth (1.50 in)
CASING_T = 1.2               # 18-gauge sheet thickness
BEZEL_LIP = 8.0              # Tile retention bezel overlap width

# 3. Quick-Swap Mounting Tabs (For M5 studs on array frame)
TAB_PROJ = 12.0              # Projection beyond casing width
TAB_L = 35.0                 # Tab length along Y
TAB_SLOT_W = 5.5             # Slot for M5 stud
TAB_SLOT_L = 10.0            # Open-ended slide slot

# 4. Atmospheric Venturi Mixer & Orifice
VENTURI_LEN = 95.0           # Venturi tube length
VENTURI_R_THROAT = 9.5       # Venturi throat radius (19 mm OD)
VENTURI_R_HORN = 14.0        # Bellmouth intake horn radius (28 mm OD)
VENTURI_HORN_LEN = 25.0      # Bellmouth cone length
SHUTTER_LEN = 16.0           # Rotatable air shutter collar length
ORIFICE_HEX_SIZE = 11.0      # 7/16 in (11 mm) brass hex body
ORIFICE_LEN = 22.0           # Brass orifice spud total length

# 5. Protective Wire Mesh Screen
WIRE_MESH_T = 1.0            # Wire screen wire thickness
WIRE_GRID_PITCH = 12.5       # Grid wire spacing


def create_modular_ceramic_burner_component(doc, name="Modular_Ceramic_Burner", placement=None):
    """
    Builds the standalone modular ceramic infrared burner cassette:
      - Cordierite honeycomb ceramic tile with simulated radiant micro-grooves
      - 304 SS protective wire screen face guard
      - Deep-drawn stainless steel combustion plenum with side slotted tabs
      - Rear venturi pre-mix tube with primary air shutter
      - Machined brass #60 orifice spud
      - Spark electrode post & thermocouple clip
      - Brass knurled thumb nuts on mounting tabs

    Returns:
      App::Part container object
    """
    if placement is None:
        placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0, 1))

    grp = doc.addObject("App::Part", name)
    grp.Label = "Modular Ceramic Infrared Burner Cassette (10,000 BTU)"
    grp.Placement = placement

    # --------------------------------------------------------------------------
    # 1. Cordierite Ceramic Radiant Plaque (1,600°F - 1,800°F Matrix)
    # --------------------------------------------------------------------------
    # Ceramic tile sits from Z = 0 to Z = TILE_T
    tile_box = Part.makeBox(
        TILE_W,
        TILE_L,
        TILE_T,
        FreeCAD.Vector(-TILE_W / 2.0, -TILE_L / 2.0, 0)
    )

    # Simulated micro-pore radiant surface slots across the face
    grooves = []
    for gx in range(int(-TILE_W / 2.0 + 15), int(TILE_W / 2.0 - 15), 14):
        g = Part.makeBox(
            2.0,
            TILE_L - 16.0,
            1.2,
            FreeCAD.Vector(gx - 1.0, -TILE_L / 2.0 + 8.0, -0.2)
        )
        tile_box = tile_box.cut(g)

    obj_tile = doc.addObject("Part::Feature", f"{name}_Ceramic_Tile")
    obj_tile.Label = "Cordierite Honeycomb Ceramic Plaque (10k BTU Matrix)"
    obj_tile.Shape = tile_box
    grp.addObject(obj_tile)
    apply_material(obj_tile, "Ceramic-Cordierite")

    # --------------------------------------------------------------------------
    # 2. 304 Stainless Steel Protective Wire Mesh Screen
    # --------------------------------------------------------------------------
    # Outer frame wire rim
    rim_outer = Part.makeBox(
        TILE_W + 4.0,
        TILE_L + 4.0,
        1.5,
        FreeCAD.Vector(-(TILE_W + 4.0) / 2.0, -(TILE_L + 4.0) / 2.0, -1.0)
    )
    rim_inner = Part.makeBox(
        TILE_W - 6.0,
        TILE_L - 6.0,
        2.5,
        FreeCAD.Vector(-(TILE_W - 6.0) / 2.0, -(TILE_L - 6.0) / 2.0, -1.5)
    )
    screen_rim = rim_outer.cut(rim_inner)

    # Cross wires across X and Y
    wires = []
    for wy in range(int(-TILE_L / 2.0 + 15), int(TILE_L / 2.0 - 10), int(WIRE_GRID_PITCH)):
        w = Part.makeCylinder(0.6, TILE_W - 4.0, FreeCAD.Vector(-TILE_W / 2.0 + 2.0, wy, -0.4), FreeCAD.Vector(1, 0, 0))
        wires.append(w)
    for wx in range(int(-TILE_W / 2.0 + 18), int(TILE_W / 2.0 - 15), int(WIRE_GRID_PITCH)):
        w = Part.makeCylinder(0.6, TILE_L - 4.0, FreeCAD.Vector(wx, -TILE_L / 2.0 + 2.0, -0.4), FreeCAD.Vector(0, 1, 0))
        wires.append(w)

    screen_shape = screen_rim
    for w in wires:
        screen_shape = screen_shape.fuse(w)

    obj_screen = doc.addObject("Part::Feature", f"{name}_Wire_Mesh_Guard")
    obj_screen.Label = "304 Stainless Steel Protective Wire Mesh Face Guard"
    obj_screen.Shape = screen_shape
    grp.addObject(obj_screen)
    apply_material(obj_screen, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 3. Deep-Drawn Stainless Steel Combustion Plenum Housing & Mounting Tabs
    # --------------------------------------------------------------------------
    # Outer plenum box
    plenum_outer = Part.makeBox(
        CASING_W,
        CASING_L,
        PLENUM_DEPTH,
        FreeCAD.Vector(-CASING_W / 2.0, -CASING_L / 2.0, TILE_T - 2.0)
    )
    # Inner combustion cavity
    plenum_inner = Part.makeBox(
        CASING_W - 2 * CASING_T,
        CASING_L - 2 * CASING_T,
        PLENUM_DEPTH - CASING_T,
        FreeCAD.Vector(-CASING_W / 2.0 + CASING_T, -CASING_L / 2.0 + CASING_T, TILE_T - 3.0)
    )
    plenum_shell = plenum_outer.cut(plenum_inner)

    # Front ceramic retention bezel lip
    bezel_outer = Part.makeBox(
        CASING_W,
        CASING_L,
        2.0,
        FreeCAD.Vector(-CASING_W / 2.0, -CASING_L / 2.0, 0)
    )
    bezel_window = Part.makeBox(
        TILE_W - 2 * BEZEL_LIP,
        TILE_L - 2 * BEZEL_LIP,
        3.0,
        FreeCAD.Vector(-(TILE_W - 2 * BEZEL_LIP) / 2.0, -(TILE_L - 2 * BEZEL_LIP) / 2.0, -0.5)
    )
    bezel = bezel_outer.cut(bezel_window)
    plenum_shell = plenum_shell.fuse(bezel)

    # Quick-swap slotted perimeter mounting tabs (2 on each side along X)
    tabs = []
    for side_x in [-CASING_W / 2.0 - TAB_PROJ, CASING_W / 2.0]:
        for tab_y in [-CASING_L / 4.0, CASING_L / 4.0]:
            tab_body = Part.makeBox(
                TAB_PROJ,
                TAB_L,
                2.5,
                FreeCAD.Vector(side_x, tab_y - TAB_L / 2.0, TILE_T + 10.0)
            )
            # Open slide slot
            slot_x = side_x if side_x < 0 else side_x + TAB_PROJ - TAB_SLOT_L
            slot_cut = Part.makeBox(
                TAB_SLOT_L + 2.0,
                TAB_SLOT_W,
                4.0,
                FreeCAD.Vector(slot_x - 1.0, tab_y - TAB_SLOT_W / 2.0, TILE_T + 9.0)
            )
            tab_body = tab_body.cut(slot_cut)
            tabs.append(tab_body)

    for t in tabs:
        plenum_shell = plenum_shell.fuse(t)

    obj_plenum = doc.addObject("Part::Feature", f"{name}_Plenum_Casing")
    obj_plenum.Label = "304 SS Deep-Drawn Combustion Plenum Chamber & Slide Tabs"
    obj_plenum.Shape = plenum_shell
    grp.addObject(obj_plenum)
    apply_material(obj_plenum, "Steel-304Stainless")

    # --------------------------------------------------------------------------
    # 4. Knurled Brass Thumb Nuts (M5 Quick-Release Retainers)
    # --------------------------------------------------------------------------
    thumb_nuts = []
    for side_x in [-CASING_W / 2.0 - TAB_PROJ / 2.0, CASING_W / 2.0 + TAB_PROJ / 2.0]:
        for tab_y in [-CASING_L / 4.0, CASING_L / 4.0]:
            # Knurled barrel
            t_cyl = Part.makeCylinder(6.0, 7.0, FreeCAD.Vector(side_x, tab_y, TILE_T + 12.5), FreeCAD.Vector(0, 0, 1))
            t_rim = Part.makeCylinder(8.0, 3.0, FreeCAD.Vector(side_x, tab_y, TILE_T + 16.5), FreeCAD.Vector(0, 0, 1))
            thumb_nuts.append(t_cyl.fuse(t_rim))

    nut_shape = thumb_nuts[0]
    for n in thumb_nuts[1:]:
        nut_shape = nut_shape.fuse(n)

    obj_nuts = doc.addObject("Part::Feature", f"{name}_Thumb_Nuts")
    obj_nuts.Label = "Knurled Brass Thumb Nuts (M5 Tool-Free Fasteners)"
    obj_nuts.Shape = nut_shape
    grp.addObject(obj_nuts)
    apply_material(obj_nuts, "Brass-C360")

    # --------------------------------------------------------------------------
    # 5. Atmospheric Pre-Mix Venturi Tube & Air Shutter Collar
    # --------------------------------------------------------------------------
    # Venturi sits centrally at rear of plenum (Z = TILE_T + PLENUM_DEPTH)
    # Extending along -Y direction
    venturi_z = TILE_T + PLENUM_DEPTH + 12.0
    v_start_y = 10.0

    # Cast iron venturi body
    v_tube = Part.makeCylinder(
        VENTURI_R_THROAT,
        VENTURI_LEN,
        FreeCAD.Vector(0, v_start_y, venturi_z),
        FreeCAD.Vector(0, -1, 0)
    )
    v_horn = Part.makeCone(
        VENTURI_R_HORN,
        VENTURI_R_THROAT,
        VENTURI_HORN_LEN,
        FreeCAD.Vector(0, v_start_y - VENTURI_LEN, venturi_z),
        FreeCAD.Vector(0, 1, 0)
    )
    # 90-degree plenum inlet elbow
    elbow = Part.makeCylinder(
        VENTURI_R_THROAT + 2.0,
        18.0,
        FreeCAD.Vector(0, v_start_y, TILE_T + PLENUM_DEPTH - 2.0),
        FreeCAD.Vector(0, 0, 1)
    )
    venturi_solid = v_tube.fuse(v_horn).fuse(elbow)

    obj_venturi = doc.addObject("Part::Feature", f"{name}_Venturi_Tube")
    obj_venturi.Label = "Atmospheric Pre-Mix Venturi Tube & Bellmouth Horn"
    obj_venturi.Shape = venturi_solid
    grp.addObject(obj_venturi)
    apply_material(obj_venturi, "CastIron-Gray")

    # Rotatable Air Shutter Collar (Aluminum)
    shutter_collar = Part.makeCylinder(
        VENTURI_R_HORN + 1.5,
        SHUTTER_LEN,
        FreeCAD.Vector(0, v_start_y - VENTURI_LEN + 5.0, venturi_z),
        FreeCAD.Vector(0, 1, 0)
    )
    shutter_slot = Part.makeBox(
        VENTURI_R_HORN * 2 + 4.0,
        6.0,
        VENTURI_R_HORN * 2 + 4.0,
        FreeCAD.Vector(-(VENTURI_R_HORN + 2.0), v_start_y - VENTURI_LEN + 10.0, venturi_z - (VENTURI_R_HORN + 2.0))
    )
    shutter_solid = shutter_collar.cut(shutter_slot)

    obj_shutter = doc.addObject("Part::Feature", f"{name}_Air_Shutter")
    obj_shutter.Label = "Rotatable Primary Air Shutter Collar (Stoichiometry Adjuster)"
    obj_shutter.Shape = shutter_solid
    grp.addObject(obj_shutter)
    apply_material(obj_shutter, "Aluminum-6061-T6")

    # --------------------------------------------------------------------------
    # 6. Machined Brass Gas Orifice Spud (#60 Drill / 1/8" NPT)
    # --------------------------------------------------------------------------
    # Aligned coaxially with venturi horn at Y = v_start_y - VENTURI_LEN
    spud_tip_y = v_start_y - VENTURI_LEN + 8.0
    spud_hex = Part.makeCylinder(
        ORIFICE_HEX_SIZE / 2.0,
        ORIFICE_LEN,
        FreeCAD.Vector(0, spud_tip_y - ORIFICE_LEN, venturi_z),
        FreeCAD.Vector(0, 1, 0)
    )
    spud_nozzle = Part.makeCone(
        4.0,
        2.5,
        6.0,
        FreeCAD.Vector(0, spud_tip_y, venturi_z),
        FreeCAD.Vector(0, 1, 0)
    )
    gas_spud = spud_hex.fuse(spud_nozzle)

    obj_spud = doc.addObject("Part::Feature", f"{name}_Orifice_Spud")
    obj_spud.Label = "Machined Brass Hex Gas Orifice Spud (#60 Drill, 10k BTU LP)"
    obj_spud.Shape = gas_spud
    grp.addObject(obj_spud)
    apply_material(obj_spud, "Brass-C360")

    # --------------------------------------------------------------------------
    # 7. Spark Ignition Electrode Post & Thermocouple Sensor Clip
    # --------------------------------------------------------------------------
    # Alumina ceramic post mounted on front side flange
    elec_insul = Part.makeCylinder(
        3.5,
        32.0,
        FreeCAD.Vector(-TILE_W / 2.0 + 20.0, -TILE_L / 2.0 - 6.0, TILE_T + 2.0),
        FreeCAD.Vector(0, 1, -0.3)
    )
    # Nickel spark probe tip bent over radiant face
    elec_probe = Part.makeCylinder(
        1.0,
        14.0,
        FreeCAD.Vector(-TILE_W / 2.0 + 20.0, -TILE_L / 2.0 + 10.0, -1.0),
        FreeCAD.Vector(0, 1, 0)
    )
    elec_bracket = Part.makeBox(
        12.0,
        14.0,
        2.0,
        FreeCAD.Vector(-TILE_W / 2.0 + 14.0, -TILE_L / 2.0 - 10.0, TILE_T)
    )
    igniter_assembly = elec_insul.fuse(elec_probe).fuse(elec_bracket)

    obj_ign = doc.addObject("Part::Feature", f"{name}_Spark_Electrode")
    obj_ign.Label = "Alumina Spark Ignition Electrode & Pulse Lead Terminal"
    obj_ign.Shape = igniter_assembly
    grp.addObject(obj_ign)
    apply_material(obj_ign, "Ceramic-Alumina")

    return grp


if __name__ == "__main__":
    doc = FreeCAD.newDocument("TestModularBurner")
    create_modular_ceramic_burner_component(doc)
    doc.recompute()
    print("Test build complete. Total objects:", len(doc.Objects))
