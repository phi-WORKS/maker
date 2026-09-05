"""
2.5 Gallon Pressurized Water Safety Tank Component
Standalone 3D Parametric CAD Module

Features:
- 7.1" (180 mm) outer diameter high-density polyethylene (HDPE) pressure vessel in safety blue
- Integral bottom foot rim for stable deck and ground seating
- Top threaded pump neck with molded poly screw cap and pressure relief valve
- Ergonomic heavy-duty pump plunger T-handle
- Brass discharge outlet port and swivel connection
- Flexible reinforced coiled washdown/spray hose
- Brass shutoff wand and cone fog nozzle clipped to tank body
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_water_tank_component(doc, placement=None):
    """
    Creates standard 2.5 gallon pressurized water safety canister in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin at bottom center of base rim)
      
    Returns:
      App::DocumentObjectGroup containing water tank subassemblies
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Water_Tank_2_5Gal")
    grp.Label = "2.5 Gallon Pressurized Water Safety Spray Tank"

    # Parametric Dimensions
    TANK_DIA = 180.0            # 7.09 in diameter
    TANK_R = TANK_DIA / 2.0     # 90.0 mm
    SHELL_H = 300.0             # Cylindrical body height
    BASE_RIM_H = 20.0           # Base foot rim height
    BASE_RIM_T = 5.0            # Base foot rim thickness
    SHOULDER_H = 45.0           # Conical dome shoulder height
    NECK_R = 42.0               # Top neck radius
    NECK_H = 25.0               # Neck height
    WALL_T = 3.5                # HDPE wall thickness

    Z_base = 0.0
    Z_shell_bot = BASE_RIM_H
    Z_shell_top = Z_shell_bot + SHELL_H
    Z_shoulder_top = Z_shell_top + SHOULDER_H
    Z_neck_top = Z_shoulder_top + NECK_H

    # 1. Tank Pressure Vessel Body (Safety Blue HDPE)
    # A. Base Foot Rim (outer ring with inner relief)
    base_rim_out = Part.makeCylinder(TANK_R, BASE_RIM_H, FreeCAD.Vector(0, 0, Z_base), FreeCAD.Vector(0, 0, 1))
    base_rim_in = Part.makeCylinder(TANK_R - BASE_RIM_T, BASE_RIM_H - 3.0, FreeCAD.Vector(0, 0, Z_base - 1.0), FreeCAD.Vector(0, 0, 1))
    base_rim = base_rim_out.cut(base_rim_in)

    # B. Vessel Outer Shell
    bottom_head = Part.makeCylinder(TANK_R - BASE_RIM_T, WALL_T, FreeCAD.Vector(0, 0, BASE_RIM_H - WALL_T), FreeCAD.Vector(0, 0, 1))
    cyl_body_out = Part.makeCylinder(TANK_R, SHELL_H, FreeCAD.Vector(0, 0, Z_shell_bot), FreeCAD.Vector(0, 0, 1))
    shoulder_cone_out = Part.makeCone(TANK_R, NECK_R, SHOULDER_H, FreeCAD.Vector(0, 0, Z_shell_top), FreeCAD.Vector(0, 0, 1))
    neck_cyl_out = Part.makeCylinder(NECK_R, NECK_H, FreeCAD.Vector(0, 0, Z_shoulder_top), FreeCAD.Vector(0, 0, 1))
    vessel_outer = base_rim.fuse(bottom_head).fuse(cyl_body_out).fuse(shoulder_cone_out).fuse(neck_cyl_out)

    # C. Hollow Internal Cavity
    cyl_body_in = Part.makeCylinder(TANK_R - WALL_T, SHELL_H, FreeCAD.Vector(0, 0, Z_shell_bot), FreeCAD.Vector(0, 0, 1))
    shoulder_cone_in = Part.makeCone(TANK_R - WALL_T, NECK_R - WALL_T, SHOULDER_H, FreeCAD.Vector(0, 0, Z_shell_top), FreeCAD.Vector(0, 0, 1))
    neck_cyl_in = Part.makeCylinder(NECK_R - WALL_T, NECK_H + 2.0, FreeCAD.Vector(0, 0, Z_shoulder_top), FreeCAD.Vector(0, 0, 1))
    vessel_inner = cyl_body_in.fuse(shoulder_cone_in).fuse(neck_cyl_in)

    vessel_shape = vessel_outer.cut(vessel_inner)

    obj_vessel = doc.addObject("Part::Feature", "Water_Tank_Vessel_Body")
    obj_vessel.Label = "2.5 Gal Safety Blue HDPE Pressure Vessel"
    obj_vessel.Shape = vessel_shape
    obj_vessel.Placement = placement
    grp.addObject(obj_vessel)
    apply_material(obj_vessel, "Polyethylene-SafetyBlue")

    # 2. Pump Plunger Assembly & Screw Cap (Molded ABS / Poly)
    # A. Threaded Neck Cap
    CAP_R = NECK_R + 5.0
    CAP_H = 18.0
    cap_cyl = Part.makeCylinder(CAP_R, CAP_H, FreeCAD.Vector(0, 0, Z_neck_top - 5.0), FreeCAD.Vector(0, 0, 1))

    # B. Pump Plunger Central Shaft
    ROD_R = 9.0
    ROD_H = 55.0
    rod_cyl = Part.makeCylinder(ROD_R, ROD_H, FreeCAD.Vector(0, 0, Z_neck_top + CAP_H - 5.0), FreeCAD.Vector(0, 0, 1))

    # C. Ergonomic T-Handle Grip
    HANDLE_L = 120.0
    HANDLE_W = 28.0
    HANDLE_H = 24.0
    Z_handle = Z_neck_top + CAP_H - 5.0 + ROD_H
    handle_box = Part.makeBox(HANDLE_L, HANDLE_W, HANDLE_H, FreeCAD.Vector(-HANDLE_L/2.0, -HANDLE_W/2.0, Z_handle))
    
    # Rounded grip end reliefs
    relief_l = Part.makeCylinder(HANDLE_W/2.0, HANDLE_H + 2.0, FreeCAD.Vector(-HANDLE_L/2.0, 0, Z_handle - 1.0), FreeCAD.Vector(0, 0, 1))
    relief_r = Part.makeCylinder(HANDLE_W/2.0, HANDLE_H + 2.0, FreeCAD.Vector(HANDLE_L/2.0, 0, Z_handle - 1.0), FreeCAD.Vector(0, 0, 1))
    t_handle = handle_box.fuse(relief_l).fuse(relief_r)

    # D. Pressure Relief Valve & Finger Latch Button
    prv_cyl = Part.makeCylinder(8.0, 16.0, FreeCAD.Vector(25.0, 0, Z_neck_top + CAP_H - 6.0), FreeCAD.Vector(0, 0, 1))

    pump_shape = cap_cyl.fuse(rod_cyl).fuse(t_handle).fuse(prv_cyl)

    obj_pump = doc.addObject("Part::Feature", "Water_Tank_Pump_Assembly")
    obj_pump.Label = "Molded Plunger Pump Cap & T-Handle Assembly"
    obj_pump.Shape = pump_shape
    obj_pump.Placement = placement
    grp.addObject(obj_pump)
    apply_material(obj_pump, "Plastic-ABS")

    # 3. Brass Discharge Port & Fittings (Brass-C360)
    # Outlet boss on shoulder at Y = -TANK_R + 15
    boss_pos = FreeCAD.Vector(0, -TANK_R + 18.0, Z_shell_top + 15.0)
    brass_boss = Part.makeCylinder(10.0, 22.0, boss_pos, FreeCAD.Vector(0, -1, 0.3).normalize())
    brass_nut = Part.makeBox(18.0, 10.0, 18.0, FreeCAD.Vector(-9.0, -TANK_R - 5.0, Z_shell_top + 6.0))
    
    # Wand brass tip
    wand_pos = FreeCAD.Vector(TANK_R + 12.0, 0, Z_shell_bot + 40.0)
    wand_brass_nozzle = Part.makeCone(7.0, 4.0, 20.0, wand_pos, FreeCAD.Vector(0, 0, 1))
    brass_fittings = brass_boss.fuse(brass_nut).fuse(wand_brass_nozzle)

    obj_brass = doc.addObject("Part::Feature", "Water_Tank_Brass_Fittings")
    obj_brass.Label = "Brass Discharge Swivel Port & Spray Nozzle"
    obj_brass.Shape = brass_fittings
    obj_brass.Placement = placement
    grp.addObject(obj_brass)
    apply_material(obj_brass, "Brass-C360")

    # 4. Flexible Coiled Discharge Spray Hose (Rubber-Solid)
    # Coiled neatly around the upper body of the vessel
    HOSE_R = TANK_R + 14.0
    HOSE_TUBE_R = 5.0
    coil_1 = Part.makeTorus(HOSE_R, HOSE_TUBE_R, FreeCAD.Vector(0, 0, Z_shell_bot + 210.0), FreeCAD.Vector(0, 0, 1))
    coil_2 = Part.makeTorus(HOSE_R, HOSE_TUBE_R, FreeCAD.Vector(0, 0, Z_shell_bot + 225.0), FreeCAD.Vector(0, 0, 1))
    hose_shape = coil_1.fuse(coil_2)

    obj_hose = doc.addObject("Part::Feature", "Water_Tank_Spray_Hose")
    obj_hose.Label = "Reinforced Flexible Spray Washdown Hose"
    obj_hose.Shape = hose_shape
    obj_hose.Placement = placement
    grp.addObject(obj_hose)
    apply_material(obj_hose, "Rubber-Solid")

    # 5. Spray Wand & Clip Assembly (Plastic-ABS / Aluminum)
    # Wand tube extending vertically along the side of the tank
    wand_tube = Part.makeCylinder(4.5, 260.0, wand_pos + FreeCAD.Vector(0, 0, 20.0), FreeCAD.Vector(0, 0, 1))
    wand_trigger = Part.makeBox(12.0, 25.0, 45.0, FreeCAD.Vector(TANK_R + 6.0, -12.5, Z_shell_bot + 270.0))
    wand_clip_upper = Part.makeBox(16.0, 12.0, 18.0, FreeCAD.Vector(TANK_R - 2.0, -6.0, Z_shell_bot + 240.0))
    wand_clip_lower = Part.makeBox(16.0, 12.0, 18.0, FreeCAD.Vector(TANK_R - 2.0, -6.0, Z_shell_bot + 80.0))
    wand_assembly = wand_tube.fuse(wand_trigger).fuse(wand_clip_upper).fuse(wand_clip_lower)

    obj_wand = doc.addObject("Part::Feature", "Water_Tank_Spray_Wand")
    obj_wand.Label = "Safety Washdown Spray Wand & Side Clip Holster"
    obj_wand.Shape = wand_assembly
    obj_wand.Placement = placement
    grp.addObject(obj_wand)
    apply_material(obj_wand, "Plastic-ABS")

    return grp
