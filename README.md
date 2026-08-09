# Maker: DIY Physical Design, CAD Modeling & Fabrication Suite

**Repository**: `phi-WORKS/maker`  
**Namespace**: `phiarchitect` / `phi-WORKS`  
**Location**: `/home/phi/PROJECTS/phi-WORKS/maker`  

---

## Overview

**Maker** is a unified physical design, CAD modeling, and fabrication project workspace. It brings together modular component libraries, physical projects, hand-sketch inflows, versioned FreeCAD parametric models, and step-by-step DIY fabrication documentation under a single repository.

---

## Directory Index

```
/home/phi/PROJECTS/phi-WORKS/maker/
├── README.md                 # Master project suite overview & workspace index
├── WORKFLOW.md               # Maker Collaboration & Modular CAD Best Practices Guide
├── GEMINI.md                 # Agent context & operating manual for Gemini CLI
├── ROADMAP.md                # Component library roadmap & physical project goals
├── pyproject.toml            # Python package metadata & settings
│
├── components/               # Standalone Reusable Commercial Tools & Hardware Modules
│   ├── torch_hf91037/        # Harbor Freight #91037 Propane Torch component module & model
│   └── kombi_tools/          # STIHL Kombi tool attachment & trimmer models
│
├── projects/                 # Physical Projects & Master Assemblies
│   ├── caddy/                # STIHL Kombi Attachment Caddy (v01..v10 master)
│   └── flame-weeding-sled/   # Towable Flame Weeding Sled (v01..v04 master)
│
├── templates/                # Boilerplates for components and projects
│   ├── component_template.py # Boilerplate template for new CAD components
│   └── project_template.py   # Boilerplate template for new physical CAD projects
│
└── sketches/                 # Raw hand sketches, field notes, and photo references
```

---

## Current Active Projects

### 1. [Towable Flame Weeding Sled](projects/flame-weeding-sled/README.md)
- **Application**: Gravel driveway weed suppression via targeted thermal shock ($150^\circ\text{F}$–$180^\circ\text{F}$).
- **Torch Unit**: Harbor Freight Propane Torch with Push-Button Igniter (Item #91037).
- **Features**: 14-gauge mild steel pyramidal hood ($18'' \times 18''$), $1.5'' \times 12.0''$ rear exhaust vent, 5 ft rigid forward tow bar with $20^\circ$ drop-stop tab, forward-leaning torch handle ergonomics, and FreeCAD subassembly tree grouping (v1.4).

### 2. [STIHL Kombi Attachment Caddy](projects/caddy/README.md)
- **Application**: Modular rack and storage caddy for STIHL KombiSystem power head and attachments.
- **Features**: Parametric VarSet geometry, versioned FreeCAD scripts (`v1`–`v10`), visual snapshots, and fabrication guides.

---

## Key Workflows & Guidelines

Refer to [**WORKFLOW.md**](WORKFLOW.md) for detailed guidelines on:
- **Component-First Modeling**: Building standalone tools in `components/` before importing into host assemblies.
- **Hand Sketch Inflow**: Ingesting freehand sketches and measurement photos into `sketches/`.
- **Tree View Subassemblies**: Grouping FreeCAD objects using `App::DocumentObjectGroup` or `App::Part`.
- **Non-Mutating Vector Math**: Preventing coordinate compounding bugs in FreeCAD Python API.
- **Fabrication Documentation Standard**: Maintaining `README.md`, `SPECIFICATION.md`, `CUT_LIST.md`, `FABRICATION_GUIDE.md`, and `BOM.md`.
