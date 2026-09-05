# Project Physical Materials Library

Welcome to the **Maker Suite Physical Materials Library**. This directory contains project-native FreeCAD 1.0/1.1 material definitions (`.FCMat`) stored directly within the repository for full portability, Git version control, and reproducible fabrication engineering.

---

## 1. Overview & Purpose

In FreeCAD 1.0 and 1.1, materials are defined using modular **YAML** files (`.FCMat`). Each material card binds two primary models:
1. **Physical Model (`Models`)**: Defines physical properties such as `Density` ($\text{kg/m}^3$), enabling exact volumetric mass calculations, center-of-gravity tracking, and engineering simulations.
2. **Appearance Model (`AppearanceModels`)**: Defines visual rendering properties (`BasicRendering`) including `DiffuseColor`, `AmbientColor`, `SpecularColor`, and `Shininess`.

By assigning materials to CAD objects rather than relying on arbitrary RGB color constants in code:
- **Exact Weight Estimation**: Compute the exact weight (in kg and lbs) of individual parts, welded frames, subassemblies, and complete machines.
- **Center of Gravity (CoG)**: Determine balance, tipping thresholds, and caster load distributions.
- **Consistent Visual Language**: Standardize surface finishes (powder coats, bare steels, anodized aluminums, brass) across all CAD models.

---

## 2. Directory Structure

```
materials/
├── README.md               # This documentation
├── metals/                 # Structural metals & alloys
│   ├── Steel-A36.FCMat             # ASTM A36 structural carbon steel (7850 kg/m³)
│   ├── Steel-304Stainless.FCMat    # AISI 304 austenitic stainless steel (8000 kg/m³)
│   ├── Steel-ZincPlated.FCMat      # Zinc-plated hardware & brackets (7850 kg/m³)
│   ├── Aluminum-6061-T6.FCMat      # Structural 6061-T6 aluminum alloy (2700 kg/m³)
│   ├── Brass-C360.FCMat            # C360 free-cutting brass (8500 kg/m³)
│   └── CastIron-Gray.FCMat         # Gray cast iron (7200 kg/m³)
├── polymers/               # Rubbers & plastics
│   ├── Rubber-Solid.FCMat          # Vulcanized solid tire/bumper rubber (1150 kg/m³)
│   ├── Plastic-ABS.FCMat           # Rigid thermoplastic for grips/cases (1040 kg/m³)
│   └── Polyurethane.FCMat          # High-impact wheel core (1200 kg/m³)
└── finishes/               # Coated & treated materials
    ├── PowderCoat-IndustrialRed.FCMat   # Industrial red powder-coated steel (7850 kg/m³)
    └── PowderCoat-SafetyYellow.FCMat    # Safety yellow powder-coated steel (7850 kg/m³)
```

---

## 3. YAML Material Card Specification

Every `.FCMat` file follows the standard FreeCAD 1.1 YAML schema:

```yaml
---
# FreeCAD Material Card
General:
  UUID: "856988e2-8719-47c0-b934-b12aa2052c6f"   # Unique UUIDv4 identifier
  Author: "phi ARCHITECT"
  License: "CC-BY-4.0"
  Name: "Steel-A36"
  Description: "ASTM A36 structural carbon steel (tubing, plate, angle iron, channels)"
  SourceURL: "https://en.wikipedia.org/wiki/A36_steel"

Models:
  Density:
    UUID: '454661e5-265b-4320-8e6f-fcf6223ac3af'  # FreeCAD standard Density model UUID
    Density: "7850 kg/m^3"
  LinearElastic:
    UUID: '7b561d1d-fb9b-44f6-9da9-56a4f74d7536'  # FreeCAD standard LinearElastic UUID
    YoungsModulus: "200000 MPa"
    PoissonRatio: "0.26"
    YieldStrength: "250 MPa"
    UltimateTensileStrength: "400 MPa"

AppearanceModels:
  BasicRendering:
    UUID: 'f006c7e4-35b7-43d5-bbf9-c5d572309e6e'  # FreeCAD standard BasicRendering UUID
    AmbientColor: "(0.22, 0.23, 0.25, 1.0)"
    DiffuseColor: "(0.42, 0.44, 0.48, 1.0)"        # Normalized RGBA values (0.0 - 1.0)
    SpecularColor: "(0.60, 0.60, 0.62, 1.0)"
    Shininess: "0.25"
    Transparency: "0.0"
```

### Standard FreeCAD Model UUIDs
- **Density**: `454661e5-265b-4320-8e6f-fcf6223ac3af`
- **Linear Elastic**: `7b561d1d-fb9b-44f6-9da9-56a4f74d7536`
- **Basic Rendering**: `f006c7e4-35b7-43d5-bbf9-c5d572309e6e`

---

## 4. Python API Usage

All material registration, retrieval, assignment, and weight calculation utilities are provided by `phi_works.maker.materials`:

```python
from phi_works.maker.materials import (
    init_materials,
    get_material,
    apply_material,
    get_mass_properties,
    format_mass_report,
)

# 1. Initialize project library (automatic in build scripts)
init_materials()

# 2. Apply material to a 3D Part object
box = doc.addObject("Part::Box", "FrameMember")
apply_material(box, "Steel-A36")

# 3. Calculate Mass & Center of Gravity for a subassembly or full document
report = get_mass_properties(doc)
print(format_mass_report(report))
```
