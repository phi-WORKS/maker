# Road Roaster — Master Technical Specification

> **Directional Upright-Vacuum Thermal Weed Shock Sled**  
> *Single-Source Architectural & Engineering Specification*

---

## 1. Executive Summary & Design Purpose

The **Road Roaster** is a directional thermal weed management machine designed for agricultural beds, gravel driveways, pathways, and municipal roadside weed shock abatement.

### Core Design Objectives
1. **Directional Forward-Firing Asymmetrical Hood**:
   - **Aerodynamic Heat Deflector**: The apex is offset rearward ($Y_{apex} = +110.0\text{ mm}$), creating a steep $\approx 66^\circ$ rear heat shield that protects the operator, wheels, and handle while forming a long forward-sloping radiant roof ramp ($\approx 28^\circ$).
   - **Forward Heat Channeling**: The $500,000\text{ BTU/hr}$ burner fires downward and forward at a $30^\circ$ pitch, driving radiant heat and hot combustion gases across the weed bed and out the front exhaust vent, completely away from the operator.
2. **Decomposed Gas-Train & Safety Squeeze Cockpit**:
   - **Handle Control Cockpit** (`components/torch_control_handle/`): Clamped to the upper right U-frame handle within natural grip reach. Includes a master needle valve knob (pilot adjustment & emergency shutoff), a dead-man turbo squeeze boost lever (hold-to-scorch), and a push-button piezo spark igniter.
   - **Chassis Burner Head** (`components/torch_burner_head/`): Hard-mounted to the rear apex of the hood with cast venturi air induction cone, precision brass orifice jet, 2.5" combustion bell, and high-voltage ceramic electrode.
   - **Flexible Plumbing**: 350 PSI flexible LP hose and spark ignition wire connect the handle cockpit to the chassis burner.
3. **Upright-Vacuum Dual-Mode Kinematics**:
   - **Roasting Mode**: Latch disengaged; hood skids glide flush with ground surfaces.
   - **Transit Mode**: Latch engaged; tilting the handle back pivots the unit on the rear $4.0''$ solid steel wheels ($Y_{axle} = +280.0\text{ mm}$), levering the entire front hood high off the ground for non-contact transit over lawns and asphalt.

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

- **Hood & Skirts**: 14-gauge Hot-Rolled Mild Steel Sheet (CNC cut, brake formed, welded).
- **Skid Runners**: $1.5'' \times 3/16''$ Steel Flat Bar with $30^\circ$ turned-up skids.
- **U-Handle Frame**: $3/4'' \times 3/4'' \times 1/8''$ Steel Square Tubing with round crossbar and rubber grips.
- **Wheels**: Dual $4.0'' \times 1.5''$ solid machined cast steel wheels with $1/2''$ Grade 5 zinc-plated axle bolts.
- **Gas Controls**: Forged brass dual-stage manifold with needle pilot valve, dead-man turbo squeeze lever, and push-button piezo igniter.
- **Burner Head**: 2.5" black steel combustion bell with cast venturi oxygen mixing cone and precision brass orifice jet ($500,000\text{ BTU/hr}$).
- **Fuel System**: Standard 1 lb Propane Cylinder mounted in quick-release steel bottle harness with 350 PSI flexible rubber hoses.
