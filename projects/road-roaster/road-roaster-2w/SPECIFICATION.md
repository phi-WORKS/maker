# Road Roaster — Master Technical Specification

> **Directional Ceramic Infrared Thermal Weed Shock Sled**  
> *Single-Source Architectural & Engineering Specification*

---

## 1. Executive Summary & Problem-Solution Engineering

The **Road Roaster** is a directional thermal weed management platform engineered to eradicate invasive hardscape weeds (gravel driveways, agricultural headlands, roadside corridors, paver paths) through concentrated **high-intensity ceramic infrared radiant shock** without chemical herbicides or open-flame fuel waste.

### The Ecological & Shop Problem
* **The Chemical Trap**: Synthetic herbicides (glyphosate, 2,4-D) poison groundwater, threaten pets and native pollinators, foster chemical-resistant weeds, and leave toxic residues in soils.
* **The Open-Air Torch Energy Trap**: Conventional handheld open-flame torches lose over 85% of their thermal energy to atmospheric wind dissipation, consuming excessive propane while presenting an open fire hazard.
* **The Aerodynamic Blast Problem**: Enclosing an open blast torch inside a hood generates severe aerodynamic pressure, blowing gravel, dust, and burning embers out from under the skirts.

### Core Thermodynamic & Design Solutions
1. **Solaronics High-Intensity Ceramic Infrared Engine** ([`components/solaronics_infrared_burner/`](../../components/solaronics_infrared_burner/)):
   - **Grooved Cordierite Ceramic Plaque Matrix**: $173\text{ sq. in}$ active radiant face emitting pure $3 - 5\,\mu\text{m}$ infrared flux at **$1,600^\circ\text{F} - 1,800^\circ\text{F}$** ($870^\circ\text{C} - 980^\circ\text{C}$).
   - **Zero Blast Pressure**: Gentle atmospheric surface micro-pore combustion at $11''\text{ W.C.}$ low pressure ($60,000\text{ BTU/hr}$) produces zero positive dynamic air pressure—whisper-quiet operation with zero gravel blowout.
   - **Deep Parabolic Aluminum Reflector**: Focuses $>90\%$ of radiant flux downward into the weed canopy.
   - **Inconel Re-Radiating Wire Grid**: Boosts radiant efficiency and acts as an integrated rock shield.
2. **Vintage Hand Truck Chassis (Restored Red Frame)** ([`components/commercial_hand_truck/`](../../components/commercial_hand_truck/)):
   - **$1.0''\text{ OD}$ Tubular Steel Inverted U-Frame**: $12.5''$ ($317.5\text{ mm}$) centerline spacing, $46.0''$ ($1168.4\text{ mm}$) top of U-bend.
   - **Center Handle Spine Pipe**: $1.0''\text{ OD}$ tube with top backward P-handle loop and vertical spine tube welded to cross straps.
   - **3 Horizontal Cross Straps**: $1.0''$ wide flat bars at $12.0''$, $22.0''$, and $31.0''$ heights.
   - **Triangular Axle Trusses**: Authentic dual-strut triangular truss brackets holding the wheel axle at $4.75''$ ($120.65\text{ mm}$) from the floor and $4.75''$ ($120.65\text{ mm}$) rearward of the uprights.
   - **$\varnothing 9.5''$ ($241.3\text{ mm}$) Heavy-Duty Wheels**: Continuous $5/8''$ solid steel axle shaft ($17.3''$ track width).
3. **Common-Wheel-Axle Triangular Sled Suspension**:
   - The wheel axle $(0, 120.65, 120.65)$ serves as the primary common datum pivot axis.
   - Matching **triangular suspension straps** mount directly onto the axle shaft (inboard of the frame trusses at $X = \pm 145.0\text{ mm}$), connecting forward to the radiant sled chassis and bridge tower.
   - Eliminates frame flex and provides a unified, rigid A-frame structure pivoting on the common wheel axis.
4. **Foot-Release Transit Tilt Latch**:
   - Foot pedal mounted on the lower cross strap ($Z \approx 300\text{ mm}$) engages the sled suspension tower. Tilting the handle backward pivots the entire machine around the $9.5''$ wheels, lifting the sled $4''-6''$ off the ground for clean rolling transport.
5. **Rear-Mounted Propane Harness & Tank Valve**:
   - The 1 lb LP cylinder and cage harness are mounted **behind the vertical supports** ($X = +80.0\text{ mm}, Y = +75.4\text{ mm}$), protected from weed snagging.
   - Clamped directly around the **middle horizontal cross-strap** (Strap 2 at $Z \approx 546\text{ mm}$) with front and rear clamping jaws.
   - Direct brass needle flow control knob and $11''\text{ W.C.}$ regulator mounted directly atop the propane canister neck with an integrated push-button piezo igniter.
   - **Center Support Flexible Hose & Wire Conduit**: A reinforced flexible LP gas hose (modeled as a smooth 3D B-spline curve) and high-voltage spark wire travel from the tank over to the **center support pipe**, run vertically down secured by retention clips, and sweep forward through the open toe bay directly into the Solaronics burner gas connector.

---

## 2. Parametric VarSet (`dims`) Specification

All dimensions are managed parametrically in FreeCAD via `App::VarSet` (`dims`):

| Parameter Name | Value (Metric / Imperial) | Description |
| :--- | :--- | :--- |
| `SledWidth` | $381.0\text{ mm}$ ($15.0\text{ in}$) | Outer steel sled cowl width |
| `SledLength` | $457.2\text{ mm}$ ($18.0\text{ in}$) | Outer steel sled cowl length |
| `SledHeight` | $130.0\text{ mm}$ ($5.12\text{ in}$) | Outer steel sled cowl height |
| `SkirtHeight` | $50.8\text{ mm}$ ($2.0\text{ in}$) | Vertical perimeter ground skirt height |
| `GroundClearance` | $12.7\text{ mm}$ ($0.5\text{ in}$) | Skid-to-ground operating clearance |
| `SheetThickness` | $1.905\text{ mm}$ ($0.075\text{ in}$) | 14-gauge mild steel sheet thickness |
| `HandTruckRiserWidth` | $370.0\text{ mm}$ ($14.57\text{ in}$) | Hand truck center-to-center riser width ($X = \pm 185\text{ mm}$) |
| `HandTruckHeight` | $1250.0\text{ mm}$ ($49.2\text{ in}$) | Hand truck total upright height |
| `WheelDiameter` | $254.0\text{ mm}$ ($10.0\text{ in}$) | Heavy-duty rubber tire diameter |
| `TrackWidth` | $490.0\text{ mm}$ ($19.3\text{ in}$) | Wheel track width center-to-center |
| `AxleDiameter` | $15.875\text{ mm}$ ($5/8\text{ in}$) | Solid steel cold-rolled through-axle |
| `BurnerBTU` | $60,000.0\text{ BTU/hr}$ | Solaronics ceramic infrared thermal input rating |

---

## 3. Structural Assembly Tree

The master assembly document `road-roaster.FCStd` consists of the following modular subassembly containers:

```
road-roaster.FCStd (Road Roaster Master Assembly)
├── dims (App::VarSet)
├── 1. Commercial Hand Truck Chassis (Cut-Away Toe Plate & 10in Wheels)
│   └── (Imported from components/commercial_hand_truck/commercial_hand_truck.FCStd)
│       ├── HandTruck_Tubular_Frame (1.0" OD tubular steel risers, top loop & ladder slats)
│       ├── HandTruck_Axle_Brackets (3/16" steel axle hanger plates & pivot tabs)
│       ├── HandTruck_Solid_Axle (5/8" solid steel through-axle & lock collars)
│       ├── HandTruck_Wheel_Rims (Stamped steel wheel hubs)
│       ├── HandTruck_Rubber_Tires (10" heavy-duty pneumatic/rubber tires)
│       └── HandTruck_Handle_Grips (Molded vinyl grips)
├── 2. Directional Radiant Ceramic Infrared Sled & Ground Skids
│   ├── Radiant_Sled_Outer_Cowl (14-gauge steel cowl with front draft vent & perimeter skirts)
│   ├── Radiant_Sled_Skid_Runners (1.5" x 3/16" flat bar skids with 30° ski tips)
│   ├── Radiant_Sled_Suspension_Bridge (Suspension bridge plate & transit latch catch tower)
│   └── (Imported from components/solaronics_infrared_burner/solaronics_infrared_burner.FCStd)
│       ├── Solaronics_Ceramic_Plaque (173 sq. in cordierite grooved ceramic face @ 1,800°F)
│       ├── Solaronics_Wire_Grid (Inconel / 304 SS re-radiating mesh screen)
│       ├── Solaronics_Parabolic_Reflector (Mirror-bright parabolic aluminum reflector)
│       ├── Solaronics_Venturi_Manifold (Atmospheric premix air induction chamber)
│       └── Solaronics_Brass_Gas_Inlet (Precision brass orifice jet & 1/2" NPT inlet)
├── 3. Trailing Swing-Arm Suspension & Dual-Mode Tilt Latch
│   ├── Suspension_Trailing_Swing_Arms (1.5" x 3/16" trailing swing arms with pivot pins)
│   └── Transit_Tilt_Snap_Latch (Foot-release upright vacuum tilt snap latch)
└── 4. Propane Gas Train, 11in W.C. Regulator & Cockpit Controls
    ├── (Imported from components/propane_cylinder_1lb/propane_cylinder_1lb.FCStd)
    ├── (Imported from components/propane_harness/propane_harness.FCStd)
    ├── Propane_Low_Pressure_Regulator (11" W.C. low-pressure LP gas regulator)
    ├── (Imported from components/torch_control_handle/torch_control_handle.FCStd)
    ├── Propane_Flexible_Gas_Hoses (1/4" 350 PSI flexible supply and feed lines)
    └── Spark_Ignition_Wire (High-voltage silicone spark lead)
```

---

## 4. Materials & Manufacturing Specifications

- **Chassis Base**: Commercial 600–800 lb rated heavy-duty tubular steel hand truck (modified by cutting away forward toe plate).
- **Wheels & Axle**: Dual 10.0" $\times$ 3.5" pneumatic/solid rubber tires with ball bearings on a continuous $5/8''$ ($15.875\text{ mm}$) 1018 cold-rolled steel through-axle with zinc clamp collars.
- **Sled Cowl & Skirts**: 14-gauge Hot-Rolled Mild Steel Sheet (CNC plasma cut, press brake formed, MIG welded).
- **Skid Runners**: $1.5'' \times 3/16''$ Steel Flat Bar with $30^\circ$ turned-up front/rear ski tips.
- **Radiant Burner**: Solaronics Cordierite Ceramic Plaque Array ($173\text{ sq. in}$, $60,000\text{ BTU/hr}$) with mirror-bright polished aluminum deep parabolic reflector and Inconel wire mesh.
- **Gas Regulation**: Low-Pressure LP Regulator ($11''\text{ W.C.} \approx 0.4\text{ PSI}$) with $1/4''$ high-pressure flexible rubber feed lines.
- **Operator Controls**: Top flow-back loop handle cockpit with needle valve, dead-man turbo boost lever, and push-button piezo igniter.

---

## 5. Operational Protocols & Field Guidelines

1. **Ignition & Pilot Setup**:
   - Open propane cylinder valve.
   - Adjust regulator to $11''\text{ W.C.}$; crack handle needle valve 1/4 turn.
   - Depress push-button piezo sparker; ceramic tiles will ignite gently across micro-pores, turning glowing cherry-red ($1,800^\circ\text{F}$) within 15–20 seconds.
2. **Glide Scorching (Walking Pace: 1–2 mph)**:
   - Disengage foot tilt-latch to let sled rest flat on skids.
   - Squeeze dead-man trigger while walking along gravel corridor.
   - 1–2 second pure radiant pulse ruptures plant cells without flame blow-out or flying gravel. Weeds wither within 24 hours.
3. **Deep Root Heat-Soak (Stationary Dwell: 15–30 sec)**:
   - For perennial taproots (dandelions, thistles), halt sled over root crown for 15–30 seconds. Concentrated downward radiant flux heats soil 1–2" deep to destroy root crowns and sterilize dormant weed seeds.
4. **Transit Mode**:
   - Step on foot latch to engage snap catch onto sled bridge tower.
   - Tilt handle back; roll effortlessly on 10.0" rubber wheels over curbs, turf, and pavement.
