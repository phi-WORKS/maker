# Compact Foam Camper v0.3.0 - Fabrication & Manufacturing Manual

> **Multi-Buck Suite, 1D Kerf-Bending Mechanics, and Walk-Through Monocoque Assembly**  
> *phi-WORKS Maker Framework (`projects/foam-camper/fabrication`)*

**Master Shop Assembly Guide**: 📋 [**`ASSEMBLY.md`**](ASSEMBLY.md) *(or [`../ASSEMBLY.md`](../ASSEMBLY.md))*  
**Master Project Root**: 📖 [**`../README.md`**](../README.md)  
**Master Assembly Buck**: [`camper_assembly_buck.FCStd`](camper_assembly_buck.FCStd) *(alias [`camper_buck.FCStd`](camper_buck.FCStd))*  
**Pop-Up Roof Canopy Buck**: [`roof_canopy_buck.FCStd`](roof_canopy_buck.FCStd)  
**Side Wall Bending Jig**: [`side_wall_buck.FCStd`](side_wall_buck.FCStd)  
**Automated Buck Suite Script**: [`build_bucks.py`](build_bucks.py)  

---

## 1. Fabrication Philosophy: Single-Axis 1D Developable Curvature

Building a compound-looking aerodynamic camper from $2.0''$ ($50.8\ \text{mm}$) Extruded Polystyrene (XPS) rigid foam insulation without complex compound foam stretching is achieved through **orthogonal 1D developable curvature intersection**:

1. **Side Walls**: Single-axis curved in the horizontal $XY$ plane (boat-tail planform curve) with strictly vertical rulings in $Z$. Flat sheets are scored with **vertical parallel kerfs** and pre-curved on the **Side Wall Bending Jig**.
2. **Pop-Up Roof Canopy**: Single-axis curved in the vertical $XZ$ plane (aerodynamic teardrop curve) with strictly lateral horizontal rulings in $Y$. Flat sheets are scored with **transverse parallel kerfs** and pre-curved on the **Roof Canopy Form Buck**.
3. **Compound 3D Shoulder Seam**: Formed along the natural 3D intersection curve of the two single-axis surfaces, supported and clamped against the **Master Assembly Buck's** shoulder stringers ($Y = \pm 533.5\ \text{mm}$).
4. **Walk-Through Center Door**: Station 0 on the master buck incorporates a full $24''$ center doorway cutout, enabling unhindered interior worker access and straightforward buck disassembly/removal straight out the front door!

```
                      END-TO-END MANUFACTURING PIPELINE
                      
┌───────────────────────────┐      ┌───────────────────────────┐
│   Parametric 3D Model     │      │   Three-Tier Buck Suite   │
│   (foam-camper.FCStd)     │      │   (build_bucks.py)        │
└─────────────┬─────────────┘      └─────────────┬─────────────┘
              │                                  │
              ▼                                  ▼
┌───────────────────────────┐      ┌───────────────────────────┐
│ 1D Kerf Score Schedules   │      │ Form Components on Benches│
│ • Side Walls (Vertical)   │─────►│ • Side Walls (side_wall)  │
│ • Roof Canopy (Transverse)│      │ • Roof Canopy (roof_canop)│
└───────────────────────────┘      └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Erect Master Assembly Buck│
                                   │ on 12' x 6.5' Trailer Deck│
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Mount Front Door Bulkhead,│
                                   │ Transom & Pre-Curved Sides│
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Inject Polyurethane Glue  │
                                   │ & Clamp Under Compression │
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Slide Out Buck Bulkheads  │
                                   │ via 24" Front Door!       │
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │ Install Pop-Top Canopy    │
                                   │ & Apply Exterior PMF Skin │
                                   └───────────────────────────┘
```

---

## 2. Multi-Buck Suite Architecture

The v0.3.0 fabrication suite replaces monolithic molds with three specialized, lightweight jigs:

### A. Master Egg-Crate Assembly Buck (`camper_assembly_buck.FCStd`)
- **Purpose**: Full-scale 12' × 6.5' jig mounted on the trailer floor deck to square and bond the modular shell pieces together.
- **Transverse Bulkheads (5 Stations)**:
  - **Station 0** ($X = 60\ \text{mm}$): Front nose bulkhead with $24.0''$ ($610\ \text{mm}$) walk-through door cutout.
  - **Station 1** ($X = 1,200\ \text{mm}$): Shoulder apex bulkhead ($6'-6''$ max width, $4'-11''$ height) with interior crawl opening.
  - **Station 2** ($X = 2,000\ \text{mm}$): Mid-cabin bulkhead with interior crawl opening.
  - **Station 3** ($X = 2,700\ \text{mm}$): Permanent birch galley bulkhead / pop-top rear curb.
  - **Station 4** ($X = 3,580\ \text{mm}$): Rear transom bulkhead with observation window aperture.
- **Longitudinal Shoulder Stringers**:
  - Two continuous curved stringers positioned at $Y = \pm 533.5\ \text{mm}$ ($42''$ center aisle well).
  - Half-lap interlocking slots ($19.5\ \text{mm}$ wide $\times 100\ \text{mm}$ deep).
  - Defines the exact 3D compound shoulder seam line and clamping ledges.
- **Weight**: **$134.3\ \text{lbs}$ ($60.9\ \text{kg}$)** (~2.8 sheets of $3/4''$ CDX plywood).

### B. Pop-Up Roof Canopy Form Buck (`roof_canopy_buck.FCStd`)
- **Purpose**: Standalone bench jig for pre-curving the $42'' \times 106''$ 1D $XZ$ arched pop-up roof canopy off-trailer.
- **Framing**:
  - 3 longitudinal profile formers (Left $Y = +420\ \text{mm}$, Center $Y = 0$, Right $Y = -420\ \text{mm}$) cut to $H_{\text{roof\_in}}(X)$.
  - 4 transverse interlocking cross-ties with half-lap slots.
  - Ratchet strap anchor points along the base table flange.
- **Weight**: **$187.3\ \text{lbs}$ ($84.9\ \text{kg}$)**.

### C. Side Wall Planform Bending Jig (`side_wall_buck.FCStd`)
- **Purpose**: Shop floor/bench jig for pre-curving the vertically kerfed $2.0''$ XPS side panels into the boat-tail planform curve.
- **Framing**:
  - Curved $3/4''$ plywood sole plate matching the inner boat-tail curve ($W_{\text{in}}(X)/2$).
  - 6 vertical $2\times 4$ clamp stanchions spaced along the curve.
- **Weight**: **$46.6\ \text{lbs}$ ($21.1\ \text{kg}$)**.

---

## 3. Kerf Scoring Mechanics & Mathematics

Rigid XPS foam has high compressive modulus but nearly zero tensile ductility. To bend thick $2.0''$ ($50.8\ \text{mm}$) sheets smoothly:
- **Always kerf the CONCAVE (inner) face.**
- Cut depth $d_k = 1.57''$ ($40.0\ \text{mm}$), leaving an uncut outer hinge skin of $t_{\text{skin}} \approx 10.8\ \text{mm}$.
- When bent over the buck, the kerfs **pinch closed** under compression.
- Polyurethane adhesive applied in the kerfs expands into the closing joint, curing into rigid composite I-beam ribs that make the cured curve stiffer than the unbent foam!

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

### Kerf Pitch Equation:
$$\text{Closing Angle: } \Delta \theta = \frac{w_k}{d_k}$$
$$\text{Score Spacing: } P = R \cdot \left(\frac{w_k}{d_k}\right)$$

For $w_k = 3.2\ \text{mm}$ ($1/8''$ blade) and $d_k = 40.0\ \text{mm}$:
$$P = 0.08 \cdot R$$

| Zone | Curve Axis | Bend Radius $R$ | Kerf Orientation | Recommended Score Pitch |
| :--- | :---: | :---: | :---: | :--- |
| **Side Walls** | $XY$ Plan | $120''$ to $240''$ | **Vertical** | **$2.0''$ ($50.8\ \text{mm}$)** uniform pitch |
| **Roof Brow** | $XZ$ Elev | $28''$ (711 mm) | **Transverse** | **$2.25''$ ($57\ \text{mm}$)** centers |
| **Roof Apex** | $XZ$ Elev | $48''$ (1,219 mm) | **Transverse** | **$3.75''$ ($95\ \text{mm}$)** centers |
| **Rear Taper**| $XZ$ Elev | $36''$ (914 mm) | **Transverse** | **$2.75''$ ($70\ \text{mm}$)** centers |

---

## 4. Summary of CAD Models & Generators

| Model File | Generator Script | Primary Function |
| :--- | :--- | :--- |
| [`camper_assembly_buck.FCStd`](camper_assembly_buck.FCStd) | [`build_bucks.py`](build_bucks.py) | Master 12' egg-crate assembly jig on trailer |
| [`roof_canopy_buck.FCStd`](roof_canopy_buck.FCStd) | [`build_bucks.py`](build_bucks.py) | Standalone pop-up roof canopy forming buck |
| [`side_wall_buck.FCStd`](side_wall_buck.FCStd) | [`build_bucks.py`](build_bucks.py) | Curved shop floor side wall bending jig |
| [`foam-camper.FCStd`](../foam-camper.FCStd) | [`../build.py`](../build.py) | Master camper shell & pop-top assembly |

*For complete step-by-step shop assembly procedures and multi-view photo/render galleries, consult [**`ASSEMBLY.md`**](ASSEMBLY.md).*
