"""
Build Script: Material Demonstration Models & Snapshot Gallery

Generates a standalone demonstration CAD model (.FCStd) and multi-view snapshot PNG
for each material in `materials/`, featuring:
  - A 50mm cube
  - A 50mm diameter sphere
Both objects have their material assigned via `obj.ShapeMaterial = mat`.
Appearance is driven 100% natively by the material card's BasicRendering model.

Also updates `materials/README.md` with an interactive visual catalog table.
"""

import os
import sys
import yaml
import FreeCAD
import FreeCADGui
FreeCADGui.showMainWindow()
import Part
import Draft

import phi_works.maker.materials as maker_mat
import phi_works.maker.render as maker_render


def build_single_material_demo(category, mat_name, card_path, out_dir):
    """
    Creates a dedicated demonstration CAD model and snapshot PNG for a single material.
    """
    safe_name = mat_name.replace("-", "_").replace(".", "_")
    doc_name = f"Demo_{safe_name}"
    doc = FreeCAD.newDocument(doc_name)

    # Wrap in group with material name
    grp = doc.addObject("App::DocumentObjectGroup", f"Group_{safe_name}")
    grp.Label = mat_name

    # 1. Create 50mm Cube (separated on the left)
    box = doc.addObject("Part::Box", f"Cube_{safe_name}")
    box.Label = f"Cube ({mat_name})"
    box.Length = 50.0
    box.Width = 50.0
    box.Height = 50.0
    box.Placement.Base = FreeCAD.Vector(-55.0, -25.0, 0.0)

    # 2. Create 50mm diameter Sphere (separated on the right, radius = 25mm)
    sphere = doc.addObject("Part::Sphere", f"Sphere_{safe_name}")
    sphere.Label = f"Sphere ({mat_name})"
    sphere.Radius = 25.0
    sphere.Placement.Base = FreeCAD.Vector(55.0, 0.0, 25.0)

    # 3. Apply material natively
    maker_mat.apply_material(box, mat_name)
    maker_mat.apply_material(sphere, mat_name)
    grp.addObject(box)
    grp.addObject(sphere)
    doc.recompute()

    # 4. Render snapshot (sets camera to isometric perspective home view)
    os.makedirs(out_dir, exist_ok=True)
    fc_path = os.path.join(out_dir, f"{mat_name}.FCStd")
    png_path = os.path.join(out_dir, f"{mat_name}.png")

    gui_doc = FreeCADGui.getDocument(doc.Name)
    maker_render.render_single_view(gui_doc, png_path, view_type="Isometric", width=800, height=600)

    # 5. Save model preserving the snapshot home view
    maker_render.save_model(doc, fc_path, camera_type="Perspective")

    # 6. Compute mass properties
    mass_props = maker_mat.get_mass_properties(doc)

    maker_render.close_model(doc)

    return {
        "category": category,
        "name": mat_name,
        "card_path": card_path,
        "fc_path": fc_path,
        "png_path": png_path,
        "mass_kg": mass_props["total_mass_kg"],
        "mass_lb": mass_props["total_mass_lb"],
        "volume_cm3": mass_props["total_volume_mm3"] / 1000.0,
    }


def main():
    print("=" * 80)
    print(" BUILDING MATERIAL DEMONSTRATION SUITE")
    print("=" * 80)

    # Initialize and sync materials
    maker_mat.init_materials(force_refresh=True)
    repo_mat_dir = maker_mat.get_materials_dir()
    demos_root = os.path.join(repo_mat_dir, "demos")
    os.makedirs(demos_root, exist_ok=True)

    # Discover all cards
    categories = sorted([d for d in os.listdir(repo_mat_dir) if os.path.isdir(os.path.join(repo_mat_dir, d)) and d != "demos"])

    material_entries = []

    for cat in categories:
        cat_dir = os.path.join(repo_mat_dir, cat)
        cards = sorted([f for f in os.listdir(cat_dir) if f.endswith(".FCMat")])
        for card_file in cards:
            mat_name = os.path.splitext(card_file)[0]
            card_path = os.path.join(cat_dir, card_file)
            out_dir = os.path.join(demos_root, cat)

            print(f"\nBuilding demo for [{cat}] {mat_name}...")
            entry = build_single_material_demo(cat, mat_name, card_path, out_dir)

            # Read card metadata
            with open(card_path, "r", encoding="utf-8") as fp:
                data = yaml.safe_load(fp)
            entry["description"] = data.get("General", {}).get("Description", "")
            entry["uuid"] = data.get("General", {}).get("UUID", "")
            
            # Density
            dens_str = data.get("Models", {}).get("Density", {}).get("Density", "N/A")
            entry["density"] = dens_str

            # Modulus
            ym = data.get("Models", {}).get("LinearElastic", {}).get("YoungsModulus", "N/A")
            entry["youngs_modulus"] = ym

            # Color
            diffuse = data.get("AppearanceModels", {}).get("BasicRendering", {}).get("DiffuseColor", "(0.8, 0.8, 0.8, 1.0)")
            entry["diffuse_color"] = diffuse

            material_entries.append(entry)

    print(f"\nSuccessfully built {len(material_entries)} material demonstration models!")

    # Build Master Overview Demonstration Model
    build_overview_demo(repo_mat_dir, demos_root)

    # Update materials/README.md index
    update_materials_readme(repo_mat_dir, material_entries)

    print("\nAll material demonstrations and catalog index generated successfully!")


def build_overview_demo(repo_mat_dir, demos_root):
    """
    Builds a composite showcase document organized by row for each material set,
    with samples separated, grouped with their material name, and category labels.
    """
    print("\nBuilding Composite Materials Overview Model...")
    doc = FreeCAD.newDocument("Materials_Overview")

    category_order = ["metals", "finishes", "polymers", "ceramics", "woods", "fluids"]
    discovered_categories = []
    for cat in category_order:
        cat_dir = os.path.join(repo_mat_dir, cat)
        if os.path.isdir(cat_dir):
            cards = sorted([os.path.splitext(f)[0] for f in os.listdir(cat_dir) if f.endswith(".FCMat")])
            if cards:
                discovered_categories.append((cat, cards))

    # Fallback if any other category directories exist
    for d in sorted(os.listdir(repo_mat_dir)):
        p = os.path.join(repo_mat_dir, d)
        if os.path.isdir(p) and d != "demos" and d not in category_order:
            cards = sorted([os.path.splitext(f)[0] for f in os.listdir(p) if f.endswith(".FCMat")])
            if cards:
                discovered_categories.append((d, cards))

    col_spacing = 80.0
    row_spacing = 75.0
    num_rows = len(discovered_categories)
    y_start = ((num_rows - 1) * row_spacing) / 2.0

    for row_idx, (cat_name, mats) in enumerate(discovered_categories):
        cat_grp = doc.addObject("App::DocumentObjectGroup", f"Category_{cat_name}")
        cat_grp.Label = cat_name.capitalize()

        y_pos = y_start - row_idx * row_spacing

        # Staggered category label on the left following camera isometric line
        x_lbl = -55.0 - (row_idx * 30.0)
        y_lbl = y_pos - 8.0
        cat_lbl = Draft.make_text([cat_name.upper()], FreeCAD.Vector(x_lbl, y_lbl, 0.0))
        cat_lbl.Label = f"Label_{cat_name.upper()}"
        cat_lbl.ViewObject.FontSize = 13.0
        cat_lbl.ViewObject.TextColor = (0.1, 0.1, 0.1)
        cat_grp.addObject(cat_lbl)

        for col_idx, mat_name in enumerate(mats):
            safe_name = mat_name.replace("-", "_").replace(".", "_")
            x_pos = col_idx * col_spacing

            mat_grp = doc.addObject("App::DocumentObjectGroup", f"Group_{safe_name}")
            mat_grp.Label = mat_name
            cat_grp.addObject(mat_grp)

            # 1. Cube: 24x24x24mm, placed on left of sample
            box = doc.addObject("Part::Box", f"Cube_{safe_name}")
            box.Label = f"Cube ({mat_name})"
            box.Length = 24.0
            box.Width = 24.0
            box.Height = 24.0
            box.Placement.Base = FreeCAD.Vector(x_pos - 28.0, y_pos - 12.0, 0.0)
            maker_mat.apply_material(box, mat_name)
            mat_grp.addObject(box)

            # 2. Sphere: 24mm diameter (radius 12mm), placed on right of sample
            sphere = doc.addObject("Part::Sphere", f"Sphere_{safe_name}")
            sphere.Label = f"Sphere ({mat_name})"
            sphere.Radius = 12.0
            sphere.Placement.Base = FreeCAD.Vector(x_pos + 18.0, y_pos, 12.0)
            maker_mat.apply_material(sphere, mat_name)
            mat_grp.addObject(sphere)

    doc.recompute()

    overview_fc = os.path.join(demos_root, "materials_overview.FCStd")
    overview_png = os.path.join(demos_root, "materials_overview.png")

    gui_doc = FreeCADGui.getDocument(doc.Name)
    maker_render.render_single_view(gui_doc, overview_png, view_type="Isometric", width=1920, height=1080)
    maker_render.save_model(doc, overview_fc, camera_type="Perspective")
    maker_render.close_model(doc)
    print("Saved Overview:", overview_fc)


def update_materials_readme(repo_mat_dir, entries):
    """
    Rewrites materials/README.md with the full visual catalog index and documentation.
    """
    readme_path = os.path.join(repo_mat_dir, "README.md")

    lines = []
    lines.append("# Project Physical Materials Library & Visual Catalog")
    lines.append("")
    lines.append("This directory contains project-native FreeCAD 1.1 material definitions (`.FCMat`) stored directly within the repository for full portability, Git version control, and reproducible fabrication engineering.")
    lines.append("")
    lines.append("Each material is synchronized into FreeCAD's native User Library (`~/.local/share/FreeCAD/v1-1/Material/maker/`) via file symlinks, ensuring instant zero-lag updates and native visual rendering without 'Material not found' report view errors.")
    lines.append("")
    lines.append("![Materials Overview Showcase](demos/materials_overview.png)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Quick Start & Synchronization")
    lines.append("")
    lines.append("To synchronize all repository materials into your FreeCAD installation:")
    lines.append("```bash")
    lines.append("./scripts/sync_materials.sh")
    lines.append("```")
    lines.append("Or in Python CAD code, initialization happens automatically:")
    lines.append("```python")
    lines.append("from phi_works.maker.materials import init_materials, apply_material, get_mass_properties")
    lines.append("")
    lines.append("# Initializes library and syncs User Material directory")
    lines.append("init_materials()")
    lines.append("")
    lines.append("# Assign material - visual appearance is derived 100% natively from the .FCMat card")
    lines.append("apply_material(my_part, 'Steel-A36')")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Visual Material Catalog & Demonstrations")
    lines.append("")
    lines.append("Each material features a dedicated demonstration CAD model (`.FCStd`) with a 50mm cube and 50mm sphere, viewable in FreeCAD for property verification and inspection.")
    lines.append("")

    # Group by category
    by_cat = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)

    for cat, cat_entries in sorted(by_cat.items()):
        lines.append(f"### {cat.upper()} ({len(cat_entries)} Materials)")
        lines.append("")
        lines.append("| Snapshot | Material | Density | Modulus | Appearance (Diffuse) | Demo Model |")
        lines.append("| :---: | :--- | :---: | :---: | :---: | :---: |")

        for e in cat_entries:
            mat_name = e["name"]
            rel_png = f"demos/{cat}/{mat_name}.png"
            rel_fc = f"demos/{cat}/{mat_name}.FCStd"
            rel_card = f"{cat}/{mat_name}.FCMat"
            diffuse_raw = e["diffuse_color"].strip("()")
            
            lines.append(
                f"| [!['{mat_name}']({rel_png})]({rel_png}) "
                f"| **[{mat_name}]({rel_card})**<br><small>{e['description']}</small> "
                f"| `{e['density']}` "
                f"| `{e['youngs_modulus']}` "
                f"| <small>`{diffuse_raw}`</small> "
                f"| [View Model]({rel_fc}) |"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. YAML Specification Standard")
    lines.append("")
    lines.append("All material cards adhere to FreeCAD 1.1's native YAML specification:")
    lines.append("```yaml")
    lines.append("---")
    lines.append("# FreeCAD Material Card")
    lines.append("General:")
    lines.append("  UUID: \"856988e2-8719-47c0-b934-b12aa2052c6f\"")
    lines.append("  Author: \"phi ARCHITECT\"")
    lines.append("  License: \"CC-BY-4.0\"")
    lines.append("  Name: \"Steel-A36\"")
    lines.append("  Description: \"ASTM A36 structural carbon steel\"")
    lines.append("Models:")
    lines.append("  Density:")
    lines.append("    UUID: '454661e5-265b-4320-8e6f-fcf6223ac3af'")
    lines.append("    Density: \"7850 kg/m^3\"")
    lines.append("  LinearElastic:")
    lines.append("    UUID: '7b561d1d-fb9b-44f6-9da9-56a4f74d7536'")
    lines.append("    YoungsModulus: \"200000 MPa\"")
    lines.append("    PoissonRatio: \"0.26\"")
    lines.append("AppearanceModels:")
    lines.append("  BasicRendering:")
    lines.append("    UUID: 'f006c7e4-35b7-43d5-bbf9-c5d572309e6e'")
    lines.append("    AmbientColor: \"(0.22, 0.23, 0.25, 1.0)\"")
    lines.append("    DiffuseColor: \"(0.42, 0.44, 0.48, 1.0)\"")
    lines.append("    SpecularColor: \"(0.60, 0.60, 0.62, 1.0)\"")
    lines.append("    EmissiveColor: \"(0.0, 0.0, 0.0, 1.0)\"")
    lines.append("    Shininess: \"0.25\"")
    lines.append("    Transparency: \"0.0\"")
    lines.append("```")
    lines.append("")

    with open(readme_path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))
    print(f"Updated catalog index: {readme_path}")


if __name__ == "__main__":
    main()
    os._exit(0)
