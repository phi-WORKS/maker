"""
5.0" Swivel Caster Assembly Component with Foot Brake
Standalone 3D Parametric CAD Module

Commercial heavy-duty 360-degree swivel plate caster with foot-locking brake:
- Top Mounting Plate: 85.0 mm x 100.0 mm x 4.0 mm with standard bolt pattern
- Dual-Ball Bearing Swivel Raceway
- Formed Stamped Steel Trailing Fork Legs (3.5 mm thickness, 25 mm trail offset)
- Foot-Operated Wheel Brake Locking Lever & Serrated Cam Tab
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

def create_caster_swivel_5in_component(doc, placement=None):
    """
    Creates the 5.0" Swivel Caster Assembly with Brake in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing swivel caster sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Caster_Swivel_5in")
    grp.Label = "5.0\" Swivel Caster Assembly with Foot Lock Brake"

    # Parametric Dimensions
    WHEEL_DIA = 127.0           # 5.0 in wheel diameter
    WHEEL_R = WHEEL_DIA / 2.0   # 63.5 mm
    AXLE_Z = WHEEL_R            # 63.5 mm above ground
    PLATE_W = 85.0              # 3.35 in plate width
    PLATE_L = 100.0             # 3.94 in plate length
    PLATE_T = 4.0               # 4 mm plate thickness
    FORK_T = 3.5                # 3.5 mm formed leg thickness
    HUB_W = 40.0                # Hub width
    LEG_SPACING = HUB_W + 10.0  # 50.0 mm
    OVERALL_H = 150.0           # Top of mounting plate
    PLATE_BOT_Z = OVERALL_H - PLATE_T # 146.0 mm
    SWIVEL_TRAIL = 25.0         # 25 mm trailing offset along Y

    # Swivel kingpin centerline is at X=0, Y=0
    # Wheel axle center is at X=0, Y=+SWIVEL_TRAIL, Z=AXLE_Z

    # 1. Top Mounting Plate with 4 Bolt Heads
    top_plate = Part.makeBox(PLATE_W, PLATE_L, PLATE_T,
                             FreeCAD.Vector(-PLATE_W/2.0, -PLATE_L/2.0, PLATE_BOT_Z))
    for bx in [-28.0, 28.0]:
        for by in [-35.0, 35.0]:
            b_head = Part.makeCylinder(4.5, 5.0,
                                       FreeCAD.Vector(bx, by, PLATE_BOT_Z - 5.0),
                                       FreeCAD.Vector(0, 0, 1))
            top_plate = top_plate.fuse(b_head)

    # 2. Swivel Bearing Raceway & Fork Crown
    swivel_race = Part.makeCylinder(36.0, 8.0,
                                    FreeCAD.Vector(0, 0, PLATE_BOT_Z - 8.0),
                                    FreeCAD.Vector(0, 0, 1))
    fork_crown = Part.makeBox(LEG_SPACING + 2*FORK_T, 52.0, 6.0,
                              FreeCAD.Vector(-(LEG_SPACING + 2*FORK_T)/2.0, -26.0, PLATE_BOT_Z - 14.0))

    # 3. Angled Trailing Fork Legs
    dy = SWIVEL_TRAIL
    dz = (PLATE_BOT_Z - 14.0) - AXLE_Z
    arm_h = math.hypot(dy, dz) + 22.0
    angle = math.degrees(math.atan2(dy, dz))

    arm_l = Part.makeBox(FORK_T, 42.0, arm_h,
                         FreeCAD.Vector(-LEG_SPACING/2.0 - FORK_T, -21.0, AXLE_Z - 12.0))
    arm_l.rotate(FreeCAD.Vector(0, 0, PLATE_BOT_Z - 14.0), FreeCAD.Vector(1, 0, 0), -angle)

    arm_r = Part.makeBox(FORK_T, 42.0, arm_h,
                         FreeCAD.Vector(LEG_SPACING/2.0, -21.0, AXLE_Z - 12.0))
    arm_r.rotate(FreeCAD.Vector(0, 0, PLATE_BOT_Z - 14.0), FreeCAD.Vector(1, 0, 0), -angle)

    swivel_bracket_solid = top_plate.fuse(swivel_race).fuse(fork_crown).fuse(arm_l).fuse(arm_r)

    # 4. Foot Brake Lock Lever & Cam
    brake_tab = Part.makeBox(LEG_SPACING + 8.0, 36.0, 3.5,
                             FreeCAD.Vector(-(LEG_SPACING + 8.0)/2.0, SWIVEL_TRAIL + 20.0, AXLE_Z + 25.0))
    brake_tab.rotate(FreeCAD.Vector(0, SWIVEL_TRAIL + 20.0, AXLE_Z + 25.0), FreeCAD.Vector(1, 0, 0), 32.0)
    paddle = Part.makeBox(32.0, 22.0, 4.0,
                          FreeCAD.Vector(-16.0, SWIVEL_TRAIL + 42.0, AXLE_Z + 40.0))
    brake_assembly = brake_tab.fuse(paddle)

    # 5. Axle Hardware (Centered at X=0, Y=SWIVEL_TRAIL, Z=AXLE_Z)
    axle_len = LEG_SPACING + 2*FORK_T + 22.0
    axle_rod = Part.makeCylinder(4.76, axle_len,
                                 FreeCAD.Vector(-axle_len/2.0, SWIVEL_TRAIL, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    hex_head = Part.makeBox(7.0, 16.0, 16.0,
                            FreeCAD.Vector(-axle_len/2.0, SWIVEL_TRAIL - 8.0, AXLE_Z - 8.0))
    hex_nut = Part.makeBox(7.0, 16.0, 16.0,
                           FreeCAD.Vector(axle_len/2.0 - 7.0, SWIVEL_TRAIL - 8.0, AXLE_Z - 8.0))
    washer_l = Part.makeCylinder(10.0, 2.5,
                                 FreeCAD.Vector(-LEG_SPACING/2.0 - FORK_T - 2.5, SWIVEL_TRAIL, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    washer_r = Part.makeCylinder(10.0, 2.5,
                                 FreeCAD.Vector(LEG_SPACING/2.0 + FORK_T, SWIVEL_TRAIL, AXLE_Z),
                                 FreeCAD.Vector(1, 0, 0))
    axle_solid = axle_rod.fuse(hex_head).fuse(hex_nut).fuse(washer_l).fuse(washer_r)

    # Apply placement
    swivel_bracket_solid.Placement = placement
    brake_assembly.Placement = placement
    axle_solid.Placement = placement

    obj_bracket = doc.addObject("Part::Feature", "Swivel_Caster_Bracket")
    obj_bracket.Label = "Heavy-Duty Swivel Caster Plate & Fork Bracket"
    obj_bracket.Shape = swivel_bracket_solid
    grp.addObject(obj_bracket)
    apply_material(obj_bracket, "Steel-ZincPlated")

    obj_brake = doc.addObject("Part::Feature", "Caster_Brake_Lever")
    obj_brake.Label = "Foot-Lock Caster Brake Pedal & Lock Tab"
    obj_brake.Shape = brake_assembly
    grp.addObject(obj_brake)
    apply_material(obj_brake, "Steel-ZincPlated")

    obj_axle = doc.addObject("Part::Feature", "Swivel_Caster_Axle_Hardware")
    obj_axle.Label = "Grade 5 3/8in Axle Bolt, Washers & Nut"
    obj_axle.Shape = axle_solid
    grp.addObject(obj_axle)
    apply_material(obj_axle, "Steel-ZincPlated")

    # 6. Import Atomic 5.0" Caster Wheel at trailing axle center
    wheel_center = FreeCAD.Vector(0, SWIVEL_TRAIL, AXLE_Z)
    combined_placement = placement.multiply(FreeCAD.Placement(wheel_center, FreeCAD.Rotation()))
    wheel_comp = import_component(doc, "caster_wheel_5in", placement=combined_placement)
    if wheel_comp:
        grp.addObject(wheel_comp)

    return grp
