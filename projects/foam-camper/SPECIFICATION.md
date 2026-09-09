# Compact Foam Camper - Technical Specification

> **Physical Dimensions, 1D Curvature Mechanics, Modular Assembly & Multi-Buck Engineering**  
> *Project Version: v0.3.0 (Active Master)*

---

## 1. Master Envelope & Parametric VarSet

The model is driven parametrically by FreeCAD's native `App::VarSet` (`Vars`) container inside `foam-camper.FCStd`:

| Parameter Name | Metric (mm) | Imperial | Description |
| :--- | :---: | :---: | :--- |
| **`Bed_Length`** | $3,658.0\ \text{mm}$ | $12'-0''$ ($144.0''$) | Overall camper body length along trailer bed |
| **`Bed_Width`** | $1,981.0\ \text{mm}$ | $6'-6''$ ($78.0''$) | Maximum outer width at shoulder apex |
| **`Nose_Width`** | $1,300.0\ \text{mm}$ | $4'-3.2''$ ($51.2''$) | Front bulkhead width at towing end |
| **`Rear_Width`** | $1,520.0\ \text{mm}$ | $4'-11.8''$ ($59.8''$) | Rear transom width |
| **`Apex_Height`** | $1,500.0\ \text{mm}$ | $4'-11''$ ($59.0''$) | Closed exterior apex height above floor |
| **`Brow_Height`** | $1,350.0\ \text{mm}$ | $4'-5.1''$ ($53.1''$) | Front brow peak height |
| **`Transom_Height`** | $850.0\ \text{mm}$ | $2'-9.5''$ ($33.5''$) | Rear transom height |
| **`Nose_Height`** | $900.0\ \text{mm}$ | $2'-11.4''$ ($35.4''$) | Front nose height |
| **`Foam_Thickness`** | $50.8\ \text{mm}$ | $2.0''$ | Commercial Extruded Polystyrene (XPS) rigid foam |
| **`PopUp_Width`** | $1,067.0\ \text{mm}$ | $42.0''$ ($3'-6''$) | Center pop-top channel width |
| **`PopUp_Length`** | $2,700.0\ \text{mm}$ | $106.3''$ ($8'-10.3''$) | Pop-top standing canopy longitudinal span |
| **`PopUp_Lift`** | **$508.0\ \text{mm}$** | **$20.0''$** | Parametric vertical stroke (0 mm travel, 508 mm camp) |
| **`Door_Width`** | $610.0\ \text{mm}$ | $24.0''$ ($2'-0''$) | Front walk-through entrance doorway |
| **`Door_Height`** | $1,270.0\ \text{mm}$ | $50.0''$ ($4'-2''$) | Lower rigid front door threshold |

---

## 2. Ergonomics & Interior Headroom Comparison

| Operational Mode | Pop-Up Stroke | Central Standing Headroom | Center Apex Headroom | 6'0" Person Clearance | Exterior Height on Trailer* |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Travel Mode (Closed)** | $0.0\ \text{mm}$ | $4'-9.5''$ ($1,460\ \text{mm}$) | $4'-11''$ ($1,500\ \text{mm}$) | Seated / Berth Mode | **$\sim 6'-5''$ ($1,955\ \text{mm}$)** |
| **Camping Mode (Elevated)** | **$508.0\ \text{mm}$ ($20''$)** | **$6'-5.5''$ ($1,968\ \text{mm}$)** | **$6'-7''$ ($2,008\ \text{mm}$)** | **+$5.5''$ to +$7.0''$ margin** | $\sim 8'-1''$ ($2,463\ \text{mm}$) |

*\* Assumes standard $18''$ trailer chassis ground clearance. Notice that Travel Mode comfortably fits under standard $7'-0''$ residential garage doors!*

```
                  CAMPING MODE (ELEVATED) HEADROOM CLEARANCE
                  
                      Center Arch Apex: 6' 7" (2,008 mm)
                                 ╭───────╮
              Perimeter Edge:   ╭╯       ╰╮   Perimeter Edge:
              6' 5.5" (1,968 mm)┌┴─────────┴┐  6' 5.5" (1,968 mm)
                               │  Canvas   │
                      ╭────────┤  Bellows  ├────────╮
            1D Curved │        ├───────────┤        │ 1D Curved
             XY Wall  │   ░░   │   ( O )   │   ░░   │ XY Wall
             Shoulder │  Bunks │     █     │ Galley │ Shoulder
                      │        │    /█\    │        │
                      │        │    / \    │        │
                      │        │  6'0" Man │        │
           Floor Deck └────────┴───────────┴────────┘ Floor Deck
                         Y = 0 (Center Aisle)
```

---

## 3. Orthogonal 1D Curvature Intersection Mechanics

The shell adopts **orthogonal single-axis developable curvature ($K = 0$)**:

1. **$XY$ Planform Boat-Tail Profile** (Vertical Rulings in $Z$):
   - $W_{\text{nose}} = 1,300\ \text{mm} \rightarrow W_{\text{shoulder}} = 1,981\ \text{mm} \rightarrow W_{\text{mid}} = 1,750\ \text{mm} \rightarrow W_{\text{rear}} = 1,520\ \text{mm}$.
   - Scored with **vertical parallel kerfs** ($50.8\ \text{mm}$ / $2.0''$ pitch).
2. **$XZ$ Elevation Aerodynamic Teardrop Profile** (Lateral Rulings in $Y$):
   - $H_{\text{nose}} = 900\ \text{mm} \rightarrow H_{\text{brow}} = 1,350\ \text{mm} \rightarrow H_{\text{apex}} = 1,500\ \text{mm} \rightarrow H_{\text{transom}} = 850\ \text{mm}$.
   - Scored with **transverse parallel kerfs** ($48\text{--}95\ \text{mm}$ pitch).
3. **Compound 3D Intersection Shoulder**:
   - The intersection of the two orthogonal cylinders produces a natural compound 3D shoulder seam at $Y = \pm 533.5\ \text{mm}$ without requiring compound double-curvature bending on individual sheets.

---

## 4. Multi-Buck Fabrication Suite Specifications

Generated programmatically by [`projects/foam-camper/fabrication/build_bucks.py`](fabrication/build_bucks.py):

| Fabrication Buck | 3D CAD Model | Construction Material | Component Breakdown | Assembled Mass | Primary Shop Role |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Master Assembly Buck** | [`camper_assembly_buck.FCStd`](fabrication/camper_assembly_buck.FCStd) | 3/4" CDX Plywood (`Wood-PlywoodSheathing`) | 5 Bulkhead Ribs + 2 Shoulder Stringers ($Y = \pm 533.5\ \text{mm}$) | **$134.3\ \text{lbs}$ ($60.9\ \text{kg}$)** | Chassis assembly, joint bonding, walk-through door extraction |
| **Pop-Up Roof Canopy Buck** | [`roof_canopy_buck.FCStd`](fabrication/roof_canopy_buck.FCStd) | 3/4" CDX Plywood (`Wood-PlywoodSheathing`) | 3 Arched Profile Formers + 4 Interlocking Cross-Ties | **$187.3\ \text{lbs}$ ($84.9\ \text{kg}$)** | Bench-top forming & gluing of $42'' \times 106''$ 1D arched canopy |
| **Side Wall Bending Jig** | [`side_wall_buck.FCStd`](fabrication/side_wall_buck.FCStd) | 3/4" Plywood + 2x4 Softwood (`Wood-SoftwoodPine`) | Curved Sole Plate + 6 Vertical Clamp Posts | **$46.6\ \text{lbs}$ ($21.1\ \text{kg}$)** | Shop floor pre-curving of vertical-kerfed 2" XPS side walls |

---

## 5. Weight, Volume & Bill of Materials

| Subassembly / Element | Material | Density | Net Volume | Weight (lbs / kg) |
| :--- | :--- | :---: | :---: | :---: |
| **Port Side Wall & Shoulder** | 2.0" XPS Foam | $32\ \text{kg/m}^3$ | $0.58\ \text{m}^3$ | $40.9\ \text{lbs}$ ($18.6\ \text{kg}$) |
| **Starboard Side Wall & Shoulder** | 2.0" XPS Foam | $32\ \text{kg/m}^3$ | $0.58\ \text{m}^3$ | $40.9\ \text{lbs}$ ($18.6\ \text{kg}$) |
| **Pop-Up Roof Canopy** | 2.0" XPS Foam | $32\ \text{kg/m}^3$ | $0.48\ \text{m}^3$ | $33.9\ \text{lbs}$ ($15.4\ \text{kg}$) |
| **Front Bulkhead (with Door)** | 2.0" XPS Foam | $32\ \text{kg/m}^3$ | $0.11\ \text{m}^3$ | $7.8\ \text{lbs}$ ($3.5\ \text{kg}$) |
| **Rear Transom (with Window)** | 2.0" XPS Foam | $32\ \text{kg/m}^3$ | $0.15\ \text{m}^3$ | $10.6\ \text{lbs}$ ($4.8\ \text{kg}$) |
| **TOTAL UNCLAD FOAM SHELL** | — | — | **$1.90\ \text{m}^3$** | **$\sim 134.1\ \text{lbs}$ ($60.8\ \text{kg}$)** |
| **PMF Skin (Canvas + Titebond II)** | 10 oz Cotton + Glue | — | — | $\sim 80.0\ \text{lbs}$ ($36.3\ \text{kg}$) |
| **FINISHED MONOCOQUE ENVELOPE**| Composite Foam Core | — | — | **$\sim 214.1\ \text{lbs}$ ($97.1\ \text{kg}$)** |
