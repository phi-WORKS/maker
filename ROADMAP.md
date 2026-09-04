# Maker Strategic Roadmap

This document outlines upcoming development goals for component library expansion, sketch inflow integration, and physical maker projects.

---

## 🎯 Component Library Development Roadmap

- [x] **Torch Control Handle Cockpit**: Handle-mounted brass valve manifold, dead-man turbo squeeze boost lever, fluted needle knob, and piezo push-button igniter (`components/torch_control_handle/`).
- [x] **500,000 BTU Burner Head**: Flared steel combustion bell, cast venturi cone with air intake windows, precision brass orifice jet, and ceramic spark electrode (`components/torch_burner_head/`).
- [x] **1 lb Propane Cylinder & Bottle Harness**: Standard 1 lb canister and quick-release steel mounting cage (`components/propane_cylinder_1lb/`, `components/propane_harness/`).
- [x] **4.0" Solid Steel Wheel**: Heat-resistant solid machined steel wheel and 1/2" zinc-plated axle hardware (`components/steel_caster_wheel/`).
- [x] **Commercial 24" x 36" Platform Cart**: Heavy-duty diamond plate deck, 4 rubber corner bumpers, 5" running gear, 29" push handle with dual cross rails (`components/platform_cart_24x36/`).
- [x] **Harbor Freight #91037 COTS Reference Module**: Full wand model and high-res reference photos (`components/torch_hf91037/`).
- [ ] **20 lb Propane Cylinder**: Standard vertical LP tank model with foot ring and collar handle (`components/propane_cylinder_20lb/`).
- [ ] **Front Cantilever 180° Flip Hinge Bracket**: Front-mounted dual-arm pivot bracket with height adjustment.
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

- [x] **Road Roaster Hand Truck (v0.7.0 Master)**: Ultra-compact directional ceramic infrared weed shock sled with common-wheel-axis triangular suspension on restored vintage hand truck chassis (`projects/road-roaster/`).
- [x] **Road Roaster 4 (v0.1.0 Master)**: Heavy-duty 4-wheel commercial platform cart foundation with 5" running gear, 29" handle, 20 lb propane capacity, and 180° flip cantilevered burner architecture (`projects/road-roaster-4/`).
- [x] **Kombi Kaddy (v0.9.0 Master)**: Modular storage rack and transport caddy for STIHL KombiSystem tools (`projects/kombi-kaddy/`).
- [ ] **Physical Cut Lists & Welding Jigs**: Parametric bill of materials and fabrication cut lists for shop assembly.

---

## 🎨 Sketch Inflow & Feedback Loop

- [ ] Support freehand sketch ingestion: Place user sketches and dimension photos in `sketches/`.
- [ ] Extract key dimensions from user sketches directly into parametric `App::VarSet` parameters.
- [ ] Generate focused component snapshot previews for fast visual verification and alignment.
