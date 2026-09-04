# Road Roaster 4 Specification

> **Engineering Design Specification: 4-Wheel Commercial Platform Dolly Architecture**  
> *Active Baseline: v0.1.0*

---

## 1. Physical Specifications & Dimensions

| Parameter | Value (Imperial) | Value (Metric) | Engineering Rationale |
| :--- | :--- | :--- | :--- |
| **Deck Width** | 24.0 in | 609.6 mm | Commercial platform cart width; fits through standard gates while providing rock-solid rollover stability. |
| **Deck Length** | 36.0 in | 914.4 mm | Abundant deck space for 20 lb LP tank, 2.5 gal water safety tank, tools, and the stowed 180° flipped burner. |
| **Deck Top Height** | 6.89 in | 175.0 mm | Low center-of-gravity deck surface; easy tank loading and low wind drag. |
| **Perimeter Skirt** | 1.77 in | 45.0 mm | Deep formed downturn lip providing edge stiffness and bumper mounting. |
| **Corner Radius** | 1.5 in | 38.1 mm | Rounded corners prevent snagging on walls, fences, and landscaping. |
| **Handle Height** | **29.0 in** | **736.6 mm** | Specified ergonomic push handle height above deck surface. |
| **Handle Tubing** | 1.25 in OD | 31.75 mm OD | Heavy-gauge tubular steel with two intermediate cross rails. |
| **Wheel Diameter** | **5.0 in** | **127.0 mm** | Heavy-duty solid rubber wheels with high-visibility yellow hub cores. |
| **Wheel Track (Width)**| 17.3 in | 440.0 mm | Caster center-to-center spacing along lateral X axis (X = ±220 mm). |
| **Wheelbase (Length)** | 25.2 in | 640.0 mm | Caster spacing along Y axis (Front at -320 mm, Rear at +320 mm). |
| **Running Gear Setup** | 2 Rigid + 2 Swivel | 2 Front rigid casters, 2 rear swivel casters with foot brake levers. |
| **Payload Capacity** | 1,000+ lbs | 450+ kg | Structural steel under-deck channels support tank, water, and accessories. |
| **Burner Hover Height**| 1.0 in (adj. 0.5–2.5 in) | 25.4 mm (adj. 13–64 mm) | Cantilevered forward suspension keeps ceramic burner hovering without ever touching the road. |
| **Cantilever Reach** | 10.3 in forward of bumper | 263.0 mm forward | Places burner forward of wheels for maximum visibility and zero wheel-heat exposure. |

---

## 2. Deck Payload Architecture & Zoning

The 24" × 36" flat deck is partitioned into three functional operational zones:

```
                  ◄─────────────────── 36.0 in (914.4 mm) ───────────────────►
        ▲       ┌──────────────────────┬──────────────────────┬──────────────────────┐
        │       │                      │                      │   [20 lb PROPANE]    │
        │       │   FRONT STOW ZONE    │   CENTER SAFETY      │   Cylinder Foot Ring │
     24.0 in    │   180° Flipped       │   2.5 Gal Pressurized│   Gas Regulator /    │ === [PUSH HANDLE]
    (609.6 mm)  │   Burner Stowed      │   Water Safety Tank  │   Dual Manifold Tee  │     (29.0" H)
        │       │   Position           │                      │                      │   + Spot Torch Wand
        │       │                      │                      │                      │
        ▼       └──────────────────────┴──────────────────────┴──────────────────────┘
                ▲                                                                    ▲
             FRONT                                                                 REAR
        [Hinged Burner]                                                        [Operator]
```

1. **Rear Zone (Handle & Fuel Train)**:
   - Houses a standard vertical **20 lb LP Propane Cylinder** (12" diameter foot ring, seated at Y = +210 mm).
   - Welded floor retention collar with 3 deck anchor tabs.
   - Dual-outlet brass manifold tee directly attached to the regulator:
     - Branch 1: Main feed to Solaronics radiant engine.
     - Branch 2: Auxiliary feed to handle-mounted spot torch wand.
   - Dual handle cross-rails serve as quick-draw retention holster clips for the **auxiliary weed torch wand** (`torch_hf91037`).
2. **Center Zone (Safety & Equipment)**:
   - 2.5-gallon pressurized stainless steel water spray tank with pump plunger and spray hose for dampening combustible dry grass edges prior to heat shocking.
   - Clear flat space reserved for the burner when folded 180° back during transit.
3. **Front Zone & Cantilever Mounting**:
   - Heavy-duty forward mounting brackets bolted to front deck skirt and top deck plate.
   - Dual-arm square-tube cantilever bracket extending the Solaronics ceramic infrared burner sled forward of the front bumper.
   - Threaded turnbuckle linkage allows precise height adjustment (0.5" to 2.5" ground clearance).
   - Burner hovers 1.0" above road surface during operation.
   - Flip-back transit hinge rotates burner 180° onto the front stow zone.

---

## 3. Fuel & Energy Capacity Comparison

| Metric | 1 lb Cylinder (Hand Truck) | 20 lb Tank (Road Roaster 4) | Advantage |
| :--- | :--- | :--- | :--- |
| **Total Propane Mass** | 1.0 lb (0.45 kg) | 20.0 lbs (9.07 kg) | **20× Fuel Capacity** |
| **Total Thermal Energy**| 21,548 BTU | 430,960 BTU | **430,960 BTU on deck** |
| **Continuous Burn Time**| ~21.5 minutes (at 60k BTU/hr)| **~7.2 Hours** | **All-day operation without tank swaps** |
| **Propane Cost per lb** | ~$3.50 – $5.00 / bottle | ~$1.00 – $1.25 / lb | **75% Fuel Cost Reduction** |
| **Vaporization Rate** | Cold freeze-up risk in continuous use | Large surface area prevents regulator freeze | **High thermal stability** |

---

## 4. Subassembly Breakdown

```
Road_Roaster_4 [FreeCAD Document: road-roaster-4.FCStd]
├── 1. Commercial 24x36 Platform Cart Foundation (5in Running Gear, 29in Handle)
│   └── platform_cart_24x36 Subassembly (Deck, C-Channels, Bumpers, 4 Casters, Handle)
├── 2. Front Cantilevered Radiant Ceramic Burner & 180-deg Flip Hinge
│   ├── Burner_Deck_Hinge_Brackets (Front Deck Twin-Ear Brackets & Pivot Pins)
│   ├── Burner_Cantilever_Arms (Dual 1.5in Square-Tube Cantilever Arms)
│   ├── Turnbuckle_Height_Adjuster (Threaded Turnbuckle Height Adjustment Struts)
│   ├── Burner_Sled_Cowl (14-Gauge Steel Cowl with Heat Skirts & Breathing Vents)
│   ├── Burner_Flexible_Gas_Loop (Flexible Reinforced LP Supply Loop)
│   └── Solaronics_Infrared_Burner Subassembly (Cordierite Ceramic Matrix, Reflector)
├── 3. 20lb Propane Tank Mounting & Primary Gas Train
│   ├── propane_cylinder_20lb Subassembly (Steel Vessel, Foot Ring, Collar, OPD Valve, Regulator)
│   ├── Tank_Deck_Retention_Ring (Welded Steel Base Retention Ring with 3 Deck Anchor Tabs)
│   └── Dual_Manifold_Gas_Tee (Brass Dual-Outlet Regulator Distribution Manifold Tee)
└── 4. Handle-Mounted Spot Torch Wand & Water Safety Reservoir
    ├── Water_Safety_Reservoir (2.5 Gal Pressurized Stainless Spray Canister & Pump Plunger)
    ├── Water_Tank_Deck_Cradle (Welded Deck Retention Ring & Mounting Pad)
    ├── Torch_Handle_Holster_Clips (Dual Quick-Draw Rubber Holster Clips on Handle Cross Rails)
    └── torch_hf91037 Subassembly (Harbor Freight #91037 Spot Weed Torch Wand)
```
