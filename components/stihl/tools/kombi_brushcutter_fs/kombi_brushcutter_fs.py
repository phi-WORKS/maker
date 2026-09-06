"""
STIHL FS-KM Brush Cutter Component (3-Tooth Metal Brush Knife)
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length)
- 35-degree Cast Angled Gearcase with grease service plug
- Concentric Swept Debris Deflector Guard (Plastic-StihlOrange) mounted to the drive shaft
- 3-Tooth Triangular Hardened Steel Brush Knife (250 mm / 9.8" cutting diameter, 3 mm thick)
- Gliding Ground Rider Cup & Clamp Nut (Steel-ZincPlated)
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_brushcutter_fs_component(doc, placement=None):
    """
    Creates the STIHL FS-KM Brush Cutter with Steel Blade in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing brush cutter sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Brushcutter_FS")
    grp.Label = "STIHL FS-KM Brush Cutter (3-Tooth Steel Blade)"

    SHAFT_LEN = 850.0

    # 1. Mount Standard Drive Shaft Component
    shaft_comp = import_component(doc, "kombi_shaft", placement=placement)
    if shaft_comp:
        grp.addObject(shaft_comp)

    # 2. 35-Degree Angled Gearbox at Z = -SHAFT_LEN
    gear_collar = Part.makeCylinder(16.0, 50.0, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    angle_rad = math.radians(35.0)
    sin_a = math.sin(angle_rad)
    cos_a = math.cos(angle_rad)
    spindle_dir = FreeCAD.Vector(0, -sin_a, -cos_a)

    gear_box = Part.makeBox(36.0, 44.0, 44.0, FreeCAD.Vector(-18.0, -22.0, -SHAFT_LEN - 32.0))
    spindle_cyl = Part.makeCylinder(16.0, 42.0, FreeCAD.Vector(0, -10.0, -SHAFT_LEN - 15.0), spindle_dir)
    gearcase_solid = gear_collar.fuse(gear_box).fuse(spindle_cyl)

    # Spindle coordinate system:
    spindle_base = FreeCAD.Vector(0, -10.0, -SHAFT_LEN - 15.0)
    rot_head = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -35.0)
    pl_head = placement.multiply(FreeCAD.Placement(spindle_base, rot_head))

    Z_HEAD = 42.0

    # 3. Concentric Swept Debris Deflector Guard (Plastic-StihlOrange)
    # Identical to trimmer: clamped to shaft tube, sweeps concentric with spindle axis
    R_outer = 210.0
    R_inner = 65.0
    SKIRT_H = 40.0
    WALL = 3.5

    skirt_outer = Part.makeCylinder(R_outer, SKIRT_H, FreeCAD.Vector(0, 0, Z_HEAD - SKIRT_H + 10.0), FreeCAD.Vector(0, 0, 1))
    skirt_inner = Part.makeCylinder(R_outer - WALL, SKIRT_H + 2.0, FreeCAD.Vector(0, 0, Z_HEAD - SKIRT_H + 9.0), FreeCAD.Vector(0, 0, 1))
    skirt = skirt_outer.cut(skirt_inner)

    deck_outer = Part.makeCone(R_inner + 15.0, R_outer, 24.0, FreeCAD.Vector(0, 0, Z_HEAD - 14.0), FreeCAD.Vector(0, 0, 1))
    deck_inner = Part.makeCone(R_inner + 15.0 - WALL, R_outer - WALL, 24.0 + 2.0, FreeCAD.Vector(0, 0, Z_HEAD - 15.0), FreeCAD.Vector(0, 0, 1))
    deck = deck_outer.cut(deck_inner)
    guard_shell = skirt.fuse(deck)

    # Sweep cut on -Y side
    cut_box = Part.makeBox(R_outer * 2.5, R_outer * 2.5, SKIRT_H * 2.5,
                           FreeCAD.Vector(-R_outer * 1.25, -25.0, Z_HEAD - SKIRT_H - 10.0))
    guard_swept = guard_shell.cut(cut_box)

    # Radial stiffeners on deck
    rib1 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(-3.0, -170.0, Z_HEAD + 7.0))
    rib2 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(40.0, -160.0, Z_HEAD + 7.0))
    rib3 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(-46.0, -160.0, Z_HEAD + 7.0))
    ribs = rib1.fuse(rib2).fuse(rib3)
    guard_hood = guard_swept.fuse(ribs)
    guard_hood.Placement = FreeCAD.Placement(spindle_base, rot_head)

    # Shaft clamp
    shaft_clamp_cyl = Part.makeCylinder(16.5, 40.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 15.0), FreeCAD.Vector(0, 0, 1))
    shaft_clamp_bore = Part.makeCylinder(12.7, 42.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 14.0), FreeCAD.Vector(0, 0, 1))
    shaft_clamp_arm = Part.makeBox(32.0, 45.0, 20.0, FreeCAD.Vector(-16.0, -45.0, -SHAFT_LEN + 20.0))
    mount_to_shaft = shaft_clamp_cyl.cut(shaft_clamp_bore).fuse(shaft_clamp_arm)
    guard_solid = guard_hood.fuse(mount_to_shaft)

    # 4. 3-Tooth Triangular Steel Brush Knife (250 mm dia x 3 mm thick)
    BLADE_R = 125.0
    BLADE_T = 3.0
    blade_center = Part.makeCylinder(BLADE_R, BLADE_T, FreeCAD.Vector(0, 0, Z_HEAD), FreeCAD.Vector(0, 0, 1))
    for ang in [0, 120, 240]:
        scallop = Part.makeCylinder(BLADE_R * 0.7, BLADE_T + 2.0,
                                    FreeCAD.Vector(BLADE_R * math.cos(math.radians(ang)),
                                                   BLADE_R * math.sin(math.radians(ang)),
                                                   Z_HEAD - 1.0),
                                    FreeCAD.Vector(0, 0, 1))
        blade_center = blade_center.cut(scallop)

    arbor_hole = Part.makeCylinder(12.7, BLADE_T + 4.0, FreeCAD.Vector(0, 0, Z_HEAD - 2.0), FreeCAD.Vector(0, 0, 1))
    blade_solid = blade_center.cut(arbor_hole)

    # 5. Gliding Ground Rider Cup & Clamp Nut
    cup_cyl = Part.makeCylinder(35.0, 14.0, FreeCAD.Vector(0, 0, Z_HEAD + BLADE_T), FreeCAD.Vector(0, 0, 1))
    cup_inner = Part.makeCylinder(30.0, 12.0, FreeCAD.Vector(0, 0, Z_HEAD + BLADE_T + 4.0), FreeCAD.Vector(0, 0, 1))
    nut_cyl = Part.makeCylinder(12.0, 16.0, FreeCAD.Vector(0, 0, Z_HEAD + BLADE_T), FreeCAD.Vector(0, 0, 1))
    rider_cup = cup_cyl.cut(cup_inner).fuse(nut_cyl)

    # Apply Placements
    gearcase_solid.Placement = placement
    guard_solid.Placement = placement
    blade_solid.Placement = pl_head
    rider_cup.Placement = pl_head

    # Add objects to document
    obj_gear = doc.addObject("Part::Feature", "Brush_Gearcase")
    obj_gear.Label = "35-Degree Cast Magnesium Gearbox"
    obj_gear.Shape = gearcase_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_guard = doc.addObject("Part::Feature", "Brush_Debris_Shield")
    obj_guard.Label = "STIHL Orange Shaft-Mounted Swept Debris Shield"
    obj_guard.Shape = guard_solid
    grp.addObject(obj_guard)
    apply_material(obj_guard, "Plastic-StihlOrange")

    obj_blade = doc.addObject("Part::Feature", "Brush_Tri_Blade")
    obj_blade.Label = "3-Tooth 250mm Hardened Steel Brush Knife"
    obj_blade.Shape = blade_solid
    grp.addObject(obj_blade)
    apply_material(obj_blade, "Steel-A36")

    obj_rider = doc.addObject("Part::Feature", "Brush_Rider_Cup")
    obj_rider.Label = "Zinc-Plated Steel Gliding Ground Rider Cup"
    obj_rider.Shape = rider_cup
    grp.addObject(obj_rider)
    apply_material(obj_rider, "Steel-ZincPlated")

    return grp
