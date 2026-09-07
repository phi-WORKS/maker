"""
Road Roaster 4W - Master Assembly Build Script
Project: 4-Wheel Commercial Platform Dolly Architecture for Ceramic Infrared Weed Eradication

Full Integrated Modular Link-Based Assembly:
  1. Commercial 24" x 36" Platform Cart Foundation (Linked Component)
  2. Front Cantilever Radiant Ceramic Burner Subassembly (Linked Subassembly)
  3. 20 lb Propane Fuel Train & Deck Retention Ring Subassembly (Linked Subassembly)
  4. Auxiliary Spot Torch Wand & Water Safety Reservoir Subassembly (Linked Subassembly)
  5. Front Deck 180° Flip Hinge Brackets & Kinematic Revolute Joint
"""

import os
import sys
import math
import shutil
import FreeCAD
import Part

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.components import import_component
from phi_works.maker.materials import (
    init_materials,
    apply_material,
    get_mass_properties,
    format_mass_report,
)
from phi_works.maker.assembly import (
    create_assembly,
    create_ground_joint,
    create_joint,
    create_exploded_view,
    add_exploded_step,
    ensure_assembly_visible,
)
from phi_works.maker.skeleton import create_skeleton_sketch

def build_road_roaster_4w():
    init_materials()
    doc_name = "road-roaster-4w"
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture)"
    doc.saveAs(fcstd_path)

    # Master Assembly
    assy = create_assembly(doc, "Road_Roaster_4W", "Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture)")

    # 2D Master Transit Skeleton (YZ Kinematic Transit)
    sk = create_skeleton_sketch(doc, "Skeleton_Chassis_Burner", plane="YZ", offset=0.0, label="Master 2D Skeleton (YZ Kinematic Transit)")
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -900, 0), FreeCAD.Vector(0, 500, 0)))           # Ground line
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -457.2, 195.0), FreeCAD.Vector(0, 457.2, 195.0))) # Deck line
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -472.2, 220.0), FreeCAD.Vector(0, -720.0, 135.4))) # Operating cantilever arm
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -472.2, 220.0), FreeCAD.Vector(0, -224.4, 304.6))) # 180-deg stowed transit arm
    sk.Visibility = False
    assy.addObject(sk)

    # Dimensional references
    DECK_TOP_Z = 195.0
    DECK_L = 914.4
    FRONT_LIP_Y = -DECK_L / 2.0  # Y = -457.2 mm
    PIVOT_Y = FRONT_LIP_Y - 20.0  # -477.2 mm
    PIVOT_Z = DECK_TOP_Z - 10.0   # 185.0 mm

    # ==========================================================================
    # 1. FRONT DECK HINGE BRACKETS (Bolted to Cart Front Lip)
    # ==========================================================================
    arm_x_positions = [-160.0, 160.0]
    hinge_parts = []
    for x_h in arm_x_positions:
        pad = Part.makeBox(40.0, 65.0, 6.0, FreeCAD.Vector(x_h - 20.0, FRONT_LIP_Y, DECK_TOP_Z))
        ear1 = Part.makeBox(6.0, 45.0, 45.0, FreeCAD.Vector(x_h - 22.0, FRONT_LIP_Y - 25.0, DECK_TOP_Z - 20.0))
        ear2 = Part.makeBox(6.0, 45.0, 45.0, FreeCAD.Vector(x_h + 16.0, FRONT_LIP_Y - 25.0, DECK_TOP_Z - 20.0))
        pin = Part.makeCylinder(6.0, 50.0, FreeCAD.Vector(x_h - 25.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
        hinge_parts.append(pad.fuse(ear1).fuse(ear2).fuse(pin))

    hinge_brackets_solid = hinge_parts[0].fuse(hinge_parts[1])
    obj_hinges = doc.addObject("Part::Feature", "Burner_Deck_Hinge_Brackets")
    obj_hinges.Label = "Front Deck 180-deg Flip Hinge Brackets & Pivot Pins"
    obj_hinges.Shape = hinge_brackets_solid
    assy.addObject(obj_hinges)
    apply_material(obj_hinges, "Steel-ZincPlated")

    # ==========================================================================
    # 2. IMPORT LINKED SUBASSEMBLIES VIA APP::LINK
    # ==========================================================================
    # A. Foundation Platform Cart
    link_cart = import_component(doc, "platform_cart_24x36", label="1. Commercial 24x36 Platform Cart Foundation", as_link=True)

    # Paths to modular subassembly documents
    sub_burner = os.path.join(script_dir, "subassemblies", "cantilever_burner", "cantilever_burner.FCStd")
    sub_fuel = os.path.join(script_dir, "subassemblies", "fuel_system", "fuel_system.FCStd")
    sub_aux = os.path.join(script_dir, "subassemblies", "aux_torch_safety", "aux_torch_safety.FCStd")

    # B. Front Cantilever Burner Subassembly
    link_burner = import_component(doc, sub_burner, label="2. Front Cantilever Radiant Burner & Sled Cowl", as_link=True)

    # C. Fuel System Subassembly
    link_fuel = import_component(doc, sub_fuel, label="3. 20lb Propane Tank Mounting & Primary Gas Train", as_link=True)

    # D. Auxiliary Spot Torch & Safety Subassembly
    link_aux = import_component(doc, sub_aux, label="4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir", as_link=True)

    # ==========================================================================
    # 3. KINEMATIC JOINTS
    # ==========================================================================
    # Ground joint anchoring the platform cart in 3D space
    create_ground_joint(doc, assy, link_cart, "GroundJoint_PlatformCart")

    # Revolute joint between deck hinge brackets and cantilever burner subassembly
    create_joint(doc, assy, "Revolute", obj_hinges, "", link_burner, "", name="RevoluteJoint_BurnerFlip")

    # ==========================================================================
    # 4. PROGRAMMATIC EXPLODED VIEW
    # ==========================================================================
    exp_assy = create_exploded_view(doc, assy, "ExplodedView_RoadRoaster4W", "Road Roaster 4W Master Exploded View")
    add_exploded_step(doc, exp_assy, link_burner, FreeCAD.Vector(0, -180, 80), label="Explode Cantilever Burner Assembly Forward")
    add_exploded_step(doc, exp_assy, link_fuel, FreeCAD.Vector(0, 0, 160), label="Explode 20lb Propane Fuel Train Upward")
    add_exploded_step(doc, exp_assy, link_aux, FreeCAD.Vector(0, 120, 100), label="Explode Spot Torch & Water Reservoir")

    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Road Roaster 4W Master Assembly Mass Report"))

    # Export 7 Multi-View Perspective PNG Renders
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

        # Archive milestone thumbnail to changelog/
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)
        home_src = os.path.join(script_dir, f"{doc_name}.png")
        home_dst = os.path.join(changelog_dir, "v0.1.0.png")
        if os.path.exists(home_src):
            shutil.copyfile(home_src, home_dst)
            print(f"Archived milestone render to changelog: {home_dst}")

    # Save Master CAD Model with framed Perspective Isometric home view
    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Road Roaster 4W v0.1.0 build complete.")

if __name__ == "__main__":
    build_road_roaster_4w()
    os._exit(0)
