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
    HAS_GUI = hasattr(FreeCADGui, "getDocument")
except Exception:
    HAS_GUI = False

def create_torch_component(doc, insertion_point=None, lean_angle_deg=35.0, flame_angle_deg=35.0):
    """
    Creates Harbor Freight #91037 Propane Torch assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      insertion_point: FreeCAD.Vector insertion origin (defaults to 0,0,0)
      lean_angle_deg: Float, forward incline of handle wand
      flame_angle_deg: Float, rearward incline of flame nozzle
      
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

    flame_dir = FreeCAD.Vector(0, math.sin(math.radians(flame_angle_deg)), math.cos(math.radians(flame_angle_deg)))
    wand_lean_dir = FreeCAD.Vector(0, -math.sin(math.radians(lean_angle_deg)), math.cos(math.radians(lean_angle_deg)))

    nozzle_pos = insertion_point
    
    # 1. Burner Bell Nozzle
    bell_nozzle = Part.makeCone(38.1, 22.0, 100.0, nozzle_pos, flame_dir)
    bell_rim = Part.makeCylinder(39.0, 10.0, nozzle_pos, flame_dir)
    burner_head = bell_nozzle.fuse(bell_rim)
    burner_obj = doc.addObject("Part::Feature", "HF_Burner_Head_Nozzle")
    burner_obj.Shape = burner_head
    grp.addObject(burner_obj)

    # 2. Chrome Wand Shaft
    wand_start = nozzle_pos + wand_lean_dir * 80.0
    wand_length = 500.0
    wand_shaft = Part.makeCylinder(9.525, wand_length, wand_start, wand_lean_dir)
    wand_obj = doc.addObject("Part::Feature", "Torch_Chrome_Wand_Shaft")
    wand_obj.Shape = wand_shaft
    grp.addObject(wand_obj)

    # 3. Torch Handle & Trigger Lever
    handle_start = wand_start + wand_lean_dir * wand_length
    handle_body = Part.makeCylinder(17.5, 180.0, handle_start, wand_lean_dir)
    grip_insert = Part.makeBox(20.0, 25.0, 120.0, FreeCAD.Vector(-10.0, handle_start.y - 12.0, handle_start.z + 30.0))
    squeeze_lever = Part.makeBox(6.0, 15.0, 100.0, FreeCAD.Vector(-3.0, handle_start.y - 25.0, handle_start.z + 20.0))
    handle_obj = doc.addObject("Part::Feature", "HF_Blue_Torch_Handle")
    handle_obj.Shape = handle_body.fuse(grip_insert).fuse(squeeze_lever)
    grp.addObject(handle_obj)

    # 4. Brass Flow Control Valve
    brass_knob_pos = handle_start + wand_lean_dir * 160.0
    brass_knob = Part.makeCylinder(14.0, 20.0, brass_knob_pos + FreeCAD.Vector(0, 0, 15.0), FreeCAD.Vector(0, 0, 1))
    brass_obj = doc.addObject("Part::Feature", "Brass_Flow_Control_Knob")
    brass_obj.Shape = brass_knob
    grp.addObject(brass_obj)

    # 5. Push-Button Piezo Igniter Module
    igniter_clamp_pos = wand_start + wand_lean_dir * 200.0
    igniter_housing = Part.makeBox(20.0, 30.0, 45.0, FreeCAD.Vector(-10.0, igniter_clamp_pos.y - 15.0, igniter_clamp_pos.z))
    igniter_button = Part.makeCylinder(6.0, 12.0, FreeCAD.Vector(0, igniter_clamp_pos.y - 20.0, igniter_clamp_pos.z + 20.0), FreeCAD.Vector(0, -1, 0))
    igniter_wire = Part.makeCylinder(2.5, 220.0, igniter_clamp_pos + FreeCAD.Vector(0, -10.0, 0), flame_dir)
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
    """Builds standalone torch_hf91037.FCStd component document."""
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
    doc = FreeCAD.newDocument("torch_91037_component")
    doc.Label = "Harbor Freight #91037 Torch Standalone Component"

    create_torch_component(doc)
    doc.recompute()

    fc_path = os.path.join(comp_dir, "torch_hf91037.FCStd")
    doc.saveAs(fc_path)
    print(f"Saved standalone torch component model: {fc_path}")
    FreeCAD.closeDocument("torch_91037_component")

if __name__ == "__main__":
    build_standalone_component()
    sys.exit(0)
