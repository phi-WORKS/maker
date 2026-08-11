# Kombi Kaddy

> *Mobile STIHL KombiSystem Attachment Rack*

---

## Active Master Release: Version 10

| Master Render Snapshot | Active Version Details & Master Links |
| :---: | :--- |
| ![Kombi Kaddy Master Render](caddy_iso.png) | • **Latest Optimal Version**: **[Version 10](v10/)**<br>• **Master CAD Model**: [`caddy.FCStd`](caddy.FCStd) (Master copy of v10)<br>• 📋 [**REQUIREMENTS.md**](REQUIREMENTS.md)<br>• 📐 [**v10/SPECIFICATION.md**](v10/SPECIFICATION.md)<br>• ✂️ [**v10/CUT_LIST.md**](v10/CUT_LIST.md)<br>• 🛠️ [**v10/build.py**](v10/build.py)<br>• 🚀 [**v10/README.md**](v10/README.md) *(Full 7-View Gallery)* |

---

## Project Overview

The **Kombi Kaddy** is a heavy-duty mobile shop rack designed to store, organize, and transport STIHL KombiSystem power heads and straight-shaft attachments. Built from standard 2x4 lumber with heavy-duty swivel casters, it features 24.0 in outer post stud alignment, 36.0 in cantilever top/bottom rails for clip spacing, 1x4 floor deck slats for gearbox resting, and anti-racking plywood corner gussets to roll effortlessly between shop storage and active job sites.

---

## Evolutionary Version History & Human-AI Design Journey

This project documents the collaborative evolutionary cycle between human shop feedback and AI-agentic parametric CAD modeling across 10 version iterations:

| Version | Directory | Design Milestones & Key Evolutionary Changes | Status |
| :---: | :--- | :--- | :---: |
| **v10** | [`v10/`](v10/) | **Master Version**: Expanded top/bottom rails to 36.0" width with 6.0" cantilever overhangs, allowing 4 full-sized attachments to be mounted without clip crowding while preserving 24.0" post alignment for garage studs. | **OPTIMAL MASTER** |
| **v09** | [`v09/`](v09/) | **Height Calibration**: Calibrated post height to 44.5" to align spring clip grab centers at 42.75", matching real-world 39.5" Kombi attachment standing heights. | Height Calibration |
| **v08** | [`v08/`](v08/) | **Mobility Refinement**: Mounted rear 5" fixed rubber casters to the heel of base feet for tilt-and-roll transport across shop floors. | Mobility Refinement |
| **v07** | [`v07/`](v07/) | **Structural Joinery**: Housed 1x4 cross rails inside 0.75" dado post pockets; added 2x 1x4 horizontal floor deck slats to support gearboxes. | Structural Refinement |
| **v06** | [`v06/`](v06/) | **Ergonomic Clearance**: Offset vertical 2x4 posts 8.5" rearward along base feet to prevent heavy tool heads (tillers, edgers, blowers) from striking posts. | Structural Refinement |
| **v05** | [`v05/`](v05/) | **Parametric Clean Rebuild**: Rebuilt 3D model using FreeCAD `App::VarSet` (`dims`) table for fully parametric dimension management. | Milestone |
| **v04** | [`v04/`](v04/) | **Anti-Racking Stability**: Added sloped front foot toe profile and 3/4" rear plywood corner gussets to eliminate lateral frame sway under load. | Deprecated |
| **v03** | [`v03/`](v03/) | **Clip Rail Integration**: Added top 1x4 cross rail and spring clip mounting layout for vertical attachment storage. | Deprecated |
| **v02** | [`v02/`](v02/) | **Foot Depth Extension**: Extended base foot depth to 15.0" to improve forward tipping stability. | Deprecated |
| **v01** | [`v01/`](v01/) | **Baseline Prototype**: Initial flat 2x4 frame prototype and baseline dimensions. | Baseline |

---

## FreeCAD Execution Command

To build the active master model (Version 10) and generate all 7 orthographic view renders:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/kombi-kaddy/v10/build.py'; exec(open(__file__).read())"
```
