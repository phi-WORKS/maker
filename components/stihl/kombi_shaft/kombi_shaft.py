"""
STIHL KombiSystem Standard Drive Shaft Component
Standalone 3D Parametric CAD Module

Standard drive shaft tube shared across STIHL KombiSystem straight-shaft attachments
(FS-KM trimmer, brush cutter, FH-KM power scythe, HT-KM pole pruner, FBD-KM bed redefiner):
- Outer Diameter: 25.4 mm (1.0") Aluminum Drive Tube
- Coupler Sleeve: 28.0 mm OD x 100 mm with alignment pin / locking hole
- Decal/Grip Zone: Molded grip collar & safety decal zone
- Standard Length: 850 mm (overall straight tube from coupler top to gearbox mount)
"""

import os
import sys
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_kombi_shaft_component(doc, length_mm=850.0, placement=None):
    """
    Creates the standard 25.4 mm (1.0") STIHL Kombi drive tube in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      length_mm: Float length of aluminum tube below the coupler (default: 850.0 mm)
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing shaft sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Drive_Shaft")
    grp.Label = "STIHL Kombi 25.4mm (1.0in) Aluminum Drive Shaft Tube"

    TUBE_OD = 25.4
    TUBE_R = TUBE_OD / 2.0  # 12.7 mm
    WALL_T = 1.65           # 16-gauge wall
    INNER_R = TUBE_R - WALL_T

    # Origin (0,0,0) is centered at the top of the insertion coupler sleeve
    # Shaft extends downwards along -Z
    COUPLER_LEN = 100.0
    COUPLER_OD = 28.6
    COUPLER_R = COUPLER_OD / 2.0

    # 1. Main Aluminum Drive Shaft Tube
    outer_tube = Part.makeCylinder(TUBE_R, length_mm, FreeCAD.Vector(0, 0, -length_mm), FreeCAD.Vector(0, 0, 1))
    inner_bore = Part.makeCylinder(INNER_R, length_mm + 2.0, FreeCAD.Vector(0, 0, -length_mm - 1.0), FreeCAD.Vector(0, 0, 1))
    shaft_solid = outer_tube.cut(inner_bore)

    # 2. Quick-Connect Coupler Sleeve & Locking Lug Collar
    sleeve_cyl = Part.makeCylinder(COUPLER_R, COUPLER_LEN, FreeCAD.Vector(0, 0, -COUPLER_LEN), FreeCAD.Vector(0, 0, 1))
    sleeve_bore = Part.makeCylinder(TUBE_R, COUPLER_LEN + 2.0, FreeCAD.Vector(0, 0, -COUPLER_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    sleeve_ring = sleeve_cyl.cut(sleeve_bore)
    # Alignment locking spring-pin / push button lug
    lock_pin = Part.makeCylinder(3.5, 6.0, FreeCAD.Vector(0, COUPLER_R - 1.0, -35.0), FreeCAD.Vector(0, 1, 0))
    coupler_solid = sleeve_ring.fuse(lock_pin)

    # 3. Molded Rubber/Polymer Grip & Decal Warning Collar
    grip_cyl = Part.makeCylinder(TUBE_R + 2.0, 140.0, FreeCAD.Vector(0, 0, -320.0), FreeCAD.Vector(0, 0, 1))
    grip_bore = Part.makeCylinder(TUBE_R, 142.0, FreeCAD.Vector(0, 0, -321.0), FreeCAD.Vector(0, 0, 1))
    grip_solid = grip_cyl.cut(grip_bore)

    # Apply placement
    shaft_solid.Placement = placement
    coupler_solid.Placement = placement
    grip_solid.Placement = placement

    obj_shaft = doc.addObject("Part::Feature", "Kombi_Aluminum_Tube")
    obj_shaft.Label = "25.4mm OD Seamless Drawn Aluminum Drive Shaft"
    obj_shaft.Shape = shaft_solid
    grp.addObject(obj_shaft)
    apply_material(obj_shaft, "Aluminum-6061-T6")

    obj_coupler = doc.addObject("Part::Feature", "Kombi_Coupler_Sleeve")
    obj_coupler.Label = "KombiSystem Quick-Connect Coupler Sleeve & Pin"
    obj_coupler.Shape = coupler_solid
    grp.addObject(obj_coupler)
    apply_material(obj_coupler, "Plastic-ABS")

    obj_grip = doc.addObject("Part::Feature", "Kombi_Shaft_Grip")
    obj_grip.Label = "Shaft Protective Grip & Warning Decal Collar"
    obj_grip.Shape = grip_solid
    grp.addObject(obj_grip)
    apply_material(obj_grip, "Rubber-Solid")

    return grp
