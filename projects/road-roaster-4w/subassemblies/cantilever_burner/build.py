"""
Road Roaster 4W - Front Cantilevered Radiant Ceramic Burner Subassembly
Parametric FreeCAD 1.0/1.1 Subassembly Model
Version: v0.2.0

Components:
  1. Axle Pivot Sleeves (3/4" OD continuous axle shaft interface)
  2. Dual Cantilever Vertical Drop Arms & Transverse Tie Bar
  3. Formed Steel Hood Mounting Brackets (4-bolt pattern interfacing burner throat)
  4. Cantilever Diagonal Truss Braces (rigidifying lower front reflector rim)
  5. Mechanical Operating Stop Pads (bear against bolted front skirt)
  6. Flexible Reinforced LP Gas Feed Hose Loop
  7. Solaronics K-30 Ceramic Infrared Burner & Flared Reflector Hood (Linked Component)
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
    doc.Label = "Front Cantilever Burner Subassembly (Solaronics K-30 & 180° Flip Bracket)"
    doc.saveAs(fcstd_path)

    # Root App::Part container
    part_root = doc.addObject("App::Part", "Cantilever_Burner")
    part_root.Label = "Front Cantilever Burner Subassembly (Solaronics K-30 & 180° Flip Bracket)"

    # Geometry references
    DECK_TOP_Z = 195.0
    FRONT_LIP_Y = -457.2
    PIVOT_Y = -475.0
    PIVOT_Z = 230.0

    # Arm lateral positions (spacing across X to fit outside the burner hood)
    ARM_X = 230.0
    SLEEVE_OD = 32.0
    SLEEVE_ID = 19.5
    SLEEVE_LEN = 36.0

    DROP_TUBE = 38.1
    DROP_BOT_Z = 65.0

    arm_solids = []
    hood_brackets = []
    braces = []

    # Burner placement parameters
    HOVER_RIM_Z = 38.1   # 1.5 in hover height of lower reflector rim above road
    REFL_DEPTH = 110.0
    BURNER_EMITTER_Z = HOVER_RIM_Z + REFL_DEPTH  # 148.1 mm (Z = 0 in local burner frame)
    BURNER_MOUTH_L = 608.0
    BURNER_Y = PIVOT_Y - 20.0 - BURNER_MOUTH_L / 2.0  # -799.0 mm

    for sign in [-1.0, 1.0]:
        x_a = sign * ARM_X

        # 1. Axle Pivot Sleeve Bushing (rotates smoothly on 3/4" continuous axle)
        sleeve_outer = Part.makeCylinder(SLEEVE_OD / 2.0, SLEEVE_LEN,
                                         FreeCAD.Vector(x_a - SLEEVE_LEN / 2.0, PIVOT_Y, PIVOT_Z),
                                         FreeCAD.Vector(1, 0, 0))
        sleeve_inner = Part.makeCylinder(SLEEVE_ID / 2.0, SLEEVE_LEN + 2.0,
                                         FreeCAD.Vector(x_a - SLEEVE_LEN / 2.0 - 1.0, PIVOT_Y, PIVOT_Z),
                                         FreeCAD.Vector(1, 0, 0))
        sleeve = sleeve_outer.cut(sleeve_inner)

        # 2. Vertical Drop Leg (extending down from sleeve in front of skirt)
        drop_h = PIVOT_Z - DROP_BOT_Z
        drop_leg = Part.makeBox(DROP_TUBE, DROP_TUBE, drop_h,
                                FreeCAD.Vector(x_a - DROP_TUBE / 2.0, PIVOT_Y - DROP_TUBE / 2.0, DROP_BOT_Z))

        # Horizontal connecting arm from axle sleeve forward to vertical drop leg
        top_connector = Part.makeBox(DROP_TUBE, 25.0, DROP_TUBE,
                                     FreeCAD.Vector(x_a - DROP_TUBE / 2.0, PIVOT_Y - DROP_TUBE / 2.0 - 10.0, PIVOT_Z - DROP_TUBE / 2.0))

        # Mechanical stop pad on rear face of drop leg (rests against front skirt)
        stop_pad = Part.makeBox(DROP_TUBE, 12.0, 30.0,
                                FreeCAD.Vector(x_a - DROP_TUBE / 2.0, PIVOT_Y + DROP_TUBE / 2.0, 145.0))

        # Lower cantilever projection arm extending forward under the hood
        lower_cantilever = Part.makeBox(DROP_TUBE, 160.0, DROP_TUBE,
                                        FreeCAD.Vector(x_a - DROP_TUBE / 2.0, PIVOT_Y - DROP_TUBE / 2.0 - 160.0, DROP_BOT_Z))

        arm_structure = sleeve.fuse(drop_leg).fuse(top_connector).fuse(stop_pad).fuse(lower_cantilever)
        arm_solids.append(arm_structure)

        # 3. "HOOD BRACKET": Formed plate with 4-bolt pattern bolting to burner side/throat
        hb_len = 90.0
        hb_h = 75.0
        hb_t = 6.0
        x_hb = x_a - sign * (DROP_TUBE / 2.0 + hb_t / 2.0)
        hb_plate = Part.makeBox(hb_t, hb_len, hb_h,
                                FreeCAD.Vector(x_hb - hb_t / 2.0, PIVOT_Y - DROP_TUBE / 2.0 - hb_len, BURNER_EMITTER_Z - 10.0))

        # 4 bolt holes (2x2) matching user sketch
        b_r = 4.5  # 3/8" bolt clearance
        for by_off in [20.0, 65.0]:
            for bz_off in [18.0, 52.0]:
                hole = Part.makeCylinder(b_r, hb_t + 4.0,
                                         FreeCAD.Vector(x_hb - hb_t / 2.0 - 2.0,
                                                        PIVOT_Y - DROP_TUBE / 2.0 - by_off,
                                                        BURNER_EMITTER_Z - 10.0 + bz_off),
                                         FreeCAD.Vector(1, 0, 0))
                hb_plate = hb_plate.cut(hole)

        # Connector attachment tab from drop leg to hood bracket
        hb_tab = Part.makeBox(DROP_TUBE, 20.0, 20.0,
                              FreeCAD.Vector(x_a - DROP_TUBE / 2.0, PIVOT_Y - DROP_TUBE / 2.0 - 20.0, BURNER_EMITTER_Z + 15.0))
        hood_brackets.append(hb_plate.fuse(hb_tab))

        # 4. "CANTILEVER BRACE": Diagonal strut from lower cantilever tip up to hood throat
        # Defined precisely in YZ plane using non-ambiguous polygon extrusion
        def make_strap_yz(y1, z1, y2, z2, width, thickness, x_center):
            dy = y2 - y1
            dz = z2 - z1
            L = math.hypot(dy, dz)
            if L == 0:
                return None
            ny = -dz / L * (width / 2.0)
            nz = dy / L * (width / 2.0)
            v1 = FreeCAD.Vector(0, y1 + ny, z1 + nz)
            v2 = FreeCAD.Vector(0, y2 + ny, z2 + nz)
            v3 = FreeCAD.Vector(0, y2 - ny, z2 - nz)
            v4 = FreeCAD.Vector(0, y1 - ny, z1 - nz)
            poly = Part.makePolygon([v1, v2, v3, v4, v1])
            face = Part.Face(poly)
            solid = face.extrude(FreeCAD.Vector(thickness, 0, 0))
            solid.translate(FreeCAD.Vector(x_center - thickness / 2.0, 0, 0))
            return solid

        y_tip = PIVOT_Y - DROP_TUBE / 2.0 - 150.0  # -644.05 mm
        z_tip = DROP_BOT_Z + DROP_TUBE / 2.0       # 84.05 mm
        y_top = PIVOT_Y - DROP_TUBE / 2.0 - 10.0   # -504.05 mm
        z_top = BURNER_EMITTER_Z - 5.0             # 143.1 mm

        brace_bar = make_strap_yz(y_tip, z_tip, y_top, z_top, 25.4, 6.0, x_a)
        tab_start = Part.makeBox(8.0, 25.0, 25.0, FreeCAD.Vector(x_a - 4.0, y_tip - 12.0, z_tip - 12.0))
        tab_end = Part.makeBox(8.0, 25.0, 25.0, FreeCAD.Vector(x_a - 4.0, y_top - 12.0, z_top - 12.0))
        braces.append(brace_bar.fuse(tab_start).fuse(tab_end))

    # Transverse cross tube connecting the drop legs into a unified frame
    tie_od = 25.4
    tie_len = 2 * (ARM_X - DROP_TUBE / 2.0)
    cross_tie = Part.makeCylinder(tie_od / 2.0, tie_len,
                                  FreeCAD.Vector(-tie_len / 2.0, PIVOT_Y, 110.0),
                                  FreeCAD.Vector(1, 0, 0))

    arms_compound = arm_solids[0].fuse(arm_solids[1]).fuse(cross_tie)
    brackets_compound = hood_brackets[0].fuse(hood_brackets[1])
    braces_compound = braces[0].fuse(braces[1])

    # 5. Flexible Gas Hose Loop - connects directly to manifold on CART SIDE
    # Rotated burner places manifold at X = -150 mm, Y = BURNER_Y + 120 mm, Z = BURNER_EMITTER_Z + 75 mm
    p_cart = FreeCAD.Vector(-100.0, FRONT_LIP_Y + 40.0, DECK_TOP_Z + 25.0)
    p_arch = FreeCAD.Vector(-120.0, PIVOT_Y - 20.0, PIVOT_Z + 45.0)
    p_drop = FreeCAD.Vector(-140.0, BURNER_Y + 220.0, BURNER_EMITTER_Z + 120.0)
    p_burner = FreeCAD.Vector(-150.0, BURNER_Y + 180.0, BURNER_EMITTER_Z + 75.0)

    spline_h = Part.BSplineCurve()
    spline_h.interpolate([p_cart, p_arch, p_drop, p_burner])
    wire_h = Part.Wire([Part.Edge(spline_h)])
    circ_h = Part.makeCircle(6.35, p_cart, spline_h.tangent(0.0)[0])
    face_h = Part.Face(Part.Wire([circ_h]))
    hose_solid = wire_h.makePipe(face_h)

    # FreeCAD Objects
    obj_arms = doc.addObject("Part::Feature", "Cantilever_Drop_Arms")
    obj_arms.Label = "Cantilever Drop Arms & Pivot Sleeves (3/4in Axle Hinge)"
    obj_arms.Shape = arms_compound
    part_root.addObject(obj_arms)
    apply_material(obj_arms, "Steel-A36")

    obj_hb = doc.addObject("Part::Feature", "Burner_Hood_Brackets")
    obj_hb.Label = "Burner Hood Side Mounting Brackets (4-Bolt Pattern)"
    obj_hb.Shape = brackets_compound
    part_root.addObject(obj_hb)
    apply_material(obj_hb, "Steel-A36")

    obj_braces = doc.addObject("Part::Feature", "Cantilever_Diagonal_Braces")
    obj_braces.Label = "Cantilever Diagonal Hood Braces (Rigidifying Truss)"
    obj_braces.Shape = braces_compound
    part_root.addObject(obj_braces)
    apply_material(obj_braces, "Steel-A36")

    obj_hose = doc.addObject("Part::Feature", "Flexible_Gas_Supply_Hose")
    obj_hose.Label = "Flexible Reinforced LP Gas Supply Loop (Cart-Side Connection)"
    obj_hose.Shape = hose_solid
    part_root.addObject(obj_hose)
    apply_material(obj_hose, "Rubber-Solid")

    # 6. Link Solaronics Infrared Ceramic Burner Component
    # Rotated 180° around Z so control box, manifold, and fittings face CART SIDE
    burner_pos = FreeCAD.Vector(0, BURNER_Y, BURNER_EMITTER_Z)
    burner_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180.0)
    burner_link = import_component(doc, "solaronics_infrared_burner",
                                   placement=FreeCAD.Placement(burner_pos, burner_rot),
                                   as_link=True)
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
