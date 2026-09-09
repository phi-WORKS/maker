# Physical Projects Index

> **Master Physical Assemblies, Parametric Models & Fabrication Documentation**  
> *phi-WORKS Maker Framework (`projects/`)*

---

## Overview

The `projects/` directory contains active physical product assemblies and fabrication documentation. Each project represents a complete physical machine, mobile cart, or shop rack designed using parametric FreeCAD modeling paired with practical shop fabrication techniques (welding, cutting, woodwork, hardware integration).

### Project Principles:
- **Pre-Built Component Integration**: Projects consume modular CAD building blocks from `components/` via `import_component()` rather than recreating hardware geometry.
- **Git-Native Versioning**: Project iterations are tracked natively in Git via version tags (`v0.0.0`, `v0.1.0`, etc.).
- **Visual Transformation History**: Historical visual snapshot thumbnails are preserved under `projects/<project>/changelog/` and documented in `CHANGELOG.md`.
- **Perspective Home Thumbnails**: Each project provides a canonical Perspective Home View render named `<model>.png` (e.g. `road-roaster-4w.png`, `road-roaster.png`, `caddy.png`), accompanied by full 6-view orthogonal projections.

---

## Project Catalog

### 1. [Road Roaster 4W](road-roaster-4w/)

*4-Wheel Commercial Platform Dolly Architecture for Directional Ceramic Infrared Weed Eradication*

| Master Assembly Thumbnail | Quick Specifications & Links |
| :---: | :--- |
| [![Road Roaster 4W](road-roaster-4w/road-roaster-4w.png)](road-roaster-4w/) | • **Application**: Heavy-duty commercial 24" × 36" platform cart for large-scale driveway, roadway, and agricultural headland weed eradication.<br>• **Core Architecture**: Commercial 24" × 36" diamond-plate steel dolly (5" wheels, 29" push handle); 30,000 BTU Solaronics K-30 ceramic infrared radiant burner engine with flared reflector hood cantilevered at front; 3-sided wrap-around rigid front skirt with continuous 3/4" pivot axle; 180° flip-over transit/stowage; cart-side protected LP gas manifold; full 20 lb propane cylinder (~14.4 hrs runtime); 2.5 gal pressurized water safety reservoir; auxiliary spot-weed torch wand (`torch_hf91037`) holstered on handle; slow-crawl propulsion ready.<br>• **Active Master**: [**v0.2.0**](road-roaster-4w/) 🟢 **`[RELEASED]`**<br>• 📖 [**`README.md`**](road-roaster-4w/README.md)<br>• 📐 [**`SPECIFICATION.md`**](road-roaster-4w/SPECIFICATION.md)<br>• 📜 [**`CHANGELOG.md`**](road-roaster-4w/CHANGELOG.md)<br>• 🛠️ [**`build.py`**](road-roaster-4w/build.py)<br>• 📦 [**`road-roaster-4w.FCStd`**](road-roaster-4w/road-roaster-4w.FCStd) |

---

### 2. [Road Roaster](road-roaster/)

*Directional Ceramic Infrared Thermal Weed Shock Sled (Compact 2-Wheel Hand Truck Variant)*

| Master Assembly Thumbnail | Quick Specifications & Links |
| :---: | :--- |
| [![Road Roaster](road-roaster/road-roaster.png)](road-roaster/) | • **Application**: Chemical-free hardscape weed eradication via Solaronics ceramic infrared radiant heat shock on an ultra-compact 2-wheel chassis.<br>• **Core Architecture**: Vintage restored tubular steel commercial hand truck donor frame (1.0" OD red tubing, 9.5" wheels); common-wheel-axle triangular suspension sled; 60,000 BTU downward-firing Solaronics ceramic infrared emitter; zero aerodynamic blast pressure; 1 lb onboard propane bottle in quick-release cage; flexible center-spine fuel hose routing; dual-mode gliding roast vs. tilt-back rolling transit.<br>• **Active Master**: [**v0.7.0**](road-roaster/) 🟡 **`[IN PROGRESS]`**<br>• 📖 [**`README.md`**](road-roaster/README.md)<br>• 📐 [**`SPECIFICATION.md`**](road-roaster/SPECIFICATION.md)<br>• 📜 [**`CHANGELOG.md`**](road-roaster/CHANGELOG.md)<br>• 🛠️ [**`build.py`**](road-roaster/build.py)<br>• 📦 [**`road-roaster.FCStd`**](road-roaster/road-roaster.FCStd) |

---

### 3. [Kombi Kaddy](kombi-kaddy/)

*Mobile STIHL KombiSystem Multi-Tool Attachment Storage Rack*

| Master Assembly Thumbnail | Quick Specifications & Links |
| :---: | :--- |
| [![Kombi Kaddy](kombi-kaddy/caddy.png)](kombi-kaddy/) | • **Application**: Heavy-duty mobile 2x4 wooden rack for organized vertical storage of STIHL KombiSystem attachments and power heads.<br>• **Core Architecture**: Modern FreeCAD 1.1 `Assembly::AssemblyObject` architecture; full commercial STIHL attachment fleet (FS-KM Trimmer, FBD-KM Bed Redefiner, BG-KM Blower, FH-KM Scythe); 36.0" expanded rails with 6.0" cantilevers; 44.5" post height; rear 5" rubber casters; kinematic Ground joint and programmatic Exploded View.<br>• **Active Master**: [**v1.0.0**](kombi-kaddy/) 🟢 **`[RELEASED]`**<br>• 📖 [**`README.md`**](kombi-kaddy/README.md)<br>• 📐 [**`SPECIFICATION.md`**](kombi-kaddy/SPECIFICATION.md)<br>• 📜 [**`CHANGELOG.md`**](kombi-kaddy/CHANGELOG.md)<br>• 🛠️ [**`build.py`**](kombi-kaddy/build.py)<br>• 📦 [**`caddy.FCStd`**](kombi-kaddy/caddy.FCStd) |

---

### 4. [Compact Foam Camper](foam-camper/)

*Ultralight 12' x 6.5' Towable Rigid Foam Camper Shell - 3D Form Studies & Compound Curve Exploration*

| Master Assembly Thumbnail | Quick Specifications & Links |
| :---: | :--- |
| [![Compact Foam Camper](foam-camper/foam-camper.png)](foam-camper/) | • **Application**: Ultralight micro-camper shell for scored and bent rigid insulation (XPS) foam construction over a standard 12'-0" × 6'-6" trailer platform.<br>• **Core Architecture**: Parametric FreeCAD 1.1 `App::VarSet` engine (`Vars`); 3 comparative solid form modeling studies (Form A: Orthogonal sketch pad & pocket intersection with shoulder roll; Form B: Ruled developable multi-chine hull modeling 12°–35° kerf-score folds; Form C: 4-station transverse spline loft teardrop shell); reference trailer bed outline with 60/40 axle balance line; comprehensive volume & mass analysis (~125–145 lbs foam shell).<br>• **Active Master**: [**v0.1.0**](foam-camper/) 🟢 **`[CURRENT / ACTIVE]`**<br>• 📖 [**`README.md`**](foam-camper/README.md)<br>• 📋 [**`ASSEMBLY.md`**](foam-camper/ASSEMBLY.md)<br>• 🔨 [**`fabrication/`**](foam-camper/fabrication/README.md)<br>• 📐 [**`SPECIFICATION.md`**](foam-camper/SPECIFICATION.md)<br>• 📜 [**`CHANGELOG.md`**](foam-camper/CHANGELOG.md)<br>• 🛠️ [**`build.py`**](foam-camper/build.py)<br>• 📦 [**`foam-camper.FCStd`**](foam-camper/foam-camper.FCStd) |

