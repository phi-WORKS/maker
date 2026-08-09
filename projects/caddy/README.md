# STIHL Kombi Tool Caddy Project

## Master Project Objectives

The **STIHL Kombi Caddy** is a mobile, heavy-duty wooden storage caddy designed to organize STIHL Kombi System powerheads, shafts, and attachments (line trimmer, hedge trimmer, pole pruner, cultivator, leaf blower, power sweep, edger). 

### Key Design Goals:
1. **Vertical Tool Storage**: Keep attachments organized vertically with quick-release spring clips.
2. **Mobility**: Heavy-duty hand-truck wheel placement for easy transport across shop and yard terrain.
3. **Robust Timber Construction**: 2x4 frame construction with 1x4 cross-rails and deck slats for durability and weather resistance.
4. **Parametric Modeling**: Full 3D parametric CAD representation in FreeCAD using `App::VarSet` (`dims`).

---

## Active Master Model

- **Latest Optimal Version**: **[Version 10](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/)**
- **Master Model File**: [`caddy.FCStd`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/caddy.FCStd) (copy of Version 10)

For complete cut lists, bill of materials, engineering specs, and build scripts, navigate directly to **[v10/](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/)**.

---

## Version Iteration Index

| Version | Directory | Description & Key Milestones |
| :---: | :--- | :--- |
| **v01** | [`v01/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v01/) | Initial flat foot frame prototype with 2x4 posts and flat 2x4 feet. |
| **v02** | [`v02/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v02/) | 90-degree rotated base foot half-lap joint for improved lateral stability. |
| **v03** | [`v03/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v03/) | Compact 15" base foot and 5" hand-truck rubber fixed caster wheel mounting. |
| **v04** | [`v04/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v04/) | Full top rail and sloped front toe on base foot. |
| **v05** | [`v05/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v05/) | Flush rear cross rail and flat 3/4" rear plywood anti-racking corner gussets. |
| **v06** | [`v06/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v06/) | Rearward post offset (8.5" from front toe) for tool head overhang clearance; introduced FreeCAD `App::VarSet`. |
| **v07** | [`v07/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v07/) | 1x4 lumber cross rails housed in 0.75" dado post pockets. |
| **v08** | [`v08/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v08/) | Added 1x4 horizontal tool head deck slats resting across base feet. |
| **v09** | [`v09/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v09/) | Real-world tool height calibration (39.5" standing height, 44.5" post height). |
| **v10** | [`v10/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/) | **Optimal Version**: 24" outside post span (shop stud alignment) and 6" cantilever rail overhangs (36" overall width). |

---

## FreeCAD Build Execution

To build Version 10 directly in FreeCAD headless mode:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/caddy/v10/build.py'; exec(open(__file__).read())"
```
