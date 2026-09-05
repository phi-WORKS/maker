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

from phi_works.maker.render import render_single_view
from phi_works.maker.materials import apply_material, get_mass_properties, format_mass_report

def render_camera_view(gui_doc, png_path):
    render_single_view(gui_doc, png_path, view_type="Isometric")


def create_kombi_tools():
    doc_name = "kombi_tools"
    try:
        if FreeCAD.getDocument(doc_name):
            FreeCAD.closeDocument(doc_name)
    except Exception:
        pass

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "STIHL Kombi Attachment Models"

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
    grp_fs.addObject(ofs_s)
    apply_material(ofs_s, "Aluminum-6061-T6")

    ofs_c = doc.addObject("Part::Feature", "FS_Coupler")
    ofs_c.Shape = coup_fs
    grp_fs.addObject(ofs_c)
    apply_material(ofs_c, "Plastic-ABS")

    ofs_g = doc.addObject("Part::Feature", "FS_Gear_Spool")
    ofs_g.Shape = gear_fs.fuse(spool_fs)
    grp_fs.addObject(ofs_g)
    apply_material(ofs_g, "Plastic-ABS")

    ofs_sh = doc.addObject("Part::Feature", "FS_Debris_Shield")
    ofs_sh.Shape = shield_fs
    grp_fs.addObject(ofs_sh)
    apply_material(ofs_sh, "PowderCoat-StihlOrange")

    # 2. KM-HL: 145° Adjustable Hedge Trimmer Attachment (Length ~1260mm / 1480mm max)
    grp_hl = doc.addObject("App::DocumentObjectGroup", "KM_HL_HedgeTrimmer")
    shaft_hl, coup_hl = make_shaft_and_coupler(750.0)
    gear_hl = Part.makeBox(60.0, 90.0, 80.0, FreeCAD.Vector(-30.0, -45.0, -830.0))
    blade_hl = Part.makeBox(12.0, 45.0, 500.0, FreeCAD.Vector(-6.0, 10.0, -1330.0))

    ohl_s = doc.addObject("Part::Feature", "HL_Shaft")
    ohl_s.Shape = shaft_hl
    grp_hl.addObject(ohl_s)
    apply_material(ohl_s, "Aluminum-6061-T6")

    ohl_c = doc.addObject("Part::Feature", "HL_Coupler")
    ohl_c.Shape = coup_hl
    grp_hl.addObject(ohl_c)
    apply_material(ohl_c, "Plastic-ABS")

    ohl_g = doc.addObject("Part::Feature", "HL_Gearbox")
    ohl_g.Shape = gear_hl
    grp_hl.addObject(ohl_g)
    apply_material(ohl_g, "PowderCoat-StihlOrange")

    ohl_b = doc.addObject("Part::Feature", "HL_Blades")
    ohl_b.Shape = blade_hl
    grp_hl.addObject(ohl_b)
    apply_material(ohl_b, "Steel-A36")

    # 3. KM-HT: Pole Pruner / Chainsaw Attachment (Length ~1260mm)
    grp_ht = doc.addObject("App::DocumentObjectGroup", "KM_HT_PolePruner")
    shaft_ht, coup_ht = make_shaft_and_coupler(900.0)
    head_ht = Part.makeBox(80.0, 130.0, 110.0, FreeCAD.Vector(-40.0, -50.0, -1010.0))
    bar_ht = Part.makeBox(8.0, 300.0, 75.0, FreeCAD.Vector(-4.0, 50.0, -1000.0))

    oht_s = doc.addObject("Part::Feature", "HT_Shaft")
    oht_s.Shape = shaft_ht
    grp_ht.addObject(oht_s)
    apply_material(oht_s, "Aluminum-6061-T6")

    oht_c = doc.addObject("Part::Feature", "HT_Coupler")
    oht_c.Shape = coup_ht
    grp_ht.addObject(oht_c)
    apply_material(oht_c, "Plastic-ABS")

    oht_g = doc.addObject("Part::Feature", "HT_SawHead")
    oht_g.Shape = head_ht
    grp_ht.addObject(oht_g)
    apply_material(oht_g, "PowderCoat-StihlOrange")

    oht_b = doc.addObject("Part::Feature", "HT_GuideBar")
    oht_b.Shape = bar_ht
    grp_ht.addObject(oht_b)
    apply_material(oht_b, "Steel-A36")

    # 4. KM-BF: Mini-Cultivator Tiller Attachment (Length ~1000mm)
    grp_bf = doc.addObject("App::DocumentObjectGroup", "KM_BF_Cultivator")
    shaft_bf, coup_bf = make_shaft_and_coupler(800.0)
    gear_bf = Part.makeBox(80.0, 100.0, 120.0, FreeCAD.Vector(-40.0, -50.0, -920.0))
    tines_bf = Part.makeCylinder(100.0, 220.0, FreeCAD.Vector(-110.0, 0, -900.0), FreeCAD.Vector(1, 0, 0))

    obf_s = doc.addObject("Part::Feature", "BF_Shaft")
    obf_s.Shape = shaft_bf
    grp_bf.addObject(obf_s)
    apply_material(obf_s, "Aluminum-6061-T6")

    obf_c = doc.addObject("Part::Feature", "BF_Coupler")
    obf_c.Shape = coup_bf
    grp_bf.addObject(obf_c)
    apply_material(obf_c, "Plastic-ABS")

    obf_g = doc.addObject("Part::Feature", "BF_Gearbox")
    obf_g.Shape = gear_bf
    grp_bf.addObject(obf_g)
    apply_material(obf_g, "Plastic-ABS")

    obf_t = doc.addObject("Part::Feature", "BF_TineRotors")
    obf_t.Shape = tines_bf
    grp_bf.addObject(obf_t)
    apply_material(obf_t, "Steel-A36")

    # 5. KM-BG: Leaf Blower Attachment (Length ~890mm)
    grp_bg = doc.addObject("App::DocumentObjectGroup", "KM_BG_Blower")
    shaft_bg, coup_bg = make_shaft_and_coupler(500.0)
    fan_housing = Part.makeCylinder(110.0, 150.0, FreeCAD.Vector(0, 0, -650.0), FreeCAD.Vector(0, 1, 0))
    nozzle_bg = Part.makeCone(60.0, 35.0, 400.0, FreeCAD.Vector(0, 75.0, -650.0), FreeCAD.Vector(0, 1, 0))

    obg_s = doc.addObject("Part::Feature", "BG_Shaft")
    obg_s.Shape = shaft_bg
    grp_bg.addObject(obg_s)
    apply_material(obg_s, "Aluminum-6061-T6")

    obg_c = doc.addObject("Part::Feature", "BG_Coupler")
    obg_c.Shape = coup_bg
    grp_bg.addObject(obg_c)
    apply_material(obg_c, "Plastic-ABS")

    obg_h = doc.addObject("Part::Feature", "BG_FanHousing")
    obg_h.Shape = fan_housing
    grp_bg.addObject(obg_h)
    apply_material(obg_h, "PowderCoat-StihlOrange")

    obg_n = doc.addObject("Part::Feature", "BG_Nozzle")
    obg_n.Shape = nozzle_bg
    grp_bg.addObject(obg_n)
    apply_material(obg_n, "Plastic-ABS")

    # 6. KM-KW: PowerSweep Rubber Paddle Attachment (Length ~1250mm)
    grp_kw = doc.addObject("App::DocumentObjectGroup", "KM_KW_PowerSweep")
    shaft_kw, coup_kw = make_shaft_and_coupler(800.0)
    gear_kw = Part.makeBox(70.0, 90.0, 100.0, FreeCAD.Vector(-35.0, -45.0, -900.0))
    drum_kw = Part.makeCylinder(135.0, 600.0, FreeCAD.Vector(-300.0, 0, -900.0), FreeCAD.Vector(1, 0, 0))

    okw_s = doc.addObject("Part::Feature", "KW_Shaft")
    okw_s.Shape = shaft_kw
    grp_kw.addObject(okw_s)
    apply_material(okw_s, "Aluminum-6061-T6")

    okw_c = doc.addObject("Part::Feature", "KW_Coupler")
    okw_c.Shape = coup_kw
    grp_kw.addObject(okw_c)
    apply_material(okw_c, "Plastic-ABS")

    okw_g = doc.addObject("Part::Feature", "KW_Gearbox")
    okw_g.Shape = gear_kw
    grp_kw.addObject(okw_g)
    apply_material(okw_g, "Plastic-ABS")

    okw_d = doc.addObject("Part::Feature", "KW_RubberDrum")
    okw_d.Shape = drum_kw
    grp_kw.addObject(okw_d)
    apply_material(okw_d, "Rubber-Solid")

    # 7. KM-FCB: Curved Shaft Lawn Edger Attachment (Length ~920mm)
    grp_fc = doc.addObject("App::DocumentObjectGroup", "KM_FCB_Edger")
    shaft_fc, coup_fc = make_shaft_and_coupler(800.0)
    guard_fc = Part.makeCylinder(110.0, 20.0, FreeCAD.Vector(0, 0, -850.0), FreeCAD.Vector(1, 0, 0))
    wheel_fc = Part.makeCylinder(50.0, 25.0, FreeCAD.Vector(60.0, 0, -850.0), FreeCAD.Vector(1, 0, 0))

    ofc_s = doc.addObject("Part::Feature", "FC_Shaft")
    ofc_s.Shape = shaft_fc
    grp_fc.addObject(ofc_s)
    apply_material(ofc_s, "Aluminum-6061-T6")

    ofc_c = doc.addObject("Part::Feature", "FC_Coupler")
    ofc_c.Shape = coup_fc
    grp_fc.addObject(ofc_c)
    apply_material(ofc_c, "Plastic-ABS")

    ofc_g = doc.addObject("Part::Feature", "FC_Guard")
    ofc_g.Shape = guard_fc
    grp_fc.addObject(ofc_g)
    apply_material(ofc_g, "PowderCoat-StihlOrange")

    ofc_w = doc.addObject("Part::Feature", "FC_Wheel")
    ofc_w.Shape = wheel_fc
    grp_fc.addObject(ofc_w)
    apply_material(ofc_w, "Rubber-Solid")

    # Arrange tools horizontally along X axis
    all_groups = [grp_fs, grp_hl, grp_ht, grp_bf, grp_bg, grp_kw, grp_fc]
    for idx, grp in enumerate(all_groups):
        x_shift = idx * 350.0
        for obj in grp.Group:
            obj.Placement.Base = FreeCAD.Vector(x_shift, 0, 0)

    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="STIHL Kombi Tools Suite Mass Report"))

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
