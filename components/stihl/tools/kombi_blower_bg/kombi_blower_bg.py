"""
STIHL BG-KM In-Line Axial Blower Attachment Component
Standalone 3D Parametric CAD Module

Features:
- In-Line Coaxial Architecture: Blower assembly is concentric on the drive shaft axis
- Drive Shaft: 25.4 mm (1.0") Aluminum tube with standard quick-connect coupler
- Orange Top Cap: STIHL Orange polymer cap (6.0" / 152.4 mm OD) with tapered collar
- Main Blower Body: STIHL White polymer cylindrical housing (6.0" / 152.4 mm OD)
  featuring circumferential stiffening ribs and clamshell assembly screw bosses
- Black Two-Stage Discharge Nozzle:
  - Stage 1: Tapered reduction cone (152.4 mm down to 92 mm OD) with bayonet latch collar
  - Stage 2: Tapered extension blower pipe (90 mm down to 68 mm OD) with cylindrical nozzle tip
- Overall Length: ~930 mm (36.6")
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_kombi_blower_bg_component(doc, placement=None):
    """
    Creates the STIHL BG-KM In-Line Axial Blower in `doc`.
    
    Parameters:
      doc: FreeCAD Document
      placement: FreeCAD.Placement or FreeCAD.Vector (default: origin)
      
    Returns:
      App::Part containing blower sub-components
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::Part", "Kombi_Blower_BG")
    grp.Label = "STIHL BG-KM In-Line Axial Blower Attachment"

    # Core Dimensions
    TUBE_OD = 25.4
    TUBE_R = TUBE_OD / 2.0
    BODY_OD = 152.4            # 6.0 inches diameter
    BODY_R = BODY_OD / 2.0     # 76.2 mm
    WALL = 3.2

    # Z-Axis Elevation Layout (Coupler at Z = 0)
    Z_COUPLER_TOP = 0.0
    Z_SHAFT_ENTRY = -100.0     # Exposed aluminum shaft length = 100 mm
    Z_CAP_BOT = -180.0         # Orange cap height = 80 mm
    Z_BODY_BOT = -480.0        # White body height = 300 mm
    Z_CONE_BOT = -700.0        # Black transition cone height = 220 mm
    Z_TIP_BOT = -930.0         # Black nozzle extension height = 230 mm (Total len = 930 mm)

    # 1. Drive Shaft Tube & Coupler
    # Shaft extends from Z = 0 down into the impeller hub at Z = -280 mm
    SHAFT_LEN = 280.0
    outer_tube = Part.makeCylinder(TUBE_R, SHAFT_LEN, FreeCAD.Vector(0, 0, -SHAFT_LEN), FreeCAD.Vector(0, 0, 1))
    inner_bore = Part.makeCylinder(TUBE_R - 1.65, SHAFT_LEN + 2.0, FreeCAD.Vector(0, 0, -SHAFT_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    shaft_solid = outer_tube.cut(inner_bore)

    # Coupler sleeve at top
    COUPLER_LEN = 80.0
    COUPLER_OD = 28.6
    sleeve_cyl = Part.makeCylinder(COUPLER_OD/2.0, COUPLER_LEN, FreeCAD.Vector(0, 0, -COUPLER_LEN), FreeCAD.Vector(0, 0, 1))
    sleeve_bore = Part.makeCylinder(TUBE_R, COUPLER_LEN + 2.0, FreeCAD.Vector(0, 0, -COUPLER_LEN - 1.0), FreeCAD.Vector(0, 0, 1))
    lock_pin = Part.makeCylinder(3.5, 6.0, FreeCAD.Vector(0, COUPLER_OD/2.0 - 1.0, -35.0), FreeCAD.Vector(0, 1, 0))
    coupler_solid = sleeve_cyl.cut(sleeve_bore).fuse(lock_pin)

    # 2. Orange Top Cap (Plastic-StihlOrange)
    # Tapered dome transitioning from 25.4 mm shaft collar to 152.4 mm (6") body
    CAP_H = abs(Z_CAP_BOT - Z_SHAFT_ENTRY) # 80 mm
    # Upper neck around shaft
    neck_cyl = Part.makeCylinder(19.0, 20.0, FreeCAD.Vector(0, 0, Z_SHAFT_ENTRY - 20.0), FreeCAD.Vector(0, 0, 1))
    # Tapered dome
    dome_cone = Part.makeCone(BODY_R, 19.0, 35.0, FreeCAD.Vector(0, 0, Z_SHAFT_ENTRY - 55.0), FreeCAD.Vector(0, 0, 1))
    # Cylindrical skirt
    skirt_cyl = Part.makeCylinder(BODY_R, 25.0, FreeCAD.Vector(0, 0, Z_CAP_BOT), FreeCAD.Vector(0, 0, 1))
    cap_outer = neck_cyl.fuse(dome_cone).fuse(skirt_cyl)
    # Hollow interior
    cap_inner = Part.makeCylinder(BODY_R - WALL, CAP_H - 10.0, FreeCAD.Vector(0, 0, Z_CAP_BOT - 1.0), FreeCAD.Vector(0, 0, 1))
    neck_bore = Part.makeCylinder(TUBE_R + 0.5, CAP_H + 4.0, FreeCAD.Vector(0, 0, Z_CAP_BOT - 2.0), FreeCAD.Vector(0, 0, 1))
    orange_cap = cap_outer.cut(cap_inner).cut(neck_bore)

    # 3. Main Blower Body (Plastic-StihlWhite)
    # 6.0" (152.4 mm OD) cylindrical barrel with circumferential ribs and clamshell screw bosses
    BODY_H = abs(Z_BODY_BOT - Z_CAP_BOT) # 300 mm
    body_cyl = Part.makeCylinder(BODY_R, BODY_H, FreeCAD.Vector(0, 0, Z_BODY_BOT), FreeCAD.Vector(0, 0, 1))
    body_bore = Part.makeCylinder(BODY_R - WALL, BODY_H + 4.0, FreeCAD.Vector(0, 0, Z_BODY_BOT - 2.0), FreeCAD.Vector(0, 0, 1))
    white_shell = body_cyl.cut(body_bore)

    # Add 4 circumferential stiffening ribs
    rib_solids = []
    for rib_z in [Z_CAP_BOT - 60.0, Z_CAP_BOT - 120.0, Z_CAP_BOT - 180.0, Z_CAP_BOT - 240.0]:
        rib_ring = Part.makeCylinder(BODY_R + 2.5, 6.0, FreeCAD.Vector(0, 0, rib_z - 3.0), FreeCAD.Vector(0, 0, 1))
        rib_cut = Part.makeCylinder(BODY_R - 0.1, 8.0, FreeCAD.Vector(0, 0, rib_z - 4.0), FreeCAD.Vector(0, 0, 1))
        white_shell = white_shell.fuse(rib_ring.cut(rib_cut))

    # Add clamshell screw bosses along the split lines (left and right at X = +/- BODY_R)
    for boss_z in [Z_CAP_BOT - 50.0, Z_CAP_BOT - 110.0, Z_CAP_BOT - 170.0, Z_CAP_BOT - 230.0, Z_CAP_BOT - 280.0]:
        # +X boss
        boss_pos = Part.makeBox(8.0, 14.0, 12.0, FreeCAD.Vector(BODY_R - 2.0, -7.0, boss_z - 6.0))
        screw_hole_pos = Part.makeCylinder(2.0, 10.0, FreeCAD.Vector(BODY_R + 4.0, 0, boss_z - 6.0), FreeCAD.Vector(1, 0, 0))
        # -X boss
        boss_neg = Part.makeBox(8.0, 14.0, 12.0, FreeCAD.Vector(-BODY_R - 6.0, -7.0, boss_z - 6.0))
        screw_hole_neg = Part.makeCylinder(2.0, 10.0, FreeCAD.Vector(-BODY_R - 6.0, 0, boss_z - 6.0), FreeCAD.Vector(1, 0, 0))
        white_shell = white_shell.fuse(boss_pos.cut(screw_hole_pos)).fuse(boss_neg.cut(screw_hole_neg))

    # Bottom alignment collar on white housing
    bottom_lip = Part.makeCylinder(BODY_R + 3.0, 14.0, FreeCAD.Vector(0, 0, Z_BODY_BOT), FreeCAD.Vector(0, 0, 1))
    lip_bore = Part.makeCylinder(BODY_R - WALL, 16.0, FreeCAD.Vector(0, 0, Z_BODY_BOT - 1.0), FreeCAD.Vector(0, 0, 1))
    white_body = white_shell.fuse(bottom_lip.cut(lip_bore))

    # 4. Black Two-Stage Discharge Nozzle (Plastic-ABS / Black)
    # Stage 1: Upper reduction cone (152.4 mm OD tapering down to 92 mm OD over 220 mm)
    CONE_H = abs(Z_CONE_BOT - Z_BODY_BOT) # 220 mm
    R_CONE_TOP = BODY_R # 76.2 mm
    R_CONE_BOT = 46.0   # 92 mm OD
    cone_outer = Part.makeCone(R_CONE_TOP, R_CONE_BOT, CONE_H, FreeCAD.Vector(0, 0, Z_BODY_BOT), FreeCAD.Vector(0, 0, -1))
    cone_inner = Part.makeCone(R_CONE_TOP - WALL, R_CONE_BOT - WALL, CONE_H + 4.0, FreeCAD.Vector(0, 0, Z_BODY_BOT + 2.0), FreeCAD.Vector(0, 0, -1))
    stage1_cone = cone_outer.cut(cone_inner)

    # Intermediate bayonet latch collar ring
    LATCH_H = 26.0
    latch_outer = Part.makeCylinder(R_CONE_BOT + 3.5, LATCH_H, FreeCAD.Vector(0, 0, Z_CONE_BOT - LATCH_H/2.0), FreeCAD.Vector(0, 0, 1))
    latch_inner = Part.makeCylinder(R_CONE_BOT - WALL, LATCH_H + 2.0, FreeCAD.Vector(0, 0, Z_CONE_BOT - LATCH_H/2.0 - 1.0), FreeCAD.Vector(0, 0, 1))
    latch_ring = latch_outer.cut(latch_inner)

    # Stage 2: Tapered extension tube & cylindrical nozzle tip
    NOZZLE_H = abs(Z_TIP_BOT - Z_CONE_BOT) # 230 mm
    R_NOZZLE_TOP = 45.0  # 90 mm OD
    R_NOZZLE_BOT = 34.0  # 68 mm OD
    TAPER_H = 170.0
    STRAIGHT_H = 60.0

    # Tapered section
    taper_outer = Part.makeCone(R_NOZZLE_TOP, R_NOZZLE_BOT, TAPER_H, FreeCAD.Vector(0, 0, Z_CONE_BOT), FreeCAD.Vector(0, 0, -1))
    taper_inner = Part.makeCone(R_NOZZLE_TOP - WALL, R_NOZZLE_BOT - WALL, TAPER_H + 4.0, FreeCAD.Vector(0, 0, Z_CONE_BOT + 2.0), FreeCAD.Vector(0, 0, -1))
    # Straight tip
    tip_outer = Part.makeCylinder(R_NOZZLE_BOT, STRAIGHT_H, FreeCAD.Vector(0, 0, Z_CONE_BOT - TAPER_H), FreeCAD.Vector(0, 0, -1))
    tip_inner = Part.makeCylinder(R_NOZZLE_BOT - WALL, STRAIGHT_H + 4.0, FreeCAD.Vector(0, 0, Z_CONE_BOT - TAPER_H + 2.0), FreeCAD.Vector(0, 0, -1))
    stage2_pipe = taper_outer.cut(taper_inner).fuse(tip_outer.cut(tip_inner))

    black_nozzle = stage1_cone.fuse(latch_ring).fuse(stage2_pipe)

    # Apply placement
    shaft_solid.Placement = placement
    coupler_solid.Placement = placement
    orange_cap.Placement = placement
    white_body.Placement = placement
    black_nozzle.Placement = placement

    obj_shaft = doc.addObject("Part::Feature", "BG_Drive_Shaft")
    obj_shaft.Label = "25.4mm Aluminum Drive Shaft Tube"
    obj_shaft.Shape = shaft_solid
    grp.addObject(obj_shaft)
    apply_material(obj_shaft, "Aluminum-6061-T6")

    obj_coupler = doc.addObject("Part::Feature", "BG_Coupler")
    obj_coupler.Label = "KombiSystem Quick-Connect Coupler"
    obj_coupler.Shape = coupler_solid
    grp.addObject(obj_coupler)
    apply_material(obj_coupler, "Plastic-ABS")

    obj_cap = doc.addObject("Part::Feature", "BG_Orange_Top_Cap")
    obj_cap.Label = "STIHL Orange 6.0in Top Air Cap & Housing"
    obj_cap.Shape = orange_cap
    grp.addObject(obj_cap)
    apply_material(obj_cap, "Plastic-StihlOrange")

    obj_body = doc.addObject("Part::Feature", "BG_White_Blower_Body")
    obj_body.Label = "STIHL White 6.0in Ribbed Impeller Housing"
    obj_body.Shape = white_body
    grp.addObject(obj_body)
    apply_material(obj_body, "Plastic-StihlWhite")

    obj_nozzle = doc.addObject("Part::Feature", "BG_Black_Nozzle_Assembly")
    obj_nozzle.Label = "Black Two-Stage Tapered Discharge Nozzle"
    obj_nozzle.Shape = black_nozzle
    grp.addObject(obj_nozzle)
    apply_material(obj_nozzle, "Plastic-ABS")

    return grp
