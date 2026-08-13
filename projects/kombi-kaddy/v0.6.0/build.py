import os
import sys
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import render_single_view

def render_camera_view(gui_doc, png_path):
    render_single_view(gui_doc, png_path, view_type="Isometric")


def build_v7():
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

    v7_doc = FreeCAD.newDocument("caddy_v7")
    v7_doc.Label = "Kombi Caddy v7 - 1x4 Cross Rails & App::VarSet"

    # --- FreeCAD App::VarSet (dims) ---
    dims = v7_doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "LumberWidth", "Dimensions", "Actual 2x4 Lumber Width").LumberWidth = 88.9
    dims.addProperty("App::PropertyLength", "LumberThickness", "Dimensions", "Actual 2x4 Lumber Thickness").LumberThickness = 38.1
    dims.addProperty("App::PropertyLength", "RailThickness", "Dimensions", "Actual 1x4 Cross Rail Thickness").RailThickness = 19.05
    dims.addProperty("App::PropertyLength", "CaddyHeight", "Dimensions", "Overall Caddy Frame Height").CaddyHeight = 1066.8
    dims.addProperty("App::PropertyLength", "CaddyWidth", "Dimensions", "Overall Caddy Frame Width").CaddyWidth = 914.4
    dims.addProperty("App::PropertyLength", "BaseLength", "Dimensions", "Base Foot Length").BaseLength = 381.0
    dims.addProperty("App::PropertyLength", "LapDepth", "Dimensions", "Half Lap Cut Depth").LapDepth = 19.05
    dims.addProperty("App::PropertyLength", "PostOffset", "Dimensions", "Vertical Post Rearward Offset from Front Toe").PostOffset = 215.9

    LUMBER_W = 88.9   # 3.5 in (2x4 & 1x4 width)
    LUMBER_T = 38.1   # 1.5 in (2x4 post thickness)
    RAIL_T = 19.05    # 0.75 in (1x4 cross rail thickness)
    CADDY_H = 1066.8
    CADDY_W = 914.4
    BASE_L = 381.0
    LAP_D = 19.05
    Y_post_v7 = 215.9 # 8.5" rearward offset from front toe
    z_top_rail = CADDY_H - LUMBER_W
    z_lower_pos = LUMBER_W + 150.0

    # 1. Base Feet (2x4 standing on 1.5" edge)
    def make_sloped_foot(x_offset, is_right):
        foot_box = Part.makeBox(LUMBER_T, BASE_L, LUMBER_W, FreeCAD.Vector(x_offset, 0, 0))
        notch_x = x_offset + LAP_D if not is_right else x_offset - 0.05
        notch = Part.makeBox(LAP_D + 0.1, LUMBER_W, LUMBER_W + 0.1, FreeCAD.Vector(notch_x, Y_post_v7, -0.05))
        
        slope_y_start = Y_post_v7 + LUMBER_W
        p1 = FreeCAD.Vector(x_offset - 1.0, slope_y_start, 0)
        p2 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 0)
        p3 = FreeCAD.Vector(x_offset - 1.0, BASE_L + 1.0, 30.0)
        wedge_poly = Part.makePolygon([p1, p2, p3, p1])
        wedge_face = Part.Face(wedge_poly)
        slope_wedge = wedge_face.extrude(FreeCAD.Vector(LUMBER_T + 2.0, 0, 0))
        return foot_box.cut(notch).cut(slope_wedge)

    lf7 = v7_doc.addObject("Part::Feature", "Base_Foot_Left")
    lf7.Shape = make_sloped_foot(0, False)
    set_vis(v7_doc, lf7, WOOD)

    right_x_base = CADDY_W - LUMBER_T
    rf7 = v7_doc.addObject("Part::Feature", "Base_Foot_Right")
    rf7.Shape = make_sloped_foot(right_x_base, True)
    set_vis(v7_doc, rf7, WOOD)

    # 2. Vertical Posts (2x4 with 0.75" dado pockets for 1x4 rails)
    def make_v7_post(x_offset, is_right):
        post_box = Part.makeBox(LUMBER_T, LUMBER_W, CADDY_H, FreeCAD.Vector(x_offset, Y_post_v7, 0))
        # Bottom half-lap notch (0.75" deep x 3.5" wide)
        b_notch_x = x_offset - 0.05 if not is_right else x_offset + LAP_D - 0.05
        b_notch = Part.makeBox(LAP_D + 0.1, LUMBER_W + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(b_notch_x, Y_post_v7 - 0.05, -0.05))
        # Top front dado pocket (0.75" deep x 3.5" wide) into front of post (Y_post_v7 to Y_post_v7 + RAIL_T)
        top_pocket = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v7 - 0.05, z_top_rail - 0.05))
        # Rear lower dado pocket (0.75" deep x 3.5" wide) into rear of post (Y_post_v7 + LUMBER_W - RAIL_T to Y_post_v7 + LUMBER_W)
        rear_notch = Part.makeBox(LUMBER_T + 0.1, RAIL_T + 0.1, LUMBER_W + 0.1, FreeCAD.Vector(x_offset - 0.05, Y_post_v7 + LUMBER_W - RAIL_T - 0.05, z_lower_pos - 0.05))
        return post_box.cut(b_notch).cut(top_pocket).cut(rear_notch)

    lp7 = v7_doc.addObject("Part::Feature", "Post_Left")
    lp7.Shape = make_v7_post(0, False)
    set_vis(v7_doc, lp7, WOOD)

    rp7 = v7_doc.addObject("Part::Feature", "Post_Right")
    rp7.Shape = make_v7_post(right_x_base, True)
    set_vis(v7_doc, rp7, WOOD)

    # 3. Upper Top Rail (1x4 Lumber: 0.75" x 3.5" x 36") - Housed FLUSH inside top front dado pocket!
    ur7 = v7_doc.addObject("Part::Feature", "Upper_Top_Rail_1x4")
    ur7.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, Y_post_v7, z_top_rail))
    set_vis(v7_doc, ur7, WOOD)

    # 4. Lower Rear Cross Rail (1x4 Lumber: 0.75" x 3.5" x 36") - Housed FLUSH inside rear lower dado pocket!
    y_lower_rail_v7 = Y_post_v7 + LUMBER_W - RAIL_T
    lr7 = v7_doc.addObject("Part::Feature", "Lower_Cross_Rail_Rear_1x4")
    lr7.Shape = Part.makeBox(CADDY_W, RAIL_T, LUMBER_W, FreeCAD.Vector(0, y_lower_rail_v7, z_lower_pos))
    set_vis(v7_doc, lr7, WOOD)

    # 5. Flat Rear-Mounted Plywood Gussets (3/4" Plywood)
    def make_flat_rear_gusset_v7(is_left):
        y_back = Y_post_v7 + LUMBER_W
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

    gl7 = v7_doc.addObject("Part::Feature", "Plywood_Gusset_Left")
    gl7.Shape = make_flat_rear_gusset_v7(True)
    set_vis(v7_doc, gl7, PLYWOOD)

    gr7 = v7_doc.addObject("Part::Feature", "Plywood_Gusset_Right")
    gr7.Shape = make_flat_rear_gusset_v7(False)
    set_vis(v7_doc, gr7, PLYWOOD)

    # 6. Hand-Truck Wheels (5" Fixed Casters)
    w7_left = v7_doc.addObject("Part::Feature", "Wheel_Left")
    w7_left.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(-37.0, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v7_doc, w7_left, RUBBER)

    w7_right = v7_doc.addObject("Part::Feature", "Wheel_Right")
    w7_right.Shape = Part.makeCylinder(63.5, 32.0, FreeCAD.Vector(919.4, 351.0, 63.5), FreeCAD.Vector(1,0,0))
    set_vis(v7_doc, w7_right, RUBBER)

    # 7. Spring Clips & Kombi Tool Shafts (Mounted on front face of flush 1x4 top rail)
    clip_margin = LUMBER_T + 60.0
    usable_width = CADDY_W - 2 * clip_margin
    clip_spacing = usable_width / 3.0

    for i in range(4):
        cx = clip_margin + (i * clip_spacing)
        cy = Y_post_v7 - 3.0
        cz = z_top_rail + (LUMBER_W / 2.0) - 25.0

        plate = Part.makeBox(45.0, 3.0, 50.0, FreeCAD.Vector(cx - 22.5, cy, cz))
        arm_l = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx - 20.0, cy - 25.0, cz + 7.5))
        arm_r = Part.makeBox(12.0, 25.0, 35.0, FreeCAD.Vector(cx + 8.0, cy - 25.0, cz + 7.5))
        clip_obj = v7_doc.addObject("Part::Feature", f"Spring_Clip_{i+1}")
        clip_obj.Shape = plate.fuse(arm_l).fuse(arm_r)
        set_vis(v7_doc, clip_obj, CLIP)

        shaft_obj = v7_doc.addObject("Part::Feature", f"Kombi_Shaft_{i+1}")
        shaft_obj.Shape = Part.makeCylinder(12.7, 850.0, FreeCAD.Vector(cx, cy - 18.0, cz - 600.0), FreeCAD.Vector(0,0,1))
        set_vis(v7_doc, shaft_obj, SHAFT)

    v7_doc.recompute()

    v7_fc = os.path.join(script_dir, "caddy_v07.FCStd")
    v7_png = os.path.join(script_dir, "caddy_v07.png")
    v7_doc.saveAs(v7_fc)

    if HAS_GUI:
        gui_d = FreeCADGui.getDocument("caddy_v7")
        if gui_d:
            gui_d.activeView().viewIsometric()
            render_camera_view(gui_d, v7_png)

    FreeCAD.closeDocument("caddy_v7")
    print(f"Successfully updated Version 7: {v7_fc} and {v7_png}")

if __name__ == "__main__":
    build_v7()
    sys.exit(0)
