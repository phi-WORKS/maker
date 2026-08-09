"""
Maker Component Template
Use this template to create new reusable CAD components.
"""

import os
import sys
import FreeCAD
import Part

def create_component(doc, origin=None):
    """
    Creates standalone component inside `doc` at `origin`.
    """
    if origin is None:
        origin = FreeCAD.Vector(0, 0, 0)

    grp = doc.addObject("App::DocumentObjectGroup", "Component_Group")
    grp.Label = "Sample Component"

    # Define CAD geometry relative to `origin`
    box = Part.makeBox(50, 50, 50, origin)
    feat = doc.addObject("Part::Feature", "SampleBox")
    feat.Shape = box
    grp.addObject(feat)

    return grp

def build_standalone():
    doc = FreeCAD.newDocument("sample_component")
    create_component(doc)
    doc.recompute()
    out_path = os.path.join(os.path.dirname(__file__), "sample_component.FCStd")
    doc.saveAs(out_path)
    print(f"Built sample component: {out_path}")
    FreeCAD.closeDocument("sample_component")

if __name__ == "__main__":
    build_standalone()
    sys.exit(0)
