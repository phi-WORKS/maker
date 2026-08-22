# Maker Strategic Roadmap

This document outlines upcoming development goals for component library expansion, sketch inflow integration, and physical maker projects.

---

## 🎯 Component Library Development Roadmap

- [x] **Harbor Freight #91037 Propane Torch**: Detailed CAD component model with insertion origin $(0,0,0)$, flame direction vector, blue handle, brass flow valve, and piezo igniter (`components/torch_hf91037/`).
- [x] **1 lb Propane Cylinder & Bottle Harness**: Standard 1 lb canister and quick-release steel mounting cage (`components/propane_cylinder_1lb/`, `components/propane_harness/`).
- [x] **4.0" Heavy-Duty Steel Caster Wheel**: Heat-resistant solid machined steel wheel and mounting yoke for high-heat equipment (`components/steel_caster_wheel/`).
- [ ] **STIHL Kombi Tool Attachments**:
  - [ ] Power Head Engine Unit
  - [x] Straight Shaft String Trimmer (`components/kombi_tools/`)
  - [ ] Edger Attachment
  - [ ] Pole Pruner Chainsaw
  - [ ] Hedge Trimmer
  - [ ] Rubber Paddle Sweeper
- [ ] **Hardware & Rigging Components**:
  - [ ] Quick-Release Snap-Latch Linkages & Pivot Hinges
  - [ ] Standard Pneumatic & Solid Rubber Wheels

---

## 🛠️ Physical Project Roadmap

- [x] **Road Roaster (v0.5.0 Master)**: Upright vacuum / hand-truck tilt-back architecture, dual hinge pivot points, 4" heavy-duty steel wheels, 48" U-handle frame, foot-release tilt latch, and onboard propane harness (`projects/road-roaster/`).
- [x] **Kombi Kaddy (v0.9.0 Master)**: Modular storage rack and transport caddy for STIHL KombiSystem tools (`projects/kombi-kaddy/`).
- [ ] **Physical Cut Lists & Welding Jigs**: Parametric bill of materials and fabrication cut lists for shop assembly.

---

## 🎨 Sketch Inflow & Feedback Loop

- [ ] Support freehand sketch ingestion: Place user sketches and dimension photos in `sketches/`.
- [ ] Extract key dimensions from user sketches directly into parametric `App::VarSet` parameters.
- [ ] Generate focused component snapshot previews for fast visual verification and alignment.
