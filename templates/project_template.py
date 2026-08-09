"""
Maker Project Template
Use this template to create new physical CAD assembly projects.
"""

import os
import sys
import FreeCAD
import Part

def build_project():
    project_dir = os.path.dirname(__file__)
    versions_dir = os.path.join(project_dir, "versions")
    os.makedirs(versions_dir, exist_ok=True)

    doc = FreeCAD.newDocument("maker_project")
    doc.Label = "New Physical Maker Project"

    # Add parametric VarSet
    dims = doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "Length", "Dimensions", "Main Length").Length = 500.0

    # Add Subassembly Part Containers / Groups
    grp1 = doc.addObject("App::DocumentObjectGroup", "Frame_Subassembly")
    grp1.Label = "1. Frame Subassembly"

    box = Part.makeBox(100, 100, 100)
    feat = doc.addObject("Part::Feature", "MainFrame")
    feat.Shape = box
    grp1.addObject(feat)

    doc.recompute()

    fc_out = os.path.join(project_dir, "project_master.FCStd")
    doc.saveAs(fc_out)
    print(f"Built project master: {fc_out}")
    FreeCAD.closeDocument("maker_project")

if __name__ == "__main__":
    build_project()
    sys.exit(0)
