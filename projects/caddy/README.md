# STIHL Kombi Attachment Caddy Project

**Project Location**: `projects/caddy/`  
**Master CAD Model**: [`caddy.FCStd`](caddy.FCStd) (Master copy of Version 10)  
**Latest Optimal Version**: **[Version 10](v10/)**  

---

## Project Overview

The **STIHL Kombi Attachment Caddy** is a heavy-duty, mobile 2x4 wooden rack designed to organize and store STIHL KombiSystem powerheads and attachments vertically. It features 24.0 in outer post stud alignment, 36.0 in cantilever top/bottom rails for clip spacing, 1x4 floor deck slats for gearbox resting, anti-racking plywood corner gussets, and rear 5-inch fixed caster wheels for easy shop transport.

---

## Active Master Model Render (Version 10)

![STIHL Kombi Caddy v10 Render](v10/caddy_v10.png)

---

## Project Master Documentation Index

- 📋 [**REQUIREMENTS.md**](REQUIREMENTS.md): Master requirements specification, functional requirements table, physical shop constraints, and version evolutionary traceability.
- 📐 [**v10/SPECIFICATION.md**](v10/SPECIFICATION.md): Version 10 engineering specification, parametric VarSet (`dims`) table, dado post joinery, and clearance specs.
- 🛠️ [**v10/CUT_LIST.md**](v10/CUT_LIST.md): Version 10 DIY cut list tailored for miter saws and table saws, board optimization, dado pocket specs, and fastener BOM.
- 🚀 [**v10/README.md**](v10/README.md): Version 10 self-contained directory index.

---

## Version Iteration Index

| Version | Directory | Description & Key Milestones | Status |
| :---: | :--- | :--- | :---: |
| **v01** | [`v01/`](v01/) | Initial flat 2x4 frame prototype. | Baseline |
| **v02** | [`v02/`](v02/) | Extended base foot depth to 15". | Deprecated |
| **v03** | [`v03/`](v03/) | Added top 1x4 cross rail and clip alignment. | Deprecated |
| **v04** | [`v04/`](v04/) | Added sloped front toe and rear plywood gussets. | Deprecated |
| **v05** | [`v05/`](v05/) | Parametric VarSet clean rebuild (`caddy_v05.FCStd`). | Milestone |
| **v06** | [`v06/`](v06/) | Offset vertical posts 8.5" rearward for tool head clearance. | Structural Refinement |
| **v07** | [`v07/`](v07/) | Housed cross rails in dado post pockets; added 1x4 floor deck slats. | Structural Refinement |
| **v08** | [`v08/`](v08/) | Added rear 5" fixed rubber casters for tilt-and-roll transport. | Mobility Refinement |
| **v09** | [`v09/`](v09/) | Height calibrated to 44.5" for 39.5" Kombi tool standing height. | Height Calibration |
| **v10** | [`v10/`](v10/) | **Master Version**: Expanded rails to 36" width with 24" post span & 6" cantilever overhangs. | **OPTIMAL MASTER** |

---

## FreeCAD Build Command

To build the active master model (Version 10) directly in FreeCAD headless mode:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/build.py'; exec(open(__file__).read())"
```
