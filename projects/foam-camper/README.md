# Compact Foam Camper

> **Ultralight 12' x 6.5' Towable Rigid Foam Camper Shell - Pop-Top Architecture & Multi-Buck Fabrication Suite**  
> *phi-WORKS Maker Framework (`projects/foam-camper`)*

**Active CAD Model**: [`foam-camper.FCStd`](foam-camper.FCStd)  
**Status**: 🟢 **`[CURRENT / ACTIVE - v0.3.0]`**  
**Master Shop Manual**: 📋 [**`ASSEMBLY.md`**](ASSEMBLY.md)  
**Fabrication & Multi-Buck Suite**: 🔨 [**`fabrication/README.md`**](fabrication/README.md)  
**Evolution History**: 📜 [**`CHANGELOG.md`**](CHANGELOG.md)

| Master Camping Mode (Pop-Up Raised — 6'5.5" Standing Headroom) | Travel / Towing Mode (Pop-Up Closed — Fits 7' Garage) |
| :---: | :---: |
| ![Camping Mode Elevated](foam-camper.png) | ![Travel Mode Closed](foam-camper_travel.png) |
| **Master Assembly Buck (Interlocking Egg-Crate Jig)** | **Assembly Buck Inside Ghost Shell Overlay** |
| ![Master Assembly Buck](fabrication/camper_assembly_buck.png) | ![Buck Inside Ghost Shell](fabrication/camper_assembly_buck_with_shell.png) |

---

## Executive Overview

The **Compact Foam Camper v0.3.0** is an ultralight, towable micro-camper designed for fabrication from $2.0''$ ($50.8\ \text{mm}$) Extruded Polystyrene (XPS) rigid foam boards using **orthogonal 1D single-axis developable curvature**, an **independent modular pop-up roof architecture**, and a **three-tier CAD fabrication buck suite**.

Sized for a standard **12'-0" (3,658 mm) length × 6'-6" (1,981 mm) width** trailer bed, the camper addresses key physical requirements:

1. **Orthogonal 1D Developable Surface Curvature ($K = 0$)**: Side walls curve along the **$XY$ planform plane** (boat-tail curve with vertical rulings in $Z$), while the roof curves along the **$XZ$ elevation plane** (aerodynamic teardrop curve with lateral rulings in $Y$). The two single-axis curved planes intersect to form a natural compound 3D shoulder seam without compound panel bending.
2. **Three-Tier CAD Buck Suite**:
   - **Master Egg-Crate Assembly Buck** ([`fabrication/camper_assembly_buck.FCStd`](fabrication/camper_assembly_buck.FCStd)): 12' × 6.5' interlocking 3/4" CDX plywood frame ($134.3\ \text{lbs}$) mounted to the trailer deck with a 24" walk-through front doorway and dual shoulder stringers at $Y = \pm 533.5\ \text{mm}$.
   - **Pop-Up Roof Canopy Form Buck** ([`fabrication/roof_canopy_buck.FCStd`](fabrication/roof_canopy_buck.FCStd)): Standalone bench jig ($187.3\ \text{lbs}$) with 3 arched profile formers for pre-curving the $42'' \times 106''$ pop-up roof canopy off-trailer.
   - **Side Wall Planform Bending Jig** ([`fabrication/side_wall_buck.FCStd`](fabrication/side_wall_buck.FCStd)): Floor template ($46.6\ \text{lbs}$) with curved sole plate and vertical 2x4 posts for pre-curving the vertically kerfed 2" XPS side walls.
3. **Walk-Through Center Entrance Doorway & Easy Buck Removal**: A $24''$ wide walk-through doorway on the front towing bulkhead provides walk-in access from the trailer tongue platform. Once the monocoque foam shell cures, the temporary egg-crate buck bulkheads are unslotted and slid straight out through the front door!
4. **$6'5.5''$ ($1,968\ \text{mm}$) Interior Standing Headroom**: The center pop-up roof elevates by $20.0''$ ($508\ \text{mm}$) on gas struts, providing ample headroom for a 6-foot person ($+5.5''$ clearance) in the central standing aisle.
5. **Standard 7-Foot Residential Garage Clearance**: In transit mode, the roof drops flush between the side shoulders, keeping total shell height at $4'11''$ ($1,500\ \text{mm}$ above bed) and total trailer height at $\sim 6'5''$ ($1,955\ \text{mm}$), easily clearing standard $7'-0''$ residential garage doors.

---

## Operational Mode Comparison

| Characteristic | Travel / Towing Mode (Closed) | Camping Mode (Popped Up) |
| :--- | :---: | :---: |
| **Model State** | `Vars.PopUp_Lift = 0 mm` | `Vars.PopUp_Lift = 508 mm` ($20.0''$) |
| **Interior Central Headroom** | $4'-9.5''$ ($1,460\ \text{mm}$) (Seated / Lounge) | **$6'-5.5''$ ($1,968\ \text{mm}$) Standing Aisle** |
| **Center Arch Apex Headroom** | $4'-11''$ ($1,500\ \text{mm}$) | **$6'-7''$ ($2,008\ \text{mm}$)** |
| **Overall Shell Height** | $4'-11''$ ($1,500\ \text{mm}$) | $6'-7''$ ($2,008\ \text{mm}$) |
| **Total Height on Trailer** | **$\sim 6'-5''$ ($1,955\ \text{mm}$)** (Garage Ready) | $\sim 8'-1''$ ($2,463\ \text{mm}$) |
| **Aerodynamic Drag** | Low frontal cross-section | High-volume standing headroom |
| **Weather Enclosure** | Hard foam nested perimeter seal | Weatherproof canvas bellows |

---

## Modular Subassembly Breakdown

```
                             MASTER ASSEMBLY GRAPH
                             
                      ┌──────────────────────────────────┐
                      │    foam-camper (Root Assembly)   │
                      └────────────────┬─────────────────┘
                                       │
          ┌───────────────┬────────────┴───┬──────────────┬───────────────┐
          │               │                │              │               │
          ▼               ▼                ▼              ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌─────────────┐ ┌───────────┐   ┌───────────┐
    │ Left Side │   │Right Side │   │Center Pop-Up│ │   Front   │   │   Rear    │
    │   Wall    │   │   Wall    │   │ Roof Frame  │ │ Bulkhead  │   │ Transom   │
    │  (Port)   │   │(Starboard)│   │  (Movable)  │ │(Tongue/Dr)│   │ (Galley)  │
    └───────────┘   └───────────┘   └─────────────┘ └───────────┘   └───────────┘
```

- **`Left_Side_Frame` (Port)**: 1D $XY$ curved XPS foam wall with $900 \times 450\ \text{mm}$ window and shoulder ledge at $Y = +533.5\ \text{mm}$.
- **`Right_Side_Frame` (Starboard)**: Symmetrical 1D $XY$ curved XPS foam wall with $900 \times 450\ \text{mm}$ window and shoulder ledge at $Y = -533.5\ \text{mm}$.
- **`PopUp_Roof_Frame`**: Arched 1D $XZ$ canopy ($42'' \times 106''$) with gas lift struts and weatherproof canvas bellows.
- **`Front_Bulkhead_Frame`**: Towing end wall with $24''$ center entrance doorway opening onto the trailer tongue A-frame platform.
- **`Rear_Transom_Frame`**: Rear vertical bulkhead with panoramic observation window ($800 \times 380\ \text{mm}$).
- **`Trailer_Chassis_Ref`**: Reference 12' × 6.5' trailer chassis with tongue drawbar, walk platform, and 60/40 balance axle line.
- **`Ergonomic_Reference`**: $6'0''$ ($1,828.8\ \text{mm}$) scale human figure standing in the central aisle.

---

## Documentation Index

- 📐 [**`SPECIFICATION.md`**](SPECIFICATION.md): Dimensional specifications, parametric VarSet parameters, station coordinates, and volumetric analysis.
- 📋 [**`ASSEMBLY.md`**](ASSEMBLY.md): **Master Shop Assembly Guide** with step-by-step photos/renders, tool checklist, buck disassembly sequence, and clamping protocol.
- 🔨 [**`fabrication/`**](fabrication/README.md): **Fabrication & Multi-Buck Manual**, automated buck builder script ([`build_bucks.py`](fabrication/build_bucks.py)), and 1D kerf pitch formulas.
- 📜 [**`CHANGELOG.md`**](CHANGELOG.md): Version iteration log and visual milestone history.
- 🛠️ [**`build.py`**](build.py): Parametric FreeCAD 1.1 Python script generating the camper assembly and multi-state snapshot renders.
- 📦 [**`foam-camper.FCStd`**](foam-camper.FCStd): Master 3D CAD project model.

---

## FreeCAD Headless Execution

To re-run the build script, recompute the models, and export all high-resolution snapshot renders:

```bash
# Rebuild Master Camper Shell Assembly & Snapshot Gallery
./scripts/run_freecad.sh projects/foam-camper/build.py

# Rebuild Multi-Buck Fabrication Suite & Assembly Jigs
./scripts/run_freecad.sh projects/foam-camper/fabrication/build_bucks.py
```
