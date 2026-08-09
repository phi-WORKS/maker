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

def render_views(gui_doc, base_path):
    if not HAS_GUI or not gui_doc:
        return
    FreeCADGui.updateGui()
    view = gui_doc.activeView()
    if view:
        try:
            view.setCameraType("Orthographic")
            
            # Iso view
            view.viewIsometric()
            view.fitAll()
            view.saveImage(f"{base_path}_iso.png", 1920, 1080, "White")
            
            # Top view
            view.viewTop()
            view.fitAll()
            view.saveImage(f"{base_path}_top.png", 1920, 1080, "White")

            # Right Side View
            view.viewRight()
            view.fitAll()
            view.saveImage(f"{base_path}_side.png", 1920, 1080, "White")
        except Exception as e:
            print(f"Camera render note: {e}")

def build_trimmer_model():
    doc_name = "kombi_trimmer"
    try:
        if FreeCAD.getDocument(doc_name):
            FreeCAD.closeDocument(doc_name)
    except Exception:
        pass

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "STIHL Kombi Line Trimmer"

    # --- Colors ---
    SHAFT_COLOR = (0.85, 0.85, 0.88, 0.0)      # Aluminum shaft
    COUPLER_COLOR = (0.15, 0.15, 0.15, 0.0)    # Black plastic coupler
    STIHL_ORANGE = (0.95, 0.35, 0.05, 0.0)     # Shield orange
    HEAD_BLACK = (0.20, 0.20, 0.20, 0.0)       # Trimmer head body

    def set_vis(obj, color):
        if HAS_GUI:
            try:
                g_obj = FreeCADGui.getDocument(doc.Name).getObject(obj.Name)
                if g_obj:
                    g_obj.Visibility = True
                    g_obj.ShapeColor = color
                    g_obj.DisplayMode = "Flat Lines"
            except Exception:
                pass

    IN2MM = 25.4
    OVERALL_H = 39.0 * IN2MM          # 990.6 mm overall vertical height
    EXPOSED_SHAFT_L = 31.0 * IN2MM    # 787.4 mm
    SHAFT_R = (1.0 * IN2MM) / 2.0     # 12.7 mm
    
    # Shield Specs: 13" wide, 7" rearward, 4.5" left offset (shifted over)
    SHIELD_W = 13.0 * IN2MM
    SHIELD_REAR = 7.0 * IN2MM
    LEFT_OFFSET = 4.5 * IN2MM
    RIGHT_SPAN = SHIELD_W - LEFT_OFFSET # 8.5"

    SPOOL_DIA = 4.75 * IN2MM          # 120.65 mm
    SPOOL_H = 2.25 * IN2MM            # 57.15 mm
    GEARBOX_H = 3.0 * IN2MM           # 76.2 mm
    TILT_ANGLE = 30.0                 # 30 degree tilt

    grp = doc.addObject("App::DocumentObjectGroup", "STIHL_KM_Trimmer")

    # 1. Main Exposed Shaft (31" long, vertical Z=203mm to Z=990.6mm)
    z_elbow = OVERALL_H - EXPOSED_SHAFT_L # Z ~ 203.2 mm
    shaft = Part.makeCylinder(SHAFT_R, EXPOSED_SHAFT_L, FreeCAD.Vector(0, 0, z_elbow), FreeCAD.Vector(0, 0, 1))
    o_shaft = doc.addObject("Part::Feature", "Exposed_Drive_Shaft_31in")
    o_shaft.Shape = shaft
    set_vis(o_shaft, SHAFT_COLOR)
    grp.addObject(o_shaft)

    # 2. Top Coupler Sleeve (Top 70mm)
    z_coupler_start = OVERALL_H - 70.0
    coupler = Part.makeCylinder(14.0, 70.0, FreeCAD.Vector(0, 0, z_coupler_start), FreeCAD.Vector(0, 0, 1))
    o_coup = doc.addObject("Part::Feature", "Quick_Connect_Sleeve")
    o_coup.Shape = coupler
    set_vis(o_coup, COUPLER_COLOR)
    grp.addObject(o_coup)

    # 3. Gear Head & Bump Spool
    gearbox = Part.makeCylinder(22.0, GEARBOX_H, FreeCAD.Vector(0, 0, -GEARBOX_H), FreeCAD.Vector(0, 0, 1))
    bump_cap = Part.makeCylinder(SPOOL_DIA / 2.0, SPOOL_H, FreeCAD.Vector(0, 0, -GEARBOX_H - SPOOL_H), FreeCAD.Vector(0, 0, 1))

    # Debris Shield X origin shifted so offset is 4.5" on left and 8.5" on right in final orientation
    x_start = -RIGHT_SPAN # -8.5" in local space -> flips to -4.5" on left in final view
    shield_plate = Part.makeBox(SHIELD_W, SHIELD_REAR, 10.0, FreeCAD.Vector(x_start, -SHIELD_REAR, -GEARBOX_H + 10.0))
    flange_poly = Part.makePolygon([
        FreeCAD.Vector(x_start, -SHIELD_REAR, -GEARBOX_H + 10.0),
        FreeCAD.Vector(x_start, -SHIELD_REAR - 25.0, -GEARBOX_H - 35.0),
        FreeCAD.Vector(x_start + SHIELD_W, -SHIELD_REAR - 25.0, -GEARBOX_H - 35.0),
        FreeCAD.Vector(x_start + SHIELD_W, -SHIELD_REAR, -GEARBOX_H + 10.0),
        FreeCAD.Vector(x_start, -SHIELD_REAR, -GEARBOX_H + 10.0)
    ])
    try:
        flange_face = Part.Face(flange_poly)
        flange_solid = flange_face.extrude(FreeCAD.Vector(0, 0, 8.0))
        shield_shape = shield_plate.fuse(flange_solid)
    except Exception:
        shield_shape = shield_plate

    head_compound = Part.makeCompound([gearbox, bump_cap])

    # Rotation: Pitch forward by -TILT_ANGLE deg around X axis, then rotate 180 deg around Z axis
    rot_forward = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180.0) * FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -TILT_ANGLE)
    trans = FreeCAD.Vector(0, 0, z_elbow)
    head_placement = FreeCAD.Placement(trans, rot_forward)

    head_compound.Placement = head_placement
    shield_shape.Placement = head_placement

    o_head = doc.addObject("Part::Feature", "Angled_Gearbox_Head")
    o_head.Shape = head_compound
    set_vis(o_head, HEAD_BLACK)
    grp.addObject(o_head)

    o_sh = doc.addObject("Part::Feature", "Angled_Debris_Shield")
    o_sh.Shape = shield_shape
    set_vis(o_sh, STIHL_ORANGE)
    grp.addObject(o_sh)

    doc.recompute()

    out_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")
    os.makedirs(out_dir, exist_ok=True)
    fc_path = os.path.join(out_dir, "trimmer.FCStd")
    base_png = os.path.join(out_dir, "trimmer")
    doc.saveAs(fc_path)
    print(f"Saved trimmer model with corrected shield offset to {fc_path}")

    if HAS_GUI:
        render_views(FreeCADGui.getDocument(doc_name), base_png)

if __name__ == "__main__":
    build_trimmer_model()
    sys.exit(0)
