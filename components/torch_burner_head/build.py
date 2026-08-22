"""
Torch Burner Head Component (Chassis-Mounted 500k BTU Venturi Burner Nozzle)
Standalone 3D Parametric CAD Module

This module provides `create_torch_burner_head_component(doc, placement)` to model the
high-output venturi combustion bell, atmospheric air induction cone, brass orifice jet,
spark electrode, and angled mounting flange for direct chassis/hood integration.
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

from phi_works.maker.render import export_orthogonal_views

def create_torch_burner_head_component(doc, placement=None):
    """
    Creates Torch Burner Head assembly in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::DocumentObjectGroup containing burner head sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Torch_Burner_Head")
    grp.Label = "500,000 BTU Chassis Burner Nozzle & Venturi Bell"

    # Color Palette
    BELL_BLACK = (0.15, 0.15, 0.15, 0.0)      # High-Temp Black Coated Steel Combustion Bell
    VENTURI_SILVER = (0.65, 0.68, 0.70, 0.0)  # Cast Venturi Air Induction Cone
    BRASS = (0.85, 0.65, 0.20, 0.0)           # Precision Brass Orifice Hex Fitting
    CERAMIC_WHITE = (0.92, 0.92, 0.95, 0.0)   # Insulated Spark Electrode
    STEEL_FLANGE = (0.45, 0.48, 0.52, 0.0)    # Hood Mounting Flange Bracket

    # Dimensions
    BELL_OD = 63.5        # 2.5 in outer bell diameter
    BELL_ID = 58.0
    BELL_L = 95.0
    VENTURI_L = 45.0
    CONE_BASE_D = 22.0

    # 1. Flared Steel Combustion Bell (along Z-axis)
    bell_outer = Part.makeCylinder(BELL_OD/2, BELL_L, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    bell_inner = Part.makeCylinder(BELL_ID/2, BELL_L + 2.0, FreeCAD.Vector(0, 0, 5.0), FreeCAD.Vector(0, 0, 1))
    bell_solid = bell_outer.cut(bell_inner)
    bell_solid.Placement = placement

    bell_obj = doc.addObject("Part::Feature", "Combustion_Bell_Cup")
    bell_obj.Shape = bell_solid
    grp.addObject(bell_obj)

    # 2. Cast Venturi Air Induction Cone with Triangular Air Windows
    cone_outer = Part.makeCone(CONE_BASE_D/2, BELL_OD/2, VENTURI_L, FreeCAD.Vector(0, 0, -VENTURI_L), FreeCAD.Vector(0, 0, 1))
    cone_inner = Part.makeCone(CONE_BASE_D/2 - 3.0, BELL_ID/2 - 3.0, VENTURI_L + 0.2, FreeCAD.Vector(0, 0, -VENTURI_L - 0.1), FreeCAD.Vector(0, 0, 1))
    cone_hollow = cone_outer.cut(cone_inner)

    # 3x Triangular Air Induction Windows
    win1 = Part.makeBox(12.0, 18.0, 16.0, FreeCAD.Vector(-6.0, 10.0, -VENTURI_L/2 - 8.0))
    win2 = Part.makeBox(18.0, 12.0, 16.0, FreeCAD.Vector(10.0, -6.0, -VENTURI_L/2 - 8.0))
    win3 = Part.makeBox(18.0, 12.0, 16.0, FreeCAD.Vector(-28.0, -6.0, -VENTURI_L/2 - 8.0))
    
    venturi_solid = cone_hollow.cut(win1).cut(win2).cut(win3)
    venturi_solid.Placement = placement

    venturi_obj = doc.addObject("Part::Feature", "Cast_Venturi_Cone")
    venturi_obj.Shape = venturi_solid
    grp.addObject(venturi_obj)

    # 3. Brass Orifice Jet Hex Fitting & Gas Inlet
    jet_hex = Part.makeBox(16.0, 16.0, 12.0, FreeCAD.Vector(-8.0, -8.0, -VENTURI_L - 12.0))
    jet_nipple = Part.makeCylinder(6.0, 15.0, FreeCAD.Vector(0, 0, -VENTURI_L - 25.0), FreeCAD.Vector(0, 0, 1))
    gas_bore = Part.makeCylinder(3.0, 30.0, FreeCAD.Vector(0, 0, -VENTURI_L - 26.0), FreeCAD.Vector(0, 0, 1))
    brass_jet = (jet_hex.fuse(jet_nipple)).cut(gas_bore)
    brass_jet.Placement = placement

    jet_obj = doc.addObject("Part::Feature", "Brass_Orifice_Jet_Inlet")
    jet_obj.Shape = brass_jet
    grp.addObject(jet_obj)

    # 4. Ceramic Spark Electrode Assembly
    ceramic_body = Part.makeCylinder(4.0, 35.0, FreeCAD.Vector(15.0, 0, -VENTURI_L/2), FreeCAD.Vector(-1, 0, 1).normalize())
    spark_pin = Part.makeCylinder(1.0, 45.0, FreeCAD.Vector(18.0, 0, -VENTURI_L/2 - 3.0), FreeCAD.Vector(-1, 0, 1).normalize())
    electrode_solid = ceramic_body.fuse(spark_pin)
    electrode_solid.Placement = placement

    electrode_obj = doc.addObject("Part::Feature", "Ceramic_Spark_Electrode")
    electrode_obj.Shape = electrode_solid
    grp.addObject(electrode_obj)

    # 5. Hood Apex Mounting Flange Bracket
    flange_plate = Part.makeBox(85.0, 75.0, 4.76, FreeCAD.Vector(-42.5, -37.5, -VENTURI_L/2 - 2.38))
    flange_cutout = Part.makeCylinder(BELL_OD/2 + 2.0, 10.0, FreeCAD.Vector(0, 0, -VENTURI_L/2 - 5.0), FreeCAD.Vector(0, 0, 1))
    
    # 4x Bolt Holes
    h1 = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(-30.0, -25.0, -VENTURI_L/2 - 5.0), FreeCAD.Vector(0, 0, 1))
    h2 = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(30.0, -25.0, -VENTURI_L/2 - 5.0), FreeCAD.Vector(0, 0, 1))
    h3 = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(-30.0, 25.0, -VENTURI_L/2 - 5.0), FreeCAD.Vector(0, 0, 1))
    h4 = Part.makeCylinder(3.5, 10.0, FreeCAD.Vector(30.0, 25.0, -VENTURI_L/2 - 5.0), FreeCAD.Vector(0, 0, 1))

    flange_solid = flange_plate.cut(flange_cutout).cut(h1).cut(h2).cut(h3).cut(h4)
    flange_solid.Placement = placement

    flange_obj = doc.addObject("Part::Feature", "Hood_Mounting_Flange")
    flange_obj.Shape = flange_solid
    grp.addObject(flange_obj)

    # Apply colors
    if HAS_GUI and hasattr(FreeCADGui, "getDocument"):
        try:
            gui_d = FreeCADGui.getDocument(doc.Name)
            if gui_d:
                color_map = [
                    (bell_obj, BELL_BLACK),
                    (venturi_obj, VENTURI_SILVER),
                    (jet_obj, BRASS),
                    (electrode_obj, CERAMIC_WHITE),
                    (flange_obj, STEEL_FLANGE)
                ]
                for o, c in color_map:
                    g_o = gui_d.getObject(o.Name)
                    if g_o:
                        g_o.Visibility = True
                        g_o.ShapeColor = c
                        g_o.DisplayMode = "Flat Lines"
        except Exception:
            pass

    return grp

def build_standalone_component():
    doc = FreeCAD.newDocument("torch_burner_head_component")
    comp_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

    create_torch_burner_head_component(doc)
    doc.recompute()

    fc_path = os.path.join(comp_dir, "torch_burner_head.FCStd")
    doc.saveAs(fc_path)
    print(f"Saved standalone torch burner head model: {fc_path}")

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        base_prefix = os.path.join(comp_dir, "torch_burner_head")
        export_orthogonal_views(FreeCADGui.getDocument(doc.Name), base_prefix, model_prefix="torch_burner_head")

    FreeCAD.closeDocument("torch_burner_head_component")

if __name__ == "__main__":
    build_standalone_component()
    sys.exit(0)
