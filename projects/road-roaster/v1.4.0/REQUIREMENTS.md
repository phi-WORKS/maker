# Version 1.4.0 Requirement Refinements — Towable Flame Weeding Sled

## 1. Iteration Objectives

Version 1.4.0 transitions the Road Roaster from inline geometry generation to clean modular component imports, refactors the build script into function-level subassemblies, and integrates an onboard 1 lb propane bottle harness:

1. **Propane Cylinder Component Isolation (`components/propane_cylinder_1lb/`)**: Create a standalone reusable 3D CAD component module for 1 lb propane tanks with threaded top brass valve assembly and bottom seat collar.
2. **Propane Bottle Harness Component (`components/propane_harness/`)**: Design a quick-slip bike-cage-style bottle harness with a bottom cup seat, dual curved retention arms, quick-latch strap, and dual tube mounting clamps.
3. **Tow Bar Handle Mounting & Hose Connection**: Securely mount the bottle harness onto the upper tow bar handle tube near the T-grip, seating the propane cylinder within safe reach of the operator and routing a high-pressure extension hose line to the torch wand handle knob.
4. **Build Script Functional Refactoring**: Structurally refactor `v1.4.0/build.py` into dedicated subassembly builder functions (`build_hood_subassembly`, `build_overhead_frame_subassembly`, `build_torch_subassembly`, `build_propane_harness_subassembly`, `build_tow_rigging_subassembly`) that instantiate imported component modules into FreeCAD `App::DocumentObjectGroup` containers.
5. **Complete Documentation Suite**: Deliver complete specification, cut list, fabrication guide, BOM, and master index updates for Version 1.4.0.

---

## 2. Requirement Delta & Verification Matrix

| Req ID | Target Requirement | v1.3.0 Baseline | v1.4.0 Specification | Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| **V05-REQ-1** | **Propane Tank Component** | Inline crude cylinder approximation in build.py | Standalone 3D module `components/propane_cylinder_1lb/` with seat collar | PASSED in FreeCAD |
| **V05-REQ-2** | **Propane Harness Component** | Shoulder strap / floating tank | Standalone quick-slip bike-style cage `components/propane_harness/` | PASSED in FreeCAD |
| **V05-REQ-3** | **Tow Bar Handle Mount** | Unmounted floating tank position | Dual 3/4" square-tube clamp bracket mounted on upper tow bar ($Z \approx 750\text{--}850\text{ mm}$) | PASSED in CAD |
| **V05-REQ-4** | **Functional Script Refactor** | Monolithic `build_v4()` script | Modular builder functions per container (`build_*_subassembly()`) & component imports | PASSED in FreeCAD |
| **V1.4.0-REQ-5** | **Documentation Suite** | v1.3.0 Master Docs | Updated v1.4.0 SPEC, CUT_LIST, FAB_GUIDE, BOM suite & master README | PASSED |
