"""
STIHL FBD-KM Bed Redefiner Component
Standalone 3D Parametric CAD Module

Features:
- Standard 25.4 mm (1.0") Aluminum Drive Tube (850 mm length)
- Heavy-Duty Right-Angle Cast Magnesium Gearbox with transverse axle journal
- White Polymer Guide Wheel Hub (Plastic-StihlWhite) with Solid Black Rubber Tire (Rubber-Solid)
  and zinc-plated wing-nut axle hardware on the right (+X) side
- 4-Tine Digging Rotor (Steel-A36) with 90-degree bent scoop tines (200 mm cutting diameter)
  on the left (-X) flowerbed edging side
- Contoured STIHL Orange Debris Deflector Shield (Plastic-StihlOrange) overarching the cutting rotor
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material
from phi_works.maker.components import import_component

def create_kombi_bed_redefiner_fbd_component(doc, placement=None):
    """
    Creates the authentic STIHL FBD-KM Bed Redefiner in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing bed redefiner sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_BedRedefiner_FBD")
    grp.Label = "STIHL FBD-KM Bed Redefiner"

    SHAFT_LEN = 850.0

    # 1. Mount Standard Drive Shaft Component
    shaft_comp = import_component(doc, "kombi_shaft", placement=placement)
    if shaft_comp:
        grp.addObject(shaft_comp)

    # 2. Right-Angle Cast Magnesium Gearbox at Z = -SHAFT_LEN
    gear_collar = Part.makeCylinder(17.0, 55.0, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    gear_body = Part.makeBox(60.0, 70.0, 65.0, FreeCAD.Vector(-30.0, -35.0, -SHAFT_LEN - 55.0))
    # Transverse axle housing along X-axis
    axle_tube = Part.makeCylinder(20.0, 120.0, FreeCAD.Vector(-60.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    # Outer bearing dome on blade side
    bearing_dome = Part.makeCylinder(24.0, 15.0, FreeCAD.Vector(-65.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    gearcase_solid = gear_collar.fuse(gear_body).fuse(axle_tube).fuse(bearing_dome)

    # 3. Guide Wheel on +X side (White Rim + Solid Black Rubber Tire)
    WHEEL_X = 35.0
    WHEEL_OD = 180.0
    WHEEL_R = WHEEL_OD / 2.0  # 90 mm
    RIM_OD = 135.0
    RIM_R = RIM_OD / 2.0      # 67.5 mm
    TIRE_W = 34.0

    # Solid rubber tire
    tire_outer = Part.makeCylinder(WHEEL_R, TIRE_W, FreeCAD.Vector(WHEEL_X, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    tire_inner = Part.makeCylinder(RIM_R, TIRE_W + 2.0, FreeCAD.Vector(WHEEL_X - 1.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    tire_solid = tire_outer.cut(tire_inner)

    # White polymer wheel hub
    hub_outer = Part.makeCylinder(RIM_R, TIRE_W - 4.0, FreeCAD.Vector(WHEEL_X + 2.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    hub_bore = Part.makeCylinder(10.0, TIRE_W + 10.0, FreeCAD.Vector(WHEEL_X - 2.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    hub_recess = Part.makeCylinder(RIM_R - 12.0, 10.0, FreeCAD.Vector(WHEEL_X + TIRE_W - 10.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    hub_solid = hub_outer.cut(hub_bore).cut(hub_recess)

    # Axle bolt & zinc-plated wing nut hardware
    axle_bolt = Part.makeCylinder(8.0, TIRE_W + 25.0, FreeCAD.Vector(WHEEL_X, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    wing1 = Part.makeBox(12.0, 24.0, 4.0, FreeCAD.Vector(WHEEL_X + TIRE_W + 5.0, -12.0, -SHAFT_LEN - 37.0))
    hardware_solid = axle_bolt.fuse(wing1)

    # 4. Bed Redefiner Digging Rotor on -X side (4-tine bent scoop rotor)
    ROTOR_X = -70.0
    ROTOR_R = 100.0 # 200 mm diameter
    tines = []
    center_hub = Part.makeCylinder(35.0, 10.0, FreeCAD.Vector(ROTOR_X - 10.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    tines.append(center_hub)

    for i, ang in enumerate([0, 90, 180, 270]):
        # Radial arm
        arm = Part.makeBox(4.0, 38.0, ROTOR_R - 25.0, FreeCAD.Vector(ROTOR_X - 4.0, -19.0, 0))
        arm.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), ang)
        arm.translate(FreeCAD.Vector(0, 0, -SHAFT_LEN - 35.0))
        
        # 90-degree bent scoop tip
        tip = Part.makeBox(35.0, 38.0, 4.0, FreeCAD.Vector(ROTOR_X - 39.0, -19.0, ROTOR_R - 4.0))
        tip.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), ang)
        tip.translate(FreeCAD.Vector(0, 0, -SHAFT_LEN - 35.0))
        
        tines.append(arm)
        tines.append(tip)

    rotor_solid = tines[0]
    for t in tines[1:]:
        rotor_solid = rotor_solid.fuse(t)

    # 5. STIHL Orange Contoured Debris Shield (Covering -X side)
    SHIELD_W = 120.0
    SHIELD_R = 135.0
    shield_cyl = Part.makeCylinder(SHIELD_R, SHIELD_W, FreeCAD.Vector(ROTOR_X - 45.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    shield_cut = Part.makeCylinder(SHIELD_R - 4.0, SHIELD_W + 4.0, FreeCAD.Vector(ROTOR_X - 47.0, 0, -SHAFT_LEN - 35.0), FreeCAD.Vector(1, 0, 0))
    shield_shell = shield_cyl.cut(shield_cut)

    # Cut hood to keep top and rear quarter
    cut_box = Part.makeBox(SHIELD_W + 10.0, SHIELD_R * 2.5, SHIELD_R * 2.5,
                           FreeCAD.Vector(ROTOR_X - 50.0, -SHIELD_R * 2.0, -SHAFT_LEN - 35.0 - SHIELD_R * 1.5))
    shield_hood = shield_shell.cut(cut_box)
    bracket = Part.makeBox(25.0, 45.0, 40.0, FreeCAD.Vector(-25.0, -22.5, -SHAFT_LEN - 45.0))
    shield_solid = shield_hood.fuse(bracket)

    # Apply placement
    gearcase_solid.Placement = placement
    tire_solid.Placement = placement
    hub_solid.Placement = placement
    hardware_solid.Placement = placement
    rotor_solid.Placement = placement
    shield_solid.Placement = placement

    # Add objects to document
    obj_gear = doc.addObject("Part::Feature", "FBD_Gearcase")
    obj_gear.Label = "Right-Angle Cast Magnesium Gearbox"
    obj_gear.Shape = gearcase_solid
    grp.addObject(obj_gear)
    apply_material(obj_gear, "CastIron-Gray")

    obj_tire = doc.addObject("Part::Feature", "FBD_Guide_Tire")
    obj_tire.Label = "180mm Solid Rubber Guide Tire"
    obj_tire.Shape = tire_solid
    grp.addObject(obj_tire)
    apply_material(obj_tire, "Rubber-Solid")

    obj_hub = doc.addObject("Part::Feature", "FBD_Guide_Hub")
    obj_hub.Label = "STIHL White Guide Wheel Hub"
    obj_hub.Shape = hub_solid
    grp.addObject(obj_hub)
    apply_material(obj_hub, "Plastic-StihlWhite")

    obj_hw = doc.addObject("Part::Feature", "FBD_Axle_Hardware")
    obj_hw.Label = "Zinc-Plated Axle Bolt & Wing Nut"
    obj_hw.Shape = hardware_solid
    grp.addObject(obj_hw)
    apply_material(obj_hw, "Steel-ZincPlated")

    obj_rotor = doc.addObject("Part::Feature", "FBD_Digging_Rotor")
    obj_rotor.Label = "4-Tine Bent Scoop Edging Rotor"
    obj_rotor.Shape = rotor_solid
    grp.addObject(obj_rotor)
    apply_material(obj_rotor, "Steel-A36")

    obj_shield = doc.addObject("Part::Feature", "FBD_Deflector_Shield")
    obj_shield.Label = "STIHL Orange Debris Deflector Canopy"
    obj_shield.Shape = shield_solid
    grp.addObject(obj_shield)
    apply_material(obj_shield, "Plastic-StihlOrange")

    return grp
