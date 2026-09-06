"""
STIHL BF-KM Mini-Cultivator Attachment Standalone Build Script

Builds kombi_cultivator_bf.FCStd, prints mass properties, and exports 7 standard orthogonal and isometric PNG renders.
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
from kombi_cultivator_bf import create_kombi_cultivator_bf_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import get_mass_properties, format_mass_report

def build():
    doc_name = "kombi_cultivator_bf"
    doc = FreeCAD.newDocument(doc_name)

    grp = create_kombi_cultivator_bf_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="STIHL BF-KM Mini-Cultivator Mass Report"))

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("STIHL BF-KM Mini-Cultivator build complete.")

if __name__ == "__main__":
    build()
    os._exit(0)
