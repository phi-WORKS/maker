"""
Road Roaster 4W - Front Cantilevered Radiant Ceramic Burner Subassembly
Parametric FreeCAD 1.0/1.1 Subassembly Model

Components:
  1. Cantilever 1.5" Square Steel Tubing Arms with 180° Flip Pivot Sleeves
  2. Threaded Turnbuckle Height Adjustment Struts & Deck Masts
  3. 14-Gauge Steel Protective Burner Sled Cowl with Draft Vents
  4. Flexible LP Gas Feed Hose Loop
  5. Solaronics Ceramic Infrared Burner (Linked Component)
"""

import os
import sys
import math
import shutil
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.materials import init_materials, apply_material, get_mass_properties, format_mass_report
from phi_works.maker.components import import_component
from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.assembly import ensure_assembly_visible

def build_cantilever_burner():
    init_materials()
    doc_name = "cantilever_burner"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.saveAs(fcstd_path)

    # Root App::Part container
    part_root = doc.addObject("App::Part", "Cantilever_Burner")
    part_root.Label = "Front Cantilever Burner Subassembly (180° Flip, Cowl & Ceramic Burner)"

    # Geometry constants
    DECK_TOP_Z = 195.0
    DECK_L = 914.4
    FRONT_LIP_Y = -DECK_L / 2.0  # -457.2 mm
    PIVOT_Y = FRONT_LIP_Y - 20.0  # -477.2 mm
    PIVOT_Z = DECK_TOP_Z - 10.0   # 185.0 mm

    BURNER_EXT = 355.6  # 14 in forward reach
    BURNER_Y = FRONT_LIP_Y - BURNER_EXT  # -812.8 mm
    HOVER_Z = 50.8  # 2 in road clearance
    BURNER_W = 609.6  # 24 in width
    BURNER_L = 304.8  # 12 in length
    BURNER_H = 100.0  # Cowl height

    arm_x_positions = [-160.0, 160.0]

    # 1. Dual Cantilever Arms
    ARM_TUBE = 38.1
    arm_solids = []
    for x_a in arm_x_positions:
        sleeve = Part.makeCylinder(12.0, 32.0, FreeCAD.Vector(x_a - 16.0, PIVOT_Y, PIVOT_Z), FreeCAD.Vector(1, 0, 0))
        target_y = BURNER_Y + BURNER_L / 2.0
        target_z = HOVER_Z + BURNER_H - 10.0
        dy = target_y - PIVOT_Y
        dz = target_z - PIVOT_Z
        arm_len = math.hypot(dy, dz)
        angle = math.degrees(math.atan2(dz, dy))

        arm_beam = Part.makeBox(ARM_TUBE, arm_len, ARM_TUBE, FreeCAD.Vector(x_a - ARM_TUBE/2.0, 0, -ARM_TUBE/2.0))
        arm_beam.rotate(FreeCAD.Vector(x_a, 0, 0), FreeCAD.Vector(1, 0, 0), -(180.0 - angle))
        arm_beam.translate(FreeCAD.Vector(0, PIVOT_Y, PIVOT_Z))

        clevis = Part.makeBox(ARM_TUBE + 10.0, 35.0, 45.0, FreeCAD.Vector(x_a - (ARM_TUBE+10)/2.0, target_y - 20.0, target_z - 20.0))
        arm_solids.append(sleeve.fuse(arm_beam).fuse(clevis))

    cantilever_arms_solid = arm_solids[0].fuse(arm_solids[1])

    # 2. Threaded Turnbuckles
    turnbuckle_parts = []
    for x_t in arm_x_positions:
        mast = Part.makeBox(30.0, 25.0, 80.0, FreeCAD.Vector(x_t - 15.0, FRONT_LIP_Y + 30.0, DECK_TOP_Z))
        tb_cyl = Part.makeCylinder(10.0, 90.0, FreeCAD.Vector(x_t, FRONT_LIP_Y + 25.0, DECK_TOP_Z + 75.0),
                                   FreeCAD.Vector(0, -0.85, -0.52).normalize())
        tb_nut = Part.makeCylinder(14.0, 20.0, FreeCAD.Vector(x_t, FRONT_LIP_Y - 10.0, DECK_TOP_Z + 55.0),
                                   FreeCAD.Vector(0, -0.85, -0.52).normalize())
        turnbuckle_parts.append(mast.fuse(tb_cyl).fuse(tb_nut))

    turnbuckle_solid = turnbuckle_parts[0].fuse(turnbuckle_parts[1])

    # 3. 14-Gauge Steel Cowl & Skirts
    SHEET_T = 1.9
    cowl_outer = Part.makeBox(BURNER_W, BURNER_L, BURNER_H,
                              FreeCAD.Vector(-BURNER_W/2.0, BURNER_Y - BURNER_L/2.0, HOVER_Z))
    cowl_inner = Part.makeBox(BURNER_W - 2*SHEET_T, BURNER_L - 2*SHEET_T, BURNER_H + 2.0,
                              FreeCAD.Vector(-BURNER_W/2.0 + SHEET_T, BURNER_Y - BURNER_L/2.0 + SHEET_T, HOVER_Z - 1.0))
    cowl_shell = cowl_outer.cut(cowl_inner)

    vent_w = BURNER_W - 80.0
    vent_h = 30.0
    vent_cut = Part.makeBox(vent_w, 20.0, vent_h,
                            FreeCAD.Vector(-vent_w/2.0, BURNER_Y - BURNER_L/2.0 - 10.0, HOVER_Z + 40.0))
    cowl_shell = cowl_shell.cut(vent_cut)

    top_vent = Part.makeBox(150.0, 180.0, 20.0,
                            FreeCAD.Vector(-75.0, BURNER_Y - 30.0, HOVER_Z + BURNER_H - 10.0))
    cowl_shell = cowl_shell.cut(top_vent)

    # 4. Gas Feed Hose Loop
    p1 = FreeCAD.Vector(0.0, FRONT_LIP_Y + 50.0, DECK_TOP_Z + 20.0)
    p2 = FreeCAD.Vector(0.0, FRONT_LIP_Y - 15.0, PIVOT_Z + 30.0)
    p3 = FreeCAD.Vector(0.0, (FRONT_LIP_Y + BURNER_Y)/2.0, HOVER_Z + BURNER_H + 35.0)
    p4 = FreeCAD.Vector(0.0, BURNER_Y + 120.0, HOVER_Z + BURNER_H - 10.0)

    spline_h = Part.BSplineCurve()
    spline_h.interpolate([p1, p2, p3, p4])
    wire_h = Part.Wire([Part.Edge(spline_h)])
    circ_h = Part.makeCircle(6.0, p1, spline_h.tangent(0.0)[0])
    face_h = Part.Face(Part.Wire([circ_h]))
    hose_solid = wire_h.makePipe(face_h)

    # Create Objects
    obj_arms = doc.addObject("Part::Feature", "Burner_Cantilever_Arms")
    obj_arms.Label = "Cantilever Square-Tube Arms (180-deg Flip & Height Adjust)"
    obj_arms.Shape = cantilever_arms_solid
    part_root.addObject(obj_arms)
    apply_material(obj_arms, "Steel-A36")

    obj_tb = doc.addObject("Part::Feature", "Turnbuckle_Height_Adjuster")
    obj_tb.Label = "Threaded Turnbuckle Height Adjustment Struts"
    obj_tb.Shape = turnbuckle_solid
    part_root.addObject(obj_tb)
    apply_material(obj_tb, "Brass-C360")

    obj_cowl = doc.addObject("Part::Feature", "Burner_Sled_Cowl")
    obj_cowl.Label = "14-Gauge Protective Burner Sled Cowl & Heat Skirts"
    obj_cowl.Shape = cowl_shell
    part_root.addObject(obj_cowl)
    apply_material(obj_cowl, "Steel-A36")

    obj_hose = doc.addObject("Part::Feature", "Burner_Flexible_Gas_Loop")
    obj_hose.Label = "Flexible Reinforced LP Gas Hose Supply Loop"
    obj_hose.Shape = hose_solid
    part_root.addObject(obj_hose)
    apply_material(obj_hose, "Rubber-Solid")

    # 5. Link Solaronics Infrared Ceramic Burner Component
    burner_pos = FreeCAD.Vector(0, BURNER_Y, HOVER_Z + 45.0)
    burner_link = import_component(doc, "solaronics_infrared_burner", placement=FreeCAD.Placement(burner_pos, FreeCAD.Rotation()), as_link=True)
    if burner_link:
        part_root.addObject(burner_link)

    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Cantilever Burner Subassembly Mass Report"))

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Cantilever Burner subassembly build complete.")

if __name__ == "__main__":
    build_cantilever_burner()
    os._exit(0)
