"""
Road Roaster 4W - 20 lb Propane Fuel Train & Deck Clamp Subassembly
Parametric FreeCAD 1.0/1.1 Subassembly Model

Components:
  1. 20 lb DOT-4BA240 Propane Cylinder (Linked Component)
  2. Heavy-Duty Welded Deck Retention Ring with Quick-Release Mounting Tabs
  3. Brass Dual-Outlet Regulator Distribution Manifold Tee
"""

import os
import sys
import math
import shutil
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.materials import init_materials, apply_material, get_mass_properties, format_mass_report
from phi_works.maker.components import import_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.assembly import ensure_assembly_visible

def build_fuel_system():
    init_materials()
    doc_name = "fuel_system"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.saveAs(fcstd_path)

    # Root App::Part container
    part_root = doc.addObject("App::Part", "Fuel_System_20lb")
    part_root.Label = "20 lb Propane Fuel System Subassembly (Cylinder, Clamp Ring & Manifold)"

    DECK_TOP_Z = 195.0
    TANK_X = 75.0   # +75.0 mm (Right-rear zone)
    TANK_Y = 220.0  # +220.0 mm

    # 1. Welded Deck Retention Ring & Quick-Release Clamp
    FOOT_R = 101.6
    RING_T = 6.0
    ring_outer = Part.makeCylinder(FOOT_R + 8.0, 35.0, FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1))
    ring_inner = Part.makeCylinder(FOOT_R + 2.0, 40.0, FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z - 1.0), FreeCAD.Vector(0, 0, 1))
    deck_ring = ring_outer.cut(ring_inner)

    tabs = []
    for ang in [30, 150, 270]:
        t_box = Part.makeBox(35.0, 40.0, 6.0, FreeCAD.Vector(-17.5, FOOT_R + 5.0, DECK_TOP_Z))
        t_box.rotate(FreeCAD.Vector(0, 0, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1), ang)
        t_box.translate(FreeCAD.Vector(TANK_X, TANK_Y, 0))
        tabs.append(t_box)

    retention_collar = deck_ring.fuse(tabs[0]).fuse(tabs[1]).fuse(tabs[2])

    # 2. Dual-Port Brass Manifold Tee at Regulator Outlet
    Z_reg = DECK_TOP_Z + 480.0
    tee_body = Part.makeBox(35.0, 30.0, 35.0, FreeCAD.Vector(TANK_X - 17.5, TANK_Y + 65.0, Z_reg))
    port_front = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(TANK_X, TANK_Y + 65.0, Z_reg + 17.5), FreeCAD.Vector(0, -1, 0))
    port_side = Part.makeCylinder(7.0, 25.0, FreeCAD.Vector(TANK_X + 17.5, TANK_Y + 80.0, Z_reg + 17.5), FreeCAD.Vector(1, 0, 0))
    tee_assembly = tee_body.fuse(port_front).fuse(port_side)

    obj_ring = doc.addObject("Part::Feature", "Tank_Deck_Retention_Ring")
    obj_ring.Label = "20 lb Propane Foot-Ring Deck Retention Clamp"
    obj_ring.Shape = retention_collar
    part_root.addObject(obj_ring)
    apply_material(obj_ring, "Steel-A36")

    obj_tee = doc.addObject("Part::Feature", "Dual_Manifold_Gas_Tee")
    obj_tee.Label = "Brass Dual-Outlet Regulator Distribution Manifold Tee"
    obj_tee.Shape = tee_assembly
    part_root.addObject(obj_tee)
    apply_material(obj_tee, "Brass-C360")

    # 3. Link 20 lb Propane Cylinder Component
    tank_pos = FreeCAD.Vector(TANK_X, TANK_Y, DECK_TOP_Z)
    tank_link = import_component(doc, "propane_cylinder_20lb", placement=FreeCAD.Placement(tank_pos, FreeCAD.Rotation()), as_link=True)
    if tank_link:
        part_root.addObject(tank_link)

    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Fuel System Subassembly Mass Report"))

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Fuel System subassembly build complete.")

if __name__ == "__main__":
    build_fuel_system()
    os._exit(0)
