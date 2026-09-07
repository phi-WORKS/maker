"""
Road Roaster 4W - Auxiliary Spot Torch Wand & Water Safety Reservoir Subassembly
Parametric FreeCAD 1.0/1.1 Subassembly Model

Components:
  1. 2.5-Gallon Pressurized Water Safety Reservoir (Linked Component)
  2. Heavy-Duty Steel Deck Cradle Bracket
  3. Harbor Freight #91037 Spot Torch Wand in Vertical Stirrup (Linked Component)
  4. Quick-Draw Upper Stirrup Loop & Lower Guide Saddle Clamped to Push Handle
  5. Auxiliary Spot Torch Reinforced Rubber Supply Hose
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

def build_aux_torch_safety():
    init_materials()
    doc_name = "aux_torch_safety"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.saveAs(fcstd_path)

    # Root App::Part container
    part_root = doc.addObject("App::Part", "Auxiliary_Torch_Safety")
    part_root.Label = "Auxiliary Spot Torch & Water Safety Subassembly (Torch, Cradle & Water Tank)"

    DECK_TOP_Z = 195.0
    DECK_L = 914.4
    HANDLE_Y = DECK_L / 2.0 - 45.0  # +412.2 mm

    WATER_X = -170.0
    WATER_Y = 220.0
    WATER_R = 90.0

    TORCH_X = 200.0
    TORCH_Y = HANDLE_Y + 28.0
    TORCH_Z = DECK_TOP_Z + 700.0  # Z = 895.0 mm

    z_rail_upper = DECK_TOP_Z + 480.0  # 675.0 mm
    z_rail_lower = DECK_TOP_Z + 240.0  # 435.0 mm

    # 1. Deck Cradle Bracket for Water Tank
    cradle_base = Part.makeBox(200.0, 200.0, 6.0, FreeCAD.Vector(WATER_X - 100.0, WATER_Y - 100.0, DECK_TOP_Z))
    cradle_lip = Part.makeCylinder(WATER_R + 5.0, 35.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z), FreeCAD.Vector(0, 0, 1))
    cradle_inner = Part.makeCylinder(WATER_R + 1.0, 40.0, FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z - 1.0), FreeCAD.Vector(0, 0, 1))
    cradle_solid = cradle_base.fuse(cradle_lip.cut(cradle_inner))

    # 2. Stirrup Loop & Guide Saddle for Spot Torch
    clamp_top = Part.makeBox(35.0, 24.0, 22.0, FreeCAD.Vector(TORCH_X - 17.5, HANDLE_Y - 12.0, z_rail_upper - 11.0))
    bore_top = Part.makeCylinder(12.7, 40.0, FreeCAD.Vector(TORCH_X - 20.0, HANDLE_Y, z_rail_upper), FreeCAD.Vector(1, 0, 0))
    clamp_top = clamp_top.cut(bore_top)
    arm_top = Part.makeBox(12.0, TORCH_Y - HANDLE_Y, 8.0, FreeCAD.Vector(TORCH_X - 6.0, HANDLE_Y, z_rail_upper - 4.0))
    loop_outer = Part.makeCylinder(22.0, 22.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_upper - 11.0), FreeCAD.Vector(0, 0, 1))
    loop_inner = Part.makeCylinder(15.0, 26.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_upper - 13.0), FreeCAD.Vector(0, 0, 1))
    stirrup_top_loop = loop_outer.cut(loop_inner)

    clamp_bot = Part.makeBox(35.0, 24.0, 20.0, FreeCAD.Vector(TORCH_X - 17.5, HANDLE_Y - 12.0, z_rail_lower - 10.0))
    bore_bot = Part.makeCylinder(12.7, 40.0, FreeCAD.Vector(TORCH_X - 20.0, HANDLE_Y, z_rail_lower), FreeCAD.Vector(1, 0, 0))
    clamp_bot = clamp_bot.cut(bore_bot)
    arm_bot = Part.makeBox(10.0, TORCH_Y - HANDLE_Y, 6.0, FreeCAD.Vector(TORCH_X - 5.0, HANDLE_Y, z_rail_lower - 3.0))
    saddle_out = Part.makeCylinder(18.0, 18.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_lower - 9.0), FreeCAD.Vector(0, 0, 1))
    saddle_in = Part.makeCylinder(11.0, 22.0, FreeCAD.Vector(TORCH_X, TORCH_Y, z_rail_lower - 11.0), FreeCAD.Vector(0, 0, 1))
    stirrup_bot_saddle = saddle_out.cut(saddle_in)

    stirrups_solid = clamp_top.fuse(arm_top).fuse(stirrup_top_loop).fuse(clamp_bot).fuse(arm_bot).fuse(stirrup_bot_saddle)

    # 3. Flexible Gas Hose to Torch
    p_tee = FreeCAD.Vector(75.0 + 42.5, 220.0 + 80.0, DECK_TOP_Z + 497.5)
    p_torch_in = FreeCAD.Vector(TORCH_X, TORCH_Y - 10.0, TORCH_Z)
    p_mid = FreeCAD.Vector((75.0 + 42.5 + TORCH_X)/2.0 + 15.0, HANDLE_Y - 10.0, (DECK_TOP_Z + 497.5 + TORCH_Z)/2.0 + 20.0)

    spline_t = Part.BSplineCurve()
    spline_t.interpolate([p_tee, p_mid, p_torch_in])
    wire_t = Part.Wire([Part.Edge(spline_t)])
    circ_t = Part.makeCircle(4.76, p_tee, spline_t.tangent(0.0)[0])
    face_t = Part.Face(Part.Wire([circ_t]))
    torch_supply_hose = wire_t.makePipe(face_t)

    # Document Objects
    obj_cradle = doc.addObject("Part::Feature", "Water_Tank_Deck_Cradle")
    obj_cradle.Label = "Water Safety Tank Quick-Lock Deck Cradle"
    obj_cradle.Shape = cradle_solid
    part_root.addObject(obj_cradle)
    apply_material(obj_cradle, "Steel-A36")

    obj_stirrups = doc.addObject("Part::Feature", "Torch_Handle_Stirrup_Holster")
    obj_stirrups.Label = "Quick-Draw Torch Handle Stirrup Loop & Guide Saddle"
    obj_stirrups.Shape = stirrups_solid
    part_root.addObject(obj_stirrups)
    apply_material(obj_stirrups, "Steel-ZincPlated")

    obj_t_hose = doc.addObject("Part::Feature", "Torch_Auxiliary_Gas_Hose")
    obj_t_hose.Label = "Auxiliary Spot Torch Flexible Gas Hose"
    obj_t_hose.Shape = torch_supply_hose
    part_root.addObject(obj_t_hose)
    apply_material(obj_t_hose, "Rubber-Solid")

    # 4. Link Water Tank Component
    water_pos = FreeCAD.Vector(WATER_X, WATER_Y, DECK_TOP_Z)
    water_link = import_component(doc, "water_tank", placement=FreeCAD.Placement(water_pos, FreeCAD.Rotation()), as_link=True)
    if water_link:
        part_root.addObject(water_link)

    # 5. Link Harbor Freight Spot Torch Component
    torch_pos = FreeCAD.Vector(TORCH_X, TORCH_Y, TORCH_Z)
    torch_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 180)
    torch_link = import_component(doc, "torch_hf91037", placement=FreeCAD.Placement(torch_pos, torch_rot), as_link=True)
    if torch_link:
        part_root.addObject(torch_link)

    ensure_assembly_visible(doc)
    doc.recompute()

    report = get_mass_properties(doc)
    print(format_mass_report(report, title="Auxiliary Torch & Water Safety Mass Report"))

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        base_prefix = os.path.join(script_dir, doc_name)
        export_orthogonal_views(gui_doc, base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fcstd_path, camera_type="Perspective")
    close_model(doc.Name)
    print("Auxiliary Torch & Safety subassembly build complete.")

if __name__ == "__main__":
    build_aux_torch_safety()
    os._exit(0)
