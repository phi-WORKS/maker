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
    doc.Label = "STIHL Kombi Line Trimmer (Angled Gearbox & Shield)"

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
    
    # Shield Specs: 13" wide, 7" rearward, 4.5" left offset
    SHIELD_W = 13.0 * IN2MM
    SHIELD_REAR = 7.0 * IN2MM
    LEFT_OFFSET = 4.5 * IN2MM

    SPOOL_DIA = 4.75 * IN2MM          # 120.65 mm
    SPOOL_H = 2.25 * IN2MM            # 57.15 mm
    GEARBOX_H = 3.0 * IN2MM           # 76.2 mm
    TILT_ANGLE = 30.0                 # 30 degree angle of head/gearbox relative to vertical shaft

    grp = doc.addObject("App::DocumentObjectGroup", "STIHL_KM_Trimmer")

    # 1. Main Exposed Shaft (31" long, vertical Z=203mm to Z=990.6mm)
    z_elbow = OVERALL_H - EXPOSED_SHAFT_L # Z ~ 203.2 mm (elbow height)
    shaft = Part.makeCylinder(SHAFT_R, EXPOSED_SHAFT_L, FreeCAD.Vector(0, 0, z_elbow), FreeCAD.Vector(0, 0, 1))
    o_shaft = doc.addObject("Part::Feature", "Exposed_Drive_Shaft_31in")
    o_shaft.Shape = shaft
    set_vis(o_shaft, SHAFT_COLOR)
    grp.addObject(o_shaft)

    # 2. Top Coupler Sleeve (Top 70mm, Z=920.6 to 990.6 mm)
    z_coupler_start = OVERALL_H - 70.0
    coupler = Part.makeCylinder(14.0, 70.0, FreeCAD.Vector(0, 0, z_coupler_start), FreeCAD.Vector(0, 0, 1))
    o_coup = doc.addObject("Part::Feature", "Quick_Connect_Sleeve")
    o_coup.Shape = coupler
    set_vis(o_coup, COUPLER_COLOR)
    grp.addObject(o_coup)

    # 3. Angled Head Assembly (Gearbox, Bump Head, & Shield tilted forward at 30°)
    # Local coordinate frame at elbow (0, 0, z_elbow)
    # Pitch forward by TILT_ANGLE (rotating around X axis by -30 deg)

    # Gearbox casting
    gearbox = Part.makeCylinder(22.0, GEARBOX_H, FreeCAD.Vector(0, 0, -GEARBOX_H), FreeCAD.Vector(0, 0, 1))
    
    # Bump head spool
    bump_cap = Part.makeCylinder(SPOOL_DIA / 2.0, SPOOL_H, FreeCAD.Vector(0, 0, -GEARBOX_H - SPOOL_H), FreeCAD.Vector(0, 0, 1))

    # Curved Debris Shield Shroud (attached to gearbox, sloped upward in the back)
    # In local head coords: extends rearward (+Y), width 13" (-4.5" to +8.5" X)
    shield_plate = Part.makeBox(SHIELD_W, SHIELD_REAR, 12.0, FreeCAD.Vector(-LEFT_OFFSET, 0, -GEARBOX_H + 10.0))
    # Angled protective rear skirt extending upwards/backwards
    skirt_poly = Part.makePolygon([
        FreeCAD.Vector(-LEFT_OFFSET, SHIELD_REAR, -GEARBOX_H + 10.0),
        FreeCAD.Vector(-LEFT_OFFSET, SHIELD_REAR + 40.0, -GEARBOX_H + 50.0),
        FreeCAD.Vector(-LEFT_OFFSET + SHIELD_W, SHIELD_REAR + 40.0, -GEARBOX_H + 50.0),
        FreeCAD.Vector(-LEFT_OFFSET + SHIELD_W, SHIELD_REAR, -GEARBOX_H + 10.0),
        FreeCAD.Vector(-LEFT_OFFSET, SHIELD_REAR, -GEARBOX_H + 10.0)
    ])
    try:
        skirt_face = Part.Face(skirt_poly)
        skirt_solid = skirt_face.extrude(FreeCAD.Vector(0, 0, 8.0))
        shield_shape = shield_plate.fuse(skirt_solid)
    except Exception:
        shield_shape = shield_plate

    # Combine local head components
    head_compound = Part.makeCompound([gearbox, bump_cap])
    
    # Apply Placement Transformation: rotate by -TILT_ANGLE deg around X axis, then translate to elbow Z
    rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -TILT_ANGLE)
    trans = FreeCAD.Vector(0, 0, z_elbow)
    head_placement = FreeCAD.Placement(trans, rot)

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

    fc_path = "/home/phi/PROJECTS/phi-WORKS/caddy/kombi_trimmer.FCStd"
    base_png = "/home/phi/PROJECTS/phi-WORKS/caddy/kombi_trimmer"
    doc.saveAs(fc_path)
    print(f"Saved angled trimmer model to {fc_path}")

    if HAS_GUI:
        render_views(FreeCADGui.getDocument(doc_name), base_png)

if __name__ == "__main__":
    build_trimmer_model()
    sys.exit(0)
