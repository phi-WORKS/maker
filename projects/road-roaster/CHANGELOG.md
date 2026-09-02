# Road Roaster — Evolutionary Changelog & Visual History

> **Directional Upright-Vacuum Thermal Weed Shock Sled**  
> *Chronological Design Transformation Log & Release History*

---

## Releases & Transformation Story

### Version 0.7.0 — Solaronics Ceramic Infrared Array, Vintage Hand Truck & Common-Axis Suspension
**Status**: 🟡 `[IN PROGRESS]`  
**Date**: 2026-09-02  
**Visual Snapshot**: ![v0.7.0 Snapshot](road-roaster_iso.png)

#### Changes & Milestones
- **Solaronics High-Intensity Ceramic Radiant Engine**: Integrated industrial cordierite grooved ceramic plaque matrix ($173\text{ sq. in}$ active radiant face, $1,800^\circ\text{F}$ surface emission) with mirror-bright deep parabolic focusing aluminum reflector and Inconel re-radiating wire grid.
- **Zero Aerodynamic Blast Pressure**: Shifted from high-velocity torch flame to low-pressure ($11''\text{ W.C.}$, $60,000\text{ BTU/hr}$) flameless surface combustion, completely eliminating the blown gravel, dust, and flying ember hazards of open blast torches.
- **Restored Vintage Commercial Hand Truck Chassis**: Modeled after user's physical vintage green donor frame (restored in industrial Red):
  - $1.0''\text{ OD}$ continuous tubular steel inverted U-frame ($12.5''$ center-to-center upright spacing, $46.0''$ top of U-bend).
  - Center handle spine pipe with ergonomic top backward loop and vertical spine tube.
  - 3 horizontal steel cross-straps ($1.0''$ wide at $12.0''$, $22.0''$, and $31.0''$ heights).
- **Authentic Dual Triangular Axle Trusses**: Modeled two-strut triangular truss brackets (lower strut from upright base at $Z = 30\text{ mm}$, upper diagonal strut from Strap 1 at $Z = 292\text{ mm}$) welded flush to vertical pipes and converging at axle sleeves.
- **$\varnothing 9.5''$ Wheels & Datum Axle Center**: Continuous $5/8''$ solid steel axle shaft centered at **$4.75''$ ($120.65\text{ mm}$)** from the floor and **$4.75''$ ($120.65\text{ mm}$)** rearward from the side rail plane.
- **Common-Wheel-Axle Triangular Sled Suspension**: The forward radiant sled connects directly to the same continuous wheel axle shaft via matching triangular straps ($X = \pm 145.0\text{ mm}$, inboard of frame trusses), providing concentric pivoting and eliminating frame flex.
- **Rear-Mounted Propane Harness & Cross-Strap Clamps**: 1 lb LP bottle and cage harness relocated behind the vertical supports ($X = +80.0\text{ mm}, Y = +75.4\text{ mm}$), clamped directly around the middle horizontal cross-strap (Strap 2) with sandwich clamp jaws and side stabilizer tab.
- **Center-Support Routed 3D B-Spline Flexible Hose & Spark Wire**: Modeled smooth 3D B-spline flexible LP gas hose and silicone igniter wire traveling down the center support pipe secured by retaining clips, sweeping under the frame directly into the Solaronics burner gas connector.
- **Solaronics Engineering Outreach Document**: Created [`SOLARONICS_INQUIRY.md`](SOLARONICS_INQUIRY.md) detailing technical collaboration and OEM component inquiries.
- **Modular Component Library**: Added standalone CAD modules [`components/commercial_hand_truck/`](../../components/commercial_hand_truck/) and [`components/solaronics_infrared_burner/`](../../components/solaronics_infrared_burner/).

---

### Version 0.6.0 — Decomposed Torch Controls & Forward-Firing Asymmetrical Hood
**Status**: 📦 `[SUPERSEDED]`  
**Date**: 2026-08-22  
**Visual Snapshot**: ![v0.6.0 Snapshot](changelog/v0.6.0_iso.png)

#### Changes & Milestones
- **Forward-Firing Asymmetrical Hood**: Re-engineered hood geometry with a rear-offset apex ($Y_{apex} = +110\text{ mm}$), creating a steep $\approx 66^\circ$ rear heat deflector shield facing the operator and a long $\approx 28^\circ$ forward-sloping radiant roof ramp. Front exhaust vent safely channels all combustion heat away from the user.
- **Continuous Longitudinal Chassis Side Rails**: Replaced patchwork extension tabs with continuous $1.5'' \times 3/16''$ steel side rails ($L = 534\text{ mm}$) running from the front of the sled to the rear axle, with integrated $1/2''$ axle pivot ears and machined bronze flange bushings.
- **Clean Coaxial Axle Stacking**: Established symmetric axle stack on each side: `[Lock Collar] ── [4" Solid Wheel] ── [Chassis Side Rail Ear] ── [Handle Clevis]`, securely bracing the sled side rail directly between the wheel and handle connector with zero interference.
- **Top Crossbar Operator Cockpit**: Created and imported standalone CAD module [`components/torch_control_handle/`](../../components/torch_control_handle/) mounted to the top horizontal crossbar adjacent to the right grip, featuring a pilot needle valve knob, dead-man turbo squeeze lever, and push-button piezo spark igniter.
- **Dual Horizontal Cross-Rail Ladder Frame**: Integrated upper ($L = 720\text{ mm}$) and lower ($L = 540\text{ mm}$) horizontal structural cross-rails bridging between the U-frame uprights.
- **Side-Mounted 1 lb Propane Bottle Harness**: Side-mounted [`components/propane_harness/`](../../components/propane_harness/) across both upper and lower horizontal cross-rails at $X = +140\text{ mm}$, leaving the entire center bay open and establishing a clean vertical fuel line run straight up to the cockpit with zero crossovers.
- **Chassis-Mounted 500k BTU Burner Head**: Created and imported standalone CAD module [`components/torch_burner_head/`](../../components/torch_burner_head/) mounted in the rear apex, firing downward and forward at a $30^\circ$ pitch.

---

### Version 0.5.0 — Upright-Vacuum Tilt-Back Frame & Dual Metal Wheels
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.5.0 Snapshot](changelog/v0.5.0_iso.png)

#### Changes & Milestones
- **Upright Vacuum Tilt-Back Concept**: Re-architected chassis with dual-pivot hinge mounts, allowing operator to tilt handle back to lever the sled/skids completely off the ground for non-contact rolling transit across lawns, asphalt, and curbs.
- **Dual Heat-Resistant Steel Wheels**: Created and imported standalone 4.0" all-metal wheel components (`components/steel_caster_wheel/`) at the rear pivot axis to handle intense radiant heat.
- **Hand-Truck U-Frame**: Replaced single square tube tow bar with a 48" dual-riser U-frame handle featuring dual pivot pin brackets, top hand grips, and cross-braces for superior torsional stability and easy pivoting.
- **Foot-Release Tilt Latch Linkage**: Added snap-lock latch mechanism linking handle lower cross-member to overhead torch frame catch tower.
- **Central Propane Bottle Mounting**: Relocated 1 lb bottle harness to handle mid-crossbar for improved balance and accessibility.

---

### Version 0.4.0 — Onboard Propane Harness & Imported Components
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.4.0 Snapshot](changelog/v0.4.0_iso.png)

#### Changes & Milestones
- **Onboard Fuel Bottle Mounting**: Integrated standalone 1 lb Propane Cylinder (`components/propane_cylinder_1lb/`) and quick-slip Propane Bottle Harness (`components/propane_harness/`) onto upper tow bar handle tube.
- **FCStd Component Import**: Refactored `build.py` to consume pre-built `.FCStd` component files directly via `import_component()` helper.
- **High-Pressure Fuel Hose Routing**: Routed flexible gas line from cylinder valve to torch handle control knob.

---

### Version 0.3.0 — Modular Master Container
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.3.0 Snapshot](changelog/v0.3.0_iso.png)

#### Changes & Milestones
- **Modular Subassemblies**: Organized 3D model into 4 modular FreeCAD `App::DocumentObjectGroup` containers (`Flame_Sled_Pyramid_Hood`, `Overhead_Support_Frame`, `Rigid_Towbar_Hitch`, `Harbor_Freight_Torch_91037`), establishing clean tree structure and parametric VarSet (`dims`) control.

---

### Version 0.2.0 — Ergonomic Forward Lean
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.2.0 Snapshot](changelog/v0.2.0_iso.png)

#### Changes & Milestones
- **Torch Re-Angling**: Re-angled torch handle wand 180° forward leaning toward the operator pulling at the front, putting the blue handle, flow knob, and piezo igniter button within comfortable walking reach.

---

### Version 0.1.0 — Mechanical Integration
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.1.0 Snapshot](changelog/v0.1.0_iso.png)

#### Changes & Milestones
- **Frame & Tow Bar Integration**: Integrated overhead steel bridge mounting frame, Harbor Freight #91037 propane torch module, 2.0" vertical skirts, and 5 ft rigid square tube tow bar with 20° drop-stop rest tab.

---

### Version 0.0.0 — Baseline Prototype
**Status**: 📦 `[SUPERSEDED]`  
**Visual Snapshot**: ![v0.0.0 Snapshot](changelog/v0.0.0_iso.png)

#### Changes & Milestones
- **Pyramid Hood Geometry**: Initial $18'' \times 18''$ closed pyramid hood geometry, 14-gauge sheet metal templates, and dual $1.5'' \times 3/16''$ flat bar skid runners with 30° turned-up tips.
