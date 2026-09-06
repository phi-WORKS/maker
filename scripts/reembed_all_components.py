"""
Batch utility to upgrade all component CAD models in components/ to:
1. Native App::Part root containers (supporting FreeCAD 1.0/1.1 App::Link assembly architecture)
2. Embedded App::MaterialObject cards in a dedicated Materials group (zero external path dependency)
"""

import os
import FreeCAD
from phi_works.maker.materials import init_materials, embed_materials_in_doc

def reembed_and_upgrade_components():
    init_materials()
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    maker_dir = os.path.abspath(os.path.join(curr_dir, ".."))
    components_dir = os.path.join(maker_dir, "components")

    upgraded_count = 0

    for root, dirs, files in os.walk(components_dir):
        for f in files:
            if f.endswith(".FCStd"):
                fcstd_path = os.path.join(root, f)
                rel_path = os.path.relpath(fcstd_path, components_dir)
                print(f"Processing: {rel_path}")

                try:
                    doc = FreeCAD.openDocument(fcstd_path)
                except Exception as e:
                    print(f"  Error opening {rel_path}: {e}")
                    continue

                # 1. Convert root App::DocumentObjectGroup to App::Part if applicable
                root_grps = [
                    o for o in doc.Objects 
                    if o.TypeId == "App::DocumentObjectGroup" and not o.InList and o.Name != "Materials"
                ]

                for grp in root_grps:
                    grp_name = grp.Name
                    grp_label = grp.Label
                    children = list(grp.Group)

                    doc.removeObject(grp_name)
                    app_part = doc.addObject("App::Part", grp_name)
                    app_part.Label = grp_label

                    for c in children:
                        app_part.addObject(c)

                    print(f"  Converted {grp_name} to App::Part ({len(children)} children)")

                # 2. Embed materials
                embedded = embed_materials_in_doc(doc)
                mat_names = [m.Label for m in embedded]
                print(f"  Embedded materials ({len(mat_names)}): {mat_names}")

                # 3. Ensure all parts, groups, and subcomponents are visible
                from phi_works.maker.assembly import ensure_assembly_visible
                ensure_assembly_visible(doc)

                doc.recompute()
                doc.save()
                FreeCAD.closeDocument(doc.Name)
                upgraded_count += 1

    print(f"Successfully upgraded and embedded materials in {upgraded_count} component files.")

if __name__ == "__main__":
    reembed_and_upgrade_components()
