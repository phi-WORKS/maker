# Road Roaster — Master Bill of Materials & Fabrication Cut List

> **Automated Physical Design & Procurement Specification (v0.7.0)**  
> *Generated on 2026-09-07 via `phi_works.maker.bom`*

---

## Executive Summary & Weight Rollup

| Classification | Line Items | Total Weight (lb) | Weight Share | Role / Scope |
| :--- | :---: | :---: | :---: | :--- |
| **Commercial / Acquired (COTS)** | 4 | 47.10 lb | 67.8% | Complete donor chassis, burner engines, pressure vessels |
| **Custom Fabricated Parts** | 6 | 20.39 lb | 29.3% | Formed sheet metal, welded flat bar skids & linkages |
| **Hardware, Fluid & Electrical** | 4 | 1.99 lb | 2.9% | Valves, LP hoses, wiring, retention hardware |
| **Total Assembly Machine** | **14** | **69.49 lb** | **100.0%** | **Operating machine weight (empty fuel)** |

---

## 1. Commercial & Acquired Components (COTS Procurement List)

Commercial off-the-shelf assemblies acquired as complete units. **Do not fabricate in-house**.

| Item Description | Component ID | Category | Qty | Vendor / Source | Part / Model # | Unit Wt | Subassembly / Reference |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **Commercial Tubular Steel Hand Truck Chassis** | [`commercial_hand_truck`](components/commercial_hand_truck/README.md) | Chassis / Running Gear | 1 | Donor / Restored Commercial Equipment | `HANDTRUCK-VINTAGE-01` | 24.5 lb | 1. Vintage Hand Truck Chassis (U-Frame, Triangular Axle Trusses, 9.5in Wheels) |
| **Solaronics High-Intensity Ceramic Infrared Burner** | [`solaronics_infrared_burner`](components/solaronics_infrared_burner/README.md) | Thermal Engine / Radiant Burner | 1 | Solaronics USA | `K-60 / 60,000 BTU` | 18.5 lb | 2. Forward Directional Radiant Ceramic Infrared Sled & Ground Skids |
| **1 lb Disposable / Refillable Propane Cylinder** | [`propane_cylinder_1lb`](components/propane_cylinder_1lb/README.md) | Fuel System / Pressure Vessel | 1 | Worthington / Flame King / Coleman | `DOT-39 / 16.4 oz` | 1.9 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |
| **1 lb Propane Bottle Retention Harness** | [`propane_harness`](components/propane_harness/README.md) | Fuel System / Mounting | 1 | Custom Fabricated / Commercial Quick-Release Bike Cage | `BOTTLE-CAGE-1LB` | 2.2 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |

*Subtotal Commercial Hardware Weight: **47.10 lb***

---

## 2. Custom Fabricated Parts & Machine Shop Cut List

Custom metal components fabricated in the shop from raw stock materials.

| Mark | Part Name | Subassembly | Material | Raw Stock Profile | Cut Dimensions (L × W × T) | Qty | Unit Wt | Primary Operations |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **P-SLED-01** | **14-Gauge Steel Protective Radiant Sled Cowl & Skirts** | 2. Forward Directional Radiant Ceramic Infrared Sled & Ground Skids | `Steel-A36` | 14-Ga (0.075") Sheet Steel | 18.00" × 15.00" × 0.075"<br>(457.2 × 381.0 × 1.90 mm) | 1 | 9.58 lb | CNC plasma cut vents, press brake 90° skirt bends, corner seam welds |
| **P-SLED-02** | **Continuous Flat Bar Skid Runners with 30-deg Ski Tips** | 2. Forward Directional Radiant Ceramic Infrared Sled & Ground Skids | `Steel-304Stainless` | 1-1/2" × 3/16" Flat Bar | 21.46" × 1.50" × 0.187"<br>(545.2 × 38.1 × 4.76 mm) | 1 | 3.49 lb | Cut to length, 30° cold tip bends front & rear, drill mounting holes |
| **P-SLED-03** | **Sled Suspension Bridge & Transit Latch Catch Tower** | 2. Forward Directional Radiant Ceramic Infrared Sled & Ground Skids | `Steel-A36` | 2-1/2" × 3/16" Flat Bar & Ø1/2" Pin | 15.39" × 2.36" × 0.187"<br>(391.0 × 60.0 × 4.76 mm) | 1 | 3.41 lb | Cut plate to length, weld upright catch tower pin |
| **P-SUSP-01** | **Axle-Mounted Triangular Sled Suspension Straps (Common Pivot Axis)** | 3. Common-Axis Triangular Sled Suspension Straps & Transit Tilt Latch | `Steel-A36` | 1.0" × 3/16" Flat Bar & 1.0" OD Sleeve | 12.40" × 1.00" × 0.187"<br>(315.0 × 25.4 × 4.76 mm) | 1 | 2.92 lb | Miter cut 3/16" bar, ream axle pivot sleeve bushings, weld triangulated truss |
| **P-SUSP-02** | **Foot-Release Upright Vacuum Tilt Snap Latch** | 3. Common-Axis Triangular Sled Suspension Straps & Transit Tilt Latch | `Steel-ZincPlated` | 5/8" × 1/4" Flat Bar & Ø3/8" Pin | 5.57" × 0.59" × 0.236"<br>(141.4 × 15.0 × 6.00 mm) | 1 | 0.45 lb | Cut to length, weld foot pedal pad & catch hook |
| **P-GAS-01** | **Propane Harness Horizontal Cross-Strap Clamping Brackets** | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve | `Steel-A36` | 2.0" × 3/16" Flat Bar | 4.08" × 1.97" × 0.187"<br>(103.8 × 50.0 × 4.76 mm) | 1 | 0.54 lb | Form cross-strap clamping lips, drill 1/4" bolt clearance holes |

*Subtotal Custom Fabricated Parts Weight: **20.39 lb***

---

## 3. Raw Stock Requisition & Material Nesting Summary

Consolidated raw stock material requirements for inventory purchasing and shop prep.

| Raw Material Grade | Stock Specification | Profile Type | Total Required | Piece Count | Total Wt | Member Part Marks |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| `Steel-304Stainless` | **1-1/2" × 3/16" Flat Bar** | Flat Bar | **1.79 ft** (21.5 in) | 1 | 3.49 lb | `P-SLED-02` |
| `Steel-A36` | **1.0" × 3/16" Flat Bar & 1.0" OD Sleeve** | Flat Bar & Bushing | **1.03 ft** (12.4 in) | 1 | 2.92 lb | `P-SUSP-01` |
| `Steel-A36` | **14-Ga (0.075") Sheet Steel** | Sheet Metal | **1.88 sq ft** (270.0 sq in) | 1 | 9.58 lb | `P-SLED-01` |
| `Steel-A36` | **2-1/2" × 3/16" Flat Bar & Ø1/2" Pin** | Flat Bar & Pin | **1.28 ft** (15.4 in) | 1 | 3.41 lb | `P-SLED-03` |
| `Steel-A36` | **2.0" × 3/16" Flat Bar** | Flat Bar | **0.34 ft** (4.1 in) | 1 | 0.54 lb | `P-GAS-01` |
| `Steel-ZincPlated` | **5/8" × 1/4" Flat Bar & Ø3/8" Pin** | Flat Bar & Pin | **0.46 ft** (5.6 in) | 1 | 0.45 lb | `P-SUSP-02` |

---

## 4. Hardware, Fluid Lines & Electrical Controls

Fittings, regulation valves, reinforced fuel hoses, retention brackets, and ignition wiring.

| Item Description | Category | Material | Specification / Model | Qty | Total Wt | Subassembly / Location |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **Tank-Mounted Rotary Flow Control Valve & 11in Regulator** | Plumbing & Fuel Lines | `Brass-C360` | Tank Mounted Regulator Valve | 1 | 0.85 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |
| **Center Support Pipe Hose & Wire Retention Clips** | Plumbing & Fuel Lines | `Steel-ZincPlated` | Center Spine Hose Clips | 1 | 0.06 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |
| **Flexible 3/8in Reinforced LP Gas Hose (Center Support Routed)** | Plumbing & Fuel Lines | `Rubber-Solid` | Flexible Gas Feed Hose | 1 | 0.87 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |
| **High-Voltage Silicone Spark Ignition Wire (Center Support Routed)** | Electrical & Ignition | `PowderCoat-StihlOrange` | Flexible Spark Ignition Wire | 1 | 0.22 lb | 4. Propane Gas Train & Tank-Mounted Rotary Flow Control Valve |

*Subtotal Hardware & Controls Weight: **1.99 lb***

---
