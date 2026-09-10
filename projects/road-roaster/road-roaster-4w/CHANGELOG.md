# Road Roaster 4W Changelog

All notable architectural transformations, parametric modifications, and visual milestone releases for the **Road Roaster 4W** (`road-roaster-4w`) are recorded here in reverse-chronological order.

---

## [[v0.2.0]](changelog/v0.2.0.png) — 2026-09-07: Solaronics K-30 Integration, Bolted Front Skirt & Cantilever Pivot Axle

<img src="changelog/v0.2.0.png" width="540" alt="Road Roaster 4W v0.2.0 Home Perspective View">

### Added
- **Bolted Front Skirt Mounting Apron**:
  - Heavy-gauge $3/16''$ ($6\text{ mm}$) formed steel mounting apron spanning $540.0\text{ mm}$ across the front downturn lip of the cart deck between the molded rubber corner bumpers.
  - Anchored with 4x $3/8''\text{-16}$ carriage through-bolts, distributing dynamic cantilever loads across the cart's extruded perimeter frame.
- **Continuous 3/4" Pivot Axle & Pillow Ear Brackets**:
  - Arched steel axle ear brackets mounted at $X = \pm 230.0\text{ mm}$ on top of the front skirt with precision $19.5\text{ mm}$ pivot bores elevated $35\text{ mm}$ ($Z = 230.0\text{ mm}$) above the deck top surface.
  - Continuous $3/4''$ ($19.05\text{ mm}$) cold-rolled steel pivot axle ($520.0\text{ mm}$ length) spanning through both brackets, secured with outer zinc-plated shaft collars.
- **Realistic Solaronics K-30 Ceramic Infrared Burner Integration**:
  - Replaced the preliminary generic cowl with the photorealistic `solaronics_infrared_burner` component featuring 4x Cordierite ceramic plaques ($173\text{ in}^2$ radiating face), 304 SS retainer frame, matte black plenum, cast iron venturi mixer, DSI pilot electrodes, and flared mirror-aluminum reflector hood with $45^\circ$ mitered relief corners.
  - **Cart-Side Fitting Orientation**: Rotated burner $180^\circ$ around Z so the NEMA control valve box, venturi tube, and brass gas orifice are positioned on the **cart side** facing the 20 lb propane cylinder, providing a clean, protected gas supply path.
- **Cantilevered Flip-Over Bracket & Brace System (Per Concept Sketch)**:
  - Modeled after the hand-drawn engineering sketch in [`projects/road-roaster-4w/sketches/side-view-proposed-burner-bracket.png`](sketches/side-view-proposed-burner-bracket.png):
    - Dual axle pivot sleeve bushings ($32\text{ mm}$ OD) rotating smoothly on the $3/4''$ axle.
    - Dual vertical drop legs ($38.1\text{ mm}$ square steel tubing) extending downward in front of the skirt.
    - Formed steel **Hood Brackets** with 4-bolt patterns ($2 \times 2$) bolting to the burner throat.
    - Forward horizontal projection arms and triangulated diagonal **Cantilever Braces** stabilizing the reflector hood.
    - Rear mechanical stop pads contacting the front skirt, locking hover height at $1.5''$ ($38.1\text{ mm}$) above the road.
    - Transverse cross-tie tube rigidifying both arms into a unified flip-up frame.
- **Kinematic 180° Flip Transit Over Axle**:
  - Burner frame rotates $180^\circ$ over the elevated pivot axle from forward operating position ($Y \approx -800\text{ mm}$) onto the clear **Front Stow Zone** of the deck ($Y \approx -150\text{ mm}$).
  - Shifts center of gravity rearward over the 4-wheel wheelbase ($X = +0.31''$, $Y = +0.53''$, $Z = +11.08''$), eliminating forward tipping risks during high-speed transit.

---

## [[v0.1.0]](changelog/v0.1.0.png) — 2026-09-04: Full 4-Wheel Dolly System Integration

<img src="changelog/v0.1.0.png" width="540" alt="Road Roaster 4W v0.1.0 Home Perspective View">

### Added
- **Project Genesis (`road-roaster-4w`)**: Established the 4-wheel commercial platform dolly parallel project, preserving the compact 2-wheel hand truck variant (`projects/road-roaster`) for tight garden paths and high slope agility.
- **Commercial 24" × 36" Cart Foundation**: Imported standalone `components/platform_cart_24x36`:
  - 24" × 36" diamond-tread aluminum deck with 1.75" perimeter skirt and 1.5" radiused corners.
  - 4 molded rubber corner impact guards with recessed blue socket screws.
  - 4-wheel running gear with **5.0" (127.0 mm)** solid rubber wheels on high-visibility yellow hubs (2 front rigid casters, 2 rear swivel casters with foot brake locks).
  - Ergonomic **29.0" (736.6 mm)** push handle with dual horizontal reinforcement/accessory cross rails.
- **Rear 20 lb Propane Fuel System**:
  - Modeled and integrated `components/propane_cylinder_20lb` (standard DOT 20 lb LP tank with foot ring, dual-handled protective collar, OPD service valve, and 11" W.C. regulator).
  - Added welded base retention ring anchored to the deck channels.
  - Modeled brass dual-outlet distribution manifold tee feeding both the radiant burner and auxiliary spot wand.
- **Front Cantilevered Radiant Burner & 180° Flip Hinge**:
  - Front deck twin-ear hinge brackets and heavy pivot pins at the front deck edge ($Y = -457.2\text{ mm}$).
  - Dual 1.5" square steel tube cantilever arms extending the burner forward past the front bumper to $Y = -720.0\text{ mm}$.
  - Threaded turnbuckle height-adjustment struts locking the burner hover height at $1.0''$ ($25.4\text{ mm}$) above the road (adjustable from $0.5''$ to $2.5''$).
  - 14-gauge protective steel burner cowl with perimeter heat skirts and breathing vents.
  - Integrated 60,000 BTU Solaronics ceramic infrared radiant engine pointing downward at the pavement.
  - Flexible high-temperature LP gas feed loop.
- **Handle-Mounted Spot Torch Wand & Safety Reservoir**:
  - Mounted Harbor Freight #91037 spot weed torch wand (`components/torch_hf91037`) to the handle cross rails using dual quick-draw holster clips.
  - Modeled 2.5-gallon pressurized stainless steel water safety spray canister with pump plunger and deck cradle for grass edge pre-wetting and emergency quenching.

### Changed / Modular Assembly Architecture
- **Idiomatic FreeCAD 1.1 Assembly Architecture (`App::Link`)**: Decomposed monolithic assembly into 4 modular, independently maintainable `.FCStd` subassemblies and components:
  1. `components/platform_cart_24x36` (Commercial Platform Cart Foundation)
  2. `subassemblies/cantilever_burner` (Front Cantilever Radiant Burner & Cowl)
  3. `subassemblies/fuel_system` (20 lb Propane Tank Retention & Primary Gas Train)
  4. `subassemblies/aux_torch_safety` (Handle-Mounted Spot Torch Wand & Water Safety Reservoir)
- **Zero-Dependency Material Embedding**: Integrated dedicated `Materials` group container into all master and subassembly models, embedding `App::MaterialObject` definitions permanently into `.FCStd` files. Resolved all `Material not found` errors.
- **Assembly Joint Normalization**: Enforced 2-element list `["", ""]` normalization in `phi_works.maker.assembly._normalize_subelements`, resolving FreeCAD `JointObject.py` migration script `list index out of range` errors.
- **Lock Symbol Glyph Removal**: Removed redundant component-level ground joint from `platform_cart_24x36`, eliminating the 3D lock symbol from platform cart renders.
- **Assembly Visibility Guarantee**: Added `ensure_assembly_visible(doc)` guaranteeing all assemblies, subassemblies, parts, and links are explicitly set to `Visibility = True` when assembling in code and saving models.
- **Recursive Multi-Material Mass Engine**: Upgraded `get_mass_properties()` to recursively traverse nested `App::Link` subassemblies and accumulate spatial placements, producing an exact 435.72 lb mass breakdown with 3D Center of Gravity across 156 leaf components.
