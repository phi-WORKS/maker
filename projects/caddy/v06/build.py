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
            view.setCameraType("Orthographic") # Orthogonal view mode
            view.viewIsometric()
        except Exception as e:
            print(f"Camera setup note: {e}")
        view.fitAll()
        view.saveImage(png_path, 1920, 1080, "White")
        print(f"Rendered snapshot: {png_path}")

def build_v6():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    WOOD = (0.82, 0.64, 0.45, 0.0)
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

    v6_doc = FreeCAD.newDocument("caddy_v6")
    v6_doc.Label = "Kombi Caddy v6 - Rearward Post Offset & App::VarSet"

    # --- FreeCAD App::VarSet (dims) ---
    dims = v6_doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "LumberWidth", "Dimensions", "Actual 2x4 Lumber Width").LumberWidth = 88.9
    dims.addProperty("App::PropertyLength", "LumberThickness", "Dimensions", "Actual 2x4 Lumber Thickness").LumberThickness = 38.1
    dims.addProperty("App::PropertyLength", "CaddyHeight", "Dimensions", "Overall Caddy Frame Height").CaddyHeight = 1066.8
    dims.addProperty("App::PropertyLength", "CaddyWidth", "Dimensions", "Overall Caddy Frame Width").CaddyWidth = 914.4
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Base Foot Length").BaseLength = 381.0
    dims.addProperty("App::PropertyLength", "LapDepth", "Dimensions", "Half Lap Cut Depth").LapDepth = 19.05
    dims.addProperty("App::PropertyLength", "PostOffset", "Dimensions", "Vertical Post Rearward Offset from Front Toe").PostOffset = 215.9

    LUMBER_W = 88.9
    LUMBER_T = 38.1
    CADDY_H = 1066.8
    CADDY_W = 914.4
    BASE_L = 381.0
    LAP_D = 19.05
    Y_post_v6 = 215.9  # 8.5" rearward offset from front toe (gives 8.5" front overhang clearance for tool heads)
    z_top_rail = CADDY_H - LUMBER_W
    z_lower_pos = LUMBER_W + 150.0

    def make_sloped_foot(x_offset, is_right):
        foot_box = Part.makeBox(LUMBER_T, BASE_L, LUMBER_W, FreeCAD.Vector(x_offset, 0, 0))
        notch_x = x_offset + LAP_D if not is_right else x_offset - 0.05
        notch = Part.makeBox(LAP_D + 0.1, LUMBER_W, LUMBER_W + 0.1, FreeCAD.Vector(notch_x, Y_post_v6, -0.05))
        
        slope_y_start = Y_post_v6 + LUMBER_W
        p1 = FreeCAD.Vector(x_offset - 1.0, slope_y_start, 0)
        p2 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 0)
        p3 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 30.0)
        wedge_poly = Part.makePolygon([p1, p2, p3, p1])
        wedge_face = Part.Face(wedge_poly)
        slope_wedge = wedge_face.extrude(FreeCAD.Vector(LUMBER_T + 2.0, 0, 0))
        return foot_box.cut(notch).cut(slope_wedge)

    lf6 = v6_doc.addObject("Part::Feature", "Base_Foot_Left")
    lf6.Shape = make_sloped_foot(0, False)
    set_vis(v6_doc, lf6, WOOD)

    right_x_base = CADDY_W - LUMBER_T
    rf6 = v6_doc.addObject("Part::Feature", "Base_Foot_Right")
    rf6.Shape = make_sloped_foot(right_x_base, True)
    set_vis(v6_doc, rf6, WOOD)

    def make_v6_post(x_offset, is_right):
        post_box = Part.makeBox(LUMBER_T, LUMBER_W, CADDY_H, FreeCAD.Vector(x_offset, Y_post_v6, 0))
        b_notch_x = x_offset - 0.05 if not is_right else x_offset + LAP_D - 0.05
        b_notch = Part.makeBox(LAP_D + 0.1, LUMBER_W + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(b_notch_x, Y_post_v6 - 0.05, -0.05))
        top_pocket = Part.makeBox(LUMBER_T + 0.1, LAP_D + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v6 - 0.05, z_top_rail - 0.05))
        rear_notch = Part.makeBox(LUMBER_T + 0.1, LUMBER_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v6 + LUMBER_W - LUMBER_T - 0.05, z_lower_pos - 0.05))
        return post_box.cut(b_notch).cut(top_pocket).cut(rear_notch)

    lp6 = v6_doc.addObject("Part::Feature", "Post_Left")
    lp6.Shape = make_v6_post(0, False)
    set_vis(v6_doc, lp6, WOOD)

    rp6 = v6_doc.addObject("Part::Feature", "Post_Right")
    rp6.Shape = make_v6_post(right_x_base, True)
    set_vis(v6_doc, rp6, WOOD)

    ur6 = v6_doc.addObject("Part::Feature", "Upper_Top_Rail")
    ur6.Shape = Part.makeBox(CADDY_W, LUMBER_T, LUMBER_W, FreeCAD.Vector(0, Y_post_v6 - LAP_D, z_top_rail))
    set_vis(v6_doc, ur6, WOOD)

    y_lower_rail_v6 = Y_post_v6 + LUMBER_W - LUMBER_T
    lr6 = v6_doc.addObject("Part::Feature", "Lower_Cross_Rail_Rear")
    lr6.Shape = Part.makeBox(CADDY_W, LUMBER_T, LUMBER_W, FreeCAD.Vector(0, y_lower_rail_v6, z_lower_pos))
    set_vis(v6_doc, lr6, WOOD)

    def make_flat_rear_gusset_v6(is_left):
        y_back = Y_post_v6 + LUMBER_W
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

    gl6 = v6_doc.addObject("Part::Feature", "Plywood_Gusset_Left")
    gl6.Shape = make_flat_rear_gusset_v6(True)
    set_vis(v6_doc, gl6, PLYWOOD)

    gr6 = v6_doc.addObject("Part::Feature", "Plywood_Gusset_Right")
    gr6.Shape = make_flat_rear_gusset_v6(False)
    set_vis(v6_doc, gr6, PLYWOOD)

    w6_left = v6_doc.addObject("Part::Feature", "Wheel_Left")
    w6_left.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(-37.0, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v6_doc, w6_left, RUBBER)

    w6_right = v6_doc.addObject("Part::Feature", "Wheel_Right")
    w6_right.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(919.4, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v6_doc, w6_right, RUBBER)

    clip_margin = LUMBER_T + 60.0
    usable_width = CADDY_W - 2 * clip_margin
    clip_spacing = usable_width / 3.0

    for i in range(4):
        cx = clip_margin + (i * clip_spacing)
        cy = Y_post_v6 - LAP_D - 3.0
        cz = z_top_rail + (LUMBER_W / 2.0) - 25.0

        plate = Part.makeBox(45.0, 3.0, 50.0, FreeCAD.Vector(cx - 22.5, cy, cz))
        arm_l = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx - 20.0, cy - 25.0, cz + 7.5))
        arm_r = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx + 8.0, cy - 25.0, cz + 7.5))
        clip_obj = v6_doc.addObject("Part::Feature", f"Spring_Clip_{i+1}")
        clip_obj.Shape = plate.fuse(arm_l).fuse(arm_r)
        set_vis(v6_doc, clip_obj, CLIP)

        shaft_obj = v6_doc.addObject("Part::Feature", f"Kombi_Shaft_{i+1}")
        shaft_obj.Shape = Part.makeCylinder(12.7, 850.0, FreeCAD.Vector(cx, cy - 18.0, cz - 600.0), FreeCAD.Vector(0,0,1))
        set_vis(v6_doc, shaft_obj, SHAFT)

    v6_doc.recompute()

    v6_fc = os.path.join(script_dir, "caddy_v06.FCStd")
    v6_png = os.path.join(script_dir, "caddy_v06.png")
    v6_doc.saveAs(v6_fc)

    if HAS_GUI:
        render_camera_view(FreeCADGui.getDocument("caddy_v6"), v6_png)

    FreeCAD.closeDocument("caddy_v6")
    print(f"Successfully created Version 6: {v6_fc} and {v6_png}")

if __name__ == "__main__":
    build_v6()
    sys.exit(0)
