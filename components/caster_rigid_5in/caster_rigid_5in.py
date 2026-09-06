"""
5.0" Rigid Caster Assembly Component
Standalone 3D Parametric CAD Module

Commercial heavy-duty rigid plate caster assembly:
- Top Mounting Plate: 85.0 mm x 100.0 mm x 4.0 mm with standard bolt pattern
- Dual Formed Stamped Steel Fork Legs (3.5 mm thickness)
- Grade 5 3/8" Axle Bolt, Flat Washers, and Locking Hex Nut
- 5.0" Caster Wheel (Yellow Polyurethane Hub / Black Solid Rubber Tread)
- Overall Height: 150.0 mm from ground to top mounting face
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_caster_rigid_5in_component(doc, placement=None):
    """
    Creates the 5.0" Rigid Caster Assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing caster sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Caster_Rigid_5in")
    grp.Label = "5.0\" Rigid Heavy-Duty Plate Caster Assembly"

    # Parametric Dimensions
    WHEEL_DIA = 127.0           # 5.0 in wheel diameter
    WHEEL_R = WHEEL_DIA / 2.0   # 63.5 mm
    AXLE_Z = WHEEL_R            # 63.5 mm above ground
    PLATE_W = 85.0              # 3.35 in plate width along X
    PLATE_L = 100.0             # 3.94 in plate length along Y
    PLATE_T = 4.0               # 4 mm plate thickness
    FORK_T = 3.5                # 3.5 mm formed leg thickness
    HUB_W = 40.0                # Hub width
    LEG_SPACING = HUB_W + 10.0  # 50.0 mm spacing between fork legs
    OVERALL_H = 150.0           # Top of mounting plate above ground
    PLATE_BOT_Z = OVERALL_H - PLATE_T # 146.0 mm

    # 1. Top Mounting Plate with 4 Bolt Heads
    top_plate = Part.makeBox(PLATE_W, PLATE_L, PLATE_T,
                             FreeCAD.Vector(-PLATE_W/2.0, -PLATE_L/2.0, PLATE_BOT_Z))
    for bx in [-28.0, 28.0]:
        for by in [-35.0, 35.0]:
            b_head = Part.makeCylinder(4.5, 5.0,
                                       FreeCAD.Vector(bx, by, PLATE_BOT_Z - 5.0),
                                       FreeCAD.Vector(0, 0, 1))
            top_plate = top_plate.fuse(b_head)

    # 2. Dual Formed Steel Fork Legs
    leg_h = PLATE_BOT_Z - AXLE_Z + 18.0
    leg_l = Part.makeBox(FORK_T, 48.0, leg_h,
                         FreeCAD.Vector(-LEG_SPACING/2.0 - FORK_T, -24.0, AXLE_Z - 18.0))
    leg_r = Part.makeBox(FORK_T, 48.0, leg_h,
                         FreeCAD.Vector(LEG_SPACING/2.0, -24.0, AXLE_Z - 18.0))
    bracket_solid = top_plate.fuse(leg_l).fuse(leg_r)

    # 3. Grade 5 3/8" Axle Hardware (Bolt, Washers, Hex Nut)
    axle_len = LEG_SPACING + 2*FORK_T + 22.0
    axle_rod = Part.makeCylinder(4.76, axle_len,
                                 FreeCAD.Vector(-axle_len/2.0, 0, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    hex_head = Part.makeBox(7.0, 16.0, 16.0,
                            FreeCAD.Vector(-axle_len/2.0, -8.0, AXLE_Z - 8.0))
    hex_nut = Part.makeBox(7.0, 16.0, 16.0,
                           FreeCAD.Vector(axle_len/2.0 - 7.0, -8.0, AXLE_Z - 8.0))
    washer_l = Part.makeCylinder(10.0, 2.5,
                                 FreeCAD.Vector(-LEG_SPACING/2.0 - FORK_T - 2.5, 0, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    washer_r = Part.makeCylinder(10.0, 2.5,
                                 FreeCAD.Vector(LEG_SPACING/2.0 + FORK_T, 0, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    axle_solid = axle_rod.fuse(hex_head).fuse(hex_nut).fuse(washer_l).fuse(washer_r)

    # Apply placement to bracket and axle
    bracket_solid.Placement = placement
    axle_solid.Placement = placement

    obj_bracket = doc.addObject("Part::Feature", "Rigid_Caster_Bracket")
    obj_bracket.Label = "Heavy-Duty Stamped Steel Rigid Caster Bracket"
    obj_bracket.Shape = bracket_solid
    grp.addObject(obj_bracket)
    apply_material(obj_bracket, "Steel-ZincPlated")

    obj_axle = doc.addObject("Part::Feature", "Rigid_Caster_Axle_Hardware")
    obj_axle.Label = "Grade 5 3/8in Axle Bolt, Washers & Nut"
    obj_axle.Shape = axle_solid
    grp.addObject(obj_axle)
    apply_material(obj_axle, "Steel-ZincPlated")

    # 4. Import Atomic 5.0" Caster Wheel (placed at axle center)
    wheel_center = FreeCAD.Vector(0, 0, AXLE_Z)
    combined_placement = placement.multiply(FreeCAD.Placement(wheel_center, FreeCAD.Rotation()))
    wheel_comp = import_component(doc, "caster_wheel_5in", placement=combined_placement)
    if wheel_comp:
        grp.addObject(wheel_comp)

    return grp
