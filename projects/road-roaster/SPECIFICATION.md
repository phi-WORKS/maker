# Road Roaster — Master Technical Specification

> **Directional Thermal Weed Shock Sled**  
> *Single-Source Architectural & Engineering Specification*

---

## 1. Executive Summary & Problem-Solution Engineering

The **Road Roaster** is a directional thermal weed management platform engineered to eradicate invasive hardscape weeds (gravel driveways, agricultural headlands, roadside corridors, paver paths) through concentrated radiant cellular shock without chemical herbicides or open-flame fuel waste.

### The Ecological & Shop Problem
* **The Chemical Trap**: Synthetic herbicides (glyphosate, 2,4-D) poison groundwater, threaten pets and native pollinators, foster chemical-resistant weeds, and leave toxic residues in soils.
* **The Open-Air Torch Energy Trap**: Conventional handheld weed torches lose over 85% of their thermal energy to atmospheric wind dissipation, consuming excessive propane while presenting an open fire hazard.
* **Mechanical Removal Inefficacy**: Hand-pulling leaves deep taproots intact to regrow, while string trimmers fling hazardous gravel projectiles.

### Core Thermodynamic & Design Solutions
1. **Enclosed Radiant Heat Trap**:
   - The 14-gauge mild steel pyramid hood and 2.0" ground skirts enclose the $500,000\text{ BTU/hr}$ burner, trapping superheated air and reradiating infrared energy downward into the soil matrix with over 80% thermal efficiency.
2. **Directional Forward-Firing Asymmetrical Hood**:
   - **Steep Rear Heat Shield**: Apex is offset rearward ($Y_{apex} = +110.0\text{ mm}$), creating an $\approx 66^\circ$ rear wall that shields the operator, wheels, and fuel cylinder from radiant heat.
   - **Forward Radiant Roof Ramp**: An $\approx 28^\circ$ forward slope directs high-velocity flame and thermal waves forward across the weed bed, expelling exhaust safely through the front vent ($Y = -228.6\text{ mm}$).
3. **Deep Conductive Heat-Soak Station**:
   - In stationary dwell mode, the closed hood traps heat, conducting $180^\circ\text{F}$ ($82^\circ\text{C}$) thermal energy **1 to 2 inches below the surface** to destroy stubborn perennial taproots (dandelions, thistles, bindweed) and sterilize dormant weed seed banks.
4. **Decomposed Dead-Man Gas Train**:
   - **Top Crossbar Cockpit** ([`components/torch_control_handle/`](../../components/torch_control_handle/)): Thumb needle valve (pilot flame/shutoff), dead-man turbo squeeze boost lever (hold-to-roast), and push-button piezo igniter.
   - **Chassis Burner Head** ([`components/torch_burner_head/`](../../components/torch_burner_head/)): Cast venturi air cone, brass jet orifice, 2.5" black steel combustion bell, and high-voltage ceramic electrode.
   - **Right-Upright Propane Mounting**: 1 lb canister clamped to the right vertical riser with zero line crossovers.
5. **Continuous Solid Through-Axle & Dual-Mode Upright Vacuum Tilt**:
   - Continuous $1/2''$ solid steel axle tie-rod absorbs all torsional loads.
   - Foot-release snap latch enables instant switching between ground-gliding roasting mode and non-contact rolling transit mode over grass, lawns, and curbs.

---

## 2. Parametric VarSet (`dims`) Specification

All dimensions are managed parametrically in FreeCAD via `App::VarSet` (`dims`):

| Parameter Name | Value (Metric / Imperial) | Description |
| :--- | :--- | :--- |
| `BaseWidth` | $457.2\text{ mm}$ ($18.0\text{ in}$) | Pyramidal hood base width |
| `BaseLength` | $457.2\text{ mm}$ ($18.0\text{ in}$) | Pyramidal hood base length |
| `ApexWidth` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Top apex exhaust opening width |
| `ApexLength` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Top apex exhaust opening length |
| `ApexOffsetY` | $110.0\text{ mm}$ ($4.33\text{ in}$) | Rearward apex offset from center for directional draft |
| `HoodHeight` | $152.4\text{ mm}$ ($6.0\text{ in}$) | Hood vertical rise height |
| `SkirtHeight` | $50.8\text{ mm}$ ($2.0\text{ in}$) | Vertical perimeter skirt extension |
| `SheetThickness` | $1.905\text{ mm}$ ($0.075\text{ in}$) | 14-gauge mild steel sheet thickness |
| `WheelDiameter` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Solid machined steel wheel diameter |
| `TrackWidth` | $533.4\text{ mm}$ ($21.0\text{ in}$) | Outer wheel track width |
| `HandleLength` | $1219.2\text{ mm}$ ($48.0\text{ in}$) | U-frame upright handle tube length |
| `HandleWidth` | $482.6\text{ mm}$ ($19.0\text{ in}$) | U-frame handle riser center-to-center width |
| `BurnerPitchAngle` | $30.0^\circ$ | Downward forward burner incline pitch angle |

---

## 3. Structural Assembly Tree

The assembly document `road-roaster.FCStd` consists of the following modular subassembly containers:

```
road-roaster.FCStd (Road Roaster Master Assembly)
├── dims (App::VarSet)
├── 1. Directional Asymmetrical Hood & Skid Subassembly
│   ├── Asymmetrical_Directional_Hood (Part::Feature - 14-ga offset-apex hood, skirts, front vent & rear axle arms)
│   ├── Corner_Gussets_AngleIron (Part::Feature - 4x Corner angle iron gussets)
│   └── Dual_Skid_Runners (Part::Feature - 1.5" x 3/16" flat bar skids with 30° tips)
├── 2. Forward-Firing 500k BTU Burner Head Subassembly
│   ├── (Imported from components/torch_burner_head/torch_burner_head.FCStd)
│   └── Burner_Mount_Overhead_Bridge (Part::Feature - Apex mounting plate & latch catch tower)
├── 3. Dual Solid Steel Wheel & Axle Subassembly
│   ├── Left 4" Solid Steel Wheel (Imported from components/steel_caster_wheel/steel_caster_wheel.FCStd)
│   ├── Right 4" Solid Steel Wheel (Imported from components/steel_caster_wheel/steel_caster_wheel.FCStd)
│   └── Solid_Through_Axle_Tie_Rod (Part::Feature - Continuous 1/2" solid cold-rolled steel through-axle shaft & lock collars)
├── 4. Dual-Pivot U-Handle & Operator Cockpit Subassembly
│   ├── HandTruck_U_Frame_Handle (Part::Feature - 3/4" square tube U-frame, top grip & cross-braces)
│   ├── Tilt_Back_Vacuum_Snap_Latch (Part::Feature - Upright vacuum foot-release snap catch linkage)
│   └── (Imported from components/torch_control_handle/torch_control_handle.FCStd)
└── 5. Propane Gas-Train & Spark Ignition Subassembly
    ├── (Imported from components/propane_harness/propane_harness.FCStd)
    ├── (Imported from components/propane_cylinder_1lb/propane_cylinder_1lb.FCStd)
    ├── Propane_Supply_Hose_Cylinder_To_Cockpit (Part::Feature - 1/4" Flexible supply line)
    ├── Burner_Feed_Hose_Cockpit_To_Burner (Part::Feature - 1/4" 350 PSI High-pressure feed line)
    └── High_Voltage_Ignition_Spark_Wire (Part::Feature - Silicone spark ignition lead)
```

---

## 4. Materials & Manufacturing Specifications

- **Hood & Skirts**: 14-gauge Hot-Rolled Mild Steel Sheet (CNC plasma cut, press brake formed, MIG welded).
- **Skid Runners**: $1.5'' \times 3/16''$ Steel Flat Bar with $30^\circ$ turned-up front/rear ski tips.
- **U-Handle Frame**: $3/4'' \times 3/4'' \times 1/8''$ Mild Steel Square Tubing with round crossbar and high-traction rubber grips.
- **Solid Axle**: Continuous $1/2''$ ($12.7\text{ mm}$) Cold-Rolled 1018 Steel Round Rod with dual zinc-plated clamp collars.
- **Wheels**: Dual $4.0'' \times 1.5''$ solid machined cast steel / ductile iron wheels.
- **Gas Controls**: Forged brass dual-stage manifold with needle pilot valve, dead-man turbo squeeze lever, and push-button piezo igniter.
- **Burner Head**: 2.5" black steel combustion bell with cast venturi oxygen mixing cone and precision brass orifice jet ($500,000\text{ BTU/hr}$).
- **Fuel System**: Standard 1 lb Propane Cylinder mounted in quick-release steel bottle harness with 350 PSI flexible rubber hoses.

---

## 5. Operational Protocols & Field Guidelines

1. **Ignition & Pilot Setup**:
   - Open cylinder valve.
   - Crack top needle valve knob 1/4 turn to initiate low pilot gas flow.
   - Depress red push-button piezo igniter to establish internal pilot flame.
2. **Glide Scorching (Walking Pace: 1–2 mph)**:
   - Disengage foot tilt-latch to let hood rest flat on skids.
   - Squeeze and hold top crossbar dead-man lever while walking along gravel/driveway corridor.
   - 2–3 second thermal pulse ruptures plant cells. Weeds will wither and desiccate within 24 hours.
3. **Deep Heat-Soak Station (Dwell Time: 15–30 sec)**:
   - For mature perennial weeds (thistle, dandelion, bindweed), halt sled directly over root crown.
   - Hold squeeze lever for 15–30 seconds.
   - Trapped heat conducts $180^\circ\text{F}$ energy 1–2" into upper soil, sterilizing taproots and ungerminated seeds.
4. **Transit Over Turf / Asphalt**:
   - Step down on foot-latch pedal to engage snap catch onto hood bridge.
   - Tilt handle back; roll smoothly on 4.0" steel wheels.
