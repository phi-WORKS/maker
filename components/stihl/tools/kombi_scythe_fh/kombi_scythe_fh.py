"""
STIHL FH-KM 145-Degree Adjustable Power Scythe Component
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length)
- Corrugated Black Rubber Boot (Rubber-Solid) at the shaft articulation joint
- 145-Degree Articulating Indexing Gearbox (CastIron-Gray)
- Ergonomic Angle Adjustment Latch Handle (Plastic-ABS) mounted along the top spine
- Dual Reciprocating Serrated Steel Scythe Blades (250 mm / 9.8" cut length, Steel-A36)
- Rounded Cast Pavement Skid Bumper Shoe (Steel-ZincPlated) at the blade tip
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_scythe_fh_component(doc, placement=None):
    """
    Creates the authentic STIHL FH-KM Power Scythe in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing power scythe sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Scythe_FH")
    grp.Label = "STIHL FH-KM 145-deg Articulating Power Scythe"

    SHAFT_LEN = 850.0

    # 1. Mount Standard Drive Shaft Component
    shaft_comp = import_component(doc, "kombi_shaft", placement=placement)
    if shaft_comp:
        grp.addObject(shaft_comp)

    # 2. Corrugated Black Rubber Boot above the joint (Z = -SHAFT_LEN to -SHAFT_LEN + 45)
    boot_outer = Part.makeCylinder(18.0, 45.0, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    boot_bore = Part.makeCylinder(12.7, 47.0, FreeCAD.Vector(0, 0, -SHAFT_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    # Rib rings
    for rz in [-SHAFT_LEN + 10.0, -SHAFT_LEN + 22.0, -SHAFT_LEN + 34.0]:
        ring = Part.makeCylinder(20.0, 5.0, FreeCAD.Vector(0, 0, rz), FreeCAD.Vector(0, 0, 1))
        boot_outer = boot_outer.fuse(ring)
    boot_solid = boot_outer.cut(boot_bore)

    # 3. 145-Degree Articulating Indexing Knuckle & Gearbox at Z = -SHAFT_LEN
    # Receiver socket clamped to shaft
    socket_cyl = Part.makeCylinder(16.5, 40.0, FreeCAD.Vector(0, 0, -SHAFT_LEN - 20.0), FreeCAD.Vector(0, 0, 1))
    # Transverse pivot knuckle
    pivot_hub = Part.makeCylinder(20.0, 44.0, FreeCAD.Vector(-22.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    # Transmission gearbox housing
    gear_housing = Part.makeBox(44.0, 50.0, 50.0, FreeCAD.Vector(-22.0, -25.0, -SHAFT_LEN - 75.0))
    knuckle_solid = socket_cyl.fuse(pivot_hub).fuse(gear_housing)

    # 4. Ergonomic Angle Adjustment Latch Handle (Plastic-ABS) mounted on top spine
    lever_base = Part.makeBox(20.0, 35.0, 24.0, FreeCAD.Vector(-10.0, -17.5, -SHAFT_LEN - 30.0))
    lever_arm = Part.makeBox(14.0, 85.0, 16.0, FreeCAD.Vector(-7.0, 5.0, -SHAFT_LEN - 20.0))
    lever_solid = lever_base.fuse(lever_arm)

    # 5. Dual Reciprocating Serrated Scythe Blades (250 mm cutting length)
    BLADE_L = 260.0
    BLADE_W = 46.0
    BLADE_T = 4.0
    Z_BLADE_TOP = -SHAFT_LEN - 75.0
    Z_BLADE_TIP = Z_BLADE_TOP - BLADE_L

    blade_spine = Part.makeBox(BLADE_T, BLADE_W, BLADE_L,
                               FreeCAD.Vector(-BLADE_T/2.0, -BLADE_W/2.0, Z_BLADE_TIP))
    
    # Machine scythe cutter teeth on both front (+Y) and rear (-Y) edges
    for tz in range(int(Z_BLADE_TIP + 15.0), int(Z_BLADE_TOP - 15.0), 22):
        t_front = Part.makeBox(BLADE_T + 2.0, 14.0, 10.0, FreeCAD.Vector(-BLADE_T/2.0 - 1.0, 12.0, tz))
        t_rear = Part.makeBox(BLADE_T + 2.0, 14.0, 10.0, FreeCAD.Vector(-BLADE_T/2.0 - 1.0, -26.0, tz))
        blade_spine = blade_spine.cut(t_front).cut(t_rear)

    # 6. Rounded Pavement Skid Bumper Shoe (Protects blade tip from stone/curb strike)
    bumper_cyl = Part.makeCylinder(26.0, BLADE_T + 6.0, FreeCAD.Vector(-(BLADE_T+6.0)/2.0, 0, Z_BLADE_TIP + 10.0), FreeCAD.Vector(1, 0, 0))
    bumper_cap = Part.makeBox(BLADE_T + 6.0, 52.0, 18.0, FreeCAD.Vector(-(BLADE_T+6.0)/2.0, -26.0, Z_BLADE_TIP - 4.0))
    bumper_solid = bumper_cyl.fuse(bumper_cap)

    # Apply placement
    boot_solid.Placement = placement
    knuckle_solid.Placement = placement
    lever_solid.Placement = placement
    blade_spine.Placement = placement
    bumper_solid.Placement = placement

    # Add objects to document
    obj_boot = doc.addObject("Part::Feature", "FH_Rubber_Boot")
    obj_boot.Label = "Flexible Corrugated Rubber Joint Boot"
    obj_boot.Shape = boot_solid
    grp.addObject(obj_boot)
    apply_material(obj_boot, "Rubber-Solid")

    obj_gear = doc.addObject("Part::Feature", "FH_Articulating_Gearcase")
    obj_gear.Label = "145-deg Cast Magnesium Articulating Gearbox"
    obj_gear.Shape = knuckle_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_lever = doc.addObject("Part::Feature", "FH_Adjust_Lever")
    obj_lever.Label = "Angle Indexing Adjustment Latch Lever"
    obj_lever.Shape = lever_solid
    grp.addObject(obj_lever)
    apply_material(obj_lever, "Plastic-ABS")

    obj_blades = doc.addObject("Part::Feature", "FH_Scythe_Blades")
    obj_blades.Label = "250mm Dual Reciprocating Serrated Blades"
    obj_blades.Shape = blade_spine
    grp.addObject(obj_blades)
    apply_material(obj_blades, "Steel-A36")

    obj_skid = doc.addObject("Part::Feature", "FH_Tip_Bumper")
    obj_skid.Label = "Zinc-Plated Pavement Skid Bumper Shoe"
    obj_skid.Shape = bumper_solid
    grp.addObject(obj_skid)
    apply_material(obj_skid, "Steel-ZincPlated")

    return grp
