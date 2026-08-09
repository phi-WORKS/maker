# Maker: AI-Augmented Physical Design & Fabrication Framework

---

> *"By 'augmenting human intellect' we mean increasing the capability of a man to approach a complex problem situation, to gain comprehension to suit his particular needs, and to derive solutions to problems... We envision a future where an architect collaborates interactively with a machine to design physical structures—manipulating representations, testing constraints, and realizing ideas in real time."*  
> — **Douglas Engelbart**, *Augmenting Human Intellect: A Conceptual Framework* (1962)

---

## Overview & Vision

**Maker** is a conceptual framework and practical workbench for **AI-Augmented Physical Fabrication and Design**. It realizes Douglas Engelbart's 1962 vision by pairing human design intent, physical fabrication experience, and practical shop constraints with AI-agentic coding, FreeCAD 3D parametric modeling, cut list generation, and automated documentation.

Rather than expecting an AI agent to generate complex physical objects out of whole cloth, **Maker** establishes an intelligent, collaborative pair-designing loop:
- **Human Partner**: Provides domain knowledge, physical requirements, ergonomic intuition, freehand sketches, material availability, and shop fabrication feedback.
- **AI Agent**: Translates prompts and field notes into formal parametric CAD code, enforces vector math safety rules, breaks assemblies into modular component libraries, generates exact cut lists / BOMs, and maintains version control integrity.

---

## Core Operating Principles

### 1. The Human-AI Collaborative Loop
The design and fabrication process follows a structured, evolutionary cycle:
```
┌───────────────────────────┐      ┌───────────────────────────────┐
│     Human Fabricator      │      │        AI Coding Agent        │
│  - Physical Intent & Goal │ ────►│  - Requirements Synthesis     │
│  - Hand Sketches & Specs  │      │  - Standalone Component Mod.  │
│  - Shop Tooling & Feedback│ ◄────│  - FreeCAD Parametric Code    │
└───────────────────────────┘      └───────────────────────────────┘
              │                                    │
              ▼                                    ▼
┌───────────────────────────┐      ┌───────────────────────────────┐
│     Shop Fabrication      │      │   Living Project Docs & Git   │
│  - Table Saw / Weld Prep  │      │  - REQUIREMENTS.md & CUT_LIST │
│  - Physical Test & Fit    │      │  - Version Folders (v01..vXX) │
└───────────────────────────┘      └───────────────────────────────┘
```

### 2. Intelligent Work Partitioning & Component Library
Real-world physical assemblies are built from reusable commercial tools, standard hardware, and custom lumber/metal fabrications:
- **Commercial & Purchased Tools (`components/`)**: Items such as the Harbor Freight #91037 Propane Torch, STIHL Kombi tool attachments, fixed caster wheels, and clevis hitches are modeled once as standalone, independent 3D modules in `components/`. Once modeled, they become permanent, reusable building blocks for any host assembly.
- **Physical Assembly Projects (`projects/`)**: Complete physical designs (e.g. `caddy`, `flame-weeding-sled`) import these component modules and structure lumber/metal frames around them.

### 3. Practical DIY Shop Focus
**Maker** prioritizes accessible, real-world shop machinery that fabricators actually own:
- **Primary Tooling**: Table saws, band saws, miter saws, angle grinders with cut-off wheels, flux-core MIG welders, drill presses, and basic hand tools.
- **Extensible Pathway**: Designed for seamless future integration with 3D printers, laser cutters, CNC routers, and plasma tables.

### 4. Living Requirements Lifecycle (`REQUIREMENTS.md`)
Requirements are not static one-time prompts. Each project maintains:
- **`projects/<project>/REQUIREMENTS.md`**: Master project vision, constraints, and target specifications.
- **`projects/<project>/vXX/REQUIREMENTS.md`**: Iteration-specific requirements, design trade-offs, and delta refinements.

### 5. Git Feature Branching Workflow
All feature development, version iterations, and refactors are performed on dedicated Git feature branches (`feature/<name>` or `version/<name>`) before being tested, documented, and merged into `main`.

---

## Directory Architecture

```
/home/phi/PROJECTS/phi-WORKS/maker/
├── README.md                 # Master framework vision, philosophy & workspace index
├── CHANGELOG.md              # Master repository changelog & release history
├── WORKFLOW.md               # Operating guidelines, CAD best practices & Git branching rules
├── GEMINI.md                 # Agent context & operating manual for Gemini CLI
├── ROADMAP.md                # Component library roadmap & physical project goals
├── pyproject.toml            # Python package metadata & build settings
│
├── components/               # Standalone Reusable Commercial Tools & Hardware Library
│   ├── torch_hf91037/        # Harbor Freight #91037 Propane Torch module & 3D model
│   └── kombi_tools/          # STIHL Kombi tool attachments & trimmer 3D models
│
├── projects/                 # Physical Projects & Master Assemblies
│   ├── caddy/                # STIHL Kombi Attachment Caddy (v01..v10 master)
│   └── flame-weeding-sled/   # Towable Flame Weeding Sled (v01..v04 master)
│
└── templates/                # Starter boilerplates for new components & projects
    ├── component_template.py # Boilerplate template for new CAD component modules
    └── project_template.py   # Boilerplate template for new physical CAD projects
```

---

## Current Active Projects

### 1. [Towable Flame Weeding Sled](projects/flame-weeding-sled/README.md)
- **Application**: Gravel driveway weed suppression via targeted thermal shock ($150^\circ\text{F}$–$180^\circ\text{F}$).
- **Torch Unit**: [Harbor Freight Propane Torch #91037](components/torch_hf91037/).
- **Features**: 14-gauge mild steel pyramidal hood ($18'' \times 18''$), $1.5'' \times 12.0''$ rear exhaust vent, 5 ft rigid forward tow bar with $20^\circ$ drop-stop tab, forward-leaning torch handle ergonomics, and FreeCAD subassembly tree grouping (v04).
- **Master Directory**: [`projects/flame-weeding-sled/v04/`](projects/flame-weeding-sled/v04/)

### 2. [STIHL Kombi Attachment Caddy](projects/caddy/README.md)
- **Application**: Heavy-duty 2x4 mobile storage rack for STIHL KombiSystem powerhead and attachments.
- **Features**: Parametric VarSet geometry, 24" post stud alignment, 36" cantilever rail overhangs, 1x4 deck slats, 5" hand-truck wheels, and self-contained version folders (`v01`–`v10`).
- **Master Directory**: [`projects/caddy/v10/`](projects/caddy/v10/)

---

## Quick Start & FreeCAD Build Execution

To build the active master model of any project directly in FreeCAD headless mode:

```bash
# Build Caddy Version 10 Master Model
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/build.py'; exec(open(__file__).read())"

# Build Flame Weeding Sled Version 04 Master Model
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v04/build.py'; exec(open(__file__).read())"
```
