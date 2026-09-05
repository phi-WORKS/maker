"""
Standard DOT 20 lb Propane Cylinder Component
Standalone 3D Parametric CAD Module

Features:
- 12.2" (310 mm) outer diameter steel pressure vessel with dished torispherical heads
- 8.0" (203 mm) bottom foot ring with ground drain ventilation slots
- 7.5" (190 mm) top protective valve collar with dual ergonomic carry handles
- Standard OPD (Overfill Protection Device) brass service valve with triangular shutoff knob
- 11" W.C. low-pressure regulator with pressure gauge and brass POL connector
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_propane_cylinder_20lb_component(doc, placement=None):
    """
    Creates standard 20 lb propane cylinder in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin at bottom of foot ring)
      
    Returns:
      App::DocumentObjectGroup containing cylinder subassemblies
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Propane_Cylinder_20lb")
    grp.Label = "Standard 20 lb DOT LP Propane Cylinder (OPD Valve & Regulator)"

    # Parametric Dimensions
    CYL_DIA = 310.0             # 12.2 in diameter
    CYL_R = CYL_DIA / 2.0       # 155.0 mm
    FOOT_R = 101.6              # 8.0 in dia foot ring (R = 4.0 in)
    FOOT_H = 38.1               # 1.5 in foot ring height
    FOOT_T = 3.2                # 1/8 in steel
    SHELL_H = 320.0             # Middle cylindrical shell height
    DOME_H = 55.0               # Dished head height top/bottom
    COLLAR_R = 95.0             # Top protective collar radius (7.5 in dia)
    COLLAR_H = 100.0            # 4.0 in collar height
    COLLAR_T = 3.2              # 1/8 in steel

    Z_foot_base = 0.0
    Z_shell_bot = FOOT_H + DOME_H
    Z_shell_top = Z_shell_bot + SHELL_H
    Z_tank_top = Z_shell_top + DOME_H

    # 1. Foot Ring Base with 4 drain slots
    foot_outer = Part.makeCylinder(FOOT_R, FOOT_H, FreeCAD.Vector(0, 0, Z_foot_base), FreeCAD.Vector(0, 0, 1))
    foot_inner = Part.makeCylinder(FOOT_R - FOOT_T, FOOT_H + 2.0, FreeCAD.Vector(0, 0, Z_foot_base - 1.0), FreeCAD.Vector(0, 0, 1))
    foot_ring = foot_outer.cut(foot_inner)

    # 4 Drain slots around bottom edge
    for i in range(4):
        ang = i * 90.0
        slot_box = Part.makeBox(20.0, 30.0, 12.0, FreeCAD.Vector(-10.0, FOOT_R - 15.0, Z_foot_base))
        slot_box.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), ang)
        foot_ring = foot_ring.cut(slot_box)

    # 2. Lower Dished Dome (approximated by truncated cone + cylinder with wall thickness)
    WALL_T = 2.4  # Standard DOT-4BA 240 cylinder ~0.095 in steel shell
    lower_dome_out = Part.makeCone(FOOT_R, CYL_R, DOME_H, FreeCAD.Vector(0, 0, FOOT_H), FreeCAD.Vector(0, 0, 1))
    lower_dome_in = Part.makeCone(FOOT_R - WALL_T, CYL_R - WALL_T, DOME_H + 2.0, FreeCAD.Vector(0, 0, FOOT_H - 1.0), FreeCAD.Vector(0, 0, 1))
    lower_dome = lower_dome_out.cut(lower_dome_in)

    # 3. Main Cylindrical Body Shell
    main_cyl_out = Part.makeCylinder(CYL_R, SHELL_H, FreeCAD.Vector(0, 0, Z_shell_bot), FreeCAD.Vector(0, 0, 1))
    main_cyl_in = Part.makeCylinder(CYL_R - WALL_T, SHELL_H + 2.0, FreeCAD.Vector(0, 0, Z_shell_bot - 1.0), FreeCAD.Vector(0, 0, 1))
    main_cyl = main_cyl_out.cut(main_cyl_in)

    # 4. Upper Dished Dome
    upper_dome_out = Part.makeCone(CYL_R, COLLAR_R, DOME_H, FreeCAD.Vector(0, 0, Z_shell_top), FreeCAD.Vector(0, 0, 1))
    upper_dome_in = Part.makeCone(CYL_R - WALL_T, COLLAR_R - WALL_T, DOME_H + 2.0, FreeCAD.Vector(0, 0, Z_shell_top - 1.0), FreeCAD.Vector(0, 0, 1))
    upper_dome = upper_dome_out.cut(upper_dome_in)

    # 5. Top Protective Collar with 2 Hand Grips
    collar_outer = Part.makeCylinder(COLLAR_R, COLLAR_H, FreeCAD.Vector(0, 0, Z_tank_top - 15.0), FreeCAD.Vector(0, 0, 1))
    collar_inner = Part.makeCylinder(COLLAR_R - COLLAR_T, COLLAR_H + 2.0, FreeCAD.Vector(0, 0, Z_tank_top - 16.0), FreeCAD.Vector(0, 0, 1))
    collar_ring = collar_outer.cut(collar_inner)

    # Dual Oblong Hand Grip Slots
    grip_l = Part.makeBox(75.0, 30.0, 28.0, FreeCAD.Vector(-37.5, COLLAR_R - 15.0, Z_tank_top + 45.0))
    grip_r = Part.makeBox(75.0, 30.0, 28.0, FreeCAD.Vector(-37.5, -COLLAR_R - 15.0, Z_tank_top + 45.0))
    collar_ring = collar_ring.cut(grip_l).cut(grip_r)

    tank_body = foot_ring.fuse(lower_dome).fuse(main_cyl).fuse(upper_dome).fuse(collar_ring)

    # 6. Brass OPD Service Valve & Handwheel
    Z_valve_base = Z_tank_top - 10.0
    v_boss = Part.makeCylinder(18.0, 25.0, FreeCAD.Vector(0, 0, Z_valve_base), FreeCAD.Vector(0, 0, 1))
    v_stem = Part.makeCylinder(9.0, 45.0, FreeCAD.Vector(0, 0, Z_valve_base + 25.0), FreeCAD.Vector(0, 0, 1))
    v_outlet = Part.makeCylinder(11.0, 30.0, FreeCAD.Vector(0, 0, Z_valve_base + 45.0), FreeCAD.Vector(0, 1, 0))
    valve_body = v_boss.fuse(v_stem).fuse(v_outlet)

    # Valve Handwheel (Triangular-lobed polymer knob)
    knob_core = Part.makeCylinder(22.0, 14.0, FreeCAD.Vector(0, 0, Z_valve_base + 70.0), FreeCAD.Vector(0, 0, 1))

    # 7. Low-Pressure LP Gas Regulator & Pressure Gauge
    reg_body = Part.makeCylinder(32.0, 20.0, FreeCAD.Vector(0, 45.0, Z_valve_base + 45.0), FreeCAD.Vector(0, 1, 0))
    gauge_body = Part.makeCylinder(15.0, 12.0, FreeCAD.Vector(0, 45.0, Z_valve_base + 75.0), FreeCAD.Vector(0, 0, 1))
    hose_nipple = Part.makeCylinder(6.0, 25.0, FreeCAD.Vector(0, 75.0, Z_valve_base + 45.0), FreeCAD.Vector(0, 1, 0))
    reg_assembly = reg_body.fuse(gauge_body).fuse(hose_nipple)

    # Transform
    if placement is not None:
        tank_body.Placement = placement.multiply(tank_body.Placement)
        valve_body.Placement = placement.multiply(valve_body.Placement)
        knob_core.Placement = placement.multiply(knob_core.Placement)
        reg_assembly.Placement = placement.multiply(reg_assembly.Placement)

    # FreeCAD Document Objects
    obj_tank = doc.addObject("Part::Feature", "Propane_Tank_Vessel")
    obj_tank.Label = "20 lb Steel Pressure Vessel, Foot Ring & Collar"
    obj_tank.Shape = tank_body
    grp.addObject(obj_tank)
    apply_material(obj_tank, "PowderCoat-GlossWhite")

    obj_valve = doc.addObject("Part::Feature", "OPD_Valve_Body")
    obj_valve.Label = "Brass OPD Service Valve & Threaded Outlet"
    obj_valve.Shape = valve_body
    grp.addObject(obj_valve)
    apply_material(obj_valve, "Brass-C360")

    obj_knob = doc.addObject("Part::Feature", "Valve_Handwheel")
    obj_knob.Label = "Polymer Triangular Shutoff Handwheel"
    obj_knob.Shape = knob_core
    grp.addObject(obj_knob)
    apply_material(obj_knob, "Plastic-ABS")

    obj_reg = doc.addObject("Part::Feature", "LP_Gas_Regulator")
    obj_reg.Label = "11in W.C. Low-Pressure Gas Regulator & Gauge"
    obj_reg.Shape = reg_assembly
    grp.addObject(obj_reg)
    apply_material(obj_reg, "Steel-ZincPlated")

    return grp
