# Road Roaster

> *Towable Thermal Weed Shock Sled*

---

## Utility & Overview

The **Road Roaster** is a heavy-duty, heat-concentrating drag hood pulled ahead of an operator via a 5 ft rigid steel tow bar. Engineered for chemical-free gravel driveway and pathway weed management via thermal shock (150°F–180°F), it mounts a high-output **[Harbor Freight #91037 Propane Torch](../../components/torch_hf91037/)** above an enclosed 14-gauge mild steel pyramidal hood to burst weed cell walls at walking speed while keeping heat safely directed away from the operator.

---

## Evolutionary Version History & Human-AI Design Journey

This project documents the collaborative evolutionary cycle between human shop feedback and AI-agentic parametric CAD modeling across 4 version iterations (newest release at the top):

| Version | Representative CAD Snapshot | Design Milestones & Key Evolutionary Changes | Status |
| :---: | :---: | :--- | :---: |
| **[Version 04](v04/)**<br>*(Master)* | ![v04 Snapshot](v04/sled_v04.png) | **Master Version**: Organized 3D model into 4 modular FreeCAD `App::DocumentObjectGroup` containers (`Flame_Sled_Pyramid_Hood`, `Overhead_Support_Frame`, `Rigid_Towbar_Hitch`, `Harbor_Freight_Torch_91037`), establishing clean tree structure and parametric VarSet (`dims`) control.<br><br>📋 [**REQUIREMENTS.md**](v04/REQUIREMENTS.md) • 📐 [**SPECIFICATION.md**](v04/SPECIFICATION.md) • ✂️ [**CUT_LIST.md**](v04/CUT_LIST.md) • 🛠️ [**FABRICATION_GUIDE.md**](v04/FABRICATION_GUIDE.md) • 📦 [**BOM.md**](v04/BOM.md) • 🛠️ [**build.py**](v04/build.py) | **OPTIMAL MASTER** |
| **[Version 03](v03/)** | ![v03 Snapshot](v03/sled_v03.png) | **Ergonomic Forward Lean**: Re-angled torch handle wand 180° forward leaning toward the operator pulling at the front, putting the blue handle, flow knob, and piezo igniter button within comfortable walking reach.<br><br>🛠️ [**build.py**](v03/build.py) | Ergonomic Refinement |
| **[Version 02](v02/)** | ![v02 Snapshot](v02/sled_v02.png) | **Mechanical Integration**: Integrated overhead steel bridge mounting frame, Harbor Freight #91037 propane torch module, 2.0" vertical skirts, and 5 ft rigid square tube tow bar with 20° drop-stop rest tab.<br><br>🛠️ [**build.py**](v02/build.py) | Mechanical Integration |
| **[Version 01](v01/)** | ![v01 Snapshot](v01/sled_v01.png) | **Baseline Prototype**: Initial $18'' \times 18''$ closed pyramid hood geometry, 14-gauge sheet metal templates, and dual $1.5'' \times 3/16''$ flat bar skid runners with 30° turned-up tips.<br><br>🛠️ [**build.py**](v01/build.py) | Baseline |

---

## FreeCAD Execution Command

To build the active master model (Version 04) and generate all orthographic view renders:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/road-roaster/v04/build.py'; exec(open(__file__).read())"
```
