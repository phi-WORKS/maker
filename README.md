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
│  - Physical Test & Fit    │      │  - Git-Native Tagged Releases │
└───────────────────────────┘      └───────────────────────────────┘
```

### 2. Intelligent Work Partitioning & Component Library
Real-world physical assemblies are built from reusable commercial tools, standard hardware, and custom lumber/metal fabrications:
- **Commercial & Fabricated Components (`components/`)**: Discrete items such as torch burner nozzles, handle control cockpits, propane cylinders, bottle cages, steel wheels, and tool attachments are modeled as independent, reusable 3D CAD modules in `components/`.
- **Physical Assembly Projects (`projects/`)**: Complete physical designs (e.g. `kombi-kaddy`, `road-roaster`) import these pre-built components and structure frames around them.

### 3. Living Requirements Lifecycle & Git-Native Versioning
Physical design iterations follow Semantic Versioning (`vMAJOR.MINOR.PATCH`) paired with standard Lifecycle Status Badges (`🟡 IN PROGRESS`, `🔵 FABRICATION READY`, `🟢 BUILT & VERIFIED`, `📦 SUPERSEDED`).
- **Git-Native History**: Historical CAD model iterations are managed natively in Git history via tags (`v0.0.0`, `v0.1.0`...).
- **Visual Transformation Changelogs**: `projects/<project>/CHANGELOG.md` and `projects/<project>/changelog/` track the visual story of design evolution with historical thumbnails.

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
├── src/                      # Primary Python library source (phi_works_maker)
│
├── components/               # Standalone Reusable Commercial Tools & Hardware Library
│   ├── torch_control_handle/ # Ergonomic Squeeze Cockpit & Valve module & 3D model
│   ├── torch_burner_head/    # 500k BTU Venturi Burner Nozzle module & 3D model
│   ├── propane_cylinder_1lb/ # 1 lb Propane Cylinder module & 3D model
│   ├── propane_harness/      # Quick-release bottle harness module & 3D model
│   ├── steel_caster_wheel/   # 4.0" Solid Steel Wheel module & 3D model
│   └── torch_hf91037/        # Harbor Freight #91037 full wand module & reference photos
│
└── projects/                 # Physical Projects & Master Assemblies
    ├── kombi-kaddy/          # STIHL Kombi Attachment Kaddy (Master active product & changelog)
    └── road-roaster/         # Directional Weed Shock Sled (Master active product & changelog)
```

---

## Physical Projects

### 1. [Road Roaster](projects/road-roaster/README.md)
*Directional Upright-Vacuum Thermal Weed Shock Sled*

| Project Master Render | Quick Specs & Master Links |
| :---: | :--- |
| ![Road Roaster Render](projects/road-roaster/road-roaster_iso.png) | • **Application**: Non-chemical gravel driveway weed management via thermal shock.<br>• **Active Master**: [**v0.6.0**](projects/road-roaster/) 🟡 **`[IN PROGRESS]`**<br>• 📐 [**SPECIFICATION.md**](projects/road-roaster/SPECIFICATION.md)<br>• 📜 [**CHANGELOG.md**](projects/road-roaster/CHANGELOG.md)<br>• 🛠️ [**build.py**](projects/road-roaster/build.py)<br>• 📦 [**road-roaster.FCStd**](projects/road-roaster/road-roaster.FCStd) |

### 2. [Kombi Kaddy](projects/kombi-kaddy/README.md)
*Mobile STIHL KombiSystem Attachment Rack*

| Project Master Render | Quick Specs & Master Links |
| :---: | :--- |
| ![Kombi Kaddy Render](projects/kombi-kaddy/caddy_iso.png) | • **Application**: Heavy-duty mobile 2x4 wooden rack for STIHL KombiSystem storage.<br>• **Active Master**: [**v0.9.0**](projects/kombi-kaddy/) 🟡 **`[IN PROGRESS]`**<br>• 📐 [**SPECIFICATION.md**](projects/kombi-kaddy/SPECIFICATION.md)<br>• 📜 [**CHANGELOG.md**](projects/kombi-kaddy/CHANGELOG.md)<br>• 🛠️ [**build.py**](projects/kombi-kaddy/build.py)<br>• 📦 [**caddy.FCStd**](projects/kombi-kaddy/caddy.FCStd) |

---

## Component Libraries

### 1. [Torch Control Handle Cockpit](components/torch_control_handle/README.md)

| Component Render | Specifications & Links |
| :---: | :--- |
| ![Torch Handle Render](components/torch_control_handle/torch_control_handle_iso.png) | • **Application**: Handle-mounted brass valve, squeeze boost lever & piezo spark igniter.<br>• 🛠️ [**`build.py`**](components/torch_control_handle/build.py)<br>• 📦 [**`torch_control_handle.FCStd`**](components/torch_control_handle/torch_control_handle.FCStd) |

### 2. [500,000 BTU Torch Burner Head](components/torch_burner_head/README.md)

| Component Render | Specifications & Links |
| :---: | :--- |
| ![Burner Head Render](components/torch_burner_head/torch_burner_head_iso.png) | • **Application**: Chassis-mounted 2.5" combustion bell, venturi cone & spark electrode.<br>• 🛠️ [**`build.py`**](components/torch_burner_head/build.py)<br>• 📦 [**`torch_burner_head.FCStd`**](components/torch_burner_head/torch_burner_head.FCStd) |

### 3. [4.0" Solid Steel Wheel](components/steel_caster_wheel/README.md)

| Component Render | Specifications & Links |
| :---: | :--- |
| ![Steel Wheel Render](components/steel_caster_wheel/steel_caster_wheel_iso.png) | • **Application**: Solid machined cast steel wheel and 1/2" Grade 5 axle hardware.<br>• 🛠️ [**`build.py`**](components/steel_caster_wheel/build.py)<br>• 📦 [**`steel_caster_wheel.FCStd`**](components/steel_caster_wheel/steel_caster_wheel.FCStd) |

### 4. [1 lb Propane Bottle Harness](components/propane_harness/README.md)

| Component Render | Specifications & Links |
| :---: | :--- |
| ![Propane Harness Render](components/propane_harness/propane_harness_iso.png) | • **Application**: Quick-release steel bottle cage for 1 lb propane canisters.<br>• 🛠️ [**`build.py`**](components/propane_harness/build.py)<br>• 📦 [**`propane_harness.FCStd`**](components/propane_harness/propane_harness.FCStd) |

---

## FreeCAD Execution Commands

```bash
# Build Kombi Kaddy Master Model
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/kombi-kaddy/build.py'; exec(open(__file__).read())"

# Build Road Roaster Master Model
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/road-roaster/build.py'; exec(open(__file__).read())"
```
