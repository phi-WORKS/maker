"""
STIHL HT-KM 12" Pole Pruner Attachment Standalone Build Script

Builds kombi_pruner_ht.FCStd, prints mass properties, and exports 7 standard orthogonal and isometric PNG renders.
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
from kombi_pruner_ht import create_kombi_pruner_ht_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import get_mass_properties, format_mass_report

def build():
    doc_name = "kombi_pruner_ht"
    doc = FreeCAD.newDocument(doc_name)

    grp = create_kombi_pruner_ht_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="STIHL HT-KM 12\" Pole Pruner Mass Report"))

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("STIHL HT-KM Pole Pruner build complete.")

if __name__ == "__main__":
    build()
    os._exit(0)
