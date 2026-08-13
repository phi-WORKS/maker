# Maker Strategic Roadmap

This document outlines upcoming development goals for component library expansion, sketch inflow integration, and physical maker projects.

---

## 🎯 Component Library Development Roadmap

- [x] **Harbor Freight #91037 Propane Torch**: Detailed CAD component model with insertion origin $(0,0,0)$, flame direction vector, blue handle, brass flow valve, and piezo igniter (`components/torch_hf91037.py`).
- [ ] **STIHL Kombi Tool Attachments**:
  - [ ] Power Head Engine Unit
  - [ ] Straight Shaft String Trimmer
  - [ ] Edger Attachment
  - [ ] Pole Pruner Chainsaw
  - [ ] Hedge Trimmer
  - [ ] Rubber Paddle Sweeper
- [ ] **Hardware & Rigging Components**:
  - [ ] Single-Axis Clevis Hitch Bracket & 20° Drop-Stop Tab (`components/clevis_hitch.py`)
  - [ ] Dual Steel Skid Runners (`components/skid_runner.py`)
  - [ ] 1 lb Disposable/Refillable Propane Cylinder (`components/propane_tank.py`)
  - [ ] Standard Pneumatic & Solid Rubber Wheels

---

## 🛠️ Physical Project Roadmap

- [x] **Road Roaster (v0.4.0 Master)**: Enclosed 14-ga mild steel pyramidal hood, rearward flame orientation, forward tow bar, forward-leaning torch handle, and FreeCAD subassembly tree grouping (`projects/road-roaster/`).
- [x] **Kombi Kaddy (v0.9.0 Master)**: Modular storage rack and transport caddy for STIHL KombiSystem tools (`projects/kombi-kaddy/`).
- [ ] **Component Refinement**: Refine project assembly scripts (`road-roaster` and `kombi-kaddy`) to import standalone components directly from `components/`.

---

## 🎨 Sketch Inflow & Feedback Loop

- [ ] Support freehand sketch ingestion: Place user sketches and dimension photos in `sketches/`.
- [ ] Extract key dimensions from user sketches directly into parametric `App::VarSet` parameters.
- [ ] Generate focused component snapshot previews for fast visual verification and alignment.
