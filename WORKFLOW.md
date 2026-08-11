# Maker Collaboration & Modular CAD Workflow Guide

This document defines the standard operating workflow and best practices for physical DIY design, CAD modeling, component modularization, Git version control, and fabrication documentation within the **`maker`** suite (`/home/phi/PROJECTS/phi-WORKS/maker`).

---

## 1. Core Operating Principles

### 1.1 The Engelbart AI-Human Pairing Model
Physical design in **Maker** is a collaborative pair-designing process between human domain expertise and AI agentic execution:
- **Human Partner**: Communicates physical intent, target constraints, ergonomics, shop tooling availability, and verification feedback.
- **AI Agent**: Translates prompts into FreeCAD parametric Python scripts, maintains modular component libraries, generates exact cut lists / BOMs, and manages Git version control.

### 1.2 Git Feature Branching Workflow
From a given baseline, all new feature developments, version iterations, and refactors must be executed on dedicated Git feature branches:
1. **Branch Naming**: Use `feature/<name>` (e.g. `feature/englebart-framework`) or `version/<project>-vXX` (e.g. `version/caddy-v11`).
2. **Commit Messages**: Write clear, descriptive commit messages summarizing structural or parametric changes.
3. **Verification**: Run headless FreeCAD build checks on the branch before merging into `main`.

### 1.3 Commercial Tools & Purchased Component Isolation
Avoid building large, monolithic CAD scripts where real-world tools, burners, or commercial hardware are re-invented inside the main assembly script.
- **Isolate Commercial Tools & Components**: Model purchased tools (e.g., Harbor Freight #91037 Propane Torch, STIHL Kombi tool attachments, standard wheels, clevis hitches) as standalone 3D modules in `components/` (e.g., `components/torch_hf91037/`, `components/kombi_tools/`).
- **Clean Insertion Origins**: Component models must define an explicit insertion origin $(0,0,0)$ and orientation vector so they can be imported and placed cleanly inside any host assembly document.
- **Fast Iteration**: Build and verify individual components in isolation before incorporating them into host projects.

### 1.4 Hand Sketch & Photo Inflow (`artifacts/`)
Fabricators and CAD designers collaborate using freehand sketches, dimensioned field notes, photo references, and raw specs:
- Place raw hand sketches, field notes, and photo references into an `artifacts/` folder within the relevant project (`projects/<project>/artifacts/` or `projects/<project>/vXX/artifacts/`).
- Translate key parameters directly into FreeCAD `App::VarSet` (e.g., `dims`) for full parametric control.

### 1.5 FreeCAD Tree View Subassembly Containers
Keep the FreeCAD object tree clean and structured:
- Group related parts into subassembly containers using `App::DocumentObjectGroup` or `App::Part`.
- Example Tree Hierarchy:
  ```
  [Project Document]
    ├── dims (App::VarSet)
    ├── 1. Main Hood & Skid Subassembly
    ├── 2. Overhead Torch Mounting Frame
    ├── 3. Harbor Freight #91037 Torch Subassembly
    └── 4. Forward Tow Rigging Subassembly
  ```

### 1.6 Semantic Versioning for Physical CAD & Fabrication (`vMAJOR.MINOR.PATCH`)
Physical design iterations follow **Semantic Versioning** rules adapted for hardware & fabrication:
- **`MAJOR` (`v1.0.0`, `v2.0.0`)**: Major structural, chassis, or architectural overhaul (e.g. frame material migration, fundamental mechanism redesign).
- **`MINOR` (`v1.1.0`, `v1.2.0`)**: Feature addition, component module swap, ergonomic adjustment, or dimensional calibration (e.g. adding swivel casters, extending top clip rails).
- **`PATCH` (`v1.0.1`, `v1.1.1`)**: Cut list tolerance adjustment, CAD script geometry refactor, or documentation fix.

### 1.7 Self-Contained Version Subdirectories & Lifecycle Status Badges
- Save each design iteration inside a dedicated version subdirectory: `projects/<project>/v1.0.0/`, `v1.1.0/`, `v2.0.0/` (or legacy `v01/`..`v10/` mapped to SemVer).
- Each version folder is **self-contained**, housing its own `build.py` script, FreeCAD model (`caddy_v10.FCStd`), render images, `REQUIREMENTS.md`, `CUT_LIST.md`, `SPECIFICATION.md`, `FABRICATION_GUIDE.md`, and `BOM.md`.
- The project root directory houses the master `README.md`, which acts as an **Evolutionary Journey Index** (newest version at the top) logging the human-AI co-design process over time.
- **Lifecycle Status Badges**: Every version listed in project history tables must display a standardized status badge:
  - `🟡 IN PROGRESS (Draft)`: Requirements defined in `REQUIREMENTS.md`; CAD script (`build.py`) or model under active development.
  - `🔵 FABRICATION READY`: CAD model finalized; complete `CUT_LIST.md`, `SPECIFICATION.md`, `FABRICATION_GUIDE.md`, and `BOM.md` compiled for shop fabrication.
  - `🟢 BUILT & VERIFIED`: Fabricated in shop and physically verified in field testing.
  - `📦 SUPERSEDED`: Historical release superseded by a newer verified iteration.
- **Dynamic Path Resolution**: Build scripts resolve output directories dynamically relative to `__file__` (never hardcode local workspace paths).

---

## 2. FreeCAD Scripting & Visual Rendering Rules

### 2.1 Non-Mutating Vector Addition
- **CRITICAL**: In FreeCAD's Python API, `vec.add(other)` mutates `vec` in place.
- **Rule**: ALWAYS use non-mutating vector addition (`v1 + v2`) or construct explicit `FreeCAD.Vector(x, y, z)` objects to prevent coordinate compounding bugs.

### 2.2 Offscreen GUI Camera Snapshot Technique
- Always call `doc.recompute()` BEFORE accessing `FreeCADGui.getDocument(doc.Name).getObject(...)`.
- When framing long apparatuses (like a 60-inch tow bar), temporarily set `Visibility = False` on distant objects during `view.fitAll()`, take the snapshot image, and restore `Visibility = True` immediately after to keep renders close-up and sharp.

---

## 3. Fabrication Documentation Standard

Every physical project within `maker/projects/` must maintain the following documentation suite:

1. **`README.md`**: Project overview, hardware links, system architecture, rendering index, and build instructions.
2. **`REQUIREMENTS.md`**: Master requirements specification, functional requirements table, physical constraints, and version traceability.
3. **`SPECIFICATION.md`**: Engineering specifications, physics/operating principles, geometric specs, and mechanical kinematics.
4. **`CUT_LIST.md`**: DIY cut list optimized for table saws, band saws, angle grinders, and flux-core MIG welding.
5. **`FABRICATION_GUIDE.md`**: Step-by-step assembly guide, weld sequence, frame fitting, and safety checklist.
7. **`CHANGELOG.md`**: Master repository changelog tracking framework releases, project milestones, and version iterations.
