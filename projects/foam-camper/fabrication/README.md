# Compact Foam Camper - Fabrication & Manufacturing Manual

> **Rigid Insulation Unfurling, Kerf-Bending Mechanics, and Interlocking Buck Construction**  
> *phi-WORKS Maker Framework (`projects/foam-camper/fabrication`)*

**Master Shop Assembly Guide**: 📋 [**`ASSEMBLY.md`**](ASSEMBLY.md) *(or [`../ASSEMBLY.md`](../ASSEMBLY.md))*  
**Master Project Root**: 📖 [**`../README.md`**](../README.md)  
**Fabrication Buck Model**: [`camper_buck.FCStd`](camper_buck.FCStd)  
**Flat Patterns Model**: [`flat_patterns.FCStd`](flat_patterns.FCStd)  

---

## 1. Fabrication Philosophy

Building a compound-curved aerodynamic camper from $2.0''$ ($50.8\ \text{mm}$) Extruded Polystyrene (XPS) rigid foam insulation requires bridging the gap between **continuous 3D CAD geometry** and **flat $4' \times 8'$ sheet materials**.

The manufacturing pipeline consists of three synchronized pillars:
1. **Surface Unfurling & Kerf Planning**: Translating 3D curved surfaces into flat 2D cut patterns with mathematically calculated score lines on the concave face.
2. **The "Egg-Crate" Interlocking Plywood Buck**: A rigid, self-squaring 3D inner skeleton constructed from interlocking slotted plywood ribs, offset inward by exactly $2.0''$ ($50.8\ \text{mm}$) to provide a solid mold for bending.
3. **Kerf-Closing Monocoque Fusion**: Applying moisture-curing expanding polyurethane (PU) adhesive into the kerf slits, wrapping the panels over the buck, and clamping with ratchet straps so the slits pinch shut and cure into high-strength composite ribs.

```
                      END-TO-END MANUFACTURING PIPELINE
                      
┌───────────────────────────┐      ┌───────────────────────────┐
│   Parametric 3D Model     │      │   Plywood Egg-Crate Buck  │
│   (12' x 6.5' Shell)      │      │   (Inner Contour - 2.0")  │
└─────────────┬─────────────┘      └─────────────┬─────────────┘
              │                                  │
              ▼                                  ▼
┌───────────────────────────┐      ┌───────────────────────────┐
│   2D Unfurled Patterns    │      │  Assemble Buck on Trailer │
│   & Calculated Kerf Lines │      │  (Self-Squaring Grid)     │
└─────────────┬─────────────┘      └─────────────┬─────────────┘
              │                                  │
              ▼                                  ▼
┌───────────────────────────┐      ┌───────────────────────────┐
│   Score Foam (Inner Face) │─────►│  Dry-Fit Panels over Buck │
│   & Track-Saw Perimeter   │      │  & Adjust Ratchet Straps  │
└───────────────────────────┘      └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Inject Polyurethane Glue  │
                                   │ & Clamp Under Compression │
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Remove Temporary Ribs     │
                                   │ & Skin Exterior with PMF  │
                                   └───────────────────────────┘
```

---

## 2. Unfurling 3D Curved Surfaces to Flat Sheets

### A. Developable Surfaces ($K = 0$, Zero-Stretch Unrolling)
Surfaces with zero Gaussian curvature ($K = k_1 \cdot k_2 = 0$) can be flattened onto sheet goods with **zero stretching, tearing, or wrinkling**:
- **Side Walls**: 2D planar profiles cut directly from $4' \times 8'$ XPS sheets.
- **Cylindrical / Ruled Roof Arches (Form A & B)**: The flat unrolled length $S$ equals the true cumulative arc length along the curve:
  $$S = \int_{x_1}^{x_2} \sqrt{1 + \left(\frac{dz}{dx}\right)^2} dx$$
- **Faceted Chine Panels (Form B)**: Every panel between chine fold lines is a planar quad. Unfurling is $100\%$ exact and produces flat polygonal nested cutouts.

### B. Compound Surfaces ($K \ne 0$, Double-Curvature)
Surfaces curved across both axes simultaneously (such as the rounded nose prow of Form A or the organic loft of Form C) cannot be unrolled without distortion. Three practical shop strategies resolve this:
1. **Longitudinal Strakes (Boatbuilding Planking)**: Slicing the compound curve into narrow developable strips ($6''$ to $10''$ wide). The lateral curvature across a narrow strip is negligible, allowing single-axis bending along the length.
2. **2D Cross-Hatch / Waffle Kerfing**: Cutting perpendicular kerf slits ($X$ and $Y$ grid) on the inner face. The uncut outer skin flexes in two directions while the grid cells compress and expand.
3. **Laminated Corner Blocks**: Using flat sheets for all developable wall and roof runs, and gluing laminated blocks of 2" foam at the compound front corners, rasped to final shape with a drywall/foam rasp.

---

## 3. Kerf Scoring Mechanics & Mathematics

### The "Kerf-Closing" Rule
Rigid foam has high compressive strength but almost zero tensile stretch. 
- **Always kerf the CONCAVE (inner) face.**
- As the foam is bent around the buck, the kerf slits **pinch closed** under compression.
- When expanding polyurethane glue (e.g. Gorilla Glue or low-expansion foam adhesive) is applied into the slits, the closing joint forces the glue throughout the seam. Upon curing, the adhesive forms rigid polyurethane "I-beam" ribs, making the bent curve significantly stiffer than the original unbent foam!

```
       FLAT UNBENT SHEET                          BENT AROUND INNER BUCK
┌───────────────────────────────┐           ───────────────────────────────── (Outer Skin)
│   Uncut Outer Skin (t_skin)   │                     ▲           ▲
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤            (t_skin) │           │
│   |   |   |   |   |   |   |   │                     ▼           ▼
│   |   |   |   |   |   |   |   │ (d_k)            \  /        \  /   <-- Kerfs CLOSE tightly
│   |   |   |   |   |   |   |   │                   \/          \/        under compression
└─ ─┴───┴───┴───┴───┴───┴───┴───┘             ───────────────────────
    ◄─ P ─►   ◄w_k►                                  (Concave Inner Face)
```

### Derivation of Kerf Pitch Formula
Let:
- $R$ = Inside bend radius (mm)
- $t$ = Foam thickness = $50.8\ \text{mm}$ ($2.0''$)
- $d_k$ = Depth of kerf cut ($75\%–80\%$ of thickness = $38\ \text{mm}$ to $40\ \text{mm}$, leaving uncut outer skin $t_{\text{skin}} \approx 10\text{--}12\ \text{mm}$)
- $w_k$ = Kerf saw blade width ($3.2\ \text{mm}$ or $1/8''$ for standard circular saw; $2.2\ \text{mm}$ for track saw)

For each kerf cut to close fully when bent to radius $R$:
$$\text{Closing Angle per Kerf: } \Delta \theta_{\text{kerf}} = \frac{w_k}{d_k}$$
$$\text{Linear Pitch between Scores: } P = R \cdot \Delta \theta_{\text{kerf}} = R \cdot \left(\frac{w_k}{d_k}\right)$$

### Kerf Pitch Lookup Table (for 2.0" XPS Foam, $d_k = 40\ \text{mm}$, $w_k = 3.2\ \text{mm}$):

| Camper Zone | Bend Radius $R$ | Pitch $P$ (Metric) | Pitch $P$ (Imperial) | Recommended Score Spacing |
| :--- | :---: | :---: | :---: | :--- |
| **Tight Roof Shoulder** | $10''$ (254 mm) | 20.3 mm | 0.80" | **$3/4''$ ($20\ \text{mm}$)** centers |
| **Front Nose Lower Prow**| $16''$ (406 mm) | 32.5 mm | 1.28" | **$1.25''$ ($32\ \text{mm}$)** centers |
| **Front Windshield Curve**| $28''$ (711 mm) | 56.9 mm | 2.24" | **$2.25''$ ($57\ \text{mm}$)** centers |
| **Mid-Roof Crown Arch** | $48''$ (1,219 mm)| 97.5 mm | 3.84" | **$3.75''$ ($95\ \text{mm}$)** centers |
| **Gentle Cabin Crown** | $72''$ (1,829 mm)| 146.3 mm | 5.76" | **$5.5''$ ($140\ \text{mm}$)** centers |

---

## 4. The "Egg-Crate" Interlocking Plywood Buck

To provide a rigid shape to wrap scored foam against, a self-squaring **egg-crate plywood skeleton** is assembled on the trailer deck.

```
                    EGG-CRATE BUCK STRUCTURE
                    
       Station 0       Station 1        Station 2        Station 3        Station 4
        (Nose)      (Shoulder Peak)    (Mid-Cabin)        (Galley)         (Transom)
          │                │                │                │                │
     ┌────┼────────────────┼────────────────┼────────────────┼────────────────┼────┐
     │    │  Upper Left Shoulder Stringer   │                │                │    │
     ├────┼────────────────┼────────────────┼────────────────┼────────────────┼────┤
     │    │                │                │                │                │    │
     │════╪════════════════╪════════════════╪════════════════╪════════════════╪════│ Center Ridge Spine
     │    │                │                │                │                │    │
     ├────┼────────────────┼────────────────┼────────────────┼────────────────┼────┤
     │    │  Upper Right Shoulder Stringer  │                │                │    │
     └────┼────────────────┼────────────────┼────────────────┼────────────────┼────┘
          │                │                │                │                │
```

### Engineering Parameters:
1. **$2.0''$ ($50.8\ \text{mm}$) Inward Offset**:
   Every exterior contour of the buck is offset inward by exactly $50.8\ \text{mm}$ so the outer surface of the $2''$ foam sits precisely on the master aerodynamic envelope.
2. **Interlocking Half-Lap Slots**:
   - Transverse bulkheads have vertical slots ($19.5\ \text{mm}$ wide for $3/4''$ plywood) running from top down to the centerline.
   - Longitudinal stringers have matching slots running from bottom up to the centerline.
   - The pieces slip together without fasteners, automatically locking into a square, rigid 3D jig.
3. **Dual-Use vs. Sacrificial Stations**:
   - **Station 3 (Galley Partition)**: Cut from high-grade birch plywood. Left permanently inside the camper as the structural bulkhead separating the sleeping cabin from the rear kitchen.
   - **Station 0, 1, 2, 4**: Temporary shaping ribs cut from cheap 1/2" or 3/4" CDX plywood or OSB. Designed with large central crawl-through cutouts so the builder can work inside the shell and remove the ribs through the door opening once the foam shell cures.

---

## 5. Shop Assembly Protocol

> For the comprehensive, illustrated step-by-step shop manual with high-resolution 3D CAD renders, hardware checklists, and clamping sequences, refer directly to [**`ASSEMBLY.md`**](ASSEMBLY.md) *(or [`../ASSEMBLY.md`](../ASSEMBLY.md))*.

1. **Erect the Buck**: Assemble the interlocking plywood egg-crate on the trailer deck. Pin the base to the trailer floor.
2. **Profile Foam Panels**: Cut flat side walls and unrolled roof blanks using a circular saw or track saw.
3. **Score Kerf Lines**: Set circular saw blade depth to $1.5''$ ($38\ \text{mm}$) on the track guide. Score the inside face according to the calculated pitch table.
4. **Dry Fit**: Drape panels over the buck. Secure with 2" cargo ratchet straps over scrap foam corner protectors to test bend radii and seam alignment.
5. **Glue & Clamp**: Release straps, apply polyurethane adhesive into kerf cuts and tongue-and-groove edge seams, re-strap tightly over the buck, and allow 12 hours to cure.
6. **Skinning (Poor Man's Fiberglass)**:
   - Roll exterior with Titebond II wood glue (or Gripper acrylic primer).
   - Lay unbleached heavy canvas drop-cloth (10 oz or 12 oz) smooth over the foam.
   - Saturate canvas with a second coat of Titebond II.
   - Once cured, sand lightly and apply 2 coats of exterior UV-resistant latex paint or elastomeric roof coating.
