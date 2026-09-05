"""
Solaronics High-Intensity Ceramic Infrared Burner Component
Standalone 3D Parametric CAD Module

This module provides `create_solaronics_infrared_burner_component(doc, placement)` to model
the Solaronics cordierite grooved ceramic plaque matrix, deep parabolic focusing aluminum reflector,
Inconel re-radiating wire grid, rear venturi pre-mix manifold, and mounting brackets.
"""

import os
import sys
import math
import FreeCAD
import Part

from phi_works.maker.materials import apply_material
 
def create_solaronics_infrared_burner_component(doc, placement=None):
    """
    Creates Solaronics Infrared Burner assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing Solaronics burner sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Solaronics_Infrared_Burner")
    grp.Label = "Solaronics 60,000 BTU High-Intensity Ceramic Infrared Burner & Parabolic Reflector"

    # Core Dimensions (Metric mm / Imperial in)
    # Radiating surface: 173 sq in (~315 mm W x 355 mm L)
    PLAQUE_W = 315.0        # 12.4 in width
    PLAQUE_L = 355.0        # 14.0 in length
    PLAQUE_T = 12.7         # 0.5 in tile thickness
    
    # Parabolic Reflector Dimensions
    REFL_BASE_W = 345.0     # 13.58 in lower reflector mouth width
    REFL_BASE_L = 385.0     # 15.16 in lower reflector mouth length
    REFL_TOP_W = 200.0      # Top throat width
    REFL_TOP_L = 240.0      # Top throat length
    REFL_H = 110.0          # 4.33 in reflector height
    SHEET_T = 1.2           # Aluminum reflector gauge

    # 1. Cordierite Ceramic Plaque Matrix (Emitting Plane at Z = 0 to Z = PLAQUE_T)
    plaque_base = Part.makeBox(PLAQUE_W, PLAQUE_L, PLAQUE_T, FreeCAD.Vector(-PLAQUE_W/2, -PLAQUE_L/2, 0))
    # Simulated ceramic grooved texture slots
    slots = []
    slot_pitch = 25.0
    for y_s in range(int(-PLAQUE_L/2 + 20), int(PLAQUE_L/2 - 20), int(slot_pitch)):
        slot = Part.makeBox(PLAQUE_W - 20.0, 3.0, 2.0, FreeCAD.Vector(-PLAQUE_W/2 + 10.0, y_s, -0.5))
        slots.append(slot)
    
    ceramic_plaque_shape = plaque_base
    for s in slots[:12]:
        ceramic_plaque_shape = ceramic_plaque_shape.cut(s)

    # 2. Inconel Re-Radiating Wire Grid (Over Ceramic Face at Z = -2.0 mm)
    grid_frame_w = PLAQUE_W + 10.0
    grid_frame_l = PLAQUE_L + 10.0
    grid_outer = Part.makeBox(grid_frame_w, grid_frame_l, 3.0, FreeCAD.Vector(-grid_frame_w/2, -grid_frame_l/2, -3.0))
    grid_inner = Part.makeBox(grid_frame_w - 16.0, grid_frame_l - 16.0, 4.0, FreeCAD.Vector(-grid_frame_w/2 + 8.0, -grid_frame_l/2 + 8.0, -3.5))
    grid_border = grid_outer.cut(grid_inner)
    
    # Grid Mesh Cross Wires
    mesh_wires = []
    for wx in range(int(-grid_frame_w/2 + 25), int(grid_frame_w/2 - 20), 30):
        wire_x = Part.makeCylinder(1.0, grid_frame_l - 16.0, FreeCAD.Vector(wx, -grid_frame_l/2 + 8.0, -1.5), FreeCAD.Vector(0, 1, 0))
        mesh_wires.append(wire_x)
    for wy in range(int(-grid_frame_l/2 + 25), int(grid_frame_l/2 - 20), 30):
        wire_y = Part.makeCylinder(1.0, grid_frame_w - 16.0, FreeCAD.Vector(-grid_frame_w/2 + 8.0, wy, -1.5), FreeCAD.Vector(1, 0, 0))
        mesh_wires.append(wire_y)
    
    wire_grid_shape = grid_border
    for mw in mesh_wires:
        wire_grid_shape = wire_grid_shape.fuse(mw)

    # 3. Deep Parabolic Focusing Reflector Hood (Lofted Aluminum Shell)
    # Lower perimeter at Z = -15 mm
    p_b0 = FreeCAD.Vector(-REFL_BASE_W/2, -REFL_BASE_L/2, -15.0)
    p_b1 = FreeCAD.Vector(REFL_BASE_W/2, -REFL_BASE_L/2, -15.0)
    p_b2 = FreeCAD.Vector(REFL_BASE_W/2, REFL_BASE_L/2, -15.0)
    p_b3 = FreeCAD.Vector(-REFL_BASE_W/2, REFL_BASE_L/2, -15.0)

    # Mid throat perimeter at Z = REFL_H/2
    REFL_MID_W = (REFL_BASE_W + REFL_TOP_W) / 2.0 - 15.0  # Parabolic curve pull
    REFL_MID_L = (REFL_BASE_L + REFL_TOP_L) / 2.0 - 15.0
    p_m0 = FreeCAD.Vector(-REFL_MID_W/2, -REFL_MID_L/2, REFL_H * 0.4)
    p_m1 = FreeCAD.Vector(REFL_MID_W/2, -REFL_MID_L/2, REFL_H * 0.4)
    p_m2 = FreeCAD.Vector(REFL_MID_W/2, REFL_MID_L/2, REFL_H * 0.4)
    p_m3 = FreeCAD.Vector(-REFL_MID_W/2, REFL_MID_L/2, REFL_H * 0.4)

    # Top throat perimeter at Z = REFL_H
    p_t0 = FreeCAD.Vector(-REFL_TOP_W/2, -REFL_TOP_L/2, REFL_H)
    p_t1 = FreeCAD.Vector(REFL_TOP_W/2, -REFL_TOP_L/2, REFL_H)
    p_t2 = FreeCAD.Vector(REFL_TOP_W/2, REFL_TOP_L/2, REFL_H)
    p_t3 = FreeCAD.Vector(-REFL_TOP_W/2, REFL_TOP_L/2, REFL_H)

    poly_base = Part.makePolygon([p_b0, p_b1, p_b2, p_b3, p_b0])
    poly_mid = Part.makePolygon([p_m0, p_m1, p_m2, p_m3, p_m0])
    poly_top = Part.makePolygon([p_t0, p_t1, p_t2, p_t3, p_t0])

    refl_outer = Part.makeLoft([poly_base, poly_mid, poly_top], True)

    # Inner cutout for thin sheet shell
    p_in_b0 = FreeCAD.Vector(-REFL_BASE_W/2 + SHEET_T, -REFL_BASE_L/2 + SHEET_T, -15.1)
    p_in_b1 = FreeCAD.Vector(REFL_BASE_W/2 - SHEET_T, -REFL_BASE_L/2 + SHEET_T, -15.1)
    p_in_b2 = FreeCAD.Vector(REFL_BASE_W/2 - SHEET_T, REFL_BASE_L/2 - SHEET_T, -15.1)
    p_in_b3 = FreeCAD.Vector(-REFL_BASE_W/2 + SHEET_T, REFL_BASE_L/2 - SHEET_T, -15.1)

    p_in_t0 = FreeCAD.Vector(-REFL_TOP_W/2 + SHEET_T, -REFL_TOP_L/2 + SHEET_T, REFL_H + 0.1)
    p_in_t1 = FreeCAD.Vector(REFL_TOP_W/2 - SHEET_T, -REFL_TOP_L/2 + SHEET_T, REFL_H + 0.1)
    p_in_t2 = FreeCAD.Vector(REFL_TOP_W/2 - SHEET_T, REFL_TOP_L/2 - SHEET_T, REFL_H + 0.1)
    p_in_t3 = FreeCAD.Vector(-REFL_TOP_W/2 + SHEET_T, REFL_TOP_L/2 - SHEET_T, REFL_H + 0.1)

    poly_in_b = Part.makePolygon([p_in_b0, p_in_b1, p_in_b2, p_in_b3, p_in_b0])
    poly_in_t = Part.makePolygon([p_in_t0, p_in_t1, p_in_t2, p_in_t3, p_in_t0])
    refl_inner = Part.makeLoft([poly_in_b, poly_in_t], True)

    reflector_shape = refl_outer.cut(refl_inner)

    # Outer mounting flange lip
    flange_lip_w = REFL_BASE_W + 30.0
    flange_lip_l = REFL_BASE_L + 30.0
    lip_outer = Part.makeBox(flange_lip_w, flange_lip_l, 2.0, FreeCAD.Vector(-flange_lip_w/2, -flange_lip_l/2, -15.0))
    lip_inner = Part.makeBox(REFL_BASE_W, REFL_BASE_L, 3.0, FreeCAD.Vector(-REFL_BASE_W/2, -REFL_BASE_L/2, -15.5))
    reflector_flange = lip_outer.cut(lip_inner)
    reflector_shape = reflector_shape.fuse(reflector_flange)

    # 4. Cast Iron / Steel Venturi Manifold & Premix Chamber (Rear/Top of ceramic plaque)
    MANI_W = PLAQUE_W - 40.0
    MANI_L = PLAQUE_L - 40.0
    MANI_H = 45.0
    manifold_box = Part.makeBox(MANI_W, MANI_L, MANI_H, FreeCAD.Vector(-MANI_W/2, -MANI_L/2, PLAQUE_T))
    
    # Venturi Air Mixing Tube extending rearward (+Y direction)
    VENTURI_DIA = 38.1     # 1.5 in OD venturi mixing tube
    VENTURI_LEN = 110.0
    venturi_tube = Part.makeCylinder(VENTURI_DIA/2, VENTURI_LEN, FreeCAD.Vector(0, MANI_L/2, PLAQUE_T + MANI_H/2), FreeCAD.Vector(0, 1, 0))
    
    # Air Shutter Cone
    cone_outer = Part.makeCone(VENTURI_DIA/2 + 8.0, VENTURI_DIA/2, 25.0, FreeCAD.Vector(0, MANI_L/2 + VENTURI_LEN - 35.0, PLAQUE_T + MANI_H/2), FreeCAD.Vector(0, 1, 0))
    
    manifold_shape = manifold_box.fuse(venturi_tube).fuse(cone_outer)

    # 5. Brass Gas Orifice & 1/2" NPT Inlet Fitting
    ORIFICE_HEX = 22.0
    ORIFICE_LEN = 35.0
    brass_body = Part.makeCylinder(ORIFICE_HEX/2, ORIFICE_LEN, FreeCAD.Vector(0, MANI_L/2 + VENTURI_LEN, PLAQUE_T + MANI_H/2), FreeCAD.Vector(0, 1, 0))
    gas_inlet = Part.makeCylinder(10.5, 20.0, FreeCAD.Vector(0, MANI_L/2 + VENTURI_LEN + ORIFICE_LEN, PLAQUE_T + MANI_H/2), FreeCAD.Vector(0, 1, 0))
    brass_orifice_shape = brass_body.fuse(gas_inlet)

    # 6. Spark Ignition Electrode & Insulator
    elec_insulator = Part.makeCylinder(6.0, 30.0, FreeCAD.Vector(-PLAQUE_W/2 + 30.0, -PLAQUE_L/2 + 30.0, PLAQUE_T), FreeCAD.Vector(0, 0, -1))
    elec_tip = Part.makeCylinder(1.2, 12.0, FreeCAD.Vector(-PLAQUE_W/2 + 30.0, -PLAQUE_L/2 + 30.0, PLAQUE_T - 30.0), FreeCAD.Vector(1, 0, 0))
    electrode_shape = elec_insulator.fuse(elec_tip)

    # Transform all shapes according to placement
    ceramic_plaque_shape.Placement = placement
    wire_grid_shape.Placement = placement
    reflector_shape.Placement = placement
    manifold_shape.Placement = placement
    brass_orifice_shape.Placement = placement
    electrode_shape.Placement = placement

    # Create Document Objects
    obj_plaque = doc.addObject("Part::Feature", "Solaronics_Ceramic_Plaque")
    obj_plaque.Label = "Cordierite Grooved Ceramic Radiant Plaque (1,800 F)"
    obj_plaque.Shape = ceramic_plaque_shape
    grp.addObject(obj_plaque)
    apply_material(obj_plaque, "Ceramic-Cordierite")

    obj_grid = doc.addObject("Part::Feature", "Solaronics_Wire_Grid")
    obj_grid.Label = "Inconel / 304 SS Re-Radiating Wire Grid Screen"
    obj_grid.Shape = wire_grid_shape
    grp.addObject(obj_grid)
    apply_material(obj_grid, "Steel-304Stainless")

    obj_refl = doc.addObject("Part::Feature", "Solaronics_Parabolic_Reflector")
    obj_refl.Label = "Mirror-Bright Aluminum Parabolic Focusing Reflector"
    obj_refl.Shape = reflector_shape
    grp.addObject(obj_refl)
    apply_material(obj_refl, "Aluminum-6061-T6")

    obj_mani = doc.addObject("Part::Feature", "Solaronics_Venturi_Manifold")
    obj_mani.Label = "Premix Venturi Induction Manifold"
    obj_mani.Shape = manifold_shape
    grp.addObject(obj_mani)
    apply_material(obj_mani, "CastIron-Gray")

    obj_brass = doc.addObject("Part::Feature", "Solaronics_Brass_Gas_Inlet")
    obj_brass.Label = "Precision Brass Orifice & 1/2in Gas Inlet"
    obj_brass.Shape = brass_orifice_shape
    grp.addObject(obj_brass)
    apply_material(obj_brass, "Brass-C360")

    obj_spark = doc.addObject("Part::Feature", "Solaronics_Ignition_Electrode")
    obj_spark.Label = "High-Voltage Ceramic Spark Electrode"
    obj_spark.Shape = electrode_shape
    grp.addObject(obj_spark)
    apply_material(obj_spark, "Ceramic-Alumina")

    return grp
