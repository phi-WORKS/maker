"""
1 lb Disposable/Refillable Propane Cylinder Component
Standalone 3D Parametric CAD Module

This module provides `create_propane_cylinder_component(doc, placement)` to create a
standard 1 lb propane cylinder (3.875" outer diameter, 7.8" total height, brass top valve,
and bottom seat collar) inside any FreeCAD document.
"""

import os
import sys
import math
import FreeCAD
import Part

# Ensure src directory is on sys.path for shared imports
maker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_dir = os.path.join(maker_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views

def create_propane_cylinder_component(doc, placement=None):
    """
    Creates 1 lb Propane Cylinder assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing cylinder sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Propane_Cylinder_1lb")
    grp.Label = "1 lb Propane Cylinder Component"

    # Color Palette
    PROPANE_GREEN = (0.12, 0.48, 0.22, 0.0)   # Standard Coleman / Flameking Dark Green
    BRASS = (0.85, 0.65, 0.20, 0.0)           # 1"-20 UNEF Valve & Fittings
    STEEL_DARK = (0.25, 0.27, 0.29, 0.0)      # Safety Collar & Base Rim

    # Parametric Dimensions (1 lb Cylinder)
    CYL_RADIUS = 49.2     # 3.875 in diameter -> 98.4 mm OD
    CYL_BODY_H = 140.0    # 5.5 in main cylindrical body
    BASE_COLLAR_R = 44.0  # Recessed bottom seating rim radius
    BASE_COLLAR_H = 12.0  # Bottom collar height
    VALVE_NECK_R = 14.0   # Upper neck collar
    VALVE_NECK_H = 15.0
    VALVE_STEM_R = 7.0    # 1"-20 UNEF Valve Stem radius (~13 mm)
    VALVE_STEM_H = 18.0

    # 1. Recessed Bottom Seat Collar
    seat_collar = Part.makeCylinder(BASE_COLLAR_R, BASE_COLLAR_H, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    seat_inner = Part.makeCylinder(BASE_COLLAR_R - 3.0, BASE_COLLAR_H + 0.1, FreeCAD.Vector(0, 0, -0.1), FreeCAD.Vector(0, 0, 1))
    seat_rim = seat_collar.cut(seat_inner)

    # 2. Main Cylinder Body & Dome
    cyl_body = Part.makeCylinder(CYL_RADIUS, CYL_BODY_H, FreeCAD.Vector(0, 0, BASE_COLLAR_H), FreeCAD.Vector(0, 0, 1))
    
    # Upper Dome Transition
    dome_sphere = Part.makeSphere(CYL_RADIUS, FreeCAD.Vector(0, 0, BASE_COLLAR_H + CYL_BODY_H - CYL_RADIUS / 2))
    dome_cut_box = Part.makeBox(CYL_RADIUS * 2 + 10, CYL_RADIUS * 2 + 10, CYL_RADIUS * 2, FreeCAD.Vector(-CYL_RADIUS - 5, -CYL_RADIUS - 5, -CYL_RADIUS * 2))
    top_dome = dome_sphere.cut(dome_cut_box)

    tank_steel_shape = seat_rim.fuse(cyl_body).fuse(top_dome)
    tank_steel_shape.Placement = placement

    tank_obj = doc.addObject("Part::Feature", "Cylinder_Steel_Body")
    tank_obj.Shape = tank_steel_shape
    grp.addObject(tank_obj)

    # 3. Brass Top Valve & Safety Neck
    neck_pos = FreeCAD.Vector(0, 0, BASE_COLLAR_H + CYL_BODY_H + 12.0)
    neck_cylinder = Part.makeCylinder(VALVE_NECK_R, VALVE_NECK_H, neck_pos, FreeCAD.Vector(0, 0, 1))
    stem_cylinder = Part.makeCylinder(VALVE_STEM_R, VALVE_STEM_H, neck_pos + FreeCAD.Vector(0, 0, VALVE_NECK_H), FreeCAD.Vector(0, 0, 1))
    
    brass_valve_shape = neck_cylinder.fuse(stem_cylinder)
    brass_valve_shape.Placement = placement

    valve_obj = doc.addObject("Part::Feature", "Brass_Threaded_Valve_1in20")
    valve_obj.Shape = brass_valve_shape
    grp.addObject(valve_obj)

    if HAS_GUI and hasattr(FreeCADGui, "getDocument"):
        try:
            gui_d = FreeCADGui.getDocument(doc.Name)
            if gui_d:
                g_tank = gui_d.getObject(tank_obj.Name)
                if g_tank:
                    g_tank.Visibility = True
                    g_tank.ShapeColor = PROPANE_GREEN
                    g_tank.DisplayMode = "Flat Lines"

                g_valve = gui_d.getObject(valve_obj.Name)
                if g_valve:
                    g_valve.Visibility = True
                    g_valve.ShapeColor = BRASS
                    g_valve.DisplayMode = "Flat Lines"
        except Exception:
            pass

    return grp

def build_standalone_component():
    doc = FreeCAD.newDocument("propane_cylinder_1lb_component")
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    create_propane_cylinder_component(doc)
    doc.recompute()

    fc_path = os.path.join(comp_dir, "propane_cylinder_1lb.FCStd")
    doc.saveAs(fc_path)
    print(f"Saved standalone propane cylinder component model: {fc_path}")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, "propane_cylinder_1lb")
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix="propane_cylinder_1lb")

    FreeCAD.closeDocument("propane_cylinder_1lb_component")

if __name__ == "__main__":
    build_standalone_component()
    sys.exit(0)
