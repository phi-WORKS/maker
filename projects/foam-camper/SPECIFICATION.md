# Compact Foam Camper - Technical Specification

> **Physical Dimensions, 1D Curvature Mechanics, Modular Assembly & Ergonomics**  
> *Project Version: v0.2.0 (Active Master)*

---

## 1. Master Envelope & Parametric VarSet

The model is driven parametrically by FreeCAD's native `App::VarSet` (`Vars`) container inside `foam-camper.FCStd`:

| Parameter Name | Metric (mm) | Imperial | Description |
| :--- | :---: | :---: | :--- |
| **`Bed_Length`** | $3,658.0\ \text{mm}$ | $12'-0''$ ($144.0''$) | Overall camper body length along trailer bed |
| **`Bed_Width`** | $1,981.0\ \text{mm}$ | $6'-6''$ ($78.0''$) | Maximum outer width at lower plinth |
| **`Wall_Height`** | $1,422.0\ \text{mm}$ | $4'-8''$ ($56.0''$) | Closed shoulder height / side wall top shelf |
| **`Apex_Height`** | $1,500.0\ \text{mm}$ | $4'-11''$ ($59.0''$) | Closed exterior apex height above floor |
| **`Foam_Thickness`** | $50.8\ \text{mm}$ | $2.0''$ | Commercial Extruded Polystyrene (XPS) rigid foam |
| **`PopUp_Width`** | $1,067.0\ \text{mm}$ | $42.0''$ ($3'-6''$) | Center pop-top channel width |
| **`PopUp_Length`** | $2,600.0\ \text{mm}$ | $102.4''$ ($8'-6.4''$) | Pop-top standing canopy longitudinal span |
| **`PopUp_Lift`** | **$508.0\ \text{mm}$** | **$20.0''$** | Parametric vertical stroke (0 mm travel, 508 mm camp) |
| **`Crown_Rise`** | $90.0\ \text{mm}$ | $3.5''$ | Transverse arch crown rise at center apex ($Y = 0$) |
| **`Door_Width`** | $610.0\ \text{mm}$ | $24.0''$ ($2'-0''$) | Front walk-through entrance doorway |
| **`Door_Height`** | $1,270.0\ \text{mm}$ | $50.0''$ ($4'-2''$) | Lower rigid front door threshold |

---

## 2. Ergonomics & Interior Headroom Comparison

| Operational Mode | Pop-Up Stroke | Perimeter Headroom | Center Apex Headroom | 6'0" Person Clearance | Exterior Height on Trailer* |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Travel Mode (Closed)** | $0.0\ \text{mm}$ | $4'-8''$ ($1,422\ \text{mm}$) | $4'-11''$ ($1,500\ \text{mm}$) | Seated / Berth Mode | **$\sim 6'-5''$ ($1,955\ \text{mm}$)** |
| **Camping Mode (Elevated)** | **$508.0\ \text{mm}$ ($20''$)** | **$6'-4''$ ($1,930\ \text{mm}$)** | **$6'-7.5''$ ($2,020\ \text{mm}$)** | **+$4.0''$ to +$7.5''$ margin** | $\sim 8'-1''$ ($2,463\ \text{mm}$) |

*\* Assumes standard $18''$ trailer chassis ground clearance. Notice that Travel Mode comfortably fits under standard $7'-0''$ residential garage doors!*

```
                  CAMPING MODE (ELEVATED) HEADROOM CLEARANCE
                  
                      Center Arch Apex: 6' 7.5" (2,020 mm)
                                 ╭───────╮
              Perimeter Edge:   ╭╯       ╰╮   Perimeter Edge:
              6' 4" (1,930 mm) ┌┴─────────┴┐  6' 4" (1,930 mm)
                              │  Canvas   │
                     ╭────────┤  Skirt    ├────────╮
           1D Curved │        ├───────────┤        │ 1D Curved
          Tumblehome │   ░░   │   ( O )   │   ░░   │ Tumblehome
           Shoulder  │  Bunks │     █     │ Galley │ Shoulder
                     │        │    /█\    │        │
                     │        │    / \    │        │
                     │        │  6'0" Man │        │
          Floor Deck └────────┴───────────┴────────┘ Floor Deck
                         Y = 0 (Center Aisle)
```

---

## 3. 1D Single-Axis Transverse Curving Strategy

The v0.2.0 shell adopts **1D transverse developable curvature ($K = 0$)**, matching the organic cross-section from the fabrication egg-crate buck (`projects/foam-camper/fabrication/`):

1. **Continuous Transverse Spline**:
   - Vertical lower plinth ($Z = 0$ to $650\ \text{mm}$ at $Y = \pm 990.5\ \text{mm}$).
   - Inward tumblehome curve ($Z = 650$ to $1,320\ \text{mm}$), narrowing to $Y = \pm 832\ \text{mm}$ ($84\%$ beam).
   - Rounded shoulder roll curving into the roof shelf at $Z = 1,420\ \text{mm}$.
   - Transverse arched crown spanning the center pop-up opening with $R \approx 1,800\ \text{mm}$.
2. **Fabrication Simplicity**:
   - All kerf cuts across $4' \times 8'$ XPS sheets are **straight and parallel to the longitudinal X-axis**.
   - No waffle kerfing, no hand-rasping, and zero compound stretching.

---

## 4. Modular Subassembly Breakdown

The CAD model is organized into independent `App::DocumentObjectGroup` modules:

1. **`Left_Side_Frame` (Port)**:
   - 1D curved XPS foam side wall + fixed roof shoulder shelf ($18''$ wide) over port bunks.
   - $900\ \text{mm} \times 450\ \text{mm}$ acrylic picture window cutout.
2. **`Right_Side_Frame` (Starboard)**:
   - Symmetrical 1D curved XPS foam side wall + fixed roof shoulder shelf over starboard galley.
   - $900\ \text{mm} \times 450\ \text{mm}$ galley window cutout.
3. **`PopUp_Roof_Frame`**:
   - Center arched canopy ($42'' \times 102.4''$) with $25\ \text{mm}$ weather-overlap lip.
   - Translucent pop-up canvas bellows / weather skirt in camping mode.
   - Parametrically elevated by `Vars.PopUp_Lift`.
4. **`Front_Bulkhead_Frame` (Towing End)**:
   - Aerodynamic front wall with $24''$ center entrance doorway opening onto the trailer tongue.
5. **`Rear_Transom_Frame`**:
   - Rear wall with $900\ \text{mm} \times 450\ \text{mm}$ rear observation window.
6. **`Trailer_Chassis_Ref`**:
   - 12' x 6.5' trailer chassis, A-frame tongue, $600 \times 450\ \text{mm}$ diamond-plate walk platform, and 60/40 axle line.
7. **`Ergonomic_Reference`**:
   - $6'0''$ ($1,828.8\ \text{mm}$) stylized human mannequin standing in the center aisle.
