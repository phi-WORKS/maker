"""
Harbor Freight Propane Torch with Push-Button Igniter (Item #91037)
Standalone CAD Component Module

This module provides a function `create_torch_component(doc, insertion_point, lean_angle_deg, flame_angle_deg)`
that creates the Harbor Freight #91037 torch as a grouped subassembly inside any FreeCAD document.
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

def create_torch_component(doc, insertion_point=None, lean_angle_deg=0.0, flame_angle_deg=0.0):
    """
    Creates Harbor Freight #91037 Propane Torch assembly in `doc`.
    By default, modeled along canonical vertical axis (0, 0, 1) with collinear handle,
    valve, chrome wand shaft, and flaring burner bell nozzle.
    
    Parameters:
      doc: FreeCAD Document
      insertion_point: FreeCAD.Vector insertion origin (defaults to 0,0,0)
      lean_angle_deg: Float, angle off vertical (defaults to 0.0 for pure vertical axis)
      flame_angle_deg: Float, retained for backward compatibility
      
    Returns:
      App::DocumentObjectGroup containing torch sub-components
    """
    if insertion_point is None:
        insertion_point = FreeCAD.Vector(0, 0, 0)

    grp = doc.addObject("App::DocumentObjectGroup", "Harbor_Freight_Torch_91037")
    grp.Label = "Harbor Freight #91037 Propane Torch Component"

    # Color Palette
    TORCH_BLACK = (0.15, 0.15, 0.15, 0.0)
    CHROME = (0.75, 0.78, 0.82, 0.0)
    HF_BLUE = (0.10, 0.35, 0.80, 0.0)
    BRASS = (0.85, 0.65, 0.20, 0.0)
    IGNITER_RED = (0.85, 0.15, 0.15, 0.0)

    # Collinear central torch axis:
    # All subcomponents (handle, valve, wand pipe, and burner bell) share the EXACT same central axis
    rad = math.radians(lean_angle_deg)
    torch_dir = FreeCAD.Vector(0, -math.sin(rad), math.cos(rad)).normalize()

    # 1. Torch Handle & Trigger Lever (At base of assembly)
    handle_len = 180.0
    handle_body = Part.makeCylinder(17.5, handle_len, insertion_point, torch_dir)
    grip_insert = Part.makeBox(20.0, 25.0, 120.0, FreeCAD.Vector(-10.0, insertion_point.y - 12.5, insertion_point.z + 30.0))
    squeeze_lever = Part.makeBox(6.0, 15.0, 100.0, FreeCAD.Vector(-3.0, insertion_point.y - 25.0, insertion_point.z + 20.0))
    handle_obj = doc.addObject("Part::Feature", "HF_Blue_Torch_Handle")
    handle_obj.Shape = handle_body.fuse(grip_insert).fuse(squeeze_lever)
    grp.addObject(handle_obj)

    # 2. Brass Flow Control Valve
    brass_knob_pos = insertion_point + torch_dir * 25.0
    brass_knob = Part.makeCylinder(14.0, 20.0, brass_knob_pos + FreeCAD.Vector(0, 10.0, 0), FreeCAD.Vector(0, 1, 0))
    brass_obj = doc.addObject("Part::Feature", "Brass_Flow_Control_Knob")
    brass_obj.Shape = brass_knob
    grp.addObject(brass_obj)

    # 3. Chrome Wand Shaft (Collinear with handle)
    wand_start = insertion_point + torch_dir * handle_len
    wand_length = 500.0
    wand_shaft = Part.makeCylinder(9.525, wand_length, wand_start, torch_dir)
    wand_obj = doc.addObject("Part::Feature", "Torch_Chrome_Wand_Shaft")
    wand_obj.Shape = wand_shaft
    grp.addObject(wand_obj)

    # 4. Burner Bell Nozzle (Collinear with wand pipe, flaring out at tip)
    nozzle_start = wand_start + torch_dir * wand_length
    bell_len = 100.0
    bell_nozzle = Part.makeCone(18.0, 38.1, bell_len, nozzle_start, torch_dir)
    bell_rim = Part.makeCylinder(39.0, 12.0, nozzle_start + torch_dir * (bell_len - 12.0), torch_dir)
    burner_head = bell_nozzle.fuse(bell_rim)
    burner_obj = doc.addObject("Part::Feature", "HF_Burner_Head_Nozzle")
    burner_obj.Shape = burner_head
    grp.addObject(burner_obj)

    # 5. Push-Button Piezo Igniter Module
    igniter_clamp_pos = wand_start + torch_dir * 80.0
    igniter_housing = Part.makeBox(20.0, 30.0, 45.0, FreeCAD.Vector(-10.0, igniter_clamp_pos.y - 15.0, igniter_clamp_pos.z))
    igniter_button = Part.makeCylinder(6.0, 12.0, FreeCAD.Vector(0, igniter_clamp_pos.y - 20.0, igniter_clamp_pos.z + 20.0), FreeCAD.Vector(0, -1, 0))
    wire_len = wand_length - 80.0 + 15.0
    igniter_wire = Part.makeCylinder(2.5, wire_len, igniter_clamp_pos + FreeCAD.Vector(0, -10.0, 0), torch_dir)
    igniter_obj = doc.addObject("Part::Feature", "Piezo_Igniter_Module")
    igniter_obj.Shape = igniter_housing.fuse(igniter_button).fuse(igniter_wire)
    grp.addObject(igniter_obj)

    if HAS_GUI and hasattr(FreeCADGui, "getDocument"):
        try:
            gui_d = FreeCADGui.getDocument(doc.Name)
            if gui_d:
                color_map = {
                    burner_obj: TORCH_BLACK,
                    wand_obj: CHROME,
                    handle_obj: HF_BLUE,
                    brass_obj: BRASS,
                    igniter_obj: IGNITER_RED
                }
                for obj, col in color_map.items():
                    g_o = gui_d.getObject(obj.Name)
                    if g_o:
                        g_o.Visibility = True
                        g_o.ShapeColor = col
                        g_o.DisplayMode = "Flat Lines"
        except Exception:
            pass

    return grp

def build_standalone_component():
    doc = FreeCAD.newDocument("torch_91037_component")
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    create_torch_component(doc)
    doc.recompute()

    fc_path = os.path.join(comp_dir, "torch_hf91037.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, "torch_hf91037")
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix="torch_hf91037", camera_type="Perspective")

    save_model(doc, fc_path, camera_type="Perspective")
    close_model(doc.Name)

if __name__ == "__main__":
    build_standalone_component()
    os._exit(0)
