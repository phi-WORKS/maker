# Maker Strategic Roadmap

This document outlines upcoming development goals for component library expansion, sketch inflow integration, and physical maker projects.

---

## 🎯 Component Library Development Roadmap

- [x] **Torch Control Handle Cockpit**: Handle-mounted brass valve manifold, dead-man turbo squeeze boost lever, fluted needle knob, and piezo push-button igniter (`components/torch_control_handle/`).
- [x] **500,000 BTU Burner Head**: Flared steel combustion bell, cast venturi cone with air intake windows, precision brass orifice jet, and ceramic spark electrode (`components/torch_burner_head/`).
- [x] **1 lb Propane Cylinder & Bottle Harness**: Standard 1 lb canister and quick-release steel mounting cage (`components/propane_cylinder_1lb/`, `components/propane_harness/`).
- [x] **4.0" Solid Steel Wheel**: Heat-resistant solid machined steel wheel and 1/2" zinc-plated axle hardware (`components/steel_caster_wheel/`).
- [x] **Harbor Freight #91037 COTS Reference Module**: Full wand model and high-res reference photos (`components/torch_hf91037/`).
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

- [x] **Road Roaster (v0.6.0 Master)**: Directional asymmetrical forward-firing hood, rearward-offset apex ($Y_{apex} = +110\text{ mm}$), decomposed handle cockpit with squeeze boost lever, chassis-mounted 500k BTU burner head, flexible LP hose routing, upright vacuum tilt-back frame with 4.0" rear steel wheels (`projects/road-roaster/`).
- [x] **Kombi Kaddy (v0.9.0 Master)**: Modular storage rack and transport caddy for STIHL KombiSystem tools (`projects/kombi-kaddy/`).
- [ ] **Physical Cut Lists & Welding Jigs**: Parametric bill of materials and fabrication cut lists for shop assembly.

---

## 🎨 Sketch Inflow & Feedback Loop

- [ ] Support freehand sketch ingestion: Place user sketches and dimension photos in `sketches/`.
- [ ] Extract key dimensions from user sketches directly into parametric `App::VarSet` parameters.
- [ ] Generate focused component snapshot previews for fast visual verification and alignment.
