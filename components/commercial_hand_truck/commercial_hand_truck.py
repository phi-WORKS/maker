"""
Vintage Commercial Hand Truck Chassis Component (Custom Restored Red Frame)
Standalone 3D Parametric CAD Module

Modeled after physical vintage green hand truck donor frame (restored in Red):
- 1.0" OD tubular steel inverted U-frame (12.5" center-to-center spacing, 46.0" top of U)
- Center handle spine pipe with ergonomic top backward loop and vertical spine tube
- 3 horizontal steel cross straps (1.0" wide at 12", 22", 31" heights)
- Authentic dual-strut triangular axle trusses connecting uprights to axle
- 9.5" diameter wheels with axle centered at 4.75" from floor and 4.75" from side rails
- Forward cut-away / notched toe plate bay for radiant sled clearance
"""

import os
import sys
import math
import FreeCAD
import Part
from phi_works.maker.materials import apply_material

def create_commercial_hand_truck_component(doc, placement=None):
    """
    Creates the Vintage Commercial Hand Truck chassis in `doc`.
    """
    if placement is None:
        placement = FreeCAD.Placement()
    elif isinstance(placement, FreeCAD.Vector):
        placement = FreeCAD.Placement(placement, FreeCAD.Rotation())

    grp = doc.addObject("App::DocumentObjectGroup", "Commercial_Hand_Truck")
    grp.Label = "Vintage Commercial Hand Truck Chassis (Restored Red Frame)"

    # Verified Physical Dimensions (Imperial user-specified converted to mm)
    TUBE_OD = 25.4              # 1.0 in OD steel tubing
    R_tube = TUBE_OD / 2.0
    FRAME_W = 317.5             # 12.5 in center-to-center upright spacing (X = ±158.75 mm)
    TOP_H = 1168.4              # 46.0 in top of the U-bend
    R_bend = FRAME_W / 2.0      # 6.25 in (158.75 mm) semi-circular bend radius
    Z_bend_start = TOP_H - R_tube - R_bend  # 996.95 mm (39.25 in) straight tube top
    Z_bot = 0.0                 # Floor datum

    # Axle & Wheel Geometry (User Specified: 9.5" wheels, axle at 4.75" from floor and side rail)
    AXLE_Z = 120.65             # 4.75 in from floor
    AXLE_Y = 120.65             # 4.75 in rearward offset from side rail plane
    AXLE_DIA = 15.875           # 5/8 in solid steel axle rod
    AXLE_LEN = 540.0            # 21.25 in total axle length
    WHEEL_OD = 241.3            # 9.5 in tire outer diameter
    WHEEL_W = 76.2              # 3.0 in tire width
    RIM_OD = 127.0              # 5.0 in rim diameter
    WHEEL_X = 220.0             # Wheel center position (X = ±220 mm, track width 440 mm)

    # --------------------------------------------------------------------------
    # 1. Outer Inverted U-Frame (Vertical Uprights + Semi-Circular Top U-Bend)
    # --------------------------------------------------------------------------
    left_tube = Part.makeCylinder(R_tube, Z_bend_start - Z_bot, FreeCAD.Vector(-FRAME_W/2, 0, Z_bot), FreeCAD.Vector(0, 0, 1))
    right_tube = Part.makeCylinder(R_tube, Z_bend_start - Z_bot, FreeCAD.Vector(FRAME_W/2, 0, Z_bot), FreeCAD.Vector(0, 0, 1))

    # Semi-Circular Top U-Bend using Torus cut in half
    torus_full = Part.makeTorus(R_bend, R_tube, FreeCAD.Vector(0, 0, Z_bend_start), FreeCAD.Vector(0, 1, 0))
    # Keep upper half (Z >= Z_bend_start)
    torus_cut_box = Part.makeBox(FRAME_W + 2*TUBE_OD + 20.0, 2*TUBE_OD + 20.0, R_bend + 20.0,
                                 FreeCAD.Vector(-(FRAME_W + 2*TUBE_OD + 20.0)/2, -(2*TUBE_OD + 20.0)/2, Z_bend_start - R_bend - 20.0))
    top_u_bend = torus_full.cut(torus_cut_box)

    outer_u_frame = left_tube.fuse(right_tube).fuse(top_u_bend)

    # --------------------------------------------------------------------------
    # 2. Center Handle Spine Pipe (Top Backward Loop + Center Vertical Spine)
    # --------------------------------------------------------------------------
    # Welded to underside of top U-bend at (0, 0, TOP_H - 2*R_tube = 1143 mm)
    # Curves backward into an ergonomic high-back loop handle to Y ~ +160 mm,
    # then bends down and forward to Y = +15 mm (rear face of cross straps),
    # and runs straight down along X = 0 to Z = 120 mm.
    loop_reach_y = 160.0
    z_apex = TOP_H - 40.0
    z_loop_bot = 900.0

    # Top backward curved loop
    handle_upper = Part.makeCylinder(R_tube, loop_reach_y, FreeCAD.Vector(0, 0, z_apex), FreeCAD.Vector(0, 1, -0.2).normalize())
    p_loop_peak = FreeCAD.Vector(0, loop_reach_y, z_apex - loop_reach_y * 0.2)
    
    # Return slant from peak down-forward to cross-strap plane (Y = 16 mm, Z = z_loop_bot)
    p_spine_start = FreeCAD.Vector(0, 16.0, z_loop_bot)
    vec_return = p_spine_start - p_loop_peak
    handle_return = Part.makeCylinder(R_tube, vec_return.Length, p_loop_peak, vec_return.normalize())

    # Vertical center spine tube from Z = z_loop_bot down to Z = 100 mm
    center_spine = Part.makeCylinder(R_tube, z_loop_bot - 100.0, FreeCAD.Vector(0, 16.0, 100.0), FreeCAD.Vector(0, 0, 1))

    # Weld spheres for smooth pipe bends
    elbow_top = Part.makeSphere(R_tube, FreeCAD.Vector(0, 0, z_apex))
    elbow_peak = Part.makeSphere(R_tube, p_loop_peak)
    elbow_spine = Part.makeSphere(R_tube, p_spine_start)

    center_pipe_assembly = handle_upper.fuse(handle_return).fuse(center_spine).fuse(elbow_top).fuse(elbow_peak).fuse(elbow_spine)

    # --------------------------------------------------------------------------
    # 3. 3 Horizontal Cross Straps (1.0" Wide Steel Flat Bar)
    # --------------------------------------------------------------------------
    # Strap 1 (Lower): Top at 12.0" (304.8 mm) -> Z in [279.4, 304.8 mm]
    # Strap 2 (Middle): Top at 22.0" (558.8 mm) -> Z in [533.4, 558.8 mm]
    # Strap 3 (Upper): Top at 31.0" (787.4 mm) -> Z in [762.0, 787.4 mm]
    STRAP_W = 25.4      # 1.0 in wide
    STRAP_T = 4.76      # 3/16 in thick
    strap_z_tops = [304.8, 558.8, 787.4]
    straps = []

    for z_top in strap_z_tops:
        strap_box = Part.makeBox(FRAME_W, STRAP_T, STRAP_W,
                                 FreeCAD.Vector(-FRAME_W/2, R_tube - 1.0, z_top - STRAP_W))
        straps.append(strap_box)

    cross_straps_compound = straps[0].fuse(straps[1]).fuse(straps[2])

    # --------------------------------------------------------------------------
    # 4. Toe Plate Stubs & Foot Base (Cut-away center bay for Road Roaster sled)
    # --------------------------------------------------------------------------
    # Base plates welded to bottom of uprights extending forward to Y = -100 mm
    stub_l = Part.makeBox(TUBE_OD + 8.0, 90.0, 6.35, FreeCAD.Vector(-FRAME_W/2 - R_tube - 4.0, -90.0, 0.0))
    stub_r = Part.makeBox(TUBE_OD + 8.0, 90.0, 6.35, FreeCAD.Vector(FRAME_W/2 - R_tube - 4.0, -90.0, 0.0))
    toe_stubs = stub_l.fuse(stub_r)

    # Combine Main Frame Body
    full_frame_shape = outer_u_frame.fuse(center_pipe_assembly).fuse(cross_straps_compound).fuse(toe_stubs)
    full_frame_shape.Placement = placement

    obj_frame = doc.addObject("Part::Feature", "Hand_Truck_U_Frame")
    obj_frame.Label = "Vintage 1.0in Tubular U-Frame with Center Spine & Straps"
    obj_frame.Shape = full_frame_shape
    grp.addObject(obj_frame)
    apply_material(obj_frame, "PowderCoat-IndustrialRed")

    # --------------------------------------------------------------------------
    # 5. Authentic Dual Triangular Axle Trusses (Left & Right)
    # --------------------------------------------------------------------------
    # Each truss forms a rigid triangle welded directly to the outside of the vertical pipe:
    # - Apex at Axle Sleeve: (X_truss, AXLE_Y = 120.65 mm, AXLE_Z = 120.65 mm)
    # - Lower Strut starts at upright base: (X_truss, 0, 30.0 mm)
    # - Upper Diagonal Strut starts at Strap 1: (X_truss, 0, 292.0 mm)
    TRUSS_W = 25.4      # 1.0 in wide flat bar
    TRUSS_T = 4.76      # 3/16 in thick
    SLEEVE_OD = 28.0
    SLEEVE_LEN = 25.0
    
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
        solid.translate(FreeCAD.Vector(x_center - thickness/2.0, 0, 0))
        return solid

    trusses = []
    # Straps welded to the outside wall of the vertical pipes:
    # Pipe centerline at ±FRAME_W/2 = ±158.75 mm, outer wall at ±(158.75 + 12.7) = ±171.45 mm
    # Strap center at ±(171.45 + TRUSS_T/2) = ±173.83 mm
    x_truss_positions = [-(FRAME_W/2 + R_tube + TRUSS_T/2), FRAME_W/2 + R_tube + TRUSS_T/2]

    for x_t in x_truss_positions:
        # Axle sleeve collar centered on axle axis at x_t
        sleeve = Part.makeCylinder(SLEEVE_OD/2, SLEEVE_LEN,
                                   FreeCAD.Vector(x_t - SLEEVE_LEN/2, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))

        # Lower Strut: connects base of vertical pipe (Y = 0, Z = 30 mm) to axle (AXLE_Y, AXLE_Z)
        strut_low = make_strap_yz(0.0, 30.0, AXLE_Y, AXLE_Z, TRUSS_W, TRUSS_T, x_t)

        # Upper Diagonal Strut: connects lower cross-strap on vertical pipe (Y = 0, Z = 292 mm) to axle (AXLE_Y, AXLE_Z)
        strut_up = make_strap_yz(0.0, 292.0, AXLE_Y, AXLE_Z, TRUSS_W, TRUSS_T, x_t)

        truss_side = sleeve.fuse(strut_low).fuse(strut_up)
        trusses.append(truss_side)

    trusses_compound = trusses[0].fuse(trusses[1])
    trusses_compound.Placement = placement

    obj_truss = doc.addObject("Part::Feature", "Triangular_Axle_Trusses")
    obj_truss.Label = "Triangular Axle Trusses (Frame-to-Axle Triangular Brackets)"
    obj_truss.Shape = trusses_compound
    grp.addObject(obj_truss)
    apply_material(obj_truss, "PowderCoat-IndustrialRed")

    # --------------------------------------------------------------------------
    # 6. Continuous Solid Steel Axle Shaft (Common Datum Axis)
    # --------------------------------------------------------------------------
    axle_shaft = Part.makeCylinder(AXLE_DIA/2.0, AXLE_LEN,
                                   FreeCAD.Vector(-AXLE_LEN/2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    # Axle retainers / lock collars
    collar_od = 28.0
    collar_w = 12.0
    collar_l = Part.makeCylinder(collar_od/2.0, collar_w, FreeCAD.Vector(-WHEEL_X - WHEEL_W/2 - collar_w - 2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    collar_r = Part.makeCylinder(collar_od/2.0, collar_w, FreeCAD.Vector(WHEEL_X + WHEEL_W/2 + 2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    axle_shape = axle_shaft.fuse(collar_l).fuse(collar_r)
    axle_shape.Placement = placement

    obj_axle = doc.addObject("Part::Feature", "Solid_Steel_Axle_Shaft")
    obj_axle.Label = "5/8in Continuous Solid Steel Axle Shaft (Common Axis)"
    obj_axle.Shape = axle_shape
    grp.addObject(obj_axle)
    apply_material(obj_axle, "Steel-ZincPlated")

    # --------------------------------------------------------------------------
    # 7. 9.5" Heavy-Duty Wheels (Tires & Stamped Steel Rims)
    # --------------------------------------------------------------------------
    # Left & Right Rims
    rim_l = Part.makeCylinder(RIM_OD/2.0, WHEEL_W - 8.0, FreeCAD.Vector(-WHEEL_X - (WHEEL_W - 8.0)/2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    rim_r = Part.makeCylinder(RIM_OD/2.0, WHEEL_W - 8.0, FreeCAD.Vector(WHEEL_X - (WHEEL_W - 8.0)/2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    rims_shape = rim_l.fuse(rim_r)
    rims_shape.Placement = placement

    obj_rims = doc.addObject("Part::Feature", "Wheel_Rims_9_5in")
    obj_rims.Label = "5.0in Stamped Steel Wheel Rims"
    obj_rims.Shape = rims_shape
    grp.addObject(obj_rims)
    apply_material(obj_rims, "Steel-ZincPlated")

    # Left & Right Tires (9.5" OD, 3.0" wide)
    tire_l_out = Part.makeCylinder(WHEEL_OD/2.0, WHEEL_W, FreeCAD.Vector(-WHEEL_X - WHEEL_W/2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    tire_l_in = Part.makeCylinder(RIM_OD/2.0, WHEEL_W + 2.0, FreeCAD.Vector(-WHEEL_X - WHEEL_W/2.0 - 1.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    tire_l = tire_l_out.cut(tire_l_in)

    tire_r_out = Part.makeCylinder(WHEEL_OD/2.0, WHEEL_W, FreeCAD.Vector(WHEEL_X - WHEEL_W/2.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    tire_r_in = Part.makeCylinder(RIM_OD/2.0, WHEEL_W + 2.0, FreeCAD.Vector(WHEEL_X - WHEEL_W/2.0 - 1.0, AXLE_Y, AXLE_Z), FreeCAD.Vector(1, 0, 0))
    tire_r = tire_r_out.cut(tire_r_in)

    tires_shape = tire_l.fuse(tire_r)
    tires_shape.Placement = placement

    obj_tires = doc.addObject("Part::Feature", "Tires_9_5in")
    obj_tires.Label = "9.5in Heavy-Duty Semi-Pneumatic All-Terrain Rubber Tires"
    obj_tires.Shape = tires_shape
    grp.addObject(obj_tires)
    apply_material(obj_tires, "Rubber-Solid")

    return grp
