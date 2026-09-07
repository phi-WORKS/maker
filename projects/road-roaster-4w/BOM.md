# Road Roaster 4W — Master Bill of Materials & Fabrication Cut List

> **Automated Physical Design & Procurement Specification (v0.2.0)**  
> *Generated on 2026-09-07 via `phi_works.maker.bom`*

---

## Executive Summary & Weight Rollup

| Classification | Line Items | Total Weight (lb) | Weight Share | Role / Scope |
| :--- | :---: | :---: | :---: | :--- |
| **Commercial / Acquired (COTS)** | 5 | 129.09 lb | 68.0% | Complete donor chassis, burner engines, pressure vessels |
| **Custom Fabricated Parts** | 7 | 55.90 lb | 29.4% | Formed sheet metal, welded flat bar skids & linkages |
| **Hardware, Fluid & Electrical** | 5 | 4.88 lb | 2.6% | Valves, LP hoses, wiring, retention hardware |
| **Total Assembly Machine** | **17** | **189.87 lb** | **100.0%** | **Operating machine weight (empty fuel)** |

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
| **P01** | **Heavy-Duty Wrap-Around Rigid Front Skirt & Wheel Shield** | Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture) | `Steel-A36` | 9.9" x 6.5" Stock | 24.94" × 9.92" × 6.535"<br>(633.6 × 252.0 × 166.00 mm) | 1 | 21.68 lb | Form 90° front mounting apron channel, drill 3/8" bolt holes |
| **P02** | **Continuous 3/4in Cold-Rolled Steel Pivot Axle & Shaft Collars** | Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture) | `Steel-ZincPlated` | 1.4" x 1.4" Stock | 20.47" × 1.38" × 1.378"<br>(520.0 × 35.0 × 34.99 mm) | 1 | 2.85 lb | Cut 3/4" cold-rolled steel axle shaft, mount zinc shaft collars |
| **P03** | **Cantilever Drop Arms & Pivot Sleeves (3/4in Axle Hinge)** | 2. Front Cantilever Radiant Burner & Sled Cowl | `Steel-A36` | 1.0" × 3/16" Flat Bar & 1.0" OD Sleeve | 19.61" × 1.00" × 0.187"<br>(498.1 × 25.4 × 4.76 mm) | 1 | 21.57 lb | Cut 3/4" cold-rolled steel axle shaft, mount zinc shaft collars |
| **P04** | **Cantilever Diagonal Hood Braces (Rigidifying Truss)** | 2. Front Cantilever Radiant Burner & Sled Cowl | `Steel-A36` | 6.5" x 3.3" Stock | 18.43" × 6.50" × 3.309"<br>(468.0 × 165.0 × 84.05 mm) | 1 | 1.03 lb | Fabricate / machine to print |
| **P05** | **20 lb Propane Foot-Ring Deck Retention Clamp** | 3. 20lb Propane Tank Mounting & Primary Gas Train | `Steel-A36` | 2.0" × 3/16" Flat Bar | 10.69" × 1.97" × 0.187"<br>(271.4 × 50.0 × 4.76 mm) | 1 | 2.84 lb | Cut diamond-plate deck, drill caster mounting holes |
| **P06** | **Water Safety Tank Quick-Lock Deck Cradle** | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir | `Steel-A36` | 7.9" x 1.4" Stock | 7.87" × 7.87" × 1.378"<br>(200.0 × 200.0 × 35.00 mm) | 1 | 5.33 lb | Cut diamond-plate deck, drill caster mounting holes |
| **P07** | **Quick-Draw Torch Handle Stirrup Loop & Guide Saddle** | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir | `Steel-ZincPlated` | 2.4" x 1.7" Stock | 10.28" × 2.44" × 1.732"<br>(261.0 × 62.0 × 43.99 mm) | 1 | 0.61 lb | Fabricate / machine to print |

*Subtotal Custom Fabricated Parts Weight: **55.90 lb***

---

## 3. Raw Stock Requisition & Material Nesting Summary

Consolidated raw stock material requirements for inventory purchasing and shop prep.

| Raw Material Grade | Stock Specification | Profile Type | Total Required | Piece Count | Total Wt | Member Part Marks |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| `Steel-A36` | **1.0" × 3/16" Flat Bar & 1.0" OD Sleeve** | Flat Bar & Bushing | **1.63 ft** (19.6 in) | 1 | 21.57 lb | `P03` |
| `Steel-A36` | **2.0" × 3/16" Flat Bar** | Flat Bar | **0.89 ft** (10.7 in) | 1 | 2.84 lb | `P05` |
| `Steel-A36` | **6.5" x 3.3" Stock** | Solid Billet | **1.54 ft** (18.4 in) | 1 | 1.03 lb | `P04` |
| `Steel-A36` | **7.9" x 1.4" Stock** | Solid Billet | **0.66 ft** (7.9 in) | 1 | 5.33 lb | `P06` |
| `Steel-A36` | **9.9" x 6.5" Stock** | Solid Billet | **2.08 ft** (24.9 in) | 1 | 21.68 lb | `P01` |
| `Steel-ZincPlated` | **1.4" x 1.4" Stock** | Solid Billet | **1.71 ft** (20.5 in) | 1 | 2.85 lb | `P02` |
| `Steel-ZincPlated` | **2.4" x 1.7" Stock** | Solid Billet | **0.86 ft** (10.3 in) | 1 | 0.61 lb | `P07` |

---

## 4. Hardware, Fluid Lines & Electrical Controls

Fittings, regulation valves, reinforced fuel hoses, retention brackets, and ignition wiring.

| Item Description | Category | Material | Specification / Model | Qty | Total Wt | Subassembly / Location |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **Axle Ear Brackets (Pillow Flanges Bolted to Skirt)** | Hardware & Fasteners | `Steel-A36` | Axle Ear Brackets | 1 | 1.36 lb | Road Roaster 4W (4-Wheel Commercial Platform Dolly Architecture) |
| **Burner Hood Side Mounting Brackets (4-Bolt Pattern)** | Hardware & Fasteners | `Steel-A36` | Burner Hood Brackets | 1 | 1.88 lb | 2. Front Cantilever Radiant Burner & Sled Cowl |
| **Flexible Reinforced LP Gas Supply Loop (Cart-Side Connection)** | Plumbing & Fuel Lines | `Rubber-Solid` | Flexible Gas Supply Hose | 1 | 0.55 lb | 2. Front Cantilever Radiant Burner & Sled Cowl |
| **Brass Dual-Outlet Regulator Distribution Manifold Tee** | Hardware & Fasteners | `Brass-C360` | Dual Manifold Gas Tee | 1 | 0.77 lb | 3. 20lb Propane Tank Mounting & Primary Gas Train |
| **Auxiliary Spot Torch Flexible Gas Hose** | Plumbing & Fuel Lines | `Rubber-Solid` | Torch Auxiliary Gas Hose | 1 | 0.32 lb | 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir |

*Subtotal Hardware & Controls Weight: **4.88 lb***

---
