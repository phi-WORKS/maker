# Road Roaster — Master Technical Specification

> **Upright Vacuum / Hand-Truck Thermal Weed Shock Sled**  
> *Single-Source Architectural & Engineering Specification*

---

## 1. Executive Summary & Design Purpose

The **Road Roaster** is a mobile thermal weed shock sled designed for agricultural rows, gravel driveways, walkways, and roadside non-chemical thermal weed management.

### Core Design Objectives
1. **Upright-Vacuum Dual-Mode Kinematics**:
   - **Roasting Mode (Ground Contact)**: Latch released; 14-gauge pyramidal hood rests flat on dual bottom skids, trapping intense radiant heat within $0.5''$ of gravel or soil surfaces.
   - **Transit Mode (Non-Contact Rolling)**: Latch engaged; tilting the U-shaped handle backward levers the hood and skids completely off the ground over the rear wheel axle, allowing smooth rolling transport across grass, turf, asphalt, or rough terrain without dragging or scorching.
2. **Dual-Pivot Hand-Truck Frame**: Dual side pivot mounts and a 48" high-visibility U-shaped tubular frame provide torsional rigidity for nimble steering, 360° pivoting, and balanced ergonomic operation.
3. **Heavy-Duty All-Metal Casters**: Standalone $4.0''$ solid steel wheels resist radiant burner heat and roll effortlessly over loose gravel and rocks.
4. **Onboard Fuel Integration**: Central U-frame cross-member houses the 1 lb propane bottle harness and cylinder for optimal center-of-gravity balance and quick bottle swaps.
5. **Component Modularity**: Consumes external commercial and fabricated CAD modules (`torch_hf91037`, `propane_cylinder_1lb`, `propane_harness`, `steel_caster_wheel`) imported directly from `components/`.

---

## 2. Parametric VarSet (`dims`) Specification

All dimensions are managed parametrically in FreeCAD via `App::VarSet` (`dims`):

| Parameter Name | Value (Metric / Imperial) | Description |
| :--- | :--- | :--- |
| `BaseWidth` | $457.2\text{ mm}$ ($18.0\text{ in}$) | Pyramidal hood base width |
| `BaseLength` | $457.2\text{ mm}$ ($18.0\text{ in}$) | Pyramidal hood base length |
| `ApexWidth` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Top apex exhaust opening width |
| `ApexLength` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Top apex exhaust opening length |
| `HoodHeight` | $152.4\text{ mm}$ ($6.0\text{ in}$) | Pyramidal rise height |
| `SkirtHeight` | $50.8\text{ mm}$ ($2.0\text{ in}$) | Vertical perimeter skirt extension |
| `SheetThickness` | $1.905\text{ mm}$ ($0.075\text{ in}$) | 14-gauge mild steel sheet thickness |
| `WheelDiameter` | $101.6\text{ mm}$ ($4.0\text{ in}$) | Heavy-duty solid steel wheel diameter |
| `TrackWidth` | $533.4\text{ mm}$ ($21.0\text{ in}$) | Outer wheel track width |
| `HandleLength` | $1219.2\text{ mm}$ ($48.0\text{ in}$) | U-frame upright handle tube length |
| `HandleWidth` | $482.6\text{ mm}$ ($19.0\text{ in}$) | U-frame handle riser center-to-center width |

---

## 3. Structural Assembly Tree

The assembly document `road-roaster.FCStd` consists of the following modular subassembly containers:

```
road-roaster.FCStd (Road Roaster Master Assembly)
├── dims (App::VarSet)
├── 1. Pyramid Hood & Skid Subassembly
│   ├── Pyramidal_Hood_Heat_Flange (Part::Feature - 14-ga Hood, skirts, side mounting wings & pivot ears)
│   ├── Corner_Gussets_AngleIron (Part::Feature - 4x Corner angle iron gussets)
│   └── Dual_Skid_Runners (Part::Feature - 1.5" x 3/16" flat bar skids with 30° tips)
├── 2. Overhead Torch Mounting Frame
│   └── Overhead_Torch_Mounting_Frame (Part::Feature - Overhead bridge, clamp sleeve & latch catch tower)
├── 3. Harbor Freight #91037 Torch Subassembly
│   └── (Imported from components/torch_hf91037/torch_hf91037.FCStd)
├── 4. Dual Metal Wheel & Axle Subassembly
│   ├── Left 4" Steel Caster Wheel (Imported from components/steel_caster_wheel/steel_caster_wheel.FCStd)
│   ├── Right 4" Steel Caster Wheel (Imported from components/steel_caster_wheel/steel_caster_wheel.FCStd)
│   └── Chassis_Pivot_Axle_Pins (Part::Feature - 1/2" Zinc-plated axle pivot hardware)
├── 5. Dual-Pivot U-Handle & Tilt Latch Subassembly
│   ├── HandTruck_U_Frame_Handle (Part::Feature - 3/4" square tube U-frame, top grip & cross-braces)
│   └── Tilt_Back_Vacuum_Snap_Latch (Part::Feature - Upright vacuum foot-release snap catch linkage)
└── 6. Propane Bottle Harness & Tank Subassembly
    ├── (Imported from components/propane_harness/propane_harness.FCStd)
    ├── (Imported from components/propane_cylinder_1lb/propane_cylinder_1lb.FCStd)
    └── High_Pressure_Propane_Extension_Hose (Part::Feature - Flexible gas line)
```

---

## 4. Materials & Manufacturing Specifications

- **Hood & Skirts**: 14-gauge Hot-Rolled Mild Steel Sheet (plasma/laser cut, brake formed, fully welded).
- **Skid Runners**: $1.5'' \times 3/16''$ Steel Flat Bar with $30^\circ$ turned-up approach and departure skids.
- **U-Handle Frame**: $3/4'' \times 3/4'' \times 1/8''$ Steel Square Tubing with round crossbar and high-traction grips.
- **Wheels**: Dual $4.0'' \times 1.5''$ solid machined cast steel wheels with $1/2''$ Grade 5 zinc-plated axle bolts.
- **Tilt Latch Linkage**: Spring-loaded steel snap catch with high-visibility red foot-release pedal tab.
- **Torch Component**: Harbor Freight #91037 ($500,000\text{ BTU/hr}$ Propane Torch with Piezo Igniter).
- **Fuel System**: Standard 1 lb Propane Cylinder mounted in quick-release steel bottle harness.
