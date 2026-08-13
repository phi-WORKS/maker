# Technical Specification — Road Roaster Version 1.4.0

**Project**: Road Roaster (Towable Thermal Weed Shock Sled)  
**Version**: `v1.4.0`  
**Status**: 🟡 **`[IN PROGRESS]`**  

---

## 1. Executive Summary & Design Milestones

Version 1.4.0 introduces onboard fuel bottle mounting, quick-release harness integration, and script refactoring:
1. **Onboard Propane Harness & Bottle**: Mounts a quick-slip bike-style canister harness (`components/propane_harness/`) onto the upper section of the 5 ft square tube tow bar, seating a 1 lb disposable or refillable propane cylinder (`components/propane_cylinder_1lb/`) within ergonomic reach of the operator ($Z \approx 750\text{--}850\text{ mm}$).
2. **Flexible High-Pressure Hose Line**: Connects the 1"-20 UNEF top valve of the mounted 1 lb propane bottle directly to the brass flow control knob on the torch wand handle, eliminating the need for shoulder straps or backpack rigs.
3. **Modular Function-Level Script Refactoring**: Structurally decomposes `v1.4.0/build.py` into dedicated subassembly builder functions (`build_hood_subassembly`, `build_overhead_frame_subassembly`, `build_torch_subassembly`, `build_propane_harness_subassembly`, `build_tow_rigging_subassembly`).

---

## 2. Key Dimensions & Parameters

| Parameter | Value (Imperial) | Value (Metric) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Hood Base Width** | $18.0''$ | $457.2\text{ mm}$ | Footprint width across skids |
| **Hood Base Length** | $18.0''$ | $457.2\text{ mm}$ | Footprint length along travel direction |
| **Pyramid Rise Height** | $6.0''$ | $152.4\text{ mm}$ | Pyramidal canopy height |
| **Skirt Extension Height** | $2.0''$ | $50.8\text{ mm}$ | Vertical heat containment skirt |
| **Ground Clearance** | $0.5''$ | $12.7\text{ mm}$ | Skid runner elevation off soil |
| **Torch Wand Angle** | $35.0^\circ$ | $35.0^\circ$ | Forward lean toward operator |
| **Tow Bar Tube** | $3/4'' \times 3/4'' \times 5\text{ ft}$ | $19.05 \times 19.05 \times 1524\text{ mm}$ | Rigid square steel tube |
| **Clevis Drop-Stop Angle** | $20.0^\circ$ | $20.0^\circ$ | Minimum rest angle above horizontal |
| **Harness Mount Height** | $\approx 31.5''\text{--}35.4''$ | $800\text{--}900\text{ mm}$ | Elevation on tow bar tube |
| **Propane Cylinder OD** | $3.875''$ | $98.4\text{ mm}$ | Standard 1 lb cylinder body OD |
| **Harness Inner Clearance**| $3.94''$ | $100.0\text{ mm}$ | ID for slip-in bottle fit |

---

## 3. Subassembly Architecture

```
road_roaster_v5 (FreeCAD Document)
├── 1. Pyramid Hood & Skid Subassembly (App::DocumentObjectGroup)
│   ├── Pyramidal_Hood_Heat_Flange (14-ga mild steel + heat flange)
│   ├── Corner_Gussets_AngleIron (1/8" structural corner gussets)
│   └── Dual_Skid_Runners (1.5" x 3/16" flat bar with 30° turned-up tips)
├── 2. Overhead Torch Mounting Frame (App::DocumentObjectGroup)
│   └── Overhead_Torch_Mounting_Frame (3/16" steel bridge + sleeve ring)
├── 3. Harbor Freight #91037 Torch Subassembly (App::DocumentObjectGroup)
│   ├── HF_Burner_Head_Nozzle (3.0" bell nozzle recessed 1.5" into apex)
│   ├── Torch_Chrome_Wand_Shaft (3/8" chrome shaft, 500 mm length)
│   ├── HF_Blue_Torch_Handle (Molded grip & squeeze lever)
│   ├── Brass_Flow_Control_Knob (1/4" NPT brass needle valve)
│   └── Piezo_Igniter_Module (Push-button igniter & lead wire)
├── 4. Propane Bottle Harness & Tank Subassembly (App::DocumentObjectGroup)
│   ├── Harness_Rear_Mounting_Spine (3/16" spine + 3/4" square tube clamps)
│   ├── Bottom_Seat_Cup_Support (100 mm ID cup seat with drain hole)
│   ├── Retention_Arms_Upper_Hoop (1/8" x 3/4" curved steel hoops)
│   ├── Quick_Release_Latch_Knob (Red knurled thumb-screw latch)
│   ├── Cylinder_Steel_Body (1 lb green propane cylinder body + base collar)
│   ├── Brass_Threaded_Valve_1in20 (1"-20 UNEF valve stem)
│   └── High_Pressure_Propane_Extension_Hose (Flexible rubber extension hose)
└── 5. Forward Tow Rigging Subassembly (App::DocumentObjectGroup)
    ├── Front_Clevis_Hitch_With_StopTab (Dual 3/16" clevis ears + 20° stop tab)
    ├── Clevis_Pin_38in (3/8" hitch pin)
    └── Forward_Rigid_Tow_Bar_5ft (5 ft 3/4" square tube + rubber T-grip)
```
