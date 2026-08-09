# Towable Flame Weeding Sled Project

## Master Project Objectives

The **Towable Flame Weeding Sled** is a lightweight, heat-concentrating drag hood pulled by an operator via a 5 ft rigid steel tow bar. Designed for gravel driveway weed management, it utilizes an overhead steel frame mounting a **Harbor Freight #91037 Propane Torch** above an enclosed 14-gauge mild steel pyramidal hood.

### Key Features:
- **Pyramidal Drag Hood**: Encloses thermal heat over target weeds while preventing heat loss.
- **Harbor Freight #91037 Torch**: High-output propane torch mounted overhead at a 35-degree incline.
- **5-ft Rigid Tow Bar & Clevis Hitch**: Allows an operator to pull the sled at a safe walking distance with a 20-degree minimum rest tab.
- **Tree View Subassembly Containers**: Organized in FreeCAD into 4 subassembly part containers for easy tree navigation.

---

## Active Master Model

- **Latest Optimal Version**: **[Version 04](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v04/)**
- **Master Model File**: [`flame_sled.FCStd`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/flame_sled.FCStd) (copy of Version 04)

For detailed cut lists, BOM, fabrication guides, and engineering specs for the latest build, navigate directly to **[v04/](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v04/)**.

---

## Version Iteration Index

| Version | Directory | Description & Key Milestones |
| :---: | :--- | :--- |
| **v01** | [`v01/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v01/) | Apex collar & closed pyramid hood prototype. |
| **v02** | [`v02/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v02/) | Integrated Harbor Freight #91037 torch, overhead frame, and forward tow bar. |
| **v03** | [`v03/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v03/) | Updated torch handle leaning 180° forward towards operator puller. |
| **v04** | [`v04/`](file:///home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v04/) | **Master Version**: Organized 3D model into 4 modular FreeCAD `App::DocumentObjectGroup` containers. |

---

## FreeCAD Execution

To build Version 04 directly in FreeCAD headless mode:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/flame-weeding-sled/v04/build.py'; exec(open(__file__).read())"
```
