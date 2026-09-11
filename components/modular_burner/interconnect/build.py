"""
Modular Burner Interconnect Standalone Build Script

Builds modular_burner_interconnect.FCStd and exports standard orthogonal and isometric PNG renders.
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

sys.path.insert(0, script_dir)
from modular_burner_interconnect import create_modular_burner_interconnect_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import (
    init_materials,
    get_mass_properties,
    format_mass_report,
)
from phi_works.maker.assembly import ensure_assembly_visible

def build():
    init_materials()
    doc_name = "modular_burner_interconnect"
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")
    doc = FreeCAD.newDocument(doc_name)
    doc.saveAs(fcstd_path)

    grp = create_modular_burner_interconnect_component(doc)
    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Modular Burner Interconnect System Mass Report"))

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Modular burner interconnect build complete.")

if __name__ == "__main__":
    build()
    os._exit(0)
