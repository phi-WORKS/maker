"""
2.5 Gallon Pressurized Water Safety Tank Standalone Build Script

Builds water_tank.FCStd and exports 7 standard orthogonal and isometric PNG renders.
"""

import os
import sys
import FreeCAD

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

# Import CAD component function
sys.path.insert(0, script_dir)
from water_tank import create_water_tank_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import get_mass_properties, format_mass_report

def build():
    doc_name = "water_tank"
    doc = FreeCAD.newDocument(doc_name)

    grp = create_water_tank_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="2.5 Gallon Water Safety Spray Tank Mass Report"))

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("2.5 gallon water safety tank build complete.")

if __name__ == "__main__":
    build()
    os._exit(0)
