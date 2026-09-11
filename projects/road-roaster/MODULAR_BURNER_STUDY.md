# Road Roaster — Modular Ceramic Infrared Burner Array Study
*Engineering Analysis: Commodity Component Sourcing, Gas Plumbing, Ignition, Flame Safety, and Platform Sizing*

---

## 1. Executive Summary & Design Rationale

The **Road Roaster** platform achieves lethal cellular shock on invasive gravel weeds via high-intensity downward radiant infrared energy ($1,600^\circ\text{F} - 1,800^\circ\text{F}$). While commercial pre-packaged industrial heaters (such as the Solaronics K-30) offer a robust proof of concept, adopting a proprietary monolithic commercial burner presents several design limitations:

1. **High Unit Cost**: Commercial industrial radiant heaters range from **$450 to $650+** per unit.
2. **Monolithic Failure Mode**: If one ceramic plaque cracks or clogs from road vibration or thermal shock, the entire commercial unit often requires full factory overhaul or total replacement.
3. **Bulky Packaging & High Center of Gravity**: Industrial heaters feature deep plenum chambers and flue hoods designed for high-bay warehouse ceilings, resulting in an overall depth of **$222.25\text{ mm}$ ($8\,\frac{3}{4}''$)** and a weight of **$29.65\text{ lbs}$ ($13.45\text{ kg}$)**. This limits transit folding clearances when hinging 180° onto mobile carts.
4. **Proprietary Geometry**: Chassis, brackets, and cowls must be contorted around the supplier's fixed casing dimensions.

### The Modular Commodity Architecture
This study designs an autonomous, scalable burner system built from **mass-market commodity ceramic infrared plaques** (commonly manufactured for shawarma/doner rotisseries, industrial powder-coating drying tunnels, and agricultural brooders).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODULAR COMMODITY BURNER PHILOSOPHY                             │
│                                                                                        │
│   • Building Block: Standard 220 × 170 mm (10,000 BTU) Cordierite Ceramic Cassette.   │
│   • Replacement Cost: ~$20 to $28 per cassette (field-swappable in 2 minutes).         │
│   • Scalability: 2–3 tiles for Road Roaster 2W; 4–6 tiles for Road Roaster 4W.        │
│   • Low Profile: Custom sheet cowl depth under 95 mm (saving 125+ mm vs Solaronics).  │
│   • 100% Fail-Safe: Thermoelectric millivolt flame supervisor + tip-over cutoff.       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Commodity Ceramic Infrared Plaque (The Modular Building Block)

### 2.1 The Standard "HD220" Format
The most widely manufactured, low-cost gas ceramic radiant element worldwide is the **220 mm × 170 mm** plaque:

| Specification | Metric | Imperial | Engineering Notes |
| :--- | :--- | :--- | :--- |
| **Outer Casing Dimensions** | $220\text{ mm} \times 170\text{ mm} \times 60\text{ mm}$ | $8.66'' \times 6.69'' \times 2.36''$ | Stamped 304 SS or aluminized steel plenum box |
| **Active Ceramic Area** | $200\text{ mm} \times 145\text{ mm}$ | $7.87'' \times 5.71''$ | $44.9\text{ sq in}$ ($290\text{ cm}^2$) active emitter |
| **Thermal Power (LPG)** | $2.93\text{ kW}$ | **$10,000\text{ BTU/hr}$** | Optimal rating for cordierite honeycomb micro-pores |
| **Fuel Consumption (LP)** | $0.21\text{ kg/hr}$ | $0.46\text{ lbs/hr}$ | At $11''\text{ W.C.}$ manifold pressure |
| **Operating Temperature** | $870^\circ\text{C} - 980^\circ\text{C}$ | $1,600^\circ\text{F} - 1,800^\circ\text{F}$ | Bright cherry-red surface incandescence |
| **Ceramic Matrix** | Cordierite ($2\text{MgO}\cdot 2\text{Al}_2\text{O}_3\cdot 5\text{SiO}_2$) | High thermal shock resistance ($\Delta T > 800^\circ\text{C}$) |
| **Face Shield** | 304 Stainless Steel Wire Mesh | $1.2\text{ mm}$ wire | Protects ceramic from pebble strike and holds matrix |
| **Pre-Mix Induction Tube**| Cast iron / steel venturi tube | $\varnothing 25\text{ mm}$ bellmouth | Atmospheric air entrainment horn with shutter collar |
| **Weight per Cassette** | $1.45\text{ kg}$ | $3.20\text{ lbs}$ | Extremely light; easy array banking |
| **Unit Market Cost** | ~$18 – $28 USD | Mass-produced commodity part |

```
                       [ CASSETTE EXPLODED SCHEMATIC ]

                   ┌──────────────────────────────────────┐
                   │    304 SS Wire Mesh Guard Screen     │
                   └──────────────────┬───────────────────┘
                                      ▼
                   ┌──────────────────────────────────────┐
                   │ Cordierite Honeycomb Ceramic Plaque  │
                   │ (Thousands of Micro-Perforations)    │
                   └──────────────────┬───────────────────┘
                                      ▼
                   ┌──────────────────────────────────────┐
                   │  High-Temp Ceramic Fiber Gasket Seal │
                   └──────────────────┬───────────────────┘
                                      ▼
                   ┌──────────────────────────────────────┐
                   │  Deep-Drawn Stainless Steel Plenum   │
                   │  with Slotted Slide-Mount Tabs       │
                   └──────────────────┬───────────────────┘
                                      ▼
                   ┌──────────────────────────────────────┐
                   │ Atmospheric Pre-Mix Venturi Tube     │
                   │ with Rotatable Primary Air Shutter   │
                   └──────────────────┬───────────────────┘
                                      ▼
                   ┌──────────────────────────────────────┐
                   │ Machined Brass Hex Orifice Spud (#60)│
                   └──────────────────────────────────────┘
```

---

## 3. Gas Plumbing, Pressure Regulation & Manifold Design

### 3.1 Gas Pressure Standard: 11" Water Column (W.C.)
Low-pressure Liquid Propane (LP) equipment in North America and Europe operates at **$11.0''\text{ W.C.}$ ($2.74\text{ kPa} \approx 0.397\text{ PSI}$)**.
- **Why NOT Unregulated Tank Pressure (100–180 PSI)?**  
  High-pressure torch heads rely on high-velocity gas jets. In an enclosed ceramic plenum, high pressure would blow the flame off the ceramic face, overheat the venturi mixer, or blow out the gasket seal. Low-pressure atmospheric premixing ensures gentle, silent surface combustion.
- **Regulator**: Standard commercial single-stage low-pressure LP regulator with an excess flow safety shut-off (QCC-1 tank connection for 20 lb tanks, or 1"-20 UNEF adapter for 1 lb bottles).

### 3.2 Orifice Sizing & Mathematical Derivation
The gas flow through an orifice is governed by the standard orifice equation:
$$Q = 1658.5 \cdot C_d \cdot A \cdot \sqrt{\frac{\Delta P}{S_g}}$$
Where:
- $Q$ = gas discharge rate ($\text{ft}^3/\text{hr}$)
- $C_d$ = orifice discharge coefficient ($\approx 0.82$ for standard chamfered brass spuds)
- $A$ = orifice area ($\text{sq inches}$)
- $\Delta P$ = pressure drop across orifice ($11.0''\text{ W.C.}$)
- $S_g$ = specific gravity of propane vapor relative to air ($1.52$)

At $11''\text{ W.C.}$ propane ($2,500\text{ BTU/ft}^3$ heating value), thermal output corresponds to standard drill sizes:

| Drill # | Diameter (in) | Diameter (mm) | Heat Output @ 11" W.C. LP | Fit for Cassette |
| :--- | :--- | :--- | :--- | :--- |
| **#65** | $0.0350''$ | $0.889\text{ mm}$ | $8,560\text{ BTU/hr}$ | Mild underfire (fuel saver) |
| **#60** | **$0.0400''$** | **$1.016\text{ mm}$** | **$11,175\text{ BTU/hr}$** | **Target Nominal Rating (10,000–11,000 BTU)** |
| **#55** | $0.0520''$ | $1.321\text{ mm}$ | $18,890\text{ BTU/hr}$ | Overfire (too rich for single HD220) |
| **#50** | $0.0700''$ | $1.778\text{ mm}$ | $34,250\text{ BTU/hr}$ | Sized for large Solaronics K-30 |

> **Selected Spud**: Standard brass $1/8''\text{ NPT}$ or $\text{M10} \times 1.0$ hex orifice spud drilled with **#60 drill ($0.040''$ / $1.02\text{ mm}$)**.

### 3.3 Primary Air Induction & Stoichiometry
Propane requires a volumetric air-to-fuel ratio of **$24:1$** for complete stoichiometric combustion:
$$\text{C}_3\text{H}_8 + 5\,\text{O}_2 + 18.8\,\text{N}_2 \longrightarrow 3\,\text{CO}_2 + 4\,\text{H}_2\text{O} + 18.8\,\text{N}_2$$
- The high-velocity stream exiting the #60 orifice enters the venturi throat, entraining **$50\% - 60\%$ primary air** through the adjustable air shutter.
- The remaining secondary air is drawn into the surface pores across the ceramic face.
- Adjusting the shutter collar allows fine-tuning between a soft rich flame and a lean crisp blue/orange incandescent ceramic glow without carbon soot.

### 3.4 Gas Distribution Manifold Rail
For multi-burner arrays, equal gas distribution to all spuds is essential:
- **Manifold Rail**: $\frac{3}{4}''$ square aluminum or 304 stainless steel tubing ($0.065''$ wall).
- **Inlet Port**: $3/8''$ male flare or $1/4''\text{ NPT}$ female port.
- **Outlet Ports**: Pre-drilled and tapped $1/8''\text{ NPT}$ ports spaced to align coaxially with each cassette's venturi induction horn.
- **Mounting**: Manifold rail is clamped to the burner chassis frame with vibration-damping standoffs.

---

## 4. Ignition & Flame Supervision Architecture

```mermaid
graph TD
    subgraph Controls on Push Handle
        ValveKnob[Safety Valve Push-to-Light Knob]
        SparkBtn[Pulse Igniter Push Button]
    end

    subgraph Gas Flow Train
        Supply[11 in W.C. LP Supply] --> SafetyValve[Thermoelectric Magnetic Valve]
        SafetyValve --> ManifoldRail[Gas Manifold Rail]
        ManifoldRail --> Orifice1[Orifice 1] --> Cassette1[Burner Cassette 1]
        ManifoldRail --> Orifice2[Orifice 2] --> Cassette2[Burner Cassette 2]
        ManifoldRail --> Orifice3[Orifice 3] --> Cassette3[Burner Cassette 3]
        ManifoldRail --> Orifice4[Orifice 4] --> Cassette4[Burner Cassette 4]
    end

    subgraph Ignition & Flame Supervision
        Battery[1.5V AA Battery] --> PulseMod[4-Port Pulse Module]
        SparkBtn --> PulseMod
        PulseMod --> Probe1[Spark Electrode 1]
        PulseMod --> Probe2[Spark Electrode 2]
        PulseMod --> Probe3[Spark Electrode 3]
        PulseMod --> Probe4[Spark Electrode 4]

        Flame1[Burner 1 Glowing] --> Thermocouple[Heavy-Duty Thermocouple]
        TiltSwitch[45 deg Tilt / Dump Switch] --- Thermocouple
        Thermocouple -->|25-30 mV DC Closed Loop| SafetyValve
    end
```

### 4.1 Multi-Port Continuous Electronic Pulse Igniter
- **Module**: Off-the-shelf 1.5V AA battery-powered pulse spark generator (2, 4, or 6 outlet ports).
- **Operation**: Holding the handle-mounted momentary push button delivers **$3 - 5\text{ sparks/second}$** at $12\text{ kV}$ across all electrodes simultaneously.
- **Electrodes**: High-alumina ceramic insulator sleeves ($\varnothing 6.35\text{ mm}$ / $1/4''$) with heat-resistant nickel-chromium probe tips spaced $3.0 - 4.0\text{ mm}$ above the ceramic tile margin.
- **Cross-Lighting Bridges**: Adjacent cassettes are fitted with perforated stainless steel crossover tunnels ($15\text{ mm}$ wide). If any single plaque ignites, the flame front traverses the crossover channel, lighting all adjacent plaques in $<0.25\text{ seconds}$.

### 4.2 Thermoelectric Flame Safety Valve (100% Fail-Safe)
Mobile outdoor gas equipment requires automatic shutdown if the flame is extinguished by wind, stone impacts, or running out of fuel:
- **Thermoelectric Principle (Seebeck Effect)**:
  - A copper-clad thermocouple probe is positioned in the radiant zone of Burner 1.
  - When heated to cherry-red ($>600^\circ\text{C}$), the dissimilar metal junction generates a **$25 - 30\text{ mV DC}$** potential.
  - This millivolt current energizes a sensitive electromagnetic solenoid inside the main gas control valve.
- **Lighting Sequence**:
  1. Operator presses and turns the gas valve knob (physically holding the magnetic valve plunger open).
  2. Operator taps the pulse igniter button. The burners light immediately.
  3. Operator holds the valve knob for **10 to 15 seconds** until the thermocouple generates holding voltage.
  4. Operator releases the knob; the valve remains magnetically held open.
- **Fail-Safe Shut-Off**:
  - If a gust of wind extinguishes the flame, the thermocouple cools rapidly ($<20\text{ seconds}$).
  - Millivolt output drops below the solenoid hold threshold ($<5\text{ mV}$).
  - A heavy return spring snaps the valve port shut, isolating the gas supply.
  - **Zero unburned gas escape, zero battery power needed for safety**.

### 4.3 Integrated Tip-Over / Tilt Dump Switch
- In series with the thermocouple millivolt loop, a mechanical **tilt switch** is mounted inside the control console.
- If the cart or hand truck is tipped beyond **45°** (e.g. curb rollover, ditch tilt, or handling slip), a weighted rolling sphere disengages the circuit contact, breaking the millivolt loop and shutting the gas valve instantaneously.

---

## 5. Replaceable Cassette Mechanics & Field Serviceability

```
                       [ QUICK-SWAP CASSETTE RETENTION ]

                  Chassis Mounting Rail (Stainless Angle)
                 ┌──────────────────────────────────────┐
                 │    (O)                 (O)           │
                 └───┬───────────────────────┬──────────┘
                     │  M5 Captive Stud      │  M5 Captive Stud
                     ▼                       ▼
               ┌───────────┐           ┌───────────┐
               │ Brass     │           │ Brass     │
               │ Knurled   │           │ Knurled   │
               │ Thumb Nut │           │ Thumb Nut │
               └─────┬─────┘           └─────┬─────┘
                     ▼                       ▼
            ═════════════════════════════════════════════
            Burner Cassette Perimeter Mounting Flange Tab
            ═════════════════════════════════════════════
                     │                       │
                     └───────► [SLIDE IN] ◄──┘
```

1. **Slotted Mounting Flanges**: Each 220×170mm cassette features slotted perimeter tabs matching standard M5 stainless studs on the array frame.
2. **Knurled Brass Thumb Nuts**: Requires zero wrenches in the field.
3. **Gas Connection**: Each burner is fed by a flexible stainless-braided pigtail with a $3/8''$ SAE 45° flare swivel nut.
4. **Maintenance Procedure**:
   - Step 1: Shut off gas supply and allow 5 minutes to cool.
   - Step 2: Loosen flare swivel nut on burner inlet.
   - Step 3: Spin off two knurled brass thumb nuts.
   - Step 4: Slide out damaged cassette and slip new replacement cassette into position.
   - Step 5: Tighten thumb nuts and flare fitting; re-ignite.
   - **Total repair time: $< 2\text{ minutes}$. Total replacement cost: ~$25.**

---

## 6. Sizing & Array Architectures: 2W vs. 4W Road Roaster

### 6.1 Road Roaster 2W (Hand Truck Sled)

```
        ◄───────────────── 381.0 mm (15.0") Sled Width ─────────────────►
        ┌───────────────────────────────────────────────────────────────┐
        │                                                               │
        │   ┌───────────────────────────┐   ┌─────────────────────────┐ │
        │   │                           │   │                         │ │
   ▲    │   │      Cassette #1          │   │       Cassette #2       │ │
 457 mm │   │      10,000 BTU           │   │       10,000 BTU        │ │
(18.0") │   │      220 × 170 mm         │   │       220 × 170 mm      │ │
   │    │   │                           │   │                         │ │
   ▼    │   └───────────────────────────┘   └─────────────────────────┘ │
        │                                                               │
        └───────────────────────────────────────────────────────────────┘
```

- **Configuration**: **Dual Cassette ($1 \times 2$) or Triple Cassette ($1 \times 3$)**
- **Nominal Power**: **$20,000\text{ to }30,000\text{ BTU/hr}$** ($5.86 - 8.79\text{ kW}$).
- **Active Area**: $340\text{ mm} \times 220\text{ mm}$ ($13.4'' \times 8.7''$) = $116.6\text{ sq in}$ (Dual) or $174.9\text{ sq in}$ (Triple).
- **Weight**: Burner core + hood = **$4.8\text{ kg}$ ($10.6\text{ lbs}$)** (saving $19\text{ lbs}$ vs Solaronics).
- **Chassis Fit**: Fits cleanly inside the existing $15.0'' \times 18.0''$ ($381 \times 457\text{ mm}$) sled footprint without modifying hand truck risers.
- **Fuel Match**: 1 lb Coleman cylinder runs ~45–60 minutes; optional 5 lb tank runs ~3.6 hours.

---

### 6.2 Road Roaster 4W (Platform Cart Cantilevered Burner)

```
             ◄─────────────── 550.0 mm (21.65") Cowl Width ───────────────►
        ▲    ┌─────────────────────────────┬─────────────────────────────┐
        │    │                             │                             │
        │    │         Cassette #1         │         Cassette #2         │
        │    │         10,000 BTU          │         10,000 BTU          │
      420 mm │         220 × 170 mm        │         220 × 170 mm        │
     (16.5") │                             │                             │
        │    ├─────────────────────────────┼─────────────────────────────┤
        │    │                             │                             │
        │    │         Cassette #3         │         Cassette #4         │
        │    │         10,000 BTU          │         10,000 BTU          │
        │    │         220 × 170 mm        │         220 × 170 mm        │
        │    │                             │                             │
        ▼    └─────────────────────────────┴─────────────────────────────┘
```

- **Configuration**: **$2 \times 2$ Grid (4 Cassettes)**
- **Nominal Power**: **$40,000\text{ BTU/hr}$** ($11.72\text{ kW}$).
- **Active Radiant Area**: $440\text{ mm} \times 340\text{ mm}$ ($17.32'' \times 13.39''$) = **$232\text{ sq in}$** ($1,496\text{ cm}^2$).
  - *Comparison*: Delivers **34% more radiant surface** and **33% more thermal power** than the Solaronics K-30 ($173\text{ sq in}$, $30,000\text{ BTU/hr}$).
- **Weight**: Complete 4-tile array with stainless cowl and manifold = **$8.2\text{ kg}$ ($18.1\text{ lbs}$)** (vs Solaronics $29.65\text{ lbs}$, saving **$11.5\text{ lbs}$**).
- **Transit Fold-Back Envelope**:
  - Outer dimensions: $550\text{ mm}\text{ W} \times 420\text{ mm}\text{ L} \times 90\text{ mm}\text{ D}$ ($21.6'' \times 16.5'' \times 3.5''$).
  - When flipped 180° around the continuous pivot axle, it drops cleanly into the **front stow zone** of the $24'' \times 36''$ deck.
  - Leaves $19.5''$ ($495\text{ mm}$) of clear deck space behind it for the 2.5-gallon water safety reservoir and rear 20 lb propane cylinder foot ring.

---

## 7. Custom Reflector Cowl Geometry & 180° Transit Clearance

```
       [ CROSS-SECTION: SOLARONICS K-30 VS. phi-WORKS MODULAR HOOD ]

   SOLARONICS K-30 (Deep Industrial Plenum)
   ┌────────────────────────────────────────────────────────┐
   │                                                        │ 222.25 mm
   │         [Deep Plenum + Heavy Cast Iron Venturi]        │ (8.75")
   │                                                        │ Overall Depth
   ├────────────────────────────────────────────────────────┤
   │               Flared Sheet Reflector Throat            │
   └────────────────────────────────────────────────────────┘

   phi-WORKS LOW-PROFILE MODULAR HOOD
   ┌────────────────────────────────────────────────────────┐
   │ [Compact 60mm Cassettes + Low-Profile Manifold Rail]   │ 90.0 mm (3.54")
   ├────────────────────────────────────────────────────────┤ Overall Depth
   │ 30° Flared Mirror-Polished 5052 Aluminum Skirt Flange  │ (SAVES 132 mm!)
   └────────────────────────────────────────────────────────┘
```

### 7.1 Reflector Optics & Material Selection
- **Body Material**: 16-gauge ($1.27\text{ mm}$) 5052-H32 aluminum sheet (lightweight, corrosion-proof, excellent thermal conductivity) or 18-gauge ($1.20\text{ mm}$) 304 stainless steel.
- **Reflective Coating**: Mirror-polished interior reflector panels ($\ge 95\%$ infrared specular reflectivity).
- **Flange Angle**: 30° outward sloping walls expand the radiant coverage field by 20% while shielding the combustion face from crosswinds.
- **Air Relief Slots**: Perimeter top louver vents allow flue gases ($\text{CO}_2$ and water vapor) to escape upward naturally without creating turbulent recirculating backpressure.

### 7.2 180° Hinge & Flip-Back Mechanics (Road Roaster 4W)
- Pivot Axis: Continuous cold-rolled solid steel shaft ($\varnothing 3/4''$ / $19.05\text{ mm}$) supported by twin arched ear brackets on the platform skirt top flange ($Z = 230\text{ mm}$).
- Cantilever Drop Arms: 1.5" square steel tubing ($0.083''$ wall) extending forward $342\text{ mm}$ ($13.5''$).
- Flip Clearance:
  - In working position: Burner hovers $38\text{ mm}$ ($1.5''$) above the ground plane.
  - In stowed transit position: Rotates 180° around the pivot axle to rest upside down (radiant face up or covered by a transit lid) directly on the deck.
  - Because total depth is only $90\text{ mm}$, the stowed burner envelope rises only $3.5''$ above the deck, dramatically lowering the center of gravity and eliminating tipping risks during transport.

---

## 8. Comparative Evaluation Matrix: Solaronics K-30 vs. Modular Commodity Array

| Parameter | Solaronics K-30 (Baseline) | phi-WORKS Modular Array (4-Tile 4W) | Engineering Verdict |
| :--- | :--- | :--- | :--- |
| **Gross Thermal Power** | $30,000\text{ BTU/hr}$ ($8.8\text{ kW}$) | **$40,000\text{ BTU/hr}$** ($11.7\text{ kW}$) | **+33% Power Advantage** |
| **Active Radiant Surface** | $173\text{ sq. in.}$ ($1,116\text{ cm}^2$) | **$232\text{ sq. in.}$** ($1,496\text{ cm}^2$) | **+34% Coverage Advantage** |
| **Total Assembly Weight** | $29.65\text{ lbs}$ ($13.45\text{ kg}$) | **$18.1\text{ lbs}$** ($8.21\text{ kg}$) | **39% Lighter (-11.5 lbs)** |
| **Assembly Depth / Profile**| $222.25\text{ mm}$ ($8.75\text{ in}$) | **$90.0\text{ mm}$** ($3.54\text{ in}$) | **60% Lower Profile (-132 mm)** |
| **Initial Hardware Cost** | ~$450 – $650 | **~$135 – $175** | **70% Cost Reduction** |
| **Plaque Replacement Cost** | N/A (Total unit replacement) | **~$25 per cassette** | **Field-Serviceable Commodity** |
| **Replacement Downtime** | Days / Factory Return | **2 minutes with thumb nuts** | **Instant Shop/Field Repair** |
| **Deck Transit Stowing** | High vertical obstruction | **Low-profile flat deck stow** | **Superior Center of Gravity** |
| **Flame Failure Safety** | Intermittent DSI (requires 24VAC) | **Millivolt Thermoelectric (Self-Powered)**| **True Off-Grid Ruggedness** |

---

## 9. Comprehensive Bill of Materials (BOM) — 4-Tile Modular System

| Item | Qty | Description / Part Source | Unit Est. | Ext. Cost |
| :---: | :---: | :--- | :---: | :---: |
| 1 | 4 | **HD220 Infrared Ceramic Burner Cassettes** (220×170mm, 10k BTU) | $22.00 | $88.00 |
| 2 | 4 | **Brass Hex Orifice Spuds (#60 Drill)** (1/8" NPT / M10) | $2.50 | $10.00 |
| 3 | 1 | **3/4" Square Aluminum / Stainless Manifold Rail** (Custom Drilled) | $18.00 | $18.00 |
| 4 | 1 | **1.5V AA 4-Port Continuous Pulse Igniter Module** | $12.50 | $12.50 |
| 5 | 4 | **Ceramic Spark Electrodes with Silicone HV Leads** | $3.00 | $12.00 |
| 6 | 1 | **Thermoelectric Gas Safety Valve + Thermocouple Kit** (11" W.C.) | $21.00 | $21.00 |
| 7 | 1 | **Mechanical Ball Tilt / Dump Switch** (45° Safety Cutoff) | $6.50 | $6.50 |
| 8 | 1 | **Low-Profile 5052 Aluminum Reflector Cowl** (Laser-cut & bent) | $28.00 | $28.00 |
| 9 | 8 | **M5 Knurled Brass Thumb Nuts & Hardware** | $0.75 | $6.00 |
| 10 | 1 | **3/8" Flexible Stainless-Braided LP Feed Line** | $9.00 | $9.00 |
| **TOTAL** | | **Complete 40,000 BTU Modular Infrared Burner System** | | **~$211.00** |

---

## 10. Conclusion & Architectural Roadmap

Building our own modular burner assembly using mass-market 220×170 mm cordierite ceramic cassettes provides compelling advantages:
1. **Economic Freedom**: Slashes hardware build costs by over 65% compared to commercial industrial heaters.
2. **True Modularity**: Eliminates single-point failure; damaged plaques can be swapped individually in minutes for $25.
3. **Optimized Vehicle Integration**: Allows designing low-profile ($90\text{ mm}$) reflector hoods tailored to the exact folding geometry of the Road Roaster chassis.
4. **Autonomous Thermal Sizing**: Enables scalable 2-tile (20k BTU) setups for the 2-wheel hand truck and 4-tile (40k BTU) setups for the 4-wheel commercial platform cart.
