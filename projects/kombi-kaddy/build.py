"""
Kombi Kaddy - Master Assembly Build Script
Project: Mobile Workshop Storage Rack for STIHL KombiSystem Fleet

Modern FreeCAD 1.1 Assembly Workbench Architecture:
1. Solid Softwood Framing (2x4 posts & base feet, 1x4 cross rails & deck slats, 3/4" gussets)
2. 5.0" COTS Running Gear (Imported caster_wheel_5in with 3/8" axle hardware)
3. 4 Tool Storage Positions across 36" rail with heavy-duty spring clips
4. Imported Commercial STIHL Tool Fleet:
   - Slot 1: FS-KM Straight Shaft String Trimmer (AutoCut head, concentric guard)
   - Slot 2: FBD-KM Bed Redefiner (rubber guide wheel, 4-tine scoop rotor, orange hood)
   - Slot 3: BG-KM In-line Axial Blower (axial fan housing, downward funnel nozzle)
   - Slot 4: FH-KM 145-deg Articulating Power Scythe (joint boot, curb skid, double blades)
5. Kinematic Ground joint & Programmatic Exploded Assembly View

Builds caddy.FCStd and exports 7 standard orthogonal and isometric PNG renders.
"""

import os
import sys
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
    embed_materials_in_doc,
)
from phi_works.maker.assembly import (
    create_assembly,
    create_ground_joint,
    create_exploded_view,
    add_exploded_step,
    ensure_assembly_visible,
)


def build():
    init_materials()
    doc_name = "caddy"
    fc_file = os.path.join(script_dir, f"{doc_name}.FCStd")
    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Kombi Kaddy - Mobile STIHL KombiSystem Attachment Rack"
    doc.saveAs(fc_file)

    # ==========================================================================
    # PARAMETRIC CORE DIMENSIONS & AP::VARSET
    # ==========================================================================
    LUMBER_W = 88.9   # 3.5 in (2x4 & 1x4 width)
    LUMBER_T = 38.1   # 1.5 in (2x4 post thickness)
    RAIL_T = 19.05    # 0.75 in (1x4 cross rail & deck thickness)
    CADDY_W = 914.4   # 36.0 in overall rail & deck width
    POST_SPAN = 609.6 # 24.0 in post outer spacing
    OVERHANG = (CADDY_W - POST_SPAN) / 2.0 # 152.4 mm (6.0 in cantilever overhang)
    BASE_L = 381.0    # 15.0 in foot length
    LAP_D = 19.05     # 0.75 in half lap depth
    Y_post = 215.9    # 8.5 in post offset from toe

    # Tool Standing Height & Clip Geometry Calculation:
    Z_deck = LUMBER_W + RAIL_T # 107.95 mm (4.25 in above floor)
    TOOL_STANDING_H = 1003.3 # 39.5 inches standing height
    Z_shaft_top = Z_deck + TOOL_STANDING_H # 1111.25 mm (43.75 in above floor)
    CLIP_GRAB_OFFSET = 25.4 # 1.0 inch below top of shaft
    Z_clip_center = Z_shaft_top - CLIP_GRAB_OFFSET # 1085.85 mm (42.75 in above floor)

    # Top rail centered with spring clips:
    z_top_rail = Z_clip_center - (LUMBER_W / 2.0) # 1041.4 mm (41.0 in above floor)
    CADDY_H = z_top_rail + LUMBER_W # 1130.3 mm (44.5 in overall post height)
    z_lower_pos = LUMBER_W + 150.0

    # Post X Positions (24" outer span centered over 36" rails)
    x_left_post = OVERHANG # 152.4 mm (6.0 in)
    x_right_post = OVERHANG + POST_SPAN - LUMBER_T # 723.9 mm (28.5 in)

    dims = doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "LumberWidth", "Dimensions", "Actual 2x4 Lumber Width").LumberWidth = LUMBER_W
    dims.addProperty("App::PropertyLength", "LumberThickness", "Dimensions", "Actual 2x4 Lumber Thickness").LumberThickness = LUMBER_T
    dims.addProperty("App::PropertyLength", "RailThickness", "Dimensions", "Actual 1x4 Cross Rail & Deck Thickness").RailThickness = RAIL_T
    dims.addProperty("App::PropertyLength", "CaddyHeight", "Dimensions", "Overall Caddy Frame Height").CaddyHeight = CADDY_H
    dims.addProperty("App::PropertyLength", "CaddyWidth", "Dimensions", "Overall Rail & Deck Width").CaddyWidth = CADDY_W
    dims.addProperty("App::PropertyLength", "PostSpan", "Dimensions", "Outside Vertical Post Spacing").PostSpan = POST_SPAN
    dims.addProperty("App::PropertyLength", "RailOverhang", "Dimensions", "Cantilever Rail Overhang on Each Side").RailOverhang = OVERHANG
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Base Foot Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "LapDepth", "Dimensions", "Half Lap Cut Depth").LapDepth = LAP_D
    dims.addProperty("App::PropertyLength", "PostOffset", "Dimensions", "Vertical Post Rearward Offset from Front Toe").PostOffset = Y_post

    # ==========================================================================
    # ROOT ASSEMBLY CONTAINER & SUBGROUPS
    # ==========================================================================
    assy = create_assembly(doc, "Kombi_Kaddy", "Kombi Kaddy - Mobile STIHL KombiSystem Attachment Rack")

    grp_frame = doc.addObject("App::DocumentObjectGroup", "Frame_Woodwork")
    grp_frame.Label = "1. Softwood Frame (2x4 Posts & Feet, 1x4 Cross Rails, Deck Slats)"

    grp_wheels = doc.addObject("App::DocumentObjectGroup", "Running_Gear")
    grp_wheels.Label = "2. Running Gear (5in COTS Wheels & 3/8in Axle Hardware)"

    grp_clips = doc.addObject("App::DocumentObjectGroup", "Tool_Spring_Clips")
    grp_clips.Label = "3. Tool Retention Spring Clips (4 Storage Bays)"

    grp_tools = doc.addObject("App::DocumentObjectGroup", "Installed_STIHL_Fleet")
    grp_tools.Label = "4. Commercial STIHL Attachment Fleet (Trimmer, Bed Redefiner, Blower, Scythe)"

    assy.addObject(grp_frame)
    assy.addObject(grp_wheels)
    assy.addObject(grp_clips)
    assy.addObject(grp_tools)

    # ==========================================================================
    # 1. SOFTWOOD FRAME
    # ==========================================================================
    # A. Base Feet (2x4 standing on 1.5" edge @ X = 6" and X = 28.5")
    def make_sloped_foot(x_offset, is_right):
        foot_box = Part.makeBox(LUMBER_T, BASE_L, LUMBER_W, FreeCAD.Vector(x_offset, 0, 0))
        notch_x = x_offset + LAP_D if not is_right else x_offset - 0.05
        notch = Part.makeBox(LAP_D + 0.1, LUMBER_W, LUMBER_W + 0.1, FreeCAD.Vector(notch_x, Y_post, -0.05))
        
        slope_y_start = Y_post + LUMBER_W
        p1 = FreeCAD.Vector(x_offset - 1.0, slope_y_start, 0)
        p2 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 0)
        p3 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 30.0)
        wedge_poly = Part.makePolygon([p1, p2, p3, p1])
        wedge_face = Part.Face(wedge_poly)
        slope_wedge = wedge_face.extrude(FreeCAD.Vector(LUMBER_T + 2.0, 0, 0))
        return foot_box.cut(notch).cut(slope_wedge)

    lf = doc.addObject("Part::Feature", "Base_Foot_Left")
    lf.Label = "Left Base Foot (2x4 Softwood with Sloped Heel)"
    lf.Shape = make_sloped_foot(x_left_post, False)
    grp_frame.addObject(lf)
    apply_material(lf, "Wood-SoftwoodPine")

    rf = doc.addObject("Part::Feature", "Base_Foot_Right")
    rf.Label = "Right Base Foot (2x4 Softwood with Sloped Heel)"
    rf.Shape = make_sloped_foot(x_right_post, True)
    grp_frame.addObject(rf)
    apply_material(rf, "Wood-SoftwoodPine")

    # Anchor assembly to the left base foot
    create_ground_joint(doc, assy, lf, "GroundJoint_LeftFoot")

    # B. Vertical Posts (2x4 with dado pockets for 1x4 rails)
    def make_post(x_offset, is_right):
        post_box = Part.makeBox(LUMBER_T, LUMBER_W, CADDY_H, FreeCAD.Vector(x_offset, Y_post, 0))
        b_notch_x = x_offset - 0.05 if not is_right else x_offset + LAP_D - 0.05
        b_notch = Part.makeBox(LAP_D + 0.1, LUMBER_W + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(b_notch_x, Y_post - 0.05, -0.05))
        top_pocket = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post - 0.05, z_top_rail - 0.05))
        rear_notch = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post + LUMBER_W - RAIL_T - 0.05, z_lower_pos - 0.05))
        return post_box.cut(b_notch).cut(top_pocket).cut(rear_notch)

    lp = doc.addObject("Part::Feature", "Post_Left")
    lp.Label = "Left Upright Post (2x4 Softwood Dadoed)"
    lp.Shape = make_post(x_left_post, False)
    grp_frame.addObject(lp)
    apply_material(lp, "Wood-SoftwoodPine")

    rp = doc.addObject("Part::Feature", "Post_Right")
    rp.Label = "Right Upright Post (2x4 Softwood Dadoed)"
    rp.Shape = make_post(x_right_post, True)
    grp_frame.addObject(rp)
    apply_material(rp, "Wood-SoftwoodPine")

    # C. Cross Rails (1x4 Lumber: 0.75" x 3.5" x 36.0")
    ur = doc.addObject("Part::Feature", "Upper_Top_Rail_1x4")
    ur.Label = "Upper Clip Rail (1x4 Softwood 36in Span with 6in Cantilevers)"
    ur.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, Y_post, z_top_rail))
    grp_frame.addObject(ur)
    apply_material(ur, "Wood-SoftwoodPine")

    y_lower_rail = Y_post + LUMBER_W - RAIL_T
    lr = doc.addObject("Part::Feature", "Lower_Cross_Rail_Rear_1x4")
    lr.Label = "Lower Stiffener Rail (1x4 Softwood Rear Inset)"
    lr.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, y_lower_rail, z_lower_pos))
    grp_frame.addObject(lr)
    apply_material(lr, "Wood-SoftwoodPine")

    # D. Tool Head Deck Slats (2x 1x4 Lumber @ 36.0")
    deck_slat_1 = doc.addObject("Part::Feature", "Tool_Deck_Slat_Front_1x4")
    deck_slat_1.Label = "Tool Rest Slat Front (1x4 Softwood Deck)"
    deck_slat_1.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 12.0, LUMBER_W))
    grp_frame.addObject(deck_slat_1)
    apply_material(deck_slat_1, "Wood-SoftwoodPine")

    deck_slat_2 = doc.addObject("Part::Feature", "Tool_Deck_Slat_Rear_1x4")
    deck_slat_2.Label = "Tool Rest Slat Rear (1x4 Softwood Deck)"
    deck_slat_2.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 114.0, LUMBER_W))
    grp_frame.addObject(deck_slat_2)
    apply_material(deck_slat_2, "Wood-SoftwoodPine")

    # E. Flat Rear Gussets (3/4" Plywood)
    def make_flat_rear_gusset(is_left):
        y_back = Y_post + LUMBER_W
        if is_left:
            p1 = FreeCAD.Vector(x_left_post, y_back, z_lower_pos)
            p2 = FreeCAD.Vector(x_left_post + 220.0, y_back, z_lower_pos)
            p3 = FreeCAD.Vector(x_left_post, y_back, z_lower_pos + LUMBER_W + 220.0)
        else:
            p1 = FreeCAD.Vector(x_right_post + LUMBER_T, y_back, z_lower_pos)
            p2 = FreeCAD.Vector(x_right_post + LUMBER_T - 220.0, y_back, z_lower_pos)
            p3 = FreeCAD.Vector(x_right_post + LUMBER_T, y_back, z_lower_pos + LUMBER_W + 220.0)
        poly = Part.makePolygon([p1, p2, p3, p1])
        return Part.Face(poly).extrude(FreeCAD.Vector(0, 19.05, 0))

    gl = doc.addObject("Part::Feature", "Plywood_Gusset_Left")
    gl.Label = "Left Rear Triangular Gusset (3/4in Plywood)"
    gl.Shape = make_flat_rear_gusset(True)
    grp_frame.addObject(gl)
    apply_material(gl, "Wood-PlywoodSheathing")

    gr = doc.addObject("Part::Feature", "Plywood_Gusset_Right")
    gr.Label = "Right Rear Triangular Gusset (3/4in Plywood)"
    gr.Shape = make_flat_rear_gusset(False)
    grp_frame.addObject(gr)
    apply_material(gr, "Wood-PlywoodSheathing")

    # ==========================================================================
    # 2. RUNNING GEAR: 5" WHEELS & 3/8" AXLE HARDWARE
    # ==========================================================================
    axle_y = 351.0
    axle_z = 63.5 # 5" wheel radius center

    p_wl = FreeCAD.Placement(FreeCAD.Vector(x_left_post - 22.0, axle_y, axle_z), FreeCAD.Rotation())
    p_wr = FreeCAD.Placement(FreeCAD.Vector(x_right_post + LUMBER_T + 22.0, axle_y, axle_z), FreeCAD.Rotation())

    wheel_left = import_component(doc, "caster_wheel_5in", placement=p_wl, label="Left 5in Caster Wheel", as_link=True)
    wheel_right = import_component(doc, "caster_wheel_5in", placement=p_wr, label="Right 5in Caster Wheel", as_link=True)
    grp_wheels.addObject(wheel_left)
    grp_wheels.addObject(wheel_right)

    # Steel Axle Bolts & Hex Nuts through feet
    axle_l_bolt = Part.makeCylinder(4.76, 75.0, FreeCAD.Vector(x_left_post - 45.0, axle_y, axle_z), FreeCAD.Vector(1, 0, 0))
    axle_l_nut = Part.makeCylinder(8.5, 8.0, FreeCAD.Vector(x_left_post + LUMBER_T + 2.0, axle_y, axle_z), FreeCAD.Vector(1, 0, 0))
    axle_r_bolt = Part.makeCylinder(4.76, 75.0, FreeCAD.Vector(x_right_post - 15.0, axle_y, axle_z), FreeCAD.Vector(1, 0, 0))
    axle_r_nut = Part.makeCylinder(8.5, 8.0, FreeCAD.Vector(x_right_post + LUMBER_T + 42.0, axle_y, axle_z), FreeCAD.Vector(1, 0, 0))

    axles_solid = axle_l_bolt.fuse(axle_l_nut).fuse(axle_r_bolt).fuse(axle_r_nut)
    axle_obj = doc.addObject("Part::Feature", "Wheel_Axle_Hardware")
    axle_obj.Label = "Grade 5 3/8in Axle Bolts, Washers & Locking Nuts"
    axle_obj.Shape = axles_solid
    grp_wheels.addObject(axle_obj)
    apply_material(axle_obj, "Steel-ZincPlated")

    # ==========================================================================
    # 3. TOOL RETENTION SPRING CLIPS (4 SLOTS)
    # ==========================================================================
    clip_margin = 114.3 # 4.5 in from rail ends (Clip 1 & 4 on cantilever overhangs!)
    usable_width = CADDY_W - 2 * clip_margin
    clip_spacing = usable_width / 3.0 # 228.6 mm (9.0 in spacing)

    clip_positions = [clip_margin + (i * clip_spacing) for i in range(4)]
    cy_clip = Y_post - 3.0
    cz_clip = Z_clip_center - 25.0

    for i, cx in enumerate(clip_positions):
        plate = Part.makeBox(45.0, 3.0, 50.0, FreeCAD.Vector(cx - 22.5, cy_clip, cz_clip))
        arm_l = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx - 20.0, cy_clip - 25.0, cz_clip + 7.5))
        arm_r = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx + 8.0, cy_clip - 25.0, cz_clip + 7.5))
        clip_obj = doc.addObject("Part::Feature", f"Spring_Clip_Bay_{i+1}")
        clip_obj.Label = f"Bay {i+1} Tool Retention Spring Clip (25.4mm Tube Grip)"
        clip_obj.Shape = plate.fuse(arm_l).fuse(arm_r)
        grp_clips.addObject(clip_obj)
        apply_material(clip_obj, "Steel-A36")

    # ==========================================================================
    # 4. IMPORT COMMERCIAL STIHL ATTACHMENT FLEET (4 SPECIFIED TOOLS)
    # ==========================================================================
    # Slot 1 (X = 114.3 mm): STIHL FS-KM Straight Shaft String Trimmer
    p_trimmer = FreeCAD.Placement(
        FreeCAD.Vector(clip_positions[0], cy_clip - 18.0, Z_shaft_top),
        FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    )
    trimmer_comp = import_component(
        doc,
        "stihl/tools/kombi_trimmer_fs",
        placement=p_trimmer,
        label="Bay 1: FS-KM String Trimmer Attachment",
        as_link=True,
    )
    if trimmer_comp:
        grp_tools.addObject(trimmer_comp)

    # Slot 2 (X = 342.9 mm): STIHL FBD-KM Bed Redefiner
    p_bed = FreeCAD.Placement(
        FreeCAD.Vector(clip_positions[1], cy_clip - 18.0, Z_shaft_top),
        FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    )
    bed_comp = import_component(
        doc,
        "stihl/tools/kombi_bed_redefiner_fbd",
        placement=p_bed,
        label="Bay 2: FBD-KM Bed Redefiner Attachment",
        as_link=True,
    )
    if bed_comp:
        grp_tools.addObject(bed_comp)

    # Slot 3 (X = 571.5 mm): STIHL BG-KM In-line Axial Blower
    p_blower = FreeCAD.Placement(
        FreeCAD.Vector(clip_positions[2], cy_clip - 18.0, Z_shaft_top),
        FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    )
    blower_comp = import_component(
        doc,
        "stihl/tools/kombi_blower_bg",
        placement=p_blower,
        label="Bay 3: BG-KM Axial Blower Attachment",
        as_link=True,
    )
    if blower_comp:
        grp_tools.addObject(blower_comp)

    # Slot 4 (X = 800.1 mm): STIHL FH-KM 145-deg Articulating Power Scythe
    # Scythe has longer shaft reach with reciprocating cutting bar resting on deck slat
    p_scythe = FreeCAD.Placement(
        FreeCAD.Vector(clip_positions[3], cy_clip - 18.0, Z_deck + 1205.0),
        FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)
    )
    scythe_comp = import_component(
        doc,
        "stihl/tools/kombi_scythe_fh",
        placement=p_scythe,
        label="Bay 4: FH-KM Power Scythe Attachment",
        as_link=True,
    )
    if scythe_comp:
        grp_tools.addObject(scythe_comp)

    # ==========================================================================
    # 5. PROGRAMMATIC EXPLODED VIEW
    # ==========================================================================
    exp_kaddy = create_exploded_view(doc, assy, "ExplodedView_KombiKaddy", "Kombi Kaddy & Tools Exploded View")
    if trimmer_comp:
        add_exploded_step(doc, exp_kaddy, trimmer_comp, FreeCAD.Vector(0, -80, 150), label="Explode Bay 1 Trimmer")
    if bed_comp:
        add_exploded_step(doc, exp_kaddy, bed_comp, FreeCAD.Vector(0, -80, 150), label="Explode Bay 2 Bed Redefiner")
    if blower_comp:
        add_exploded_step(doc, exp_kaddy, blower_comp, FreeCAD.Vector(0, -80, 150), label="Explode Bay 3 Blower")
    if scythe_comp:
        add_exploded_step(doc, exp_kaddy, scythe_comp, FreeCAD.Vector(0, -80, 150), label="Explode Bay 4 Scythe")
    if wheel_left:
        add_exploded_step(doc, exp_kaddy, wheel_left, FreeCAD.Vector(-60, 0, 0), label="Explode Left Wheel")
    if wheel_right:
        add_exploded_step(doc, exp_kaddy, wheel_right, FreeCAD.Vector(60, 0, 0), label="Explode Right Wheel")

    embed_materials_in_doc(doc)
    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Kombi Kaddy Master Assembly Mass Report"))

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, "caddy")
        export_orthogonal_views(gui_d, base_prefix, model_prefix="caddy", camera_type="Perspective")

        # Archive milestone thumbnail
        changelog_dir = os.path.join(script_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)
        home_src = os.path.join(script_dir, "caddy.png")
        home_dst = os.path.join(changelog_dir, "v1.0.0.png")
        if os.path.exists(home_src):
            shutil.copyfile(home_src, home_dst)
            print(f"Archived milestone render to changelog: {home_dst}")

    save_model(doc, fc_file, camera_type="Perspective")
    close_model(doc.Name)
    print(f"Successfully created Kombi Kaddy master model & multi-view renders in {script_dir}")


if __name__ == "__main__":
    build()
    os._exit(0)
