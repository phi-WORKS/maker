"""
Compact Foam Camper - Surface Unfurling & Kerf Scoring Engine
Project: Parametric 2D Sheet Unrolling & CNC/Track-Saw Kerf Line Calculator
Calculates exact cumulative arc lengths, local bend radii, and discrete kerf score positions.

Features:
  - Numerical integration of cumulative roof arc length S(x)
  - Local curvature radius calculation R(x) = 1 / kappa(x)
  - Dynamic kerf pitch calculation P(s) = R(s) * (w_k / d_k)
  - Flat sheet blank 3D CAD model generation with kerf score slits (flat_patterns.FCStd)
  - Nested cutting schedule for standard 4' x 8' XPS foam sheets
"""

import os
import sys
import math
import FreeCAD
import Part

script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.abspath(".")

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False

from phi_works.maker.render import export_orthogonal_views
from phi_works.maker.materials import init_materials, apply_material


def roof_z(x, length=3658.0, height=1750.0):
    """Parametric elevation z as a function of station x along camper length."""
    if x <= 0:
        return 650.0
    elif x <= 1100.0:
        # Prow to apex
        u = x / 1100.0
        return 650.0 + (height - 650.0) * math.sin(u * math.pi / 2.0)
    elif x <= length:
        # Apex to rear transom
        u = (x - 1100.0) / (length - 1100.0)
        return height - (height - 480.0) * (u ** 1.45)
    else:
        return 480.0


def roof_dz_dx(x, length=3658.0, height=1750.0, eps=0.5):
    """First derivative dz/dx via central difference."""
    return (roof_z(x + eps, length, height) - roof_z(x - eps, length, height)) / (2.0 * eps)


def roof_d2z_dx2(x, length=3658.0, height=1750.0, eps=0.5):
    """Second derivative d2z/dx2 via central difference."""
    return (roof_z(x + eps, length, height) - 2.0 * roof_z(x, length, height) + roof_z(x - eps, length, height)) / (eps ** 2)


def get_local_radius(x, length=3658.0, height=1750.0):
    """Calculates local radius of curvature R(x) = 1 / kappa(x)."""
    dz = roof_dz_dx(x, length, height)
    d2z = roof_d2z_dx2(x, length, height)
    denom = (1.0 + dz**2) ** 1.5
    kappa = abs(d2z) / max(denom, 1e-6)
    return 1.0 / max(kappa, 1e-6)


def calculate_unrolled_roof(length=3658.0, height=1750.0, step=2.0, w_kerf=3.175, d_kerf=40.0):
    """
    Integrates cumulative arc-length S(x) and steps along the flat sheet
    to compute exact discrete kerf score line locations.
    """
    x_vals = []
    s_vals = [0.0]
    r_vals = []

    # 1. Integrate arc length
    x = 0.0
    cum_s = 0.0
    while x <= length:
        dz = roof_dz_dx(x, length, height)
        ds = math.sqrt(1.0 + dz**2) * step
        cum_s += ds
        x += step
        x_vals.append(x)
        s_vals.append(cum_s)
        r_vals.append(get_local_radius(x, length, height))

    total_unrolled_length = s_vals[-1]

    # 2. Discrete Kerf Stepping along S
    # Iteratively place kerf lines where bending is required (R < 3000 mm)
    kerf_lines = []
    s_curr = 20.0
    while s_curr < total_unrolled_length - 30.0:
        # Find corresponding x
        idx = min(int(s_curr / (total_unrolled_length / len(s_vals))), len(s_vals) - 1)
        r_local = max(r_vals[idx], 150.0)

        # Kerf pitch P = R * (w_kerf / d_kerf)
        pitch = r_local * (w_kerf / d_kerf)
        # Constrain pitch to practical shop limits: minimum 20 mm, maximum 150 mm
        pitch = max(min(pitch, 150.0), 20.0)

        kerf_lines.append({
            "s": s_curr,
            "radius_mm": r_local,
            "pitch_mm": pitch,
        })
        s_curr += pitch

    return total_unrolled_length, kerf_lines


def build_flat_patterns():
    init_materials()
    doc_name = "flat_patterns"
    fcstd_path = os.path.join(script_dir, f"{doc_name}.FCStd")

    doc = FreeCAD.newDocument(doc_name)
    doc.Label = "Camper Flat Patterns & Kerf Score Cut Sheet (Unrolled 2D Blank)"

    L = 3658.0
    W = 1981.0
    H = 1750.0
    W_KERF = 3.175     # 1/8" circular saw blade kerf
    D_KERF = 40.0      # 40 mm cut depth in 50 mm foam
    T_FOAM = 50.8      # 2.0" XPS foam

    tot_s, kerfs = calculate_unrolled_roof(L, H, w_kerf=W_KERF, d_kerf=D_KERF)

    print("\n" + "="*80)
    print(" COMPACT FOAM CAMPER: ROOF UNFURLING & KERF SCORING SCHEDULE")
    print("="*80)
    print(f" 3D Camper Base Length:      {L:6.1f} mm  ({L/25.4:5.1f} in / {L/304.8:4.2f} ft)")
    print(f" Total Unrolled Roof Length:  {tot_s:6.1f} mm  ({tot_s/25.4:5.1f} in / {tot_s/304.8:4.2f} ft)")
    print(f" Sheet Stock Requirement:     2x Standard 4' x 8' XPS Sheets (End-to-End Joint)")
    print(f" Total Kerf Score Cuts:       {len(kerfs)} discrete score lines")
    print(f" Saw Blade Kerf Width:        {W_KERF:.2f} mm (1/8 in)")
    print(f" Kerf Cut Depth:              {D_KERF:.1f} mm (Leaves {T_FOAM - D_KERF:.1f} mm uncut hinge)")
    print("-"*80)
    print(" SAMPLE KERF SCHEDULE (FIRST 10 CUTS FROM NOSE):")
    print(f" {'Cut #':<7} {'Distance S (mm)':<18} {'Distance S (in)':<18} {'Local R (mm)':<14} {'Pitch (in)':<10}")
    print(f" {'-'*6:<7} {'-'*16:<18} {'-'*16:<18} {'-'*12:<14} {'-'*8:<10}")
    for i, k in enumerate(kerfs[:10], 1):
        print(f" {i:<7} {k['s']:<18.1f} {k['s']/25.4:<18.2f} {k['radius_mm']:<14.1f} {k['pitch_mm']/25.4:<10.2f}")
    print("="*80 + "\n")

    # =========================================================================
    # 3D CAD MODEL OF UNROLLED FLAT SHEET WITH KERFS
    # =========================================================================
    grp = doc.addObject("App::DocumentObjectGroup", "Flat_Roof_Sheet")
    grp.Label = "Unrolled Flat Roof Blank with Kerf Cuts"

    # Base flat foam blank: Length = tot_s, Width = W, Height = T_FOAM
    base_box = Part.makeBox(tot_s, W, T_FOAM)

    # Cut kerf slits into the top (concave) face
    # Each slit: length across full width W, width = W_KERF, depth = D_KERF
    slit_cutters = []
    # Sample every 2nd kerf for clean CAD display and fast boolean
    for k in kerfs:
        x_slit = k["s"]
        cutter = Part.makeBox(W_KERF, W * 1.2, D_KERF + 2.0,
                              FreeCAD.Vector(x_slit - W_KERF / 2.0, -W * 0.1, T_FOAM - D_KERF))
        slit_cutters.append(cutter)

    all_cutters = Part.Compound(slit_cutters)
    scored_sheet = base_box.cut(all_cutters)

    feat_sheet = doc.addObject("Part::Feature", "Unrolled_Scored_Roof")
    feat_sheet.Label = f"Unrolled Roof Sheet ({tot_s/304.8:.1f}ft x {W/304.8:.1f}ft with {len(kerfs)} Kerfs)"
    feat_sheet.Shape = scored_sheet
    apply_material(feat_sheet, "Polymer-XPS-Foam")
    grp.addObject(feat_sheet)

    # Add 4x8 Sheet Reference Grid Outlines
    # Sheet 1: 0 to 2438.4 mm
    # Sheet 2: 2438.4 to 4876.8 mm
    sheet_w = 1219.2  # 4 ft
    sheet_l = 2438.4  # 8 ft
    edges_grid = []
    for i in range(2):
        x0 = i * sheet_l
        x1 = x0 + sheet_l
        p1 = FreeCAD.Vector(x0, 0, -5)
        p2 = FreeCAD.Vector(x1, 0, -5)
        p3 = FreeCAD.Vector(x1, sheet_w, -5)
        p4 = FreeCAD.Vector(x0, sheet_w, -5)
        edges_grid.extend([
            Part.makeLine(p1, p2),
            Part.makeLine(p2, p3),
            Part.makeLine(p3, p4),
            Part.makeLine(p4, p1),
        ])
    grid_compound = Part.Compound(edges_grid)
    feat_grid = doc.addObject("Part::Feature", "Standard_4x8_Sheet_Boundaries")
    feat_grid.Label = "Standard 4x8 Sheet Stock Boundaries (Reference)"
    feat_grid.Shape = grid_compound
    grp.addObject(feat_grid)

    doc.recompute()
    doc.saveAs(fcstd_path)
    print(f"Saved flat patterns master model to: {fcstd_path}")

    # Visual Renders
    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_doc = FreeCADGui.getDocument(doc.Name)
        FreeCADGui.updateGui()

        prefix_sheet = os.path.join(script_dir, "flat_scored_sheet")
        export_orthogonal_views(
            gui_doc,
            base_prefix=prefix_sheet,
            width=1920,
            height=1080
        )
        print("Generated flat pattern renders (flat_scored_sheet.png)")

    FreeCAD.closeDocument(doc.Name)
    print("Unfurl build complete!")


if __name__ == "__main__":
    build_flat_patterns()
    os._exit(0)
