"""
STIHL BF-KM Mini-Cultivator Component
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length)
- Center Worm-Drive Cast Magnesium Gearbox (CastIron-Gray) with horizontal axle shaft
- Arched Black High-Impact Polymer Debris Shield / Soil Fender (Plastic-ABS)
- 4 Rotary Digging Pick Tines (Steel-A36) with 12 starburst teeth per rotor (220 mm / 8.7" cultivating width)
- Zinc-Plated Hairpin Lynch Pin Axle Retainers (Steel-ZincPlated)
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_cultivator_bf_component(doc, placement=None):
    """
    Creates the authentic STIHL BF-KM Mini-Cultivator in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing mini-cultivator sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Cultivator_BF")
    grp.Label = "STIHL BF-KM Mini-Cultivator"

    SHAFT_LEN = 850.0

    # 1. Mount Standard Drive Shaft Component
    shaft_comp = import_component(doc, "kombi_shaft", placement=placement)
    if shaft_comp:
        grp.addObject(shaft_comp)

    # 2. Worm Drive Center Gearbox at Z = -SHAFT_LEN
    socket_cyl = Part.makeCylinder(16.5, 50.0, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    socket_bore = Part.makeCylinder(12.7, 52.0, FreeCAD.Vector(0, 0, -SHAFT_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    socket_solid = socket_cyl.cut(socket_bore)

    gear_box = Part.makeBox(38.0, 52.0, 75.0, FreeCAD.Vector(-19.0, -26.0, -SHAFT_LEN - 75.0))
    AXLE_W = 220.0
    axle_cyl = Part.makeCylinder(14.0, AXLE_W, FreeCAD.Vector(-AXLE_W/2.0, 0, -SHAFT_LEN - 45.0), FreeCAD.Vector(1, 0, 0))
    gearcase_solid = socket_solid.fuse(gear_box).fuse(axle_cyl)

    # 3. Arched Black Debris Shield / Soil Fender (Plastic-ABS)
    FENDER_W = 260.0
    FENDER_R = 140.0
    fender_outer = Part.makeCylinder(FENDER_R, FENDER_W, FreeCAD.Vector(-FENDER_W/2.0, -20.0, -SHAFT_LEN + 40.0), FreeCAD.Vector(1, 0, 0))
    fender_inner = Part.makeCylinder(FENDER_R - 3.5, FENDER_W + 2.0, FreeCAD.Vector(-FENDER_W/2.0 - 1.0, -20.0, -SHAFT_LEN + 40.0), FreeCAD.Vector(1, 0, 0))
    fender_shell = fender_outer.cut(fender_inner)

    cut_box = Part.makeBox(FENDER_W + 10.0, FENDER_R * 2.5, FENDER_R * 2.5,
                           FreeCAD.Vector(-FENDER_W/2.0 - 5.0, -FENDER_R * 2.0, -SHAFT_LEN + 40.0 - FENDER_R * 1.5))
    fender_arch = fender_shell.cut(cut_box)

    clamp_cyl = Part.makeCylinder(16.5, 35.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 25.0), FreeCAD.Vector(0, 0, 1))
    clamp_bore = Part.makeCylinder(12.7, 37.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 24.0), FreeCAD.Vector(0, 0, 1))
    clamp_lug = Part.makeBox(14.0, 18.0, 25.0, FreeCAD.Vector(-7.0, 10.0, -SHAFT_LEN + 30.0))
    fender_solid = fender_arch.fuse(clamp_cyl.cut(clamp_bore)).fuse(clamp_lug)

    # 4. 4 Starburst Pick Tines (Steel-A36)
    TINE_R = 100.0
    TINE_T = 3.2
    AXIS_Z = -SHAFT_LEN - 45.0

    tine_positions = [-90.0, -45.0, 45.0, 90.0]
    tine_solids = []

    for tx in tine_positions:
        hub = Part.makeCylinder(32.0, TINE_T, FreeCAD.Vector(tx - TINE_T/2.0, 0, AXIS_Z), FreeCAD.Vector(1, 0, 0))
        teeth = []
        for tooth_idx in range(12):
            ang = tooth_idx * 30.0
            tooth = Part.makeBox(TINE_T, 18.0, TINE_R - 25.0, FreeCAD.Vector(tx - TINE_T/2.0, -9.0, 0))
            tooth.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), ang)
            tooth.translate(FreeCAD.Vector(0, 0, AXIS_Z))
            teeth.append(tooth)
        
        tine_disc = hub
        for t in teeth:
            tine_disc = tine_disc.fuse(t)
        
        arbor = Part.makeCylinder(14.2, TINE_T + 2.0, FreeCAD.Vector(tx - TINE_T/2.0 - 1.0, 0, AXIS_Z), FreeCAD.Vector(1, 0, 0))
        tine_solids.append(tine_disc.cut(arbor))

    all_tines = tine_solids[0]
    for t in tine_solids[1:]:
        all_tines = all_tines.fuse(t)

    # 5. Axle Hairpin Lynch Pins (Steel-ZincPlated)
    pin_left = Part.makeCylinder(4.0, 18.0, FreeCAD.Vector(-AXLE_W/2.0 + 2.0, 0, AXIS_Z - 9.0), FreeCAD.Vector(0, 0, 1))
    pin_ring_l = Part.makeCylinder(12.0, 4.0, FreeCAD.Vector(-AXLE_W/2.0 + 2.0, 0, AXIS_Z + 5.0), FreeCAD.Vector(1, 0, 0))
    pin_right = Part.makeCylinder(4.0, 18.0, FreeCAD.Vector(AXLE_W/2.0 - 2.0, 0, AXIS_Z - 9.0), FreeCAD.Vector(0, 0, 1))
    pin_ring_r = Part.makeCylinder(12.0, 4.0, FreeCAD.Vector(AXLE_W/2.0 - 6.0, 0, AXIS_Z + 5.0), FreeCAD.Vector(1, 0, 0))
    hardware_solid = pin_left.fuse(pin_ring_l).fuse(pin_right).fuse(pin_ring_r)

    # Apply placement
    gearcase_solid.Placement = placement
    fender_solid.Placement = placement
    all_tines.Placement = placement
    hardware_solid.Placement = placement

    # Add objects to document
    obj_gear = doc.addObject("Part::Feature", "BF_Center_Gearbox")
    obj_gear.Label = "Center Worm-Drive Transmission Gearbox"
    obj_gear.Shape = gearcase_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_fender = doc.addObject("Part::Feature", "BF_Debris_Fender")
    obj_fender.Label = "Black High-Impact Polymer Soil Fender"
    obj_fender.Shape = fender_solid
    grp.addObject(obj_fender)
    apply_material(obj_fender, "Plastic-ABS")

    obj_tines = doc.addObject("Part::Feature", "BF_Pick_Tines")
    obj_tines.Label = "4-Rotor 12-Tooth Steel Cultivator Pick Tines"
    obj_tines.Shape = all_tines
    grp.addObject(obj_tines)
    apply_material(obj_tines, "Steel-A36")

    obj_hw = doc.addObject("Part::Feature", "BF_Lynch_Pins")
    obj_hw.Label = "Zinc-Plated Axle Retaining Lynch Pins"
    obj_hw.Shape = hardware_solid
    grp.addObject(obj_hw)
    apply_material(obj_hw, "Steel-ZincPlated")

    return grp
