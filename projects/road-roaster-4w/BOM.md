# Road Roaster 4W — Master Bill of Materials & Fabrication Cut List

> **Automated Physical Design & Procurement Specification (v0.1.0)**  
> *Generated on 2026-09-07 via `phi_works.maker.bom`*

---

## Executive Summary & Weight Rollup

| Classification | Line Items | Total Weight (lb) | Weight Share | Role / Scope |
| :--- | :---: | :---: | :---: | :--- |
| **Commercial / Acquired (COTS)** | 5 | 129.09 lb | 79.6% | Complete donor chassis, burner engines, pressure vessels |
| **Custom Fabricated Parts** | 6 | 29.85 lb | 18.4% | Formed sheet metal, welded flat bar skids & linkages |
| **Hardware, Fluid & Electrical** | 4 | 3.19 lb | 2.0% | Valves, LP hoses, wiring, retention hardware |
| **Total Assembly Machine** | **15** | **162.12 lb** | **100.0%** | **Operating machine weight (empty fuel)** |

---

## 1. Commercial & Acquired Components (COTS Procurement List)

Commercial off-the-shelf assemblies acquired as complete units. **Do not fabricate in-house**.

| Item Description | Component ID | Category | Qty | Vendor / Source | Part / Model # | Unit Wt | Subassembly / Reference |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **Commercial 24" x 36" Platform Truck / Dolly** | [`platform_cart_24x36`](components/platform_cart_24x36/README.md) | Chassis / Rolling Platform | 1 | Commercial Equipment / Harbor Freight / Uline | `PLATFORM-24X36-1000LB` | 48.0 lb | Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture) |
| **Solaronics High-Intensity Ceramic Infrared Burner** | [`solaronics_infrared_burner`](components/solaronics_infrared_burner/README.md) | Thermal Engine / Radiant Burner | 1 | Solaronics USA | `K-60 / 60,000 BTU` | 18.5 lb | 2. Front Cantilever Radiant Burner & Sled Cowl |
| **DOT 20 lb Steel Propane Cylinder** | [`propane_cylinder_20lb`](components/propane_cylinder_20lb/README.md) | Fuel System / Pressure Vessel | 1 | Worthington / Manchester Tank | `DOT-4BA240 / 20 lb` | 17.0 lb | 3. 20lb Propane Tank Mounting & Primary Gas Train |
| **2.5 Gallon Pressurized Water Safety Spray Tank Component** | `water_tank` | Commercial Hardware | 1 | Commercial Supplier / COTS | `WATER_TANK` | 41.5 lb | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir |
| **Harbor Freight #91037 Propane Torch Assembly** | [`torch_hf91037`](components/torch_hf91037/README.md) | Combustion / Auxiliary Torch | 1 | Harbor Freight | `ITEM 91037` | 4.1 lb | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir |

*Subtotal Commercial Hardware Weight: **129.09 lb***

---

## 2. Custom Fabricated Parts & Machine Shop Cut List

Custom metal components fabricated in the shop from raw stock materials.

| Mark | Part Name | Subassembly | Material | Raw Stock Profile | Cut Dimensions (L × W × T) | Qty | Unit Wt | Primary Operations |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **P01** | **Cantilever Square-Tube Arms (180-deg Flip & Height Adjust)** | 2. Front Cantilever Radiant Burner & Sled Cowl | `Steel-A36` | 1.0" × 3/16" Flat Bar & 1.0" OD Sleeve | 15.39" × 1.00" × 0.187"<br>(390.9 × 25.4 × 4.76 mm) | 1 | 12.34 lb | Assemble cantilever burner channel, mount Solaronics engine |
| **P02** | **Threaded Turnbuckle Height Adjustment Struts** | 2. Front Cantilever Radiant Burner & Sled Cowl | `Brass-C360` | 4.4" x 3.3" Stock | 13.78" × 4.41" × 3.288"<br>(350.0 × 112.0 × 83.53 mm) | 1 | 3.26 lb | Fabricate / machine to print |
| **P03** | **14-Gauge Protective Burner Sled Cowl & Heat Skirts** | 2. Front Cantilever Radiant Burner & Sled Cowl | `Steel-A36` | 14-Ga (0.075") Sheet Steel | 24.00" × 12.00" × 0.075"<br>(609.6 × 304.8 × 1.90 mm) | 1 | 5.47 lb | Assemble cantilever burner channel, mount Solaronics engine |
| **P04** | **20 lb Propane Foot-Ring Deck Retention Clamp** | 3. 20lb Propane Tank Mounting & Primary Gas Train | `Steel-A36` | 2.0" × 3/16" Flat Bar | 10.69" × 1.97" × 0.187"<br>(271.4 × 50.0 × 4.76 mm) | 1 | 2.84 lb | Cut diamond-plate deck, drill caster mounting holes |
| **P05** | **Water Safety Tank Quick-Lock Deck Cradle** | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir | `Steel-A36` | 7.9" x 1.4" Stock | 7.87" × 7.87" × 1.378"<br>(200.0 × 200.0 × 35.00 mm) | 1 | 5.33 lb | Cut diamond-plate deck, drill caster mounting holes |
| **P06** | **Quick-Draw Torch Handle Stirrup Loop & Guide Saddle** | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir | `Steel-ZincPlated` | 2.4" x 1.7" Stock | 10.28" × 2.44" × 1.732"<br>(261.0 × 62.0 × 43.99 mm) | 1 | 0.61 lb | Fabricate / machine to print |

*Subtotal Custom Fabricated Parts Weight: **29.85 lb***

---

## 3. Raw Stock Requisition & Material Nesting Summary

Consolidated raw stock material requirements for inventory purchasing and shop prep.

| Raw Material Grade | Stock Specification | Profile Type | Total Required | Piece Count | Total Wt | Member Part Marks |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| `Brass-C360` | **4.4" x 3.3" Stock** | Solid Billet | **1.15 ft** (13.8 in) | 1 | 3.26 lb | `P02` |
| `Steel-A36` | **1.0" × 3/16" Flat Bar & 1.0" OD Sleeve** | Flat Bar & Bushing | **1.28 ft** (15.4 in) | 1 | 12.34 lb | `P01` |
| `Steel-A36` | **14-Ga (0.075") Sheet Steel** | Sheet Metal | **2.00 sq ft** (288.0 sq in) | 1 | 5.47 lb | `P03` |
| `Steel-A36` | **2.0" × 3/16" Flat Bar** | Flat Bar | **0.89 ft** (10.7 in) | 1 | 2.84 lb | `P04` |
| `Steel-A36` | **7.9" x 1.4" Stock** | Solid Billet | **0.66 ft** (7.9 in) | 1 | 5.33 lb | `P05` |
| `Steel-ZincPlated` | **2.4" x 1.7" Stock** | Solid Billet | **0.86 ft** (10.3 in) | 1 | 0.61 lb | `P06` |

---

## 4. Hardware, Fluid Lines & Electrical Controls

Fittings, regulation valves, reinforced fuel hoses, retention brackets, and ignition wiring.

| Item Description | Category | Material | Specification / Model | Qty | Total Wt | Subassembly / Location |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **Front Deck 180-deg Flip Hinge Brackets & Pivot Pins** | Hardware & Fasteners | `Steel-ZincPlated` | Burner Deck Hinge Brackets | 1 | 1.50 lb | Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture) |
| **Flexible Reinforced LP Gas Hose Supply Loop** | Hardware & Fasteners | `Rubber-Solid` | Burner Flexible Gas Loop | 1 | 0.60 lb | 2. Front Cantilever Radiant Burner & Sled Cowl |
| **Brass Dual-Outlet Regulator Distribution Manifold Tee** | Hardware & Fasteners | `Brass-C360` | Dual Manifold Gas Tee | 1 | 0.77 lb | 3. 20lb Propane Tank Mounting & Primary Gas Train |
| **Auxiliary Spot Torch Flexible Gas Hose** | Plumbing & Fuel Lines | `Rubber-Solid` | Torch Auxiliary Gas Hose | 1 | 0.32 lb | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir |

*Subtotal Hardware & Controls Weight: **3.19 lb***

---
