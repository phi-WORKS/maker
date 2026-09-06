"""
STIHL FS-KM / FSS-KM Straight Shaft String Trimmer Component
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length)
- 35-degree Cast Angled Gearcase with grease service plug
- STIHL AutoCut 25-2 dual-line bump feed cutting head with white spool rim, white bump knob, and orange trimmer line
- Concentric Swept Debris Deflector Guard (Plastic-StihlOrange):
  - Clamped directly to the aluminum drive tube above the gearbox
  - Sweeps concentric with the cutting head on the rearward side
  - Molded radial strengthening ridges and downward perimeter skirt
- Steel Line Limiting Cutter Knife in Black Polymer Guard Bracket
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_trimmer_fs_component(doc, placement=None):
    """
    Creates the STIHL FS-KM Straight Shaft Trimmer in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing trimmer sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Trimmer_FS")
    grp.Label = "STIHL FS-KM Straight Shaft String Trimmer"

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

    # 3. AutoCut Bump Feed Trimmer Spool Head
    Z_HEAD = 42.0
    spool_black = Part.makeCylinder(60.0, 32.0, FreeCAD.Vector(0, 0, Z_HEAD), FreeCAD.Vector(0, 0, 1))
    spool_white_rim = Part.makeCylinder(62.0, 6.0, FreeCAD.Vector(0, 0, Z_HEAD + 32.0), FreeCAD.Vector(0, 0, 1))
    bump_knob = Part.makeCylinder(28.0, 12.0, FreeCAD.Vector(0, 0, Z_HEAD + 38.0), FreeCAD.Vector(0, 0, 1))
    spool_white_solid = spool_white_rim.fuse(bump_knob)

    # Trimmer lines: two 2.4 mm lines extending out radially
    line1 = Part.makeCylinder(1.2, 140.0, FreeCAD.Vector(58.0, 0, Z_HEAD + 25.0), FreeCAD.Vector(1, 0, 0))
    line2 = Part.makeCylinder(1.2, 140.0, FreeCAD.Vector(-58.0, 0, Z_HEAD + 25.0), FreeCAD.Vector(-1, 0, 0))
    lines_solid = line1.fuse(line2)

    # 4. Concentric Swept Debris Deflector Guard (Plastic-StihlOrange)
    # Clamped to the shaft tube, sweeps concentric with spindle axis
    R_outer = 210.0
    R_inner = 65.0
    SKIRT_H = 40.0
    WALL = 3.5

    # Downward perimeter skirt
    skirt_outer = Part.makeCylinder(R_outer, SKIRT_H, FreeCAD.Vector(0, 0, Z_HEAD - SKIRT_H + 10.0), FreeCAD.Vector(0, 0, 1))
    skirt_inner = Part.makeCylinder(R_outer - WALL, SKIRT_H + 2.0, FreeCAD.Vector(0, 0, Z_HEAD - SKIRT_H + 9.0), FreeCAD.Vector(0, 0, 1))
    skirt = skirt_outer.cut(skirt_inner)

    # Sloped conical top deck
    deck_outer = Part.makeCone(R_inner + 15.0, R_outer, 24.0, FreeCAD.Vector(0, 0, Z_HEAD - 14.0), FreeCAD.Vector(0, 0, 1))
    deck_inner = Part.makeCone(R_inner + 15.0 - WALL, R_outer - WALL, 24.0 + 2.0, FreeCAD.Vector(0, 0, Z_HEAD - 15.0), FreeCAD.Vector(0, 0, 1))
    deck = deck_outer.cut(deck_inner)
    guard_shell = skirt.fuse(deck)

    # Sweep cut: rotated 180 to opposite side (-Y)
    cut_box = Part.makeBox(R_outer * 2.5, R_outer * 2.5, SKIRT_H * 2.5,
                           FreeCAD.Vector(-R_outer * 1.25, -25.0, Z_HEAD - SKIRT_H - 10.0))
    guard_swept = guard_shell.cut(cut_box)

    # Radial stiffener ribs on deck
    rib1 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(-3.0, -170.0, Z_HEAD + 7.0))
    rib2 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(40.0, -160.0, Z_HEAD + 7.0))
    rib3 = Part.makeBox(6.0, 120.0, 4.0, FreeCAD.Vector(-46.0, -160.0, Z_HEAD + 7.0))
    ribs = rib1.fuse(rib2).fuse(rib3)
    guard_hood = guard_swept.fuse(ribs)

    # Transform hood into spindle orientation
    guard_hood.Placement = FreeCAD.Placement(spindle_base, rot_head)

    # Mount clamp to shaft tube
    shaft_clamp_cyl = Part.makeCylinder(16.5, 40.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 15.0), FreeCAD.Vector(0, 0, 1))
    shaft_clamp_bore = Part.makeCylinder(12.7, 42.0, FreeCAD.Vector(0, 0, -SHAFT_LEN + 14.0), FreeCAD.Vector(0, 0, 1))
    shaft_clamp_arm = Part.makeBox(32.0, 45.0, 20.0, FreeCAD.Vector(-16.0, -45.0, -SHAFT_LEN + 20.0))
    mount_to_shaft = shaft_clamp_cyl.cut(shaft_clamp_bore).fuse(shaft_clamp_arm)

    guard_solid = guard_hood.fuse(mount_to_shaft)

    # 5. Line Limiter Knife & Bracket on trailing skirt edge
    knife_local = Part.makeBox(18.0, 22.0, 2.0, FreeCAD.Vector(150.0, -97.0, Z_HEAD - 25.0))
    holder_local = Part.makeBox(24.0, 28.0, 8.0, FreeCAD.Vector(147.0, -100.0, Z_HEAD - 28.0))

    # Apply Placements
    gearcase_solid.Placement = placement
    spool_black.Placement = pl_head
    spool_white_solid.Placement = pl_head
    lines_solid.Placement = pl_head
    guard_solid.Placement = placement
    knife_local.Placement = pl_head
    holder_local.Placement = pl_head

    # Add objects to document
    obj_gear = doc.addObject("Part::Feature", "FS_Gearcase")
    obj_gear.Label = "35-Degree Cast Magnesium Trimmer Gearcase"
    obj_gear.Shape = gearcase_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_spool = doc.addObject("Part::Feature", "FS_AutoCut_Body")
    obj_spool.Label = "STIHL AutoCut 25-2 Head Body"
    obj_spool.Shape = spool_black
    grp.addObject(obj_spool)
    apply_material(obj_spool, "Plastic-ABS")

    obj_spool_white = doc.addObject("Part::Feature", "FS_AutoCut_Spool")
    obj_spool_white.Label = "AutoCut Spool Rim & Bump Knob"
    obj_spool_white.Shape = spool_white_solid
    grp.addObject(obj_spool_white)
    apply_material(obj_spool_white, "Plastic-StihlWhite")

    obj_lines = doc.addObject("Part::Feature", "FS_Trimmer_Line")
    obj_lines.Label = "STIHL Orange Dual 2.4mm Monofilament Line"
    obj_lines.Shape = lines_solid
    grp.addObject(obj_lines)
    apply_material(obj_lines, "Plastic-StihlOrange")

    obj_guard = doc.addObject("Part::Feature", "FS_Concentric_Debris_Shield")
    obj_guard.Label = "STIHL Orange Shaft-Mounted Swept Debris Shield"
    obj_guard.Shape = guard_solid
    grp.addObject(obj_guard)
    apply_material(obj_guard, "Plastic-StihlOrange")

    obj_holder = doc.addObject("Part::Feature", "FS_Blade_Holder")
    obj_holder.Label = "Line Limiter Knife Bracket"
    obj_holder.Shape = holder_local
    grp.addObject(obj_holder)
    apply_material(obj_holder, "Plastic-ABS")

    obj_blade = doc.addObject("Part::Feature", "FS_Line_Limiter_Blade")
    obj_blade.Label = "Hardened Steel Line Cutting Knife"
    obj_blade.Shape = knife_local
    grp.addObject(obj_blade)
    apply_material(obj_blade, "Steel-A36")

    return grp
