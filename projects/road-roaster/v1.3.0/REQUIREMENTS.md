# Version 1.3.0 Requirement Refinements — Towable Flame Weeding Sled

## 1. Iteration Objectives

Version 1.3.0 establishes full tree container organization in FreeCAD and refines operator pull ergonomics:
1. **Tree Container Modularization**: Organize the complete FreeCAD model into 4 `App::DocumentObjectGroup` containers (Pyramid Hood & Skids, Overhead Torch Frame, Harbor Freight Torch, Tow Rigging).
2. **Torch Incline Angle**: Angle torch wand 35° forward toward puller so handle squeeze lever and flow valve knob align ergonomically with operator hand position.
3. **Drop-Stop Clevis Rest**: Restrict tow bar drop to 20° minimum angle using welded stop tab on clevis ears.

---

## 2. Requirement Delta & Verification Matrix

| Req ID | Target Requirement | v03 Baseline | v04 Specification | Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| **V04-REQ-1** | **Tree Organization** | Flat object list | 4 Subassembly Part Containers | PASSED in FreeCAD |
| **V04-REQ-2** | **Torch Ergonomics** | 35° rearward inclination | 35° forward inclination leaning toward puller | PASSED in CAD |
| **V04-REQ-3** | **Clevis Drop-Stop** | Loose pin connection | 20° welded stop tab | PASSED in CAD |
| **V04-REQ-4** | **Documentation** | Single README | Full SPEC, CUT_LIST, FAB_GUIDE, BOM suite | PASSED |
