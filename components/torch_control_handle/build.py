"""
Torch Control Handle Component (Handle-Mounted Cockpit with Squeeze Lever & Piezo Igniter)
Standalone 3D Parametric CAD Module

This module provides `create_torch_control_handle_component(doc, placement)` to model the
ergonomic operator control station: master needle valve, dead-man turbo squeeze boost lever,
piezo push-button igniter, and 3/4" square tube clamp bracket.
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

def create_torch_control_handle_component(doc, placement=None):
    """
    Creates Torch Control Handle assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing handle sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Torch_Control_Handle")
    grp.Label = "Torch Operator Control Handle & Squeeze Cockpit"

    # Dimensions
    HANDLE_L = 160.0
    HANDLE_W = 28.0
    HANDLE_H = 42.0

    # 1. Blue Ergonomic Grip Body & Rubber Inlay
    grip_box = Part.makeBox(HANDLE_W, HANDLE_L, HANDLE_H, FreeCAD.Vector(-HANDLE_W/2, -HANDLE_L/2, -HANDLE_H/2))
    grip_chamfer = Part.makeBox(HANDLE_W + 4, 30.0, 30.0, FreeCAD.Vector(-HANDLE_W/2 - 2, HANDLE_L/2 - 20, HANDLE_H/2 - 15))
    grip_shell = grip_box.cut(grip_chamfer)
    
    # Top Rubber Inlay
    inlay = Part.makeBox(HANDLE_W - 6, HANDLE_L - 30, 4.0, FreeCAD.Vector(-HANDLE_W/2 + 3, -HANDLE_L/2 + 10, HANDLE_H/2 - 3))
    
    grip_shell.Placement = placement
    inlay.Placement = placement

    grip_obj = doc.addObject("Part::Feature", "Blue_Molded_Handle_Grip")
    grip_obj.Label = "Blue Ergonomic Molded Grip Housing"
    grip_obj.Shape = grip_shell
    grp.addObject(grip_obj)
    apply_material(grip_obj, "PowderCoat-IndustrialBlue")

    inlay_obj = doc.addObject("Part::Feature", "Rubber_Traction_Inlay")
    inlay_obj.Label = "Textured Rubber Top Palm Inlay"
    inlay_obj.Shape = inlay
    grp.addObject(inlay_obj)
    apply_material(inlay_obj, "Rubber-Solid")

    # 2. Brass Valve Manifold Body & Inlet/Outlet Hex Fittings
    valve_body = Part.makeBox(22.0, 45.0, 28.0, FreeCAD.Vector(-11.0, HANDLE_L/2 - 30.0, -14.0))
    rear_inlet = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(0, -HANDLE_L/2 - 20.0, 0), FreeCAD.Vector(0, 1, 0))
    inlet_hex = Part.makeBox(16.0, 12.0, 16.0, FreeCAD.Vector(-8.0, -HANDLE_L/2 - 15.0, -8.0))
    front_outlet = Part.makeCylinder(6.0, 25.0, FreeCAD.Vector(0, HANDLE_L/2 + 10.0, 0), FreeCAD.Vector(0, 1, 0))
    outlet_hex = Part.makeBox(15.0, 12.0, 15.0, FreeCAD.Vector(-7.5, HANDLE_L/2 + 10.0, -7.5))
    
    brass_manifold = valve_body.fuse(rear_inlet).fuse(inlet_hex).fuse(front_outlet).fuse(outlet_hex)
    brass_manifold.Placement = placement

    valve_obj = doc.addObject("Part::Feature", "Brass_Valve_Manifold_Core")
    valve_obj.Label = "Machined Brass Needle Valve Manifold Body"
    valve_obj.Shape = brass_manifold
    grp.addObject(valve_obj)
    apply_material(valve_obj, "Brass-C360")

    # 3. Fluted Pilot Flame Adjustment / Shut-off Knob
    knob_base = Part.makeCylinder(12.0, 14.0, FreeCAD.Vector(0, HANDLE_L/2 - 10.0, HANDLE_H/2), FreeCAD.Vector(0, 0, 1))
    knob_flute1 = Part.makeBox(28.0, 6.0, 14.2, FreeCAD.Vector(-14.0, HANDLE_L/2 - 13.0, HANDLE_H/2))
    knob_flute2 = Part.makeBox(6.0, 28.0, 14.2, FreeCAD.Vector(-3.0, HANDLE_L/2 - 24.0, HANDLE_H/2))
    knob_solid = knob_base.fuse(knob_flute1).fuse(knob_flute2)
    knob_solid.Placement = placement

    knob_obj = doc.addObject("Part::Feature", "Fluted_Pilot_Needle_Knob")
    knob_obj.Label = "Fluted Polymer Needle Valve Adjustment Knob"
    knob_obj.Shape = knob_solid
    grp.addObject(knob_obj)
    apply_material(knob_obj, "Plastic-ABS")

    # 4. Chrome Dead-Man Turbo Squeeze Boost Lever
    lever_arm = Part.makeBox(12.0, 130.0, 5.0, FreeCAD.Vector(-6.0, -HANDLE_L/2 + 10.0, -HANDLE_H/2 - 16.0))
    lever_hook = Part.makeBox(12.0, 15.0, 18.0, FreeCAD.Vector(-6.0, -HANDLE_L/2 + 5.0, -HANDLE_H/2 - 16.0))
    lever_pivot = Part.makeCylinder(4.0, 20.0, FreeCAD.Vector(-10.0, HANDLE_L/2 - 15.0, -HANDLE_H/2 - 5.0), FreeCAD.Vector(1, 0, 0))
    lever_solid = lever_arm.fuse(lever_hook).fuse(lever_pivot)
    lever_solid.Placement = placement

    lever_obj = doc.addObject("Part::Feature", "Turbo_Boost_Squeeze_Lever")
    lever_obj.Label = "Plated Dead-Man Turbo Boost Squeeze Lever"
    lever_obj.Shape = lever_solid
    grp.addObject(lever_obj)
    apply_material(lever_obj, "Steel-ZincPlated")

    # 5. Brass Piezo Igniter Barrel & Red Push Button
    piezo_barrel = Part.makeCylinder(9.0, 45.0, FreeCAD.Vector(HANDLE_W/2 + 10.0, HANDLE_L/2 - 20.0, 0), FreeCAD.Vector(0, 1, 0))
    piezo_btn = Part.makeCylinder(6.0, 10.0, FreeCAD.Vector(HANDLE_W/2 + 10.0, HANDLE_L/2 - 28.0, 0), FreeCAD.Vector(0, 1, 0))
    piezo_bracket = Part.makeBox(15.0, 12.0, 4.0, FreeCAD.Vector(HANDLE_W/2, HANDLE_L/2 - 10.0, -2.0))
    
    piezo_body = piezo_barrel.fuse(piezo_bracket)
    piezo_body.Placement = placement
    piezo_btn.Placement = placement

    piezo_body_obj = doc.addObject("Part::Feature", "Piezo_Igniter_Barrel")
    piezo_body_obj.Label = "Brass Piezo Igniter Mechanism Body"
    piezo_body_obj.Shape = piezo_body
    grp.addObject(piezo_body_obj)
    apply_material(piezo_body_obj, "Brass-C360")

    piezo_btn_obj = doc.addObject("Part::Feature", "Piezo_Push_Button_Red")
    piezo_btn_obj.Label = "High-Visibility Red Piezo Push Button"
    piezo_btn_obj.Shape = piezo_btn
    grp.addObject(piezo_btn_obj)
    apply_material(piezo_btn_obj, "PowderCoat-IndustrialRed")

    # 6. 3/4" Square Tube Frame Mounting Clamp Bracket
    clamp_body = Part.makeBox(30.0, 35.0, 25.4, FreeCAD.Vector(-HANDLE_W/2 - 26.0, -17.5, -12.7))
    tube_cutout = Part.makeBox(19.05, 37.0, 19.05, FreeCAD.Vector(-HANDLE_W/2 - 22.0, -18.5, -9.525))
    clamp_solid = clamp_body.cut(tube_cutout)
    clamp_solid.Placement = placement

    clamp_obj = doc.addObject("Part::Feature", "Square_Tube_Mounting_Clamp")
    clamp_obj.Label = "Stainless 3/4in Tube Frame Clamp Bracket"
    clamp_obj.Shape = clamp_solid
    grp.addObject(clamp_obj)
    apply_material(clamp_obj, "Steel-304Stainless")

    return grp

def build_standalone_component():
    doc_name = "torch_control_handle"
    doc = FreeCAD.newDocument(doc_name)
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    grp = create_torch_control_handle_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="Torch Control Handle Component Mass Report"))

    fc_path = os.path.join(comp_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, doc_name)
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fc_path, camera_type="Perspective")
    close_model(doc.Name)

if __name__ == "__main__":
    build_standalone_component()
    os._exit(0)
