"""
STIHL KMA 200 R Cordless KombiEngine Power Head Component
Standalone 3D Parametric CAD Module

Features:
- High-Torque EC Brushless Electric Motor in STIHL Orange Housing
- AP-System Battery Housing in STIHL White Polymer with AP Battery Slot
- Removable STIHL AP 500 S Lithium-Ion Battery Pack
- Ergonomic Control Handle with safety interlock, variable throttle trigger, and LED display
- Adjustable Rubber-Coated Loop Handle (R) with barrier bar
- Quick-Release Tool Coupler Clamp Sleeve at Z = 0 mating datum
- Total Length: 960 mm (37.8")
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_stihl_kma200r_component(doc, placement=None):
    """
    Creates the STIHL KMA 200 R Power Head in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing power head sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "STIHL_KMA200R")
    grp.Label = "STIHL KMA 200 R AP-System KombiEngine Power Head"

    # 1. Quick-Release Tool Coupler at Z = 0
    # Receives the 25.4 mm (1.0") shaft of any Kombi attachment
    coupler_cyl = Part.makeCylinder(18.0, 70.0, FreeCAD.Vector(0, 0, -10.0), FreeCAD.Vector(0, 0, 1))
    coupler_bore = Part.makeCylinder(12.7, 72.0, FreeCAD.Vector(0, 0, -11.0), FreeCAD.Vector(0, 0, 1))
    coupler_clamp_lug = Part.makeBox(20.0, 16.0, 30.0, FreeCAD.Vector(0, -8.0, 15.0))
    coupler_knob = Part.makeCylinder(14.0, 16.0, FreeCAD.Vector(20.0, 0, 30.0), FreeCAD.Vector(1, 0, 0))
    coupler_solid = coupler_cyl.cut(coupler_bore).fuse(coupler_clamp_lug).fuse(coupler_knob)

    # 2. Main Aluminum Drive Shaft Tube
    # Extends from Z = 50 up into the motor housing at Z = 600
    tube_cyl = Part.makeCylinder(12.7, 560.0, FreeCAD.Vector(0, 0, 50.0), FreeCAD.Vector(0, 0, 1))
    tube_bore = Part.makeCylinder(11.0, 562.0, FreeCAD.Vector(0, 0, 49.0), FreeCAD.Vector(0, 0, 1))
    shaft_solid = tube_cyl.cut(tube_bore)

    # 3. Ergonomic Loop Handle (R) with Barrier Bar at Z = 260
    clamp_ring = Part.makeCylinder(17.0, 35.0, FreeCAD.Vector(0, 0, 245.0), FreeCAD.Vector(0, 0, 1))
    clamp_inner = Part.makeCylinder(12.7, 37.0, FreeCAD.Vector(0, 0, 244.0), FreeCAD.Vector(0, 0, 1))
    # Loop arch (oval profile extending upwards +Y)
    arch_outer = Part.makeBox(170.0, 110.0, 24.0, FreeCAD.Vector(-85.0, 12.0, 250.0))
    arch_inner = Part.makeBox(122.0, 75.0, 30.0, FreeCAD.Vector(-61.0, 24.0, 247.0))
    # Barrier bar extending downwards (-Y) to keep operator feet away from cutting head
    barrier_bar = Part.makeBox(22.0, 95.0, 24.0, FreeCAD.Vector(-11.0, -95.0, 250.0))
    loop_handle_solid = clamp_ring.cut(clamp_inner).fuse(arch_outer.cut(arch_inner)).fuse(barrier_bar)

    # 4. Control Grip Handle with Trigger at Z = 450 to 600
    grip_box = Part.makeBox(34.0, 52.0, 150.0, FreeCAD.Vector(-17.0, -26.0, 450.0))
    grip_bore = Part.makeCylinder(12.7, 152.0, FreeCAD.Vector(0, 0, 449.0), FreeCAD.Vector(0, 0, 1))
    # Throttle trigger on bottom (-Y)
    trigger = Part.makeBox(14.0, 22.0, 45.0, FreeCAD.Vector(-7.0, -42.0, 490.0))
    # Safety lockout lever on top (+Y)
    lockout = Part.makeBox(14.0, 10.0, 60.0, FreeCAD.Vector(-7.0, 24.0, 480.0))
    control_handle_solid = grip_box.cut(grip_bore).fuse(trigger).fuse(lockout)

    # 5. EC Brushless Motor Shroud (STIHL Orange) at Z = 600 to 780
    motor_box = Part.makeBox(110.0, 120.0, 180.0, FreeCAD.Vector(-55.0, -60.0, 600.0))
    motor_taper = Part.makeCone(55.0, 22.0, 60.0, FreeCAD.Vector(0, 0, 570.0), FreeCAD.Vector(0, 0, 1))
    # Motor intake cooling vents
    vent_cut1 = Part.makeBox(114.0, 8.0, 80.0, FreeCAD.Vector(-57.0, 35.0, 640.0))
    vent_cut2 = Part.makeBox(114.0, 8.0, 80.0, FreeCAD.Vector(-57.0, -43.0, 640.0))
    motor_housing_solid = motor_box.fuse(motor_taper).cut(vent_cut1).cut(vent_cut2)

    # 6. Rear Powerhead & AP Battery Bay (STIHL White) at Z = 780 to 960
    rear_box = Part.makeBox(116.0, 128.0, 180.0, FreeCAD.Vector(-58.0, -64.0, 780.0))
    # Battery slot cavity on top
    batt_slot = Part.makeBox(84.0, 108.0, 130.0, FreeCAD.Vector(-42.0, -54.0, 840.0))
    # Rear foot / support rest
    foot_rest = Part.makeBox(90.0, 30.0, 25.0, FreeCAD.Vector(-45.0, -60.0, 940.0))
    rear_housing_solid = rear_box.cut(batt_slot).fuse(foot_rest)

    # 7. STIHL AP 500 S Battery Pack (Plastic-ABS / Dark Charcoal) inserted in bay
    batt_body = Part.makeBox(80.0, 102.0, 120.0, FreeCAD.Vector(-40.0, -51.0, 845.0))
    latch_tab = Part.makeBox(30.0, 14.0, 12.0, FreeCAD.Vector(-15.0, 48.0, 955.0))
    battery_solid = batt_body.fuse(latch_tab)

    # Apply placement
    coupler_solid.Placement = placement
    shaft_solid.Placement = placement
    loop_handle_solid.Placement = placement
    control_handle_solid.Placement = placement
    motor_housing_solid.Placement = placement
    rear_housing_solid.Placement = placement
    battery_solid.Placement = placement

    # Add objects to document
    obj_coupler = doc.addObject("Part::Feature", "KMA_Tool_Coupler")
    obj_coupler.Label = "Quick-Release Tool Coupler Sleeve"
    obj_coupler.Shape = coupler_solid
    grp.addObject(obj_coupler)
    apply_material(obj_coupler, "CastIron-Gray")

    obj_shaft = doc.addObject("Part::Feature", "KMA_Shaft_Tube")
    obj_shaft.Label = "25.4mm Aluminum Upper Drive Tube"
    obj_shaft.Shape = shaft_solid
    grp.addObject(obj_shaft)
    apply_material(obj_shaft, "Aluminum-6061-T6")

    obj_loop = doc.addObject("Part::Feature", "KMA_Loop_Handle")
    obj_loop.Label = "Loop Handle (R) with Barrier Bar"
    obj_loop.Shape = loop_handle_solid
    grp.addObject(obj_loop)
    apply_material(obj_loop, "Rubber-Solid")

    obj_ctrl = doc.addObject("Part::Feature", "KMA_Control_Grip")
    obj_ctrl.Label = "Ergonomic Control Grip & Throttle Trigger"
    obj_ctrl.Shape = control_handle_solid
    grp.addObject(obj_ctrl)
    apply_material(obj_ctrl, "Plastic-ABS")

    obj_motor = doc.addObject("Part::Feature", "KMA_Motor_Housing")
    obj_motor.Label = "STIHL Orange EC Brushless Motor Shroud"
    obj_motor.Shape = motor_housing_solid
    grp.addObject(obj_motor)
    apply_material(obj_motor, "Plastic-StihlOrange")

    obj_rear = doc.addObject("Part::Feature", "KMA_Battery_Housing")
    obj_rear.Label = "STIHL White Powerhead & AP Battery Bay"
    obj_rear.Shape = rear_housing_solid
    grp.addObject(obj_rear)
    apply_material(obj_rear, "Plastic-StihlWhite")

    obj_batt = doc.addObject("Part::Feature", "KMA_AP500S_Battery")
    obj_batt.Label = "STIHL AP 500 S Lithium-Ion Battery Pack"
    obj_batt.Shape = battery_solid
    grp.addObject(obj_batt)
    apply_material(obj_batt, "Plastic-ABS")

    return grp
