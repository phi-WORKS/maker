# Road Roaster

> **Upright Vacuum / Hand-Truck Thermal Weed Shock Sled**  
> *Git-Native Parametric CAD Model & Fabrication Documentation*

**Active CAD Model**: [`road-roaster.FCStd`](road-roaster.FCStd)  
**Status**: 🟡 **`[IN PROGRESS]`**  

---

## Active Model Gallery

| Isometric View | Top Plan View |
| :---: | :---: |
| ![Isometric View](road-roaster_iso.png) | ![Top View](road-roaster_top.png) |
| **Front Elevation** | **Rear Elevation** |
| ![Front Elevation](road-roaster_front.png) | ![Rear Elevation](road-roaster_back.png) |
| **Right Side Elevation** | **Left Side Elevation** |
| ![Right Side View](road-roaster_right.png) | ![Left Side View](road-roaster_left.png) |
| **Bottom Plan View** | |
| ![Bottom View](road-roaster_bottom.png) | |

---

## Documentation Index

- 📐 [**`SPECIFICATION.md`**](SPECIFICATION.md): Master technical specification, parametric VarSet (`dims`) table, joinery, and hardware.
- 📜 [**`CHANGELOG.md`**](CHANGELOG.md): Complete chronological version transformation log and release history.
- 🛠️ [**`build.py`**](build.py): Master FreeCAD Python parametric generator script.
- 📦 [**`road-roaster.FCStd`**](road-roaster.FCStd): Active 3D Master Model document file.

---

## Evolutionary Transformation Story

This project documents the evolutionary design transformation of the Road Roaster. Historical CAD models are preserved natively via Git tags (`v0.0.0` .. `v0.5.0`).

| Version | Visual Milestone Snapshot | Key Evolutionary Milestone | Lifecycle Status |
| :---: | :---: | :--- | :---: |
| **v0.5.0** | ![v0.5.0 Snapshot](road-roaster_iso.png) | **Upright-Vacuum Tilt-Back Frame & Dual Metal Wheels**: Transformed towing concept to an upright vacuum / hand-truck architecture. Integrated dual 4.0" solid steel wheels at the rear pivot axis, a 48" dual-riser U-frame handle, and a foot-release snap tilt-latch allowing the sled to be levered completely off the ground for non-contact rolling transit across grass and asphalt. | 🟡 **`[IN PROGRESS]`** |
| **v0.4.0** | ![v0.4.0 Snapshot](changelog/v0.4.0_iso.png) | **Onboard Propane Harness & Imported Components**: Integrated standalone 1 lb Propane Cylinder (`components/propane_cylinder_1lb/`) and quick-slip Propane Bottle Harness (`components/propane_harness/`) onto handle tube. Refactored `build.py` to consume pre-built `.FCStd` component files directly via `import_component()`. | 📦 **`[SUPERSEDED]`** |
| **v0.3.0** | ![v0.3.0 Snapshot](changelog/v0.3.0_iso.png) | **Modular Master Container**: Organized 3D model into modular FreeCAD `App::DocumentObjectGroup` containers (`Flame_Sled_Pyramid_Hood`, `Overhead_Support_Frame`, `Rigid_Towbar_Hitch`, `Harbor_Freight_Torch_91037`), establishing clean tree structure and parametric VarSet (`dims`) control. | 📦 **`[SUPERSEDED]`** |
| **v0.2.0** | ![v0.2.0 Snapshot](changelog/v0.2.0_iso.png) | **Ergonomic Forward Lean**: Re-angled torch handle wand 180° forward leaning toward the operator pulling at the front, putting the blue handle, flow knob, and piezo igniter button within comfortable walking reach. | 📦 **`[SUPERSEDED]`** |
| **v0.1.0** | ![v0.1.0 Snapshot](changelog/v0.1.0_iso.png) | **Mechanical Integration**: Integrated overhead steel bridge mounting frame, Harbor Freight #91037 propane torch module, 2.0" vertical skirts, and 5 ft rigid square tube tow bar with 20° drop-stop rest tab. | 📦 **`[SUPERSEDED]`** |
| **v0.0.0** | ![v0.0.0 Snapshot](changelog/v0.0.0_iso.png) | **Baseline Prototype**: Initial $18'' \times 18''$ closed pyramid hood geometry, 14-gauge sheet metal templates, and dual $1.5'' \times 3/16''$ flat bar skid runners with 30° turned-up tips. | 📦 **`[SUPERSEDED]`** |

---

## FreeCAD Execution Command

To build the active master model (`road-roaster.FCStd`) and export all 7 orthographic/isometric PNG snapshot renders:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='/home/phi/PROJECTS/phi-WORKS/maker/projects/road-roaster/build.py'; exec(open(__file__).read())"
```
