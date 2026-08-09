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
            view.setCameraType("Orthographic")
            view.viewIsometric()
        except Exception as e:
            print(f"Camera setup note: {e}")
        view.fitAll()
        view.saveImage(png_path, 1920, 1080, "White")
        print(f"Rendered snapshot: {png_path}")

def create_kombi_tools():
    doc_name = "kombi_tools"
    try:
        if FreeCAD.getDocument(doc_name):
            FreeCAD.closeDocument(doc_name)
    except Exception:
        pass

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "STIHL Kombi Attachment Models"

    # Color Palette
    SHAFT_COLOR = (0.85, 0.85, 0.88, 0.0)    # Aluminum shaft
    COUPLER_COLOR = (0.15, 0.15, 0.15, 0.0)  # Matte black plastic coupler
    STIHL_ORANGE = (0.95, 0.35, 0.05, 0.0)   # STIHL Orange
    STEEL_COLOR = (0.70, 0.70, 0.72, 0.0)    # Metal blade/tine
    RUBBER_COLOR = (0.12, 0.12, 0.12, 0.0)   # Black rubber paddle

    def setup_vis(obj, color):
        if HAS_GUI:
            try:
                g_obj = FreeCADGui.getDocument(doc.Name).getObject(obj.Name)
                if g_obj:
                    g_obj.Visibility = True
                    g_obj.ShapeColor = color
                    g_obj.DisplayMode = "Flat Lines"
            except Exception:
                pass

    def make_shaft_and_coupler(length_mm=850.0):
        # Standard 25.4mm (1.0") OD drive shaft tube
        shaft = Part.makeCylinder(12.7, length_mm, FreeCAD.Vector(0, 0, -length_mm), FreeCAD.Vector(0, 0, 1))
        # Top quick-connect coupling sleeve (28mm OD x 100mm)
        coupler = Part.makeCylinder(14.0, 100.0, FreeCAD.Vector(0, 0, -100.0), FreeCAD.Vector(0, 0, 1))
        return shaft, coupler

    # 1. KM-FS: Line Trimmer Attachment (Length ~920mm)
    grp_fs = doc.addObject("App::DocumentObjectGroup", "KM_FS_Trimmer")
    shaft_fs, coup_fs = make_shaft_and_coupler(800.0)
    gear_fs = Part.makeCylinder(20.0, 60.0, FreeCAD.Vector(0, 0, -840.0), FreeCAD.Vector(0, 0, 1))
    spool_fs = Part.makeCylinder(60.0, 45.0, FreeCAD.Vector(0, 0, -885.0), FreeCAD.Vector(0, 0, 1))
    shield_fs = Part.makeBox(360.0, 200.0, 40.0, FreeCAD.Vector(-180.0, -50.0, -840.0))

    ofs_s = doc.addObject("Part::Feature", "FS_Shaft")
    ofs_s.Shape = shaft_fs
    setup_vis(ofs_s, SHAFT_COLOR)
    grp_fs.addObject(ofs_s)

    ofs_c = doc.addObject("Part::Feature", "FS_Coupler")
    ofs_c.Shape = coup_fs
    setup_vis(ofs_c, COUPLER_COLOR)
    grp_fs.addObject(ofs_c)

    ofs_g = doc.addObject("Part::Feature", "FS_Gear_Spool")
    ofs_g.Shape = gear_fs.fuse(spool_fs)
    setup_vis(ofs_g, COUPLER_COLOR)
    grp_fs.addObject(ofs_g)

    ofs_sh = doc.addObject("Part::Feature", "FS_Debris_Shield")
    ofs_sh.Shape = shield_fs
    setup_vis(ofs_sh, STIHL_ORANGE)
    grp_fs.addObject(ofs_sh)

    # 2. KM-HL: 145° Adjustable Hedge Trimmer Attachment (Length ~1260mm / 1480mm max)
    grp_hl = doc.addObject("App::DocumentObjectGroup", "KM_HL_HedgeTrimmer")
    shaft_hl, coup_hl = make_shaft_and_coupler(750.0)
    gear_hl = Part.makeBox(60.0, 90.0, 80.0, FreeCAD.Vector(-30.0, -45.0, -830.0))
    blade_hl = Part.makeBox(12.0, 45.0, 500.0, FreeCAD.Vector(-6.0, 10.0, -1330.0))

    ohl_s = doc.addObject("Part::Feature", "HL_Shaft")
    ohl_s.Shape = shaft_hl
    setup_vis(ohl_s, SHAFT_COLOR)
    grp_hl.addObject(ohl_s)

    ohl_c = doc.addObject("Part::Feature", "HL_Coupler")
    ohl_c.Shape = coup_hl
    setup_vis(ohl_c, COUPLER_COLOR)
    grp_hl.addObject(ohl_c)

    ohl_g = doc.addObject("Part::Feature", "HL_Gearbox")
    ohl_g.Shape = gear_hl
    setup_vis(ohl_g, STIHL_ORANGE)
    grp_hl.addObject(ohl_g)

    ohl_b = doc.addObject("Part::Feature", "HL_Blades")
    ohl_b.Shape = blade_hl
    setup_vis(ohl_b, STEEL_COLOR)
    grp_hl.addObject(ohl_b)

    # 3. KM-HT: Pole Pruner / Chainsaw Attachment (Length ~1260mm)
    grp_ht = doc.addObject("App::DocumentObjectGroup", "KM_HT_PolePruner")
    shaft_ht, coup_ht = make_shaft_and_coupler(900.0)
    head_ht = Part.makeBox(80.0, 130.0, 110.0, FreeCAD.Vector(-40.0, -50.0, -1010.0))
    bar_ht = Part.makeBox(8.0, 300.0, 75.0, FreeCAD.Vector(-4.0, 50.0, -1000.0))

    oht_s = doc.addObject("Part::Feature", "HT_Shaft")
    oht_s.Shape = shaft_ht
    setup_vis(oht_s, SHAFT_COLOR)
    grp_ht.addObject(oht_s)

    oht_c = doc.addObject("Part::Feature", "HT_Coupler")
    oht_c.Shape = coup_ht
    setup_vis(oht_c, COUPLER_COLOR)
    grp_ht.addObject(oht_c)

    oht_g = doc.addObject("Part::Feature", "HT_SawHead")
    oht_g.Shape = head_ht
    setup_vis(oht_g, STIHL_ORANGE)
    grp_ht.addObject(oht_g)

    oht_b = doc.addObject("Part::Feature", "HT_GuideBar")
    oht_b.Shape = bar_ht
    setup_vis(oht_b, STEEL_COLOR)
    grp_ht.addObject(oht_b)

    # 4. KM-BF: Mini-Cultivator Tiller Attachment (Length ~1000mm)
    grp_bf = doc.addObject("App::DocumentObjectGroup", "KM_BF_Cultivator")
    shaft_bf, coup_bf = make_shaft_and_coupler(800.0)
    gear_bf = Part.makeBox(80.0, 100.0, 120.0, FreeCAD.Vector(-40.0, -50.0, -920.0))
    tines_bf = Part.makeCylinder(100.0, 220.0, FreeCAD.Vector(-110.0, 0, -900.0), FreeCAD.Vector(1, 0, 0))

    obf_s = doc.addObject("Part::Feature", "BF_Shaft")
    obf_s.Shape = shaft_bf
    setup_vis(obf_s, SHAFT_COLOR)
    grp_bf.addObject(obf_s)

    obf_c = doc.addObject("Part::Feature", "BF_Coupler")
    obf_c.Shape = coup_bf
    setup_vis(obf_c, COUPLER_COLOR)
    grp_bf.addObject(obf_c)

    obf_g = doc.addObject("Part::Feature", "BF_Gearbox")
    obf_g.Shape = gear_bf
    setup_vis(obf_g, COUPLER_COLOR)
    grp_bf.addObject(obf_g)

    obf_t = doc.addObject("Part::Feature", "BF_TineRotors")
    obf_t.Shape = tines_bf
    setup_vis(obf_t, STEEL_COLOR)
    grp_bf.addObject(obf_t)

    # 5. KM-BG: Leaf Blower Attachment (Length ~890mm)
    grp_bg = doc.addObject("App::DocumentObjectGroup", "KM_BG_Blower")
    shaft_bg, coup_bg = make_shaft_and_coupler(500.0)
    fan_housing = Part.makeCylinder(110.0, 150.0, FreeCAD.Vector(0, 0, -650.0), FreeCAD.Vector(0, 1, 0))
    nozzle_bg = Part.makeCone(60.0, 35.0, 400.0, FreeCAD.Vector(0, 75.0, -650.0), FreeCAD.Vector(0, 1, 0))

    obg_s = doc.addObject("Part::Feature", "BG_Shaft")
    obg_s.Shape = shaft_bg
    setup_vis(obg_s, SHAFT_COLOR)
    grp_bg.addObject(obg_s)

    obg_c = doc.addObject("Part::Feature", "BG_Coupler")
    obg_c.Shape = coup_bg
    setup_vis(obg_c, COUPLER_COLOR)
    grp_bg.addObject(obg_c)

    obg_h = doc.addObject("Part::Feature", "BG_FanHousing")
    obg_h.Shape = fan_housing
    setup_vis(obg_h, STIHL_ORANGE)
    grp_bg.addObject(obg_h)

    obg_n = doc.addObject("Part::Feature", "BG_Nozzle")
    obg_n.Shape = nozzle_bg
    setup_vis(obg_n, COUPLER_COLOR)
    grp_bg.addObject(obg_n)

    # 6. KM-KW: PowerSweep Rubber Paddle Attachment (Length ~1250mm)
    grp_kw = doc.addObject("App::DocumentObjectGroup", "KM_KW_PowerSweep")
    shaft_kw, coup_kw = make_shaft_and_coupler(800.0)
    gear_kw = Part.makeBox(70.0, 90.0, 100.0, FreeCAD.Vector(-35.0, -45.0, -900.0))
    drum_kw = Part.makeCylinder(135.0, 600.0, FreeCAD.Vector(-300.0, 0, -900.0), FreeCAD.Vector(1, 0, 0))

    okw_s = doc.addObject("Part::Feature", "KW_Shaft")
    okw_s.Shape = shaft_kw
    setup_vis(okw_s, SHAFT_COLOR)
    grp_kw.addObject(okw_s)

    okw_c = doc.addObject("Part::Feature", "KW_Coupler")
    okw_c.Shape = coup_kw
    setup_vis(okw_c, COUPLER_COLOR)
    grp_kw.addObject(okw_c)

    okw_g = doc.addObject("Part::Feature", "KW_Gearbox")
    okw_g.Shape = gear_kw
    setup_vis(okw_g, COUPLER_COLOR)
    grp_kw.addObject(okw_g)

    okw_d = doc.addObject("Part::Feature", "KW_RubberDrum")
    okw_d.Shape = drum_kw
    setup_vis(okw_d, RUBBER_COLOR)
    grp_kw.addObject(okw_d)

    # 7. KM-FCB: Curved Shaft Lawn Edger Attachment (Length ~920mm)
    grp_fc = doc.addObject("App::DocumentObjectGroup", "KM_FCB_Edger")
    shaft_fc, coup_fc = make_shaft_and_coupler(800.0)
    guard_fc = Part.makeCylinder(110.0, 20.0, FreeCAD.Vector(0, 0, -850.0), FreeCAD.Vector(1, 0, 0))
    wheel_fc = Part.makeCylinder(50.0, 25.0, FreeCAD.Vector(60.0, 0, -850.0), FreeCAD.Vector(1, 0, 0))

    ofc_s = doc.addObject("Part::Feature", "FC_Shaft")
    ofc_s.Shape = shaft_fc
    setup_vis(ofc_s, SHAFT_COLOR)
    grp_fc.addObject(ofc_s)

    ofc_c = doc.addObject("Part::Feature", "FC_Coupler")
    ofc_c.Shape = coup_fc
    setup_vis(ofc_c, COUPLER_COLOR)
    grp_fc.addObject(ofc_c)

    ofc_g = doc.addObject("Part::Feature", "FC_Guard")
    ofc_g.Shape = guard_fc
    setup_vis(ofc_g, STIHL_ORANGE)
    grp_fc.addObject(ofc_g)

    ofc_w = doc.addObject("Part::Feature", "FC_Wheel")
    ofc_w.Shape = wheel_fc
    setup_vis(ofc_w, RUBBER_COLOR)
    grp_fc.addObject(ofc_w)

    # Arrange tools horizontally along X axis
    all_groups = [grp_fs, grp_hl, grp_ht, grp_bf, grp_bg, grp_kw, grp_fc]
    for idx, grp in enumerate(all_groups):
        x_shift = idx * 350.0
        for obj in grp.Group:
            obj.Placement.Base = FreeCAD.Vector(x_shift, 0, 0)

    doc.recompute()

    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
    fc_path = os.path.join(script_dir, "kombi_tools.FCStd")
    png_path = os.path.join(script_dir, "kombi_tools.png")
    doc.saveAs(fc_path)
    print(f"Saved FreeCAD Kombi tools to {fc_path}")

    if HAS_GUI:
        render_camera_view(FreeCADGui.getDocument(doc_name), png_path)

if __name__ == "__main__":
    create_kombi_tools()
    sys.exit(0)
