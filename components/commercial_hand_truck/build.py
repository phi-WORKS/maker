"""
Commercial Hand Truck Standalone Build Script

Builds commercial_hand_truck.FCStd and exports 7 standard orthogonal and isometric PNG renders.
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
from commercial_hand_truck import create_commercial_hand_truck_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model

def build():
    doc_name = "commercial_hand_truck"
    doc = FreeCAD.newDocument(doc_name)

    create_commercial_hand_truck_component(doc)
    doc.recompute()

    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Hand truck build complete.")

if __name__ == "__main__":
    build()
    os._exit(0)
