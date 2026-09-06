"""
5.0" Commercial Caster Wheel Component
Standalone 3D Parametric CAD Module

Atomic commercial running gear component:
- Outer Diameter: 127.0 mm (5.0")
- Tread Width: 35.0 mm (1.38")
- Hub Width: 40.0 mm (1.57") across bearing faces
- Axle Bore: 9.525 mm (3/8") through-bore
- Hub Core: Molded Polyurethane core in safety yellow
- Tire: Solid non-marking molded industrial rubber tread
- Bearing Sleeve: Steel zinc-plated center bushing sleeve
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_caster_wheel_5in_component(doc, placement=None):
    """
    Creates the atomic 5.0" Caster Wheel in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing wheel sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Caster_Wheel_5in")
    grp.Label = "5.0\" Industrial Caster Wheel (Yellow Hub / Black Tread)"

    # Parametric Dimensions
    WHEEL_DIA = 127.0           # 5.0 in outer diameter
    WHEEL_R = WHEEL_DIA / 2.0   # 63.5 mm
    WHEEL_W = 35.0              # 1.38 in tread width
    HUB_DIA = 65.0              # 2.56 in hub diameter
    HUB_R = HUB_DIA / 2.0       # 32.5 mm
    HUB_W = 40.0                # 1.57 in hub width across bearings
    AXLE_DIA = 9.525            # 3/8 in axle bore diameter
    AXLE_R = AXLE_DIA / 2.0     # 4.76 mm
    SLEEVE_OD = 14.0            # Bushing sleeve OD

    # Wheel is centered at (0, 0, 0) with rotation axis along X:
    # 1. Solid Rubber Tire Tread (Rim cylinder cut by hub cylinder)
    tire_cyl = Part.makeCylinder(WHEEL_R, WHEEL_W, FreeCAD.Vector(-WHEEL_W/2.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    hub_void = Part.makeCylinder(HUB_R, WHEEL_W + 2.0, FreeCAD.Vector(-WHEEL_W/2.0 - 1.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    tread_core = tire_cyl.cut(hub_void)

    # 2. Polyurethane Hub Core (Extends laterally to HUB_W)
    hub_outer = Part.makeCylinder(HUB_R, HUB_W, FreeCAD.Vector(-HUB_W/2.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    sleeve_void = Part.makeCylinder(SLEEVE_OD/2.0, HUB_W + 2.0, FreeCAD.Vector(-HUB_W/2.0 - 1.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    pocket_l = Part.makeCylinder(HUB_R - 5.0, 4.0, FreeCAD.Vector(-HUB_W/2.0 - 0.1, 0, 0), FreeCAD.Vector(1, 0, 0))
    pocket_r = Part.makeCylinder(HUB_R - 5.0, 4.0, FreeCAD.Vector(HUB_W/2.0 - 3.9, 0, 0), FreeCAD.Vector(1, 0, 0))
    hub_core = hub_outer.cut(sleeve_void).cut(pocket_l).cut(pocket_r)

    # 3. Steel Axle Bushing Sleeve
    sleeve_outer = Part.makeCylinder(SLEEVE_OD/2.0, HUB_W + 1.0, FreeCAD.Vector(-HUB_W/2.0 - 0.5, 0, 0), FreeCAD.Vector(1, 0, 0))
    bore_void = Part.makeCylinder(AXLE_R, HUB_W + 4.0, FreeCAD.Vector(-HUB_W/2.0 - 2.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    bushing_sleeve = sleeve_outer.cut(bore_void)

    # Apply placement
    tread_core.Placement = placement
    hub_core.Placement = placement
    bushing_sleeve.Placement = placement

    # Create Document Objects
    obj_tire = doc.addObject("Part::Feature", "Wheel_Rubber_Tread")
    obj_tire.Label = "5.0\" Solid Industrial Rubber Tread"
    obj_tire.Shape = tread_core
    grp.addObject(obj_tire)
    apply_material(obj_tire, "Rubber-Solid")

    obj_hub = doc.addObject("Part::Feature", "Wheel_Hub_Core")
    obj_hub.Label = "High-Visibility Yellow Polyurethane Hub Core"
    obj_hub.Shape = hub_core
    grp.addObject(obj_hub)
    apply_material(obj_hub, "Polyurethane")

    obj_sleeve = doc.addObject("Part::Feature", "Wheel_Bushing_Sleeve")
    obj_sleeve.Label = "Zinc-Plated Steel 3/8in Bearing Bushing Sleeve"
    obj_sleeve.Shape = bushing_sleeve
    grp.addObject(obj_sleeve)
    apply_material(obj_sleeve, "Steel-ZincPlated")

    return grp
