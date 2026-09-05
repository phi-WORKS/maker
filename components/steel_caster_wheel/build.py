"""
Steel Caster Wheel Component (4.0" Heavy-Duty All-Metal Wheel)
Standalone 3D Parametric CAD Module

This module provides `create_steel_caster_wheel_component(doc, placement)` to create a
heavy-duty, heat-resistant solid machined steel wheel and axle assembly for high-temperature
agricultural, driveway, and road maintenance equipment.
"""

import os
import sys
import math
import FreeCAD
import Part

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views, save_model, close_model
from phi_works.maker.materials import apply_material, get_mass_properties, format_mass_report

def create_steel_caster_wheel_component(doc, placement=None):
    """
    Creates 4.0" Steel Wheel assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing wheel sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Steel_Caster_Wheel")
    grp.Label = "4.0\" Heavy-Duty Solid Steel Wheel"

    # Parametric Dimensions (4.0" Dia x 1.5" Face)
    WHEEL_DIA = 101.6     # 4.0 in outer diameter
    WHEEL_RADIUS = WHEEL_DIA / 2.0
    WHEEL_WIDTH = 38.1    # 1.5 in tread face width
    HUB_DIA = 38.1        # 1.5 in hub diameter
    HUB_WIDTH = 44.45     # 1.75 in hub width across bearings
    AXLE_DIA = 12.7       # 1/2 in axle bolt diameter
    WEB_THICK = 12.7      # 0.5 in central web thickness

    # 1. Wheel Geometry (Rim, Web, Hub, Axle Bore)
    # Wheel centered at (0, 0, 0) with rotation axis along X
    outer_rim = Part.makeCylinder(WHEEL_RADIUS, WHEEL_WIDTH, FreeCAD.Vector(-WHEEL_WIDTH/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    rim_recess_left = Part.makeCylinder(WHEEL_RADIUS - 6.35, (WHEEL_WIDTH - WEB_THICK)/2, FreeCAD.Vector(-WHEEL_WIDTH/2 - 0.1, 0, 0), FreeCAD.Vector(1, 0, 0))
    rim_recess_right = Part.makeCylinder(WHEEL_RADIUS - 6.35, (WHEEL_WIDTH - WEB_THICK)/2, FreeCAD.Vector(WEB_THICK/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    
    hub_cyl = Part.makeCylinder(HUB_DIA/2, HUB_WIDTH, FreeCAD.Vector(-HUB_WIDTH/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    axle_bore = Part.makeCylinder(AXLE_DIA/2, HUB_WIDTH + 10.0, FreeCAD.Vector(-HUB_WIDTH/2 - 5.0, 0, 0), FreeCAD.Vector(1, 0, 0))
    
    wheel_solid = outer_rim.cut(rim_recess_left).cut(rim_recess_right).fuse(hub_cyl).cut(axle_bore)
    wheel_solid.Placement = placement

    wheel_obj = doc.addObject("Part::Feature", "Machined_Steel_Wheel_Body")
    wheel_obj.Label = "Machined Cast Steel Wheel Body (4in Dia x 1.5in Face)"
    wheel_obj.Shape = wheel_solid
    grp.addObject(wheel_obj)
    apply_material(wheel_obj, "CastIron-Gray")

    # 2. Axle Pin Bolt, Spacers & Hex Nut
    bolt_len = HUB_WIDTH + 30.0
    axle_bolt = Part.makeCylinder(AXLE_DIA/2, bolt_len, FreeCAD.Vector(-bolt_len/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    hex_head = Part.makeBox(9.525, 22.2, 22.2, FreeCAD.Vector(-bolt_len/2, -11.1, -11.1))
    hex_nut = Part.makeBox(9.525, 22.2, 22.2, FreeCAD.Vector(bolt_len/2 - 9.525, -11.1, -11.1))
    washer_l = Part.makeCylinder(19.05/2, 3.175, FreeCAD.Vector(-HUB_WIDTH/2 - 3.175, 0, 0), FreeCAD.Vector(1, 0, 0))
    washer_r = Part.makeCylinder(19.05/2, 3.175, FreeCAD.Vector(HUB_WIDTH/2, 0, 0), FreeCAD.Vector(1, 0, 0))
    axle_assembly = axle_bolt.fuse(hex_head).fuse(hex_nut).fuse(washer_l).fuse(washer_r)
    axle_assembly.Placement = placement

    axle_obj = doc.addObject("Part::Feature", "Steel_Axle_Bolt_Hardware")
    axle_obj.Label = "Zinc-Plated 1/2in Grade 5 Axle Bolt, Washers & Nut"
    axle_obj.Shape = axle_assembly
    grp.addObject(axle_obj)
    apply_material(axle_obj, "Steel-ZincPlated")

    return grp

def build_standalone_component():
    doc_name = "steel_caster_wheel"
    doc = FreeCAD.newDocument(doc_name)
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    grp = create_steel_caster_wheel_component(doc)
    doc.recompute()

    report = get_mass_properties(grp)
    print(format_mass_report(report, title="4.0\" Steel Caster Wheel Mass Report"))

    fc_path = os.path.join(comp_dir, f"{doc_name}.FCStd")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, doc_name)
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix=doc_name, camera_type="Perspective")

    save_model(doc, fc_path, camera_type="Perspective")
    close_model(doc.Name)

if __name__ == "__main__":
    build_standalone_component()
    os._exit(0)
