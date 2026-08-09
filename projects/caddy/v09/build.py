import os
import sys
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    HAS_GUI = False

def render_camera_view(gui_doc, png_path):
    if not HAS_GUI or not gui_doc:
        return
    FreeCADGui.updateGui()
    view = gui_doc.activeView()
    if view:
        try:
            view.setCameraType("Orthographic") # 0 - Orthogonal view
            view.viewIsometric()               # Standard Home Isometric angle
            view.fitAll()
        except Exception as e:
            print(f"Camera setup note: {e}")
        view.saveImage(png_path, 1920, 1080, "White")
        print(f"Rendered snapshot: {png_path}")

def build_v9():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    WOOD = (0.82, 0.64, 0.45, 0.0)
    DECK_WOOD = (0.78, 0.58, 0.38, 0.0)
    PLYWOOD = (0.76, 0.60, 0.42, 0.0)
    CLIP = (0.15, 0.15, 0.15, 0.0)
    SHAFT = (0.85, 0.85, 0.88, 0.0)
    RUBBER = (0.12, 0.12, 0.12, 0.0)

    def set_vis(doc, obj, color):
        if HAS_GUI:
            g_obj = FreeCADGui.getDocument(doc.Name).getObject(obj.Name)
            if g_obj:
                g_obj.Visibility = True
                g_obj.ShapeColor = color
                g_obj.DisplayMode = "Flat Lines"

    v9_doc = FreeCAD.newDocument("caddy_v9")
    v9_doc.Label = "Kombi Caddy v9 - Real-World Tool Height & Clip Calibration"

    # Core Dimensions
    LUMBER_W = 88.9   # 3.5 in (2x4 & 1x4 width)
    LUMBER_T = 38.1   # 1.5 in (2x4 post thickness)
    RAIL_T = 19.05    # 0.75 in (1x4 cross rail & deck thickness)
    CADDY_W = 914.4   # 36 in width
    BASE_L = 381.0    # 15 in foot length
    LAP_D = 19.05     # 0.75 in half lap depth
    Y_post_v9 = 215.9 # 8.5 in post offset from toe

    # Tool Standing Height & Clip Geometry Calculation:
    # Deck surface Z = LUMBER_W + RAIL_T = 107.95 mm (4.25 in)
    Z_deck = LUMBER_W + RAIL_T
    TOOL_STANDING_H = 1003.3 # 39.5 inches average height of tool standing on deck
    Z_shaft_top = Z_deck + TOOL_STANDING_H # 1111.25 mm (43.75 in above floor)
    CLIP_GRAB_OFFSET = 25.4 # 1.0 inch below top of shaft
    Z_clip_center = Z_shaft_top - CLIP_GRAB_OFFSET # 1085.85 mm (42.75 in above floor)

    # Top rail centered with spring clips:
    z_top_rail = Z_clip_center - (LUMBER_W / 2.0) # 1041.4 mm (41.0 in above floor)
    CADDY_H = z_top_rail + LUMBER_W # 1130.3 mm (44.5 in overall post height)
    z_lower_pos = LUMBER_W + 150.0

    # --- FreeCAD App::VarSet (dims) ---
    dims = v9_doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "LumberWidth", "Dimensions", "Actual 2x4 Lumber Width").LumberWidth = LUMBER_W
    dims.addProperty("App::PropertyLength", "LumberThickness", "Dimensions", "Actual 2x4 Lumber Thickness").LumberThickness = LUMBER_T
    dims.addProperty("App::PropertyLength", "RailThickness", "Dimensions", "Actual 1x4 Cross Rail & Deck Thickness").RailThickness = RAIL_T
    dims.addProperty("App::PropertyLength", "CaddyHeight", "Dimensions", "Overall Caddy Frame Height").CaddyHeight = CADDY_H
    dims.addProperty("App::PropertyLength", "CaddyWidth", "Dimensions", "Overall Caddy Frame Width").CaddyWidth = CADDY_W
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Base Foot Length").BaseLength = BASE_L
    dims.addProperty("App::PropertyLength", "LapDepth", "Dimensions", "Half Lap Cut Depth").LapDepth = LAP_D
    dims.addProperty("App::PropertyLength", "PostOffset", "Dimensions", "Vertical Post Rearward Offset from Front Toe").PostOffset = Y_post_v9
    dims.addProperty("App::PropertyLength", "ToolStandingHeight", "Tool Specs", "Standing Tool Height from Deck").ToolStandingHeight = TOOL_STANDING_H
    dims.addProperty("App::PropertyLength", "ClipGrabOffsetFromTop", "Tool Specs", "Clip Grab Distance Below Shaft Tip").ClipGrabOffsetFromTop = CLIP_GRAB_OFFSET

    # 1. Base Feet (2x4 standing on 1.5" edge)
    def make_sloped_foot(x_offset, is_right):
        foot_box = Part.makeBox(LUMBER_T, BASE_L, LUMBER_W, FreeCAD.Vector(x_offset, 0, 0))
        notch_x = x_offset + LAP_D if not is_right else x_offset - 0.05
        notch = Part.makeBox(LAP_D + 0.1, LUMBER_W, LUMBER_W + 0.1, FreeCAD.Vector(notch_x, Y_post_v9, -0.05))
        
        slope_y_start = Y_post_v9 + LUMBER_W
        p1 = FreeCAD.Vector(x_offset - 1.0, slope_y_start, 0)
        p2 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 0)
        p3 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 30.0)
        wedge_poly = Part.makePolygon([p1, p2, p3, p1])
        wedge_face = Part.Face(wedge_poly)
        slope_wedge = wedge_face.extrude(FreeCAD.Vector(LUMBER_T + 2.0, 0, 0))
        return foot_box.cut(notch).cut(slope_wedge)

    lf9 = v9_doc.addObject("Part::Feature", "Base_Foot_Left")
    lf9.Shape = make_sloped_foot(0, False)
    set_vis(v9_doc, lf9, WOOD)

    right_x_base = CADDY_W - LUMBER_T
    rf9 = v9_doc.addObject("Part::Feature", "Base_Foot_Right")
    rf9.Shape = make_sloped_foot(right_x_base, True)
    set_vis(v9_doc, rf9, WOOD)

    # 2. Vertical Posts (2x4 with 0.75" dado pockets for 1x4 rails, calibrated height = 44.5")
    def make_v9_post(x_offset, is_right):
        post_box = Part.makeBox(LUMBER_T, LUMBER_W, CADDY_H, FreeCAD.Vector(x_offset, Y_post_v9, 0))
        # Bottom half-lap notch (0.75" deep x 3.5" wide)
        b_notch_x = x_offset - 0.05 if not is_right else x_offset + LAP_D - 0.05
        b_notch = Part.makeBox(LAP_D + 0.1, LUMBER_W + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(b_notch_x, Y_post_v9 - 0.05, -0.05))
        # Top front dado pocket (0.75" deep x 3.5" wide) into front of post (Y_post_v9 to Y_post_v9 + RAIL_T)
        top_pocket = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v9 - 0.05, z_top_rail - 0.05))
        # Rear lower dado pocket (0.75" deep x 3.5" wide) into rear of post (Y_post_v9 + LUMBER_W - RAIL_T to Y_post_v9 + LUMBER_W)
        rear_notch = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v9 + LUMBER_W - RAIL_T - 0.05, z_lower_pos - 0.05))
        return post_box.cut(b_notch).cut(top_pocket).cut(rear_notch)

    lp9 = v9_doc.addObject("Part::Feature", "Post_Left")
    lp9.Shape = make_v9_post(0, False)
    set_vis(v9_doc, lp9, WOOD)

    rp9 = v9_doc.addObject("Part::Feature", "Post_Right")
    rp9.Shape = make_v9_post(right_x_base, True)
    set_vis(v9_doc, rp9, WOOD)

    # 3. Upper Top Rail (1x4 Lumber: 0.75" x 3.5" x 36") - Housed FLUSH inside top front dado pocket!
    ur9 = v9_doc.addObject("Part::Feature", "Upper_Top_Rail_1x4")
    ur9.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, Y_post_v9, z_top_rail))
    set_vis(v9_doc, ur9, WOOD)

    # 4. Lower Rear Cross Rail (1x4 Lumber: 0.75" x 3.5" x 36") - Housed FLUSH inside rear lower dado pocket!
    y_lower_rail_v9 = Y_post_v9 + LUMBER_W - RAIL_T
    lr9 = v9_doc.addObject("Part::Feature", "Lower_Cross_Rail_Rear_1x4")
    lr9.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, y_lower_rail_v9, z_lower_pos))
    set_vis(v9_doc, lr9, WOOD)

    # 5. Tool Head Deck Slats (2x 1x4 Lumber @ 36" running horizontally across base feet)
    deck_slat_1 = v9_doc.addObject("Part::Feature", "Tool_Deck_Slat_Front_1x4")
    deck_slat_1.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 12.0, LUMBER_W))
    set_vis(v9_doc, deck_slat_1, DECK_WOOD)

    deck_slat_2 = v9_doc.addObject("Part::Feature", "Tool_Deck_Slat_Rear_1x4")
    deck_slat_2.Shape = Part.makeBox(CADDY_W, LUMBER_W, RAIL_T, FreeCAD.Vector(0, 114.0, LUMBER_W))
    set_vis(v9_doc, deck_slat_2, DECK_WOOD)

    # 6. Flat Rear-Mounted Plywood Gussets (3/4" Plywood)
    def make_flat_rear_gusset_v9(is_left):
        y_back = Y_post_v9 + LUMBER_W
        if is_left:
            p1 = FreeCAD.Vector(0, y_back, z_lower_pos)
            p2 = FreeCAD.Vector(220.0, y_back, z_lower_pos)
            p3 = FreeCAD.Vector(0, y_back, z_lower_pos + LUMBER_W + 220.0)
        else:
            p1 = FreeCAD.Vector(CADDY_W, y_back, z_lower_pos)
            p2 = FreeCAD.Vector(CADDY_W - 220.0, y_back, z_lower_pos)
            p3 = FreeCAD.Vector(CADDY_W, y_back, z_lower_pos + LUMBER_W + 220.0)
        poly = Part.makePolygon([p1, p2, p3, p1])
        return Part.Face(poly).extrude(FreeCAD.Vector(0, 19.05, 0))

    gl9 = v9_doc.addObject("Part::Feature", "Plywood_Gusset_Left")
    gl9.Shape = make_flat_rear_gusset_v9(True)
    set_vis(v9_doc, gl9, PLYWOOD)

    gr9 = v9_doc.addObject("Part::Feature", "Plywood_Gusset_Right")
    gr9.Shape = make_flat_rear_gusset_v9(False)
    set_vis(v9_doc, gr9, PLYWOOD)

    # 7. Hand-Truck Wheels (5" Fixed Casters)
    w9_left = v9_doc.addObject("Part::Feature", "Wheel_Left")
    w9_left.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(-37.0, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v9_doc, w9_left, RUBBER)

    w9_right = v9_doc.addObject("Part::Feature", "Wheel_Right")
    w9_right.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(919.4, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v9_doc, w9_right, RUBBER)

    # 8. Spring Clips & Kombi Tool Shafts Calibrated to 39.5" Standing Tool Height
    clip_margin = LUMBER_T + 60.0
    usable_width = CADDY_W - 2 * clip_margin
    clip_spacing = usable_width / 3.0

    for i in range(4):
        cx = clip_margin + (i * clip_spacing)
        cy = Y_post_v9 - 3.0
        # Spring clip centered at Z_clip_center (1085.85 mm / 42.75 in)
        cz = Z_clip_center - 25.0

        plate = Part.makeBox(45.0, 3.0, 50.0, FreeCAD.Vector(cx - 22.5, cy, cz))
        arm_l = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx - 20.0, cy - 25.0, cz + 7.5))
        arm_r = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx + 8.0, cy - 25.0, cz + 7.5))
        clip_obj = v9_doc.addObject("Part::Feature", f"Spring_Clip_{i+1}")
        clip_obj.Shape = plate.fuse(arm_l).fuse(arm_r)
        set_vis(v9_doc, clip_obj, CLIP)

        # Shaft sits directly on deck (Z = Z_deck = 107.95 mm) and rises to Z_shaft_top = 1111.25 mm (39.5" tall)
        shaft_obj = v9_doc.addObject("Part::Feature", f"Kombi_Shaft_{i+1}")
        shaft_obj.Shape = Part.makeCylinder(12.7, TOOL_STANDING_H, FreeCAD.Vector(cx, cy - 18.0, Z_deck), FreeCAD.Vector(0,0,1))
        set_vis(v9_doc, shaft_obj, SHAFT)

    v9_doc.recompute()

    v9_fc = os.path.join(script_dir, "caddy_v09.FCStd")
    v9_png = os.path.join(script_dir, "caddy_v09.png")
    v9_doc.saveAs(v9_fc)

    if HAS_GUI:
        gui_d = FreeCADGui.getDocument("caddy_v9")
        if gui_d:
            gui_d.activeView().viewIsometric()
            render_camera_view(gui_d, v9_png)

    FreeCAD.closeDocument("caddy_v9")
    print(f"Successfully created Version 9: {v9_fc} and {v9_png}")

if __name__ == "__main__":
    build_v9()
    sys.exit(0)
