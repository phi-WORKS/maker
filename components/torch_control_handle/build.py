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

from phi_works.maker.render import export_orthogonal_views

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

    # Color Palette
    HF_BLUE = (0.10, 0.35, 0.80, 0.0)         # Molded Blue Grip Shell
    TORCH_BLACK = (0.15, 0.15, 0.15, 0.0)     # Rubber Grip Inlay & Fluted Valve Knob
    BRASS = (0.85, 0.65, 0.20, 0.0)           # Machined Brass Valve Body & Fittings
    CHROME = (0.75, 0.78, 0.82, 0.0)          # Squeeze Trigger Lever & Hardware
    IGNITER_RED = (0.85, 0.15, 0.15, 0.0)     # Push-Button Piezo Cap
    STEEL_CLAMP = (0.45, 0.48, 0.52, 0.0)     # 3/4" Tube Mounting Clamp

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
    grip_obj.Shape = grip_shell
    grp.addObject(grip_obj)

    inlay_obj = doc.addObject("Part::Feature", "Rubber_Traction_Inlay")
    inlay_obj.Shape = inlay
    grp.addObject(inlay_obj)

    # 2. Brass Valve Manifold Body & Inlet/Outlet Hex Fittings
    valve_body = Part.makeBox(22.0, 45.0, 28.0, FreeCAD.Vector(-11.0, HANDLE_L/2 - 30.0, -14.0))
    rear_inlet = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(0, -HANDLE_L/2 - 20.0, 0), FreeCAD.Vector(0, 1, 0))
    inlet_hex = Part.makeBox(16.0, 12.0, 16.0, FreeCAD.Vector(-8.0, -HANDLE_L/2 - 15.0, -8.0))
    front_outlet = Part.makeCylinder(6.0, 25.0, FreeCAD.Vector(0, HANDLE_L/2 + 10.0, 0), FreeCAD.Vector(0, 1, 0))
    outlet_hex = Part.makeBox(15.0, 12.0, 15.0, FreeCAD.Vector(-7.5, HANDLE_L/2 + 10.0, -7.5))
    
    brass_manifold = valve_body.fuse(rear_inlet).fuse(inlet_hex).fuse(front_outlet).fuse(outlet_hex)
    brass_manifold.Placement = placement

    valve_obj = doc.addObject("Part::Feature", "Brass_Valve_Manifold_Core")
    valve_obj.Shape = brass_manifold
    grp.addObject(valve_obj)

    # 3. Fluted Pilot Flame Adjustment / Shut-off Knob
    knob_base = Part.makeCylinder(12.0, 14.0, FreeCAD.Vector(0, HANDLE_L/2 - 10.0, HANDLE_H/2), FreeCAD.Vector(0, 0, 1))
    knob_flute1 = Part.makeBox(28.0, 6.0, 14.2, FreeCAD.Vector(-14.0, HANDLE_L/2 - 13.0, HANDLE_H/2))
    knob_flute2 = Part.makeBox(6.0, 28.0, 14.2, FreeCAD.Vector(-3.0, HANDLE_L/2 - 24.0, HANDLE_H/2))
    knob_solid = knob_base.fuse(knob_flute1).fuse(knob_flute2)
    knob_solid.Placement = placement

    knob_obj = doc.addObject("Part::Feature", "Fluted_Pilot_Needle_Knob")
    knob_obj.Shape = knob_solid
    grp.addObject(knob_obj)

    # 4. Chrome Dead-Man Turbo Squeeze Boost Lever
    lever_arm = Part.makeBox(12.0, 130.0, 5.0, FreeCAD.Vector(-6.0, -HANDLE_L/2 + 10.0, -HANDLE_H/2 - 16.0))
    lever_hook = Part.makeBox(12.0, 15.0, 18.0, FreeCAD.Vector(-6.0, -HANDLE_L/2 + 5.0, -HANDLE_H/2 - 16.0))
    lever_pivot = Part.makeCylinder(4.0, 20.0, FreeCAD.Vector(-10.0, HANDLE_L/2 - 15.0, -HANDLE_H/2 - 5.0), FreeCAD.Vector(1, 0, 0))
    lever_solid = lever_arm.fuse(lever_hook).fuse(lever_pivot)
    lever_solid.Placement = placement

    lever_obj = doc.addObject("Part::Feature", "Turbo_Boost_Squeeze_Lever")
    lever_obj.Shape = lever_solid
    grp.addObject(lever_obj)

    # 5. Brass Piezo Igniter Barrel & Red Push Button
    piezo_barrel = Part.makeCylinder(9.0, 45.0, FreeCAD.Vector(HANDLE_W/2 + 10.0, HANDLE_L/2 - 20.0, 0), FreeCAD.Vector(0, 1, 0))
    piezo_btn = Part.makeCylinder(6.0, 10.0, FreeCAD.Vector(HANDLE_W/2 + 10.0, HANDLE_L/2 - 28.0, 0), FreeCAD.Vector(0, 1, 0))
    piezo_bracket = Part.makeBox(15.0, 12.0, 4.0, FreeCAD.Vector(HANDLE_W/2, HANDLE_L/2 - 10.0, -2.0))
    
    piezo_body = piezo_barrel.fuse(piezo_bracket)
    piezo_body.Placement = placement
    piezo_btn.Placement = placement

    piezo_body_obj = doc.addObject("Part::Feature", "Piezo_Igniter_Barrel")
    piezo_body_obj.Shape = piezo_body
    grp.addObject(piezo_body_obj)

    piezo_btn_obj = doc.addObject("Part::Feature", "Piezo_Push_Button_Red")
    piezo_btn_obj.Shape = piezo_btn
    grp.addObject(piezo_btn_obj)

    # 6. 3/4" Square Tube Frame Mounting Clamp Bracket
    clamp_body = Part.makeBox(30.0, 35.0, 25.4, FreeCAD.Vector(-HANDLE_W/2 - 26.0, -17.5, -12.7))
    tube_cutout = Part.makeBox(19.05, 37.0, 19.05, FreeCAD.Vector(-HANDLE_W/2 - 22.0, -18.5, -9.525))
    clamp_solid = clamp_body.cut(tube_cutout)
    clamp_solid.Placement = placement

    clamp_obj = doc.addObject("Part::Feature", "Square_Tube_Mounting_Clamp")
    clamp_obj.Shape = clamp_solid
    grp.addObject(clamp_obj)

    # Apply colors
    if HAS_GUI and hasattr(FreeCADGui, "getDocument"):
        try:
            gui_d = FreeCADGui.getDocument(doc.Name)
            if gui_d:
                color_map = [
                    (grip_obj, HF_BLUE),
                    (inlay_obj, TORCH_BLACK),
                    (valve_obj, BRASS),
                    (knob_obj, TORCH_BLACK),
                    (lever_obj, CHROME),
                    (piezo_body_obj, BRASS),
                    (piezo_btn_obj, IGNITER_RED),
                    (clamp_obj, STEEL_CLAMP)
                ]
                for o, c in color_map:
                    g_o = gui_d.getObject(o.Name)
                    if g_o:
                        g_o.Visibility = True
                        g_o.ShapeColor = c
                        g_o.DisplayMode = "Flat Lines"
        except Exception:
            pass

    return grp

def build_standalone_component():
    doc = FreeCAD.newDocument("torch_control_handle_component")
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    create_torch_control_handle_component(doc)
    doc.recompute()

    fc_path = os.path.join(comp_dir, "torch_control_handle.FCStd")
    doc.saveAs(fc_path)
    print(f"Saved standalone torch control handle model: {fc_path}")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, "torch_control_handle")
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix="torch_control_handle")

    FreeCAD.closeDocument("torch_control_handle_component")

if __name__ == "__main__":
    build_standalone_component()
    sys.exit(0)
