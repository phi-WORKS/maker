import os
import sys
import math
import FreeCAD
import Part

# Ensure src directory is on sys.path for shared imports
maker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
src_dir = os.path.join(maker_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    HAS_GUI = False

from phi_works.maker.render import render_single_view

def render_camera_view(gui_doc, png_path, view_type="Isometric"):
    render_single_view(gui_doc, png_path, view_type=view_type)


def build_v1():
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    STEEL_DARK = (0.28, 0.30, 0.33, 0.0)
    STEEL_BRIGHT = (0.55, 0.58, 0.62, 0.0)

    v1_doc = FreeCAD.newDocument("caddy_v1")
    v1_doc.Label = "Flame Sled v1 - Apex Collar & Closed Pyramid"

    BASE_W = 457.2
    BASE_L = 457.2
    APEX_W = 76.2
    APEX_L = 76.2
    HOOD_H = 152.4
    SKIRT_H = 50.8
    SHEET_T = 1.905
    GROUND_CLR = 12.7

    Z_skirt_bot = GROUND_CLR
    Z_base = Z_skirt_bot + SKIRT_H
    Z_apex = Z_base + HOOD_H

    dims = v1_doc.addObject("App::VarSet", "dims")
    dims.addProperty("App::PropertyLength", "BaseWidth", "Dimensions", "Hood Base Width").BaseWidth = BASE_W
    dims.addProperty("App::PropertyLength", "HoodHeight", "Dimensions", "Pyramid Rise Height").HoodHeight = HOOD_H

    p_b0 = FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_base)
    p_b1 = FreeCAD.Vector(BASE_W/2, -BASE_L/2, Z_base)
    p_b2 = FreeCAD.Vector(BASE_W/2, BASE_L/2, Z_base)
    p_b3 = FreeCAD.Vector(-BASE_W/2, BASE_L/2, Z_base)

    p_a0 = FreeCAD.Vector(-APEX_W/2, -APEX_L/2, Z_apex)
    p_a1 = FreeCAD.Vector(APEX_W/2, -APEX_L/2, Z_apex)
    p_a2 = FreeCAD.Vector(APEX_W/2, APEX_L/2, Z_apex)
    p_a3 = FreeCAD.Vector(-APEX_W/2, APEX_L/2, Z_apex)

    pyr_outer = Part.makeLoft([
        Part.makePolygon([p_b0, p_b1, p_b2, p_b3, p_b0]),
        Part.makePolygon([p_a0, p_a1, p_a2, p_a3, p_a0])
    ], True)

    p_in_b0 = FreeCAD.Vector(-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, Z_base - 0.1)
    p_in_b1 = FreeCAD.Vector(BASE_W/2 - SHEET_T, -BASE_L/2 + SHEET_T, Z_base - 0.1)
    p_in_b2 = FreeCAD.Vector(BASE_W/2 - SHEET_T, BASE_L/2 - SHEET_T, Z_base - 0.1)
    p_in_b3 = FreeCAD.Vector(-BASE_W/2 + SHEET_T, BASE_L/2 - SHEET_T, Z_base - 0.1)

    p_in_a0 = FreeCAD.Vector(-APEX_W/2 + SHEET_T, -APEX_L/2 + SHEET_T, Z_apex + 0.1)
    p_in_a1 = FreeCAD.Vector(APEX_W/2 - SHEET_T, -APEX_L/2 + SHEET_T, Z_apex + 0.1)
    p_in_a2 = FreeCAD.Vector(APEX_W/2 - SHEET_T, APEX_L/2 - SHEET_T, Z_apex + 0.1)
    p_in_a3 = FreeCAD.Vector(-APEX_W/2 + SHEET_T, APEX_L/2 - SHEET_T, Z_apex + 0.1)

    pyr_inner = Part.makeLoft([
        Part.makePolygon([p_in_b0, p_in_b1, p_in_b2, p_in_b3, p_in_b0]),
        Part.makePolygon([p_in_a0, p_in_a1, p_in_a2, p_in_a3, p_in_a0])
    ], True)

    pyramid_shell = pyr_outer.cut(pyr_inner)

    skirt_outer = Part.makeBox(BASE_W, BASE_L, SKIRT_H, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, Z_skirt_bot))
    skirt_inner = Part.makeBox(BASE_W - 2*SHEET_T, BASE_L - 2*SHEET_T, SKIRT_H + 0.2, FreeCAD.Vector(-BASE_W/2 + SHEET_T, -BASE_L/2 + SHEET_T, Z_skirt_bot - 0.1))
    skirt_shell = skirt_outer.cut(skirt_inner)

    hood_full = pyramid_shell.fuse(skirt_shell)
    vent_box = Part.makeBox(304.8, SHEET_T * 4.0, 38.1, FreeCAD.Vector(-152.4, BASE_L/2 - SHEET_T*2, Z_base - 38.1))
    hood_with_vent = hood_full.cut(vent_box)

    hood_obj = v1_doc.addObject("Part::Feature", "Pyramidal_Hood_v1")
    hood_obj.Shape = hood_with_vent

    skid_l = Part.makeBox(38.1, BASE_L, 4.76, FreeCAD.Vector(-BASE_W/2, -BASE_L/2, 0))
    skid_r = Part.makeBox(38.1, BASE_L, 4.76, FreeCAD.Vector(BASE_W/2 - 38.1, -BASE_L/2, 0))
    skids_obj = v1_doc.addObject("Part::Feature", "Dual_Skid_Runners")
    skids_obj.Shape = skid_l.fuse(skid_r)

    collar_pipe = Part.makeCylinder(24.13, 152.4, FreeCAD.Vector(0, 0, Z_apex - 25.4), FreeCAD.Vector(0, 0.5735, 0.8191))
    collar_inner = Part.makeCylinder(20.44, 160.0, FreeCAD.Vector(0, 0, Z_apex - 30.0), FreeCAD.Vector(0, 0.5735, 0.8191))
    collar_obj = v1_doc.addObject("Part::Feature", "Apex_Pipe_Collar")
    collar_obj.Shape = collar_pipe.cut(collar_inner)

    # RECOMPUTE FIRST BEFORE GUI SETUP
    v1_doc.recompute()

    if HAS_GUI:
        gui_d = FreeCADGui.getDocument(v1_doc.Name)
        if gui_d:
            g_h = gui_d.getObject(hood_obj.Name)
            if g_h:
                g_h.ShapeColor = STEEL_DARK
                g_h.Visibility = True
                g_h.DisplayMode = "Flat Lines"

            g_s = gui_d.getObject(skids_obj.Name)
            if g_s:
                g_s.ShapeColor = STEEL_BRIGHT
                g_s.Visibility = True
                g_s.DisplayMode = "Flat Lines"

            g_c = gui_d.getObject(collar_obj.Name)
            if g_c:
                g_c.ShapeColor = STEEL_BRIGHT
                g_c.Visibility = True
                g_c.DisplayMode = "Flat Lines"

            gui_d.activeView().viewIsometric()
            gui_d.activeView().fitAll()
        FreeCADGui.updateGui()

    fc_file = os.path.join(script_dir, "sled_v01.FCStd")
    png_file = os.path.join(script_dir, "sled_v01.png")
    v1_doc.saveAs(fc_file)
    if HAS_GUI:
        render_camera_view(FreeCADGui.getDocument(v1_doc.Name), png_file)

    FreeCAD.closeDocument("caddy_v1")
    print(f"Built Version 1: {fc_file} and {png_file}")

if __name__ == "__main__":
    build_v1()
    sys.exit(0)
