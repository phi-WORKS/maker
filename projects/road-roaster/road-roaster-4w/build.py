"""
Road Roaster 4W - Master Assembly Build Script
Project: 4-Wheel Commercial Platform Dolly Architecture for Ceramic Infrared Weed Eradication
Version: v0.2.0

Full Integrated Modular Link-Based Assembly:
  1. Commercial 24" x 36" Platform Cart Foundation (Linked Component)
  2. Bolted Front Skirt Mounting Apron (Formed Heavy-Gauge Steel)
  3. Axle Brackets & 3/4" Continuous Pivot Axle (Left/Right Pillow Ear Brackets)
  4. Front Cantilever Radiant Solaronics K-30 Ceramic Burner Subassembly (Linked Subassembly)
  5. 20 lb Propane Fuel Train & Deck Retention Ring Subassembly (Linked Subassembly)
  6. Auxiliary Spot Torch Wand & Water Safety Reservoir Subassembly (Linked Subassembly)
  7. Kinematic Revolute Joint (180° Flip Transit Over Axle)
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
from phi_works.maker.bom import export_bom

def build_road_roaster_4w():
    init_materials()
    doc_name = "road-roaster-4w"
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Road Roaster 4W v0.2.0 (4-Wheel Commercial Platform Dolly Architecture)"
    doc.saveAs(fcstd_path)

    # Master Assembly
    assy = create_assembly(doc, "Road_Roaster_4W", "Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture)")

    # Dimensional references
    DECK_TOP_Z = 195.0
    DECK_L = 914.4
    FRONT_LIP_Y = -DECK_L / 2.0  # Y = -457.2 mm
    PIVOT_Y = -475.0             # Center of continuous pivot axle
    PIVOT_Z = 230.0              # Elevated 35 mm above deck top for 180° flip clearance
    AXLE_DIA = 19.05             # 3/4" continuous cold-rolled steel axle
    AXLE_LEN = 520.0             # Spans across both brackets
    ARM_X = 230.0                # Axle brackets and drop arms lateral spacing

    # 2D Master Transit Skeleton (YZ Kinematic Transit)
    sk = create_skeleton_sketch(doc, "Skeleton_Chassis_Burner", plane="YZ", offset=0.0, label="Master 2D Skeleton (YZ Kinematic Transit)")
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -1100, 0), FreeCAD.Vector(0, 500, 0)))             # Ground line
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, -457.2, 195.0), FreeCAD.Vector(0, 457.2, 195.0)))   # Deck line
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(0, -799.0, 148.1))) # Operating cantilever arm (0 deg)
    sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(0, -151.0, 311.9))) # Stowed transit arm (180 deg flip)
    sk.addGeometry(Part.Circle(FreeCAD.Vector(0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0), 334.0))        # 180-deg swing trajectory arc
    sk.Visibility = False
    assy.addObject(sk)

    # ==========================================================================
    # 1. HEAVY-DUTY WRAP-AROUND RIGID FRONT SKIRT & WHEEL SHIELD
    # ==========================================================================
    # Heavy-duty 3/16" (6 mm) formed steel skirt wrapping around the front and sides
    # of the cart platform, dropping down to Z = 35 mm to completely shield the
    # 5" front caster wheels from heat, gravel, and impacts while providing
    # rigid landing anvils for the cantilever drop arms to rest on.
    DECK_W = 609.6
    SKIRT_T = 6.0
    SKIRT_BOT_Z = 35.0           # Drops down to 35 mm above ground (shields 150 mm casters!)
    SKIRT_W = DECK_W + 2 * SKIRT_T + 4.0  # 625.6 mm outer width
    SKIRT_FRONT_Y = FRONT_LIP_Y - SKIRT_T # -463.2 mm
    SIDE_WING_L = 230.0          # Extends rearward along sides past front casters (to Y = -227.2 mm)
    h_front = DECK_TOP_Z - SKIRT_BOT_Z

    # A. Front Face Plate (drops from deck top to 35 mm above ground)
    front_plate = Part.makeBox(SKIRT_W, SKIRT_T, h_front,
                               FreeCAD.Vector(-SKIRT_W / 2.0, SKIRT_FRONT_Y, SKIRT_BOT_Z))

    # B. Top Deck Mounting Flange (bends back over the deck top)
    top_flange = Part.makeBox(SKIRT_W, 35.0, SKIRT_T,
                              FreeCAD.Vector(-SKIRT_W / 2.0, FRONT_LIP_Y, DECK_TOP_Z))

    # C. Left and Right Side Wrap Wings (protect wheels from sides)
    left_wing = Part.makeBox(SKIRT_T, SIDE_WING_L, h_front,
                             FreeCAD.Vector(-SKIRT_W / 2.0, FRONT_LIP_Y, SKIRT_BOT_Z))
    right_wing = Part.makeBox(SKIRT_T, SIDE_WING_L, h_front,
                              FreeCAD.Vector(SKIRT_W / 2.0 - SKIRT_T, FRONT_LIP_Y, SKIRT_BOT_Z))

    # D. Angled relief cuts on the rear of side wings for curb / obstacle clearance
    cut_l = 80.0
    cut_h = 50.0
    v1 = FreeCAD.Vector(-SKIRT_W / 2.0 - 5.0, FRONT_LIP_Y + SIDE_WING_L - cut_l, SKIRT_BOT_Z - 5.0)
    v2 = FreeCAD.Vector(-SKIRT_W / 2.0 - 5.0, FRONT_LIP_Y + SIDE_WING_L + 5.0, SKIRT_BOT_Z - 5.0)
    v3 = FreeCAD.Vector(-SKIRT_W / 2.0 - 5.0, FRONT_LIP_Y + SIDE_WING_L + 5.0, SKIRT_BOT_Z + cut_h)
    poly_cut = Part.makePolygon([v1, v2, v3, v1])
    cut_solid_left = Part.Face(poly_cut).extrude(FreeCAD.Vector(SKIRT_T + 10.0, 0, 0))
    left_wing = left_wing.cut(cut_solid_left)

    v1_r = FreeCAD.Vector(SKIRT_W / 2.0 - SKIRT_T - 5.0, FRONT_LIP_Y + SIDE_WING_L - cut_l, SKIRT_BOT_Z - 5.0)
    v2_r = FreeCAD.Vector(SKIRT_W / 2.0 - SKIRT_T - 5.0, FRONT_LIP_Y + SIDE_WING_L + 5.0, SKIRT_BOT_Z - 5.0)
    v3_r = FreeCAD.Vector(SKIRT_W / 2.0 - SKIRT_T - 5.0, FRONT_LIP_Y + SIDE_WING_L + 5.0, SKIRT_BOT_Z + cut_h)
    poly_cut_r = Part.makePolygon([v1_r, v2_r, v3_r, v1_r])
    cut_solid_right = Part.Face(poly_cut_r).extrude(FreeCAD.Vector(SKIRT_T + 10.0, 0, 0))
    right_wing = right_wing.cut(cut_solid_right)

    # E. Cantilever Rest Anvils (solid landing pads on front face for drop legs)
    anvils = []
    for sign in [-1.0, 1.0]:
        x_a = sign * ARM_X
        # Upper rest anvil
        a_up = Part.makeBox(45.0, 12.0, 35.0,
                            FreeCAD.Vector(x_a - 22.5, SKIRT_FRONT_Y - 12.0, 140.0))
        # Lower rest foot anvil
        a_low = Part.makeBox(45.0, 16.0, 35.0,
                             FreeCAD.Vector(x_a - 22.5, SKIRT_FRONT_Y - 16.0, SKIRT_BOT_Z + 10.0))
        anvils.append(a_up.fuse(a_low))

    skirt_body = front_plate.fuse(top_flange).fuse(left_wing).fuse(right_wing).fuse(anvils[0]).fuse(anvils[1])

    # F. Mounting Through-Bolts (Front and Sides)
    bolt_parts = []
    for x_b in [-220.0, -90.0, 90.0, 220.0]:
        for z_b in [90.0, 165.0]:
            head = Part.makeCylinder(9.5, 4.0, FreeCAD.Vector(x_b, SKIRT_FRONT_Y, z_b), FreeCAD.Vector(0, -1, 0))
            bolt_parts.append(head)
    for sign in [-1.0, 1.0]:
        x_side = sign * (SKIRT_W / 2.0)
        vec_norm = FreeCAD.Vector(sign, 0, 0)
        for y_b in [FRONT_LIP_Y + 50.0, FRONT_LIP_Y + 150.0]:
            head = Part.makeCylinder(9.5, 4.0, FreeCAD.Vector(x_side, y_b, 165.0), vec_norm)
            bolt_parts.append(head)

    for bp in bolt_parts:
        skirt_body = skirt_body.fuse(bp)

    obj_skirt = doc.addObject("Part::Feature", "Wrap_Around_Rigid_Skirt")
    obj_skirt.Label = "Heavy-Duty Wrap-Around Rigid Front Skirt & Wheel Shield"
    obj_skirt.Shape = skirt_body
    assy.addObject(obj_skirt)
    apply_material(obj_skirt, "Steel-A36")

    # ==========================================================================
    # 2. AXLE BRACKETS & 3/4" CONTINUOUS PIVOT AXLE
    # ==========================================================================
    bracket_parts = []
    BRK_W = 50.0
    BRK_L = 55.0
    BRK_T = 8.0
    EAR_R = 25.0

    for sign in [-1.0, 1.0]:
        x_brk = sign * ARM_X
        # Base plate bolted to skirt and deck
        pad = Part.makeBox(BRK_W, BRK_L, BRK_T,
                            FreeCAD.Vector(x_brk - BRK_W / 2.0, FRONT_LIP_Y - BRK_T, DECK_TOP_Z))
        # Upright arched ear
        ear_box = Part.makeBox(BRK_T, 45.0, PIVOT_Z - DECK_TOP_Z,
                               FreeCAD.Vector(x_brk - BRK_T / 2.0, PIVOT_Y - 22.5, DECK_TOP_Z))
        ear_top = Part.makeCylinder(EAR_R, BRK_T,
                                    FreeCAD.Vector(x_brk - BRK_T / 2.0, PIVOT_Y, PIVOT_Z),
                                    FreeCAD.Vector(1, 0, 0))
        ear = ear_box.fuse(ear_top)
        # Axle bore hole
        bore = Part.makeCylinder(AXLE_DIA / 2.0 + 0.5, BRK_T + 4.0,
                                 FreeCAD.Vector(x_brk - BRK_T / 2.0 - 2.0, PIVOT_Y, PIVOT_Z),
                                 FreeCAD.Vector(1, 0, 0))
        bracket_parts.append(pad.fuse(ear).cut(bore))

    brackets_solid = bracket_parts[0].fuse(bracket_parts[1])

    # 3/4" Continuous Cold-Rolled Steel Pivot Axle
    axle_shaft = Part.makeCylinder(AXLE_DIA / 2.0, AXLE_LEN,
                                   FreeCAD.Vector(-AXLE_LEN / 2.0, PIVOT_Y, PIVOT_Z),
                                   FreeCAD.Vector(1, 0, 0))
    # 2x Shaft Collars at outer ends
    collar1 = Part.makeCylinder(17.5, 12.0, FreeCAD.Vector(-250.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
    collar2 = Part.makeCylinder(17.5, 12.0, FreeCAD.Vector(238.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
    axle_solid = axle_shaft.fuse(collar1).fuse(collar2)

    obj_brackets = doc.addObject("Part::Feature", "Axle_Ear_Brackets")
    obj_brackets.Label = "Axle Ear Brackets (Pillow Flanges Bolted to Skirt)"
    obj_brackets.Shape = brackets_solid
    assy.addObject(obj_brackets)
    apply_material(obj_brackets, "Steel-A36")

    obj_axle = doc.addObject("Part::Feature", "Continuous_Pivot_Axle")
    obj_axle.Label = "Continuous 3/4in Cold-Rolled Steel Pivot Axle & Shaft Collars"
    obj_axle.Shape = axle_solid
    assy.addObject(obj_axle)
    apply_material(obj_axle, "Steel-ZincPlated")

    # ==========================================================================
    # 3. IMPORT LINKED SUBASSEMBLIES VIA APP::LINK
    # ==========================================================================
    # A. Foundation Platform Cart
    link_cart = import_component(doc, "platform_cart_24x36", label="1. Commercial 24x36 Platform Cart Foundation", as_link=True)

    # Paths to modular subassembly documents
    sub_burner = os.path.join(script_dir, "subassemblies", "cantilever_burner", "cantilever_burner.FCStd")
    sub_fuel = os.path.join(script_dir, "subassemblies", "fuel_system", "fuel_system.FCStd")
    sub_aux = os.path.join(script_dir, "subassemblies", "aux_torch_safety", "aux_torch_safety.FCStd")

    # B. Front Cantilever Burner Subassembly (Solaronics K-30 & 180° Flip Bracket)
    link_burner = import_component(doc, sub_burner, label="2. Front Cantilever Radiant Burner & Sled Cowl", as_link=True)

    # C. Fuel System Subassembly
    link_fuel = import_component(doc, sub_fuel, label="3. 20lb Propane Tank Mounting & Primary Gas Train", as_link=True)

    # D. Auxiliary Spot Torch & Safety Subassembly
    link_aux = import_component(doc, sub_aux, label="4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir", as_link=True)

    # ==========================================================================
    # 4. KINEMATIC JOINTS
    # ==========================================================================
    # Ground joint anchoring the platform cart in 3D space
    create_ground_joint(doc, assy, link_cart, "GroundJoint_PlatformCart")

    # Revolute joint between pivot axle and cantilever burner subassembly (180° flip)
    create_joint(doc, assy, "Revolute", obj_axle, "", link_burner, "", name="RevoluteJoint_BurnerFlip")

    # ==========================================================================
    # 5. PROGRAMMATIC EXPLODED VIEW
    # ==========================================================================
    exp_assy = create_exploded_view(doc, assy, "ExplodedView_RoadRoaster4W", "Road Roaster 4W Master Exploded View")
    add_exploded_step(doc, exp_assy, link_burner, FreeCAD.Vector(0, -180, 80), label="Explode Cantilever Burner Assembly Forward")
    add_exploded_step(doc, exp_assy, link_fuel, FreeCAD.Vector(0, 0, 160), label="Explode 20lb Propane Fuel Train Upward")
    add_exploded_step(doc, exp_assy, link_aux, FreeCAD.Vector(0, 120, 100), label="Explode Spot Torch & Water Reservoir")

    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Road Roaster 4W v0.2.0 Master Assembly Mass Report"))

    # Export 7 Multi-View Perspective PNG Renders
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

        # Archive milestone thumbnail to changelog/
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)
        home_src = os.path.join(script_dir, f"{doc_name}.png")
        home_dst = os.path.join(changelog_dir, "v0.2.0.png")
        if os.path.exists(home_src):
            shutil.copyfile(home_src, home_dst)
            print(f"Archived milestone render to changelog: {home_dst}")

    # Generate Master Bill of Materials (BOM) & Fabrication Cut List
    bom_config = {
        "project_name": "Road Roaster 4W",
        "version": "0.2.0",
        "operations_map": {
            "deck": "Cut diamond-plate deck, drill caster mounting holes",
            "skirt": "Form 90° front mounting apron channel, drill 3/8\" bolt holes",
            "brackets": "Machine arched axle ear brackets, bore 3/4\" pivot bushing holes",
            "axle": "Cut 3/4\" cold-rolled steel axle shaft, mount zinc shaft collars",
            "burner": "Assemble cantilever drop arms, weld hood brackets and diagonal braces, mount Solaronics K-30 engine",
        },
    }
    export_bom(doc, script_dir, formats=["markdown", "csv", "json"], config=bom_config)

    # Save Master CAD Model with framed Perspective Isometric home view
    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Road Roaster 4W v0.2.0 build complete.")

if __name__ == "__main__":
    build_road_roaster_4w()
    os._exit(0)
