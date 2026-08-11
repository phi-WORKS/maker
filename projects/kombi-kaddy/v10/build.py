import os
import sys
import FreeCAD
import Part

maker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
src_dir = os.path.join(maker_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views

def set_vis(doc, obj, color):
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        if gui_d:
            g_obj = gui_d.getObject(obj.Name)
            if g_obj:
                g_obj.Visibility = True
                g_obj.ShapeColor = color
                g_obj.DisplayMode = "Flat Lines"

def build_v10():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
    caddy_dir = os.path.dirname(script_dir)

    WOOD = (0.82, 0.64, 0.45, 0.0)
    DECK_WOOD = (0.78, 0.58, 0.38, 0.0)
    PLYWOOD = (0.76, 0.60, 0.42, 0.0)
    CLIP = (0.15, 0.15, 0.15, 0.0)
    SHAFT = (0.85, 0.85, 0.88, 0.0)
    RUBBER = (0.12, 0.12, 0.12, 0.0)

    v10_doc = FreeCAD.newDocument("caddy_v10")
    v10_doc.Label = "Kombi Kaddy v10 - 24in Post Spacing & 6in Cantilever Rail Overhangs"

    # Core Dimensions
    LUMBER_W = 88.9   # 3.5 in (2x4 & 1x4 width)
    LUMBER_T = 38.1   # 1.5 in (2x4 post thickness)
    RAIL_T = 19.05    # 0.75 in (1x4 cross rail & deck thickness)
    CADDY_W = 914.4   # 36.0 in overall rail & deck width
    POST_SPAN = 609.6 # 24.0 in post outer spacing
    OVERHANG = (CADDY_W - POST_SPAN) / 2.0 # 152.4 mm (6.0 in cantilever overhang)
    BASE_L = 381.0    # 15.0 in foot length
    LAP_D = 19.05     # 0.75 in half lap depth
    Y_post_v10 = 215.9 # 8.5 in post offset from toe

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

    # --- FreeCAD App::VarSet (dims) ---
    dims = v10_doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "LumberWidth", "Dimensions", "Actual 2x4 Lumber Width").LumberWidth = LUMBER_W
    dims.addProperty("App::PropertyLength", "LumberThickness", "Dimensions", "Actual 2x4 Lumber Thickness").LumberThickness = LUMBER_T
    dims.addProperty("App::PropertyLength", "RailThickness", "Dimensions", "Actual 1x4 Cross Rail & Deck Thickness").RailThickness = RAIL_T
    dims.addProperty("App::PropertyLength", "CaddyHeight", "Dimensions", "Overall Caddy Frame Height").CaddyHeight = CADDY_H
    dims.addProperty("App::PropertyLength", "CaddyWidth", "Dimensions", "Overall Rail & Deck Width").CaddyWidth = CADDY_W
    dims.addProperty("App::PropertyLength", "PostSpan", "Dimensions", "Outside Vertical Post Spacing").PostSpan = POST_SPAN
    dims.addProperty("App::PropertyLength", "RailOverhang", "Dimensions", "Cantilever Rail Overhang on Each Side").RailOverhang = OVERHANG
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Base Foot Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "LapDepth", "Dimensions", "Half Lap Cut Depth").LapDepth = LAP_D
    dims.addProperty("App::PropertyLength", "PostOffset", "Dimensions", "Vertical Post Rearward Offset from Front Toe").PostOffset = Y_post_v10

    # 1. Base Feet (2x4 standing on 1.5" edge @ X = 6" and X = 28.5")
    def make_sloped_foot(x_offset, is_right):
        foot_box = Part.makeBox(LUMBER_T, BASE_L, LUMBER_W, FreeCAD.Vector(x_offset, 0, 0))
        notch_x = x_offset + LAP_D if not is_right else x_offset - 0.05
        notch = Part.makeBox(LAP_D + 0.1, LUMBER_W, LUMBER_W + 0.1, FreeCAD.Vector(notch_x, Y_post_v10, -0.05))
        
        slope_y_start = Y_post_v10 + LUMBER_W
        p1 = FreeCAD.Vector(x_offset - 1.0, slope_y_start, 0)
        p2 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 0)
        p3 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 30.0)
        wedge_poly = Part.makePolygon([p1, p2, p3, p1])
        wedge_face = Part.Face(wedge_poly)
        slope_wedge = wedge_face.extrude(FreeCAD.Vector(LUMBER_T + 2.0, 0, 0))
        return foot_box.cut(notch).cut(slope_wedge)

    lf10 = v10_doc.addObject("Part::Feature", "Base_Foot_Left")
    lf10.Shape = make_sloped_foot(x_left_post, False)
    set_vis(v10_doc, lf10, WOOD)

    rf10 = v10_doc.addObject("Part::Feature", "Base_Foot_Right")
    rf10.Shape = make_sloped_foot(x_right_post, True)
    set_vis(v10_doc, rf10, WOOD)

    # 2. Vertical Posts (2x4 @ X = 6" and X = 28.5" with 0.75" dado pockets for 1x4 rails)
    def make_v10_post(x_offset, is_right):
        post_box = Part.makeBox(LUMBER_T, LUMBER_W, CADDY_H, FreeCAD.Vector(x_offset, Y_post_v10, 0))
        # Bottom half-lap notch (0.75" deep x 3.5" wide)
        b_notch_x = x_offset - 0.05 if not is_right else x_offset + LAP_D - 0.05
        b_notch = Part.makeBox(LAP_D + 0.1, LUMBER_W + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(b_notch_x, Y_post_v10 - 0.05, -0.05))
        # Top front dado pocket (0.75" deep x 3.5" wide) into front of post (Y_post_v10 to Y_post_v10 + RAIL_T)
        top_pocket = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v10 - 0.05, z_top_rail - 0.05))
        # Rear lower dado pocket (0.75" deep x 3.5" wide) into rear of post (Y_post_v10 + LUMBER_W - RAIL_T to Y_post_v10 + LUMBER_W)
        rear_notch = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v10 + LUMBER_W - RAIL_T - 0.05, z_lower_pos - 0.05))
        return post_box.cut(b_notch).cut(top_pocket).cut(rear_notch)

    lp10 = v10_doc.addObject("Part::Feature", "Post_Left")
    lp10.Shape = make_v10_post(x_left_post, False)
    set_vis(v10_doc, lp10, WOOD)

    rp10 = v10_doc.addObject("Part::Feature", "Post_Right")
    rp10.Shape = make_v10_post(x_right_post, True)
    set_vis(v10_doc, rp10, WOOD)

    # 3. Upper Top Rail (1x4 Lumber: 0.75" x 3.5" x 36.0") - 6" Cantilever Overhang on each side!
    ur10 = v10_doc.addObject("Part::Feature", "Upper_Top_Rail_1x4")
    ur10.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, Y_post_v10, z_top_rail))
    set_vis(v10_doc, ur10, WOOD)

    # 4. Lower Rear Cross Rail (1x4 Lumber: 0.75" x 3.5" x 36.0") - 6" Cantilever Overhang on each side!
    y_lower_rail_v10 = Y_post_v10 + LUMBER_W - RAIL_T
    lr10 = v10_doc.addObject("Part::Feature", "Lower_Cross_Rail_Rear_1x4")
    lr10.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, y_lower_rail_v10, z_lower_pos))
    set_vis(v10_doc, lr10, WOOD)

    # 5. Tool Head Deck Slats (2x 1x4 Lumber @ 36.0" running horizontally across base feet)
    deck_slat_1 = v10_doc.addObject("Part::Feature", "Tool_Deck_Slat_Front_1x4")
    deck_slat_1.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 12.0, LUMBER_W))
    set_vis(v10_doc, deck_slat_1, DECK_WOOD)

    deck_slat_2 = v10_doc.addObject("Part::Feature", "Tool_Deck_Slat_Rear_1x4")
    deck_slat_2.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 114.0, LUMBER_W))
    set_vis(v10_doc, deck_slat_2, DECK_WOOD)

    # 6. Flat Rear-Mounted Plywood Gussets (3/4" Plywood mounted across post span)
    def make_flat_rear_gusset_v10(is_left):
        y_back = Y_post_v10 + LUMBER_W
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

    gl10 = v10_doc.addObject("Part::Feature", "Plywood_Gusset_Left")
    gl10.Shape = make_flat_rear_gusset_v10(True)
    set_vis(v10_doc, gl10, PLYWOOD)

    gr10 = v10_doc.addObject("Part::Feature", "Plywood_Gusset_Right")
    gr10.Shape = make_flat_rear_gusset_v10(False)
    set_vis(v10_doc, gr10, PLYWOOD)

    # 7. Hand-Truck Wheels (5" Fixed Casters mounted at outer face of base feet)
    w10_left = v10_doc.addObject("Part::Feature", "Wheel_Left")
    w10_left.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(x_left_post - 37.0, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v10_doc, w10_left, RUBBER)

    w10_right = v10_doc.addObject("Part::Feature", "Wheel_Right")
    w10_right.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(x_right_post + LUMBER_T + 5.0, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v10_doc, w10_right, RUBBER)

    # 8. Spring Clips & Kombi Tool Shafts Spaced Across Full 36" Rail Width
    clip_margin = 114.3 # 4.5 in from rail ends (Clip 1 & 4 on cantilever overhangs!)
    usable_width = CADDY_W - 2 * clip_margin
    clip_spacing = usable_width / 3.0

    for i in range(4):
        cx = clip_margin + (i * clip_spacing)
        cy = Y_post_v10 - 3.0
        cz = Z_clip_center - 25.0

        plate = Part.makeBox(45.0, 3.0, 50.0, FreeCAD.Vector(cx - 22.5, cy, cz))
        arm_l = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx - 20.0, cy - 25.0, cz + 7.5))
        arm_r = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx + 8.0, cy - 25.0, cz + 7.5))
        clip_obj = v10_doc.addObject("Part::Feature", f"Spring_Clip_{i+1}")
        clip_obj.Shape = plate.fuse(arm_l).fuse(arm_r)
        set_vis(v10_doc, clip_obj, CLIP)

        shaft_obj = v10_doc.addObject("Part::Feature", f"Kombi_Shaft_{i+1}")
        shaft_obj.Shape = Part.makeCylinder(12.7, TOOL_STANDING_H, FreeCAD.Vector(cx, cy - 18.0, Z_deck), FreeCAD.Vector(0,0,1))
        set_vis(v10_doc, shaft_obj, SHAFT)

    v10_doc.recompute()

    v10_fc = os.path.join(script_dir, "caddy_v10.FCStd")
    v10_png = os.path.join(script_dir, "caddy_v10.png")
    v10_doc.saveAs(v10_fc)

    if HAS_GUI:
        try:
            import FreeCADGui
            gui_d = FreeCADGui.getDocument("caddy_v10")
            if gui_d:
                base_prefix = os.path.join(script_dir, "caddy_v10")
                export_orthogonal_views(gui_d, base_prefix)
        except Exception as e:
            print(f"Render error: {e}")

    FreeCAD.closeDocument("caddy_v10")
    print(f"Successfully created Version 10 model & multi-view renders in {script_dir}")

if __name__ == "__main__":
    build_v10()
    sys.exit(0)
