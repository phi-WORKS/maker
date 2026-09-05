"""
Propane Bottle Harness Component (1 lb Canister Cage)
Standalone 3D Parametric CAD Module

This module provides `create_propane_harness_component(doc, placement)` to create a
quick-slip bike-cage-style bottle harness designed specifically for 1 lb propane cylinders
(3.875" / 98.4 mm outer diameter) and 3/4" square-tube handle mounting.
"""

import os
import sys
import math
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import apply_material, get_mass_properties, format_mass_report

def create_propane_harness_component(doc, placement=None):
    """
    Creates Propane Bottle Harness assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing harness sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Propane_Bottle_Harness")
    grp.Label = "Propane Bottle Harness Component (1 lb)"

    # Parametric Dimensions (Harness for 98.4 mm / 3.875" Cylinder)
    CYL_OD = 98.4
    CAGE_ID = 100.0       # 100 mm clear inner clearance
    CAGE_WALL = 3.175     # 1/8 in steel flat bar
    CAGE_OD = CAGE_ID + 2 * CAGE_WALL
    CAGE_H = 150.0        # Total cage height

    SPINE_W = 40.0        # Rear mounting spine width
    SPINE_T = 4.76        # 3/16 in thick spine plate
    SPINE_H = 180.0       # Rear spine height

    CLAMP_SQ = 19.05      # 3/4 in square tube clamp size
    CLAMP_THICK = 3.175

    # 1. Rear Mounting Spine & 3/4" Tube Clamps
    spine_box = Part.makeBox(SPINE_T, SPINE_W, SPINE_H, FreeCAD.Vector(-CAGE_OD/2 - SPINE_T, -SPINE_W/2, 0))
    
    # Upper & Lower 3/4" Square Tube Clamp Ears
    def make_tube_clamp(z_pos):
        clamp_body = Part.makeBox(CLAMP_SQ + 2*CLAMP_THICK, SPINE_W, 25.4, FreeCAD.Vector(-CAGE_OD/2 - SPINE_T - CLAMP_SQ - CLAMP_THICK, -SPINE_W/2, z_pos))
        tube_cutout = Part.makeBox(CLAMP_SQ, SPINE_W + 2, 25.6, FreeCAD.Vector(-CAGE_OD/2 - SPINE_T - CLAMP_SQ, -SPINE_W/2 - 1, z_pos - 0.1))
        return clamp_body.cut(tube_cutout)

    clamp_bottom = make_tube_clamp(15.0)
    clamp_top = make_tube_clamp(SPINE_H - 40.0)
    spine_assembly = spine_box.fuse(clamp_bottom).fuse(clamp_top)
    spine_assembly.Placement = placement

    spine_obj = doc.addObject("Part::Feature", "Harness_Rear_Mounting_Spine")
    spine_obj.Label = "Zinc-Plated Rear Mounting Spine & 3/4in Tube Clamps"
    spine_obj.Shape = spine_assembly
    grp.addObject(spine_obj)
    apply_material(spine_obj, "Steel-ZincPlated")

    # 2. Bottom Support Seat Cup
    seat_outer = Part.makeCylinder(CAGE_OD/2, 20.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    seat_inner = Part.makeCylinder(CAGE_ID/2, 20.2, FreeCAD.Vector(0, 0, 2.0), FreeCAD.Vector(0, 0, 1))
    seat_bottom_shelf = Part.makeCylinder(CAGE_OD/2, 2.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    seat_drain_hole = Part.makeCylinder(25.0, 3.0, FreeCAD.Vector(0, 0, -0.5), FreeCAD.Vector(0, 0, 1))
    
    seat_cup = seat_outer.cut(seat_inner).fuse(seat_bottom_shelf.cut(seat_drain_hole))
    seat_cup.Placement = placement

    seat_obj = doc.addObject("Part::Feature", "Bottom_Seat_Cup_Support")
    seat_obj.Label = "Powder-Coated Steel Bottom Support Seat Cup"
    seat_obj.Shape = seat_cup
    grp.addObject(seat_obj)
    apply_material(seat_obj, "PowderCoat-MatteBlack")

    # 3. Dual Vertical Side Retention Arms & Upper Ring
    arm_left = Part.makeBox(CAGE_WALL, 19.05, CAGE_H, FreeCAD.Vector(-10.0, -CAGE_OD/2 - CAGE_WALL, 0))
    arm_right = Part.makeBox(CAGE_WALL, 19.05, CAGE_H, FreeCAD.Vector(-10.0, CAGE_OD/2 - 19.05 + CAGE_WALL, 0))
    
    upper_ring_out = Part.makeCylinder(CAGE_OD/2, 18.0, FreeCAD.Vector(0, 0, CAGE_H - 18.0), FreeCAD.Vector(0, 0, 1))
    upper_ring_in = Part.makeCylinder(CAGE_ID/2, 18.2, FreeCAD.Vector(0, 0, CAGE_H - 18.1), FreeCAD.Vector(0, 0, 1))
    upper_hoop = upper_ring_out.cut(upper_ring_in)

    cage_arms_shape = arm_left.fuse(arm_right).fuse(upper_hoop)
    cage_arms_shape.Placement = placement

    arms_obj = doc.addObject("Part::Feature", "Retention_Arms_Upper_Hoop")
    arms_obj.Label = "Powder-Coated Steel Side Retention Arms & Hoop"
    arms_obj.Shape = cage_arms_shape
    grp.addObject(arms_obj)
    apply_material(arms_obj, "PowderCoat-MatteBlack")

    # 4. Quick-Release Thumb-Screw Latch Strap
    latch_block = Part.makeBox(15.0, 25.0, 20.0, FreeCAD.Vector(CAGE_OD/2, -12.5, CAGE_H - 25.0))
    latch_knob = Part.makeCylinder(10.0, 12.0, FreeCAD.Vector(CAGE_OD/2 + 15.0, 0, CAGE_H - 15.0), FreeCAD.Vector(1, 0, 0))
    
    latch_shape = latch_block.fuse(latch_knob)
    latch_shape.Placement = placement

    latch_obj = doc.addObject("Part::Feature", "Quick_Release_Latch_Knob")
    latch_obj.Label = "Red Quick-Release Retention Latch Knob"
    latch_obj.Shape = latch_shape
    grp.addObject(latch_obj)
    apply_material(latch_obj, "PowderCoat-IndustrialRed")

    return grp

def build_standalone_component():
    doc_name = "propane_harness"
    doc = FreeCAD.newDocument(doc_name)
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    grp = create_propane_harness_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="Propane Bottle Harness Mass Report"))

    fc_path = os.path.join(comp_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, doc_name)
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fc_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Propane harness build complete.")

if __name__ == "__main__":
    build_standalone_component()
    os._exit(0)
