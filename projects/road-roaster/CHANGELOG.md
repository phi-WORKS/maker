# Road Roaster — Evolutionary Changelog & Visual History

> **Towable Thermal Weed Shock Sled**  
> *Chronological Design Transformation Log & Release History*

---

## Releases & Transformation Story

### Version 0.4.0 — Onboard Propane Harness & Imported Components
**Status**: 🟡 `[IN PROGRESS]`  
**Date**: 2026-08-13  
**Visual Snapshot**: ![v0.4.0 Snapshot](sled_iso.png)

#### Changes & Milestones
- **Onboard Fuel Bottle Mounting**: Integrated standalone 1 lb Propane Cylinder (`components/propane_cylinder_1lb/`) and quick-slip Propane Bottle Harness (`components/propane_harness/`) onto upper tow bar handle tube.
- **FCStd Component Import**: Refactored `build.py` to consume pre-built `.FCStd` component files directly via `import_component()` helper.
- **High-Pressure Fuel Hose Routing**: Routed flexible gas line from cylinder valve to torch handle control knob.

---

### Version 0.3.0 — Modular Master Container
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.3.0 Snapshot](changelog/v0.3.0_iso.png)

#### Changes & Milestones
- **Modular Subassemblies**: Organized 3D model into 4 modular FreeCAD `App::DocumentObjectGroup` containers (`Flame_Sled_Pyramid_Hood`, `Overhead_Support_Frame`, `Rigid_Towbar_Hitch`, `Harbor_Freight_Torch_91037`), establishing clean tree structure and parametric VarSet (`dims`) control.

---

### Version 0.2.0 — Ergonomic Forward Lean
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.2.0 Snapshot](changelog/v0.2.0_iso.png)

#### Changes & Milestones
- **Torch Re-Angling**: Re-angled torch handle wand 180° forward leaning toward the operator pulling at the front, putting the blue handle, flow knob, and piezo igniter button within comfortable walking reach.

---

### Version 0.1.0 — Mechanical Integration
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.1.0 Snapshot](changelog/v0.1.0_iso.png)

#### Changes & Milestones
- **Frame & Tow Bar Integration**: Integrated overhead steel bridge mounting frame, Harbor Freight #91037 propane torch module, 2.0" vertical skirts, and 5 ft rigid square tube tow bar with 20° drop-stop rest tab.

---

### Version 0.0.0 — Baseline Prototype
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.0.0 Snapshot](changelog/v0.0.0_iso.png)

#### Changes & Milestones
- **Pyramid Hood Geometry**: Initial $18'' \times 18''$ closed pyramid hood geometry, 14-gauge sheet metal templates, and dual $1.5'' \times 3/16''$ flat bar skid runners with 30° turned-up tips.
