# Maker Collaboration & Modular CAD Workflow Guide

This document defines the standard operating workflow and best practices for physical DIY design, CAD modeling, component modularization, and fabrication documentation within the **`maker`** suite (`/home/phi/PROJECTS/phi-WORKS/maker`).

---

## 1. Core Operating Principles

### 1.1 Commercial Tools & Purchased Component Isolation
Avoid building large, monolithic CAD scripts where real-world tools, burners, or commercial hardware are re-invented inside the main assembly script.
- **Isolate Commercial Tools & Components**: Model purchased tools (e.g., Harbor Freight #91037 Propane Torch, STIHL Kombi tool attachments, standard wheels, clevis hitches) as standalone 3D modules in `components/` (e.g., `components/torch_hf91037/`, `components/kombi_tools/`).
- **Clean Insertion Origins**: Component models must define an explicit insertion origin $(0,0,0)$ and orientation vector so they can be imported and placed cleanly inside any host assembly document.
- **Fast Iteration**: Build and verify individual components in isolation before incorporating them into host projects.

### 1.2 Hand Sketch & Dimension Inflow
Fabricators and CAD designers collaborate using freehand sketches, dimensioned field notes, and photographs:
- Place raw hand sketches, field notes, and photo references into `sketches/` within the relevant project or component folder.
- Translate key parameters directly into FreeCAD `App::VarSet` (e.g., `dims`) for full parametric control.

### 1.3 FreeCAD Tree View Subassembly Containers
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

### 1.4 Self-Contained Version Subdirectories (`v01/`, `v02/`, ..., `vXX/`)
- Save each major design iteration inside a dedicated version subdirectory: `projects/<project>/v01/`, `v02/`, ..., `v10/`.
- Each version folder is **self-contained**, housing its own `build.py` script, FreeCAD model (`caddy_v10.FCStd`), render images, `CUT_LIST.md`, and `SPECIFICATION.md`.
- The project root directory houses the master `README.md` (which details master project objectives and indexes all version iterations) and a copy of the active master CAD model (`caddy.FCStd`).
- **Dynamic Path Resolution**: Build scripts resolve output directories dynamically relative to `__file__` (never hardcode local workspace paths).
- **Lightweight Builds**: Do not generate STEP models during routine iterations; generate STEP exports only when explicitly requested for external manufacturing.

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
2. **`SPECIFICATION.md`**: Engineering specifications, physics/operating principles, geometric specs, and mechanical kinematics.
3. **`CUT_LIST.md`**: DIY cut list optimized for angle grinder cut-off wheels and flux-core MIG welding, flat sheet metal panel templates, and cut diagrams.
4. **`FABRICATION_GUIDE.md`**: Step-by-step assembly guide, weld sequence, frame fitting, and safety checklist.
5. **`BOM.md`**: Itemized Bill of Materials with specs, quantities, weights, and sourcing sources.
