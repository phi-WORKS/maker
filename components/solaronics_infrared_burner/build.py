"""
Solaronics Ceramic Infrared Burner Standalone Build Script

Builds solaronics_infrared_burner.FCStd and exports 7 standard orthogonal and isometric PNG renders.
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
from solaronics_infrared_burner import create_solaronics_infrared_burner_component
from phi_works.maker.render import export_orthogonal_views

def build():
    doc_name = "solaronics_infrared_burner"
    doc = FreeCAD.newDocument(doc_name)

    create_solaronics_infrared_burner_component(doc)
    doc.recompute()

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")
    doc.saveAs(fcstd_path)
    print(f"Saved standalone Solaronics burner model: {fcstd_path}")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name)

    FreeCAD.closeDocument(doc.Name)
    print("Solaronics burner build complete.")

if __name__ == "__main__":
    build()
    sys.exit(0)
