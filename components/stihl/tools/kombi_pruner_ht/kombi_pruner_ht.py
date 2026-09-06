"""
STIHL HT-KM 12" Pole Pruner (Chainsaw) Component
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length) with ribbed rubber handle grip
- Cast Magnesium Drive Gearcase with integrated branch hook
- Translucent Bar & Chain Lubricant Reservoir Tank with black quarter-turn filler cap
- STIHL Orange Sprocket Guard Cover with single captive zinc-plated bar clamp nut
- In-Line 12" (300 mm) Rollomatic E Mini Guide Bar (Plastic-StihlWhite body) & Picco Saw Chain (Steel-A36)
  extending straight along the drive shaft axis for overhead canopy reach
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_pruner_ht_component(doc, placement=None):
    """
    Creates the authentic in-line STIHL HT-KM 12" Pole Pruner in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing pole pruner sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Pruner_HT")
    grp.Label = "STIHL HT-KM 12in Pole Pruner Chainsaw"

    SHAFT_LEN = 850.0

    # 1. Mount Standard Drive Shaft Component
    shaft_comp = import_component(doc, "kombi_shaft", placement=placement)
    if shaft_comp:
        grp.addObject(shaft_comp)

    # 2. Drive Shaft Ribbed Rubber Handle Grip Sleeve (Z = -200 to -420)
    grip_outer = Part.makeCylinder(16.5, 220.0, FreeCAD.Vector(0, 0, -420.0), FreeCAD.Vector(0, 0, 1))
    grip_bore = Part.makeCylinder(12.7, 222.0, FreeCAD.Vector(0, 0, -421.0), FreeCAD.Vector(0, 0, 1))
    grip_solid = grip_outer.cut(grip_bore)

    # 3. Cast Magnesium Drive Head with Branch Hook at Z = -SHAFT_LEN
    socket_cyl = Part.makeCylinder(17.0, 50.0, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    socket_bore = Part.makeCylinder(12.7, 52.0, FreeCAD.Vector(0, 0, -SHAFT_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    clamp_flange = Part.makeBox(12.0, 20.0, 35.0, FreeCAD.Vector(12.0, -10.0, -SHAFT_LEN + 8.0))
    socket_solid = socket_cyl.cut(socket_bore).fuse(clamp_flange)

    gear_body = Part.makeBox(60.0, 55.0, 80.0, FreeCAD.Vector(-30.0, -27.5, -SHAFT_LEN - 80.0))
    # Integrated branch hook extending backward (-Y)
    hook_spine = Part.makeBox(14.0, 30.0, 16.0, FreeCAD.Vector(-7.0, -57.5, -SHAFT_LEN - 75.0))
    hook_tip = Part.makeBox(14.0, 14.0, 28.0, FreeCAD.Vector(-7.0, -57.5, -SHAFT_LEN - 55.0))
    gearcase_solid = socket_solid.fuse(gear_body).fuse(hook_spine).fuse(hook_tip)

    # 4. Translucent Bar Oil Reservoir & Cap (on +X side)
    tank_box = Part.makeBox(28.0, 48.0, 65.0, FreeCAD.Vector(25.0, -24.0, -SHAFT_LEN - 72.0))
    cap_neck = Part.makeCylinder(11.0, 12.0, FreeCAD.Vector(45.0, 0, -SHAFT_LEN - 40.0), FreeCAD.Vector(1, 0, 0))
    tank_solid = tank_box.fuse(cap_neck)

    cap_body = Part.makeCylinder(14.0, 8.0, FreeCAD.Vector(55.0, 0, -SHAFT_LEN - 40.0), FreeCAD.Vector(1, 0, 0))
    cap_wing = Part.makeBox(6.0, 24.0, 12.0, FreeCAD.Vector(58.0, -12.0, -SHAFT_LEN - 46.0))
    oil_cap_solid = cap_body.fuse(cap_wing)

    # 5. STIHL Orange Sprocket Guard Cover with Single Captive Nut (on -X side)
    cover_box = Part.makeBox(22.0, 58.0, 85.0, FreeCAD.Vector(-52.0, -29.0, -SHAFT_LEN - 82.0))
    nut_boss = Part.makeCylinder(10.0, 8.0, FreeCAD.Vector(-52.0, 0, -SHAFT_LEN - 42.0), FreeCAD.Vector(-1, 0, 0))
    sprocket_cover_solid = cover_box.fuse(nut_boss)

    bar_nut = Part.makeCylinder(7.0, 10.0, FreeCAD.Vector(-56.0, 0, -SHAFT_LEN - 42.0), FreeCAD.Vector(-1, 0, 0))

    # 6. In-Line 12" (300 mm) Rollomatic E Mini Guide Bar & Picco Saw Chain
    # Extends straight out along -Z in line with the shaft
    BAR_L = 300.0
    BAR_W = 55.0   # Width along Y
    BAR_T = 4.5    # Thickness along X
    Z_BAR_TOP = -SHAFT_LEN - 50.0
    Z_BAR_TIP = Z_BAR_TOP - BAR_L

    # Bar body
    bar_plate = Part.makeBox(BAR_T, BAR_W, BAR_L - BAR_W/2.0, FreeCAD.Vector(-BAR_T/2.0, -BAR_W/2.0, Z_BAR_TIP + BAR_W/2.0))
    nose_cyl = Part.makeCylinder(BAR_W/2.0, BAR_T, FreeCAD.Vector(-BAR_T/2.0, 0, Z_BAR_TIP + BAR_W/2.0), FreeCAD.Vector(1, 0, 0))
    bar_solid = bar_plate.fuse(nose_cyl)

    # Saw chain wrapping around perimeter
    chain_outer = Part.makeBox(BAR_T + 1.6, BAR_W + 6.0, BAR_L - BAR_W/2.0,
                               FreeCAD.Vector(-(BAR_T + 1.6)/2.0, -(BAR_W + 6.0)/2.0, Z_BAR_TIP + BAR_W/2.0))
    chain_inner = Part.makeBox(BAR_T + 2.0, BAR_W - 2.0, BAR_L - BAR_W/2.0 + 2.0,
                               FreeCAD.Vector(-(BAR_T + 2.0)/2.0, -(BAR_W - 2.0)/2.0, Z_BAR_TIP + BAR_W/2.0 - 1.0))
    chain_nose_out = Part.makeCylinder((BAR_W + 6.0)/2.0, BAR_T + 1.6, FreeCAD.Vector(-(BAR_T + 1.6)/2.0, 0, Z_BAR_TIP + BAR_W/2.0), FreeCAD.Vector(1, 0, 0))
    chain_nose_in = Part.makeCylinder((BAR_W - 2.0)/2.0, BAR_T + 2.0, FreeCAD.Vector(-(BAR_T + 2.0)/2.0, 0, Z_BAR_TIP + BAR_W/2.0), FreeCAD.Vector(1, 0, 0))
    chain_solid = chain_outer.cut(chain_inner).fuse(chain_nose_out.cut(chain_nose_in))

    # Apply placement
    grip_solid.Placement = placement
    gearcase_solid.Placement = placement
    tank_solid.Placement = placement
    oil_cap_solid.Placement = placement
    sprocket_cover_solid.Placement = placement
    bar_nut.Placement = placement
    bar_solid.Placement = placement
    chain_solid.Placement = placement

    # Add objects to document
    obj_grip = doc.addObject("Part::Feature", "HT_Shaft_Grip")
    obj_grip.Label = "Ribbed Rubber Handle Grip Sleeve"
    obj_grip.Shape = grip_solid
    grp.addObject(obj_grip)
    apply_material(obj_grip, "Rubber-Solid")

    obj_gear = doc.addObject("Part::Feature", "HT_Gearhead")
    obj_gear.Label = "Cast Magnesium Drive Head & Branch Hook"
    obj_gear.Shape = gearcase_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_tank = doc.addObject("Part::Feature", "HT_Oil_Reservoir")
    obj_tank.Label = "Translucent Bar Oil Reservoir"
    obj_tank.Shape = tank_solid
    grp.addObject(obj_tank)
    apply_material(obj_tank, "Plastic-StihlWhite")

    obj_cap = doc.addObject("Part::Feature", "HT_Oil_Cap")
    obj_cap.Label = "Black Quarter-Turn Oil Filler Cap"
    obj_cap.Shape = oil_cap_solid
    grp.addObject(obj_cap)
    apply_material(obj_cap, "Plastic-ABS")

    obj_cover = doc.addObject("Part::Feature", "HT_Sprocket_Cover")
    obj_cover.Label = "STIHL Orange Drive Sprocket Cover"
    obj_cover.Shape = sprocket_cover_solid
    grp.addObject(obj_cover)
    apply_material(obj_cover, "Plastic-StihlOrange")

    obj_nut = doc.addObject("Part::Feature", "HT_Bar_Nut")
    obj_nut.Label = "Single Captive Zinc-Plated Bar Nut"
    obj_nut.Shape = bar_nut
    grp.addObject(obj_nut)
    apply_material(obj_nut, "Steel-ZincPlated")

    obj_bar = doc.addObject("Part::Feature", "HT_Guide_Bar")
    obj_bar.Label = "12in Rollomatic E Mini Guide Bar"
    obj_bar.Shape = bar_solid
    grp.addObject(obj_bar)
    apply_material(obj_bar, "Plastic-StihlWhite")

    obj_chain = doc.addObject("Part::Feature", "HT_Saw_Chain")
    obj_chain.Label = "3/8 Picco Micro Mini Saw Chain"
    obj_chain.Shape = chain_solid
    grp.addObject(obj_chain)
    apply_material(obj_chain, "Steel-A36")

    return grp
