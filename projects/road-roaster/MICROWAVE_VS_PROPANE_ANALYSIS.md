# Road Roaster — Microwave vs. Propane Thermal Analysis
*Feasibility Study: Repurposed Microwave Magnetrons vs. Ceramic Infrared Gas Burners for Mobile Weed Eradication*

---

## 1. Executive Summary & The Dielectric Hypothesis

A persistent question in thermal weed eradication is whether **dielectric microwave heating** could serve as a superior alternative to gas combustion. In concept, repurposing a consumer or commercial microwave oven (magnetron and high-voltage power supply) offers an intriguing hypothesis:

Rather than heating the plant's waxy outer cuticle via convection or surface infrared radiation and waiting for heat to conduct inward, **2.45 GHz microwave radiation penetrates volumetrically, exciting polar water molecules directly within the plant's vascular bundles and boiling cellular sap from the inside out**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          THE DIELECTRIC WEEDING HYPOTHESIS                             │
│                                                                                        │
│     • Volumetric Coupling: Direct absorption into cellular moisture and sap          │
│     • Dielectric Transparency: Dry gravel, sand, and asphalt pass RF with low loss    │
│     • Root Crown & Seed Kill: Penetrates 1 to 3 inches below the surface line          │
│     • Instantaneous Electronic Control: Microsecond RF shutoff with zero thermal lag   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

This engineering evaluation analyzes the thermodynamic, electrical, kinetic, and safety trade-offs of repurposing microwave oven hardware versus the current baseline architecture: **Solaronics High-Intensity Ceramic Infrared Propane Burners**.

---

## 2. Comparative Engineering Decision Matrix

| Engineering Metric | Repurposed Microwave Unit (1kW RF) | Solaronics Ceramic IR Propane (Road Roaster Baseline) | High-Output Propane Blast Torch (Greenwood 91037) |
| :--- | :--- | :--- | :--- |
| **Gross Thermal / RF Power** | **700 – 1,100 W** ($2,400 - 3,750\text{ BTU/hr}$) | **10,250 – 17,600 W** ($35,000 - 60,000\text{ BTU/hr}$) | **30,000 – 100,000 W** ($100,000 - 340,000\text{ BTU/hr}$) |
| **Relative Power Ratio** | **$1.0\times$ (Baseline)** | **$\mathbf{15\times - 18\times}$ more delivered power** | **$\mathbf{30\times - 100\times}$ more delivered power** |
| **Energy Source Payload** | 45 lb Generator (+ gas) OR 35 lb LiFePO4 battery pack | **1.9 lb (1 lb LP bottle)** or **30 lb (20 lb BBQ tank)** | 1.9 lb – 30 lb Propane Tank |
| **Effective Ground Speed** | **0.01 – 0.03 mph** ($30\text{s} - 90\text{s}$ stationary dwell) | **0.8 – 1.5 mph** (Continuous walking glide) | 1.0 – 2.0 mph (Continuous walking sweep) |
| **Dwell Time per Foot** | **$30\text{ to }90\text{ seconds}$ stationary** | **$1\text{ to }2\text{ seconds}$ continuous glide** | $<1\text{ second}$ (Blasts gravel violently) |
| **Dynamic Blast Pressure** | **Zero** (Silent electromagnetic waves) | **Zero** (Flameless micro-pore combustion) | **Severe** (High-velocity jet blows stones/dirt) |
| **Modulation / Control** | **Microsecond electronic PWM** (Instant cut) | Mechanical needle valve / 2:1 turndown | Rough ball / needle valve |
| **Thermal Inertia / Lag** | **Zero** (Ceases emission instantly on cut) | 15–30s warm-up / 60s cool-down lag | Instant ignition / hot hood retention |
| **Penetration Depth** | **1 – 3 inches** into soil / seed bank | **$<0.5\text{ mm}$** (Surface leaf cuticle) | Surface only |
| **Primary Safety Hazard** | **Stray RF leakage & 2–4kV DC electrocution** | Hot glowing tile & open flame source | Flying gravel projectiles & uncontrolled fire |
| **Hardware Complexity** | High (Waveguide, RF chokes, inverter, HV tank) | Low (Off-the-shelf gas train, regulator, burner) | Ultra-low (Single-tube venturi wand) |

---

## 3. Power Levels & The Gravimetric Energy Penalty

The single greatest physical barrier to mobile microwave weeding is **energy density and continuous thermal output**.

```
[ 1 LB PROPANE CYLINDER ]                     [ 1,000 W DOMESTIC MICROWAVE ]
Weight: 1.9 lbs gross                         Weight: 45 lb Generator OR 35 lb Battery
Chemical Energy: 21,548 BTU (6.3 kWh)         Electrical Wall Draw: 1,500 – 1,650 W
Continuous Heat: 17.6 kW (60,000 BTU/hr)      Delivered RF Power: 1.0 kW (3,412 BTU/hr)
Continuous Runtime: ~40 minutes               Continuous Runtime: ~40 minutes (per 100Ah LiFePO4)
──────────────────────────────────────────────────────────────────────────────────────────
         Propane yields ~17.5× higher thermal power per unit time at 5% of the weight.
```

### 3.1 Delivered Thermal Output
* A standard domestic microwave advertised as a "1,000-Watt oven" generates **$1,000\text{ Watts}$ of RF radiation at $2.45\text{ GHz}$** ($3,412\text{ BTU/hr}$).
* Magnetrons achieve an electrical-to-RF conversion efficiency of approximately **$60\% - 65\%$**. Including filament heating and cooling fan loads, the unit draws **$1,500\text{ to }1,650\text{ Watts}$** from the electrical supply.
* In contrast, the Solaronics dual ceramic burner array on the Road Roaster produces **$60,000\text{ BTU/hr}$ ($17.58\text{ kW}$)** of focused downward radiant flux.
* **The Power Gap:** To match the thermal output of a single standard propane ceramic burner, an electrical sled would require **seventeen (17) 1kW domestic magnetrons** operating simultaneously, demanding **$25.5\text{ kW}$ of electrical power**.

### 3.2 Dose Requirements & Ground Speed
Extensive agricultural studies (e.g., University of Melbourne, CSIRO) establish the biological energy threshold for thermal weed mortality:
* **Foliar Cell Lysis (Seedlings / Annuals):** Requires an absorbed thermal dose of **$40\text{ to }80\text{ kJ/m}^2$** ($25\text{ to }50\text{ BTU/ft}^2$).
* **Deep Taproot Crown / Seedbank Sterilization:** Requires **$400\text{ to }1,000\text{ kJ/m}^2$**.

Across an 18" × 18" ($0.21\text{ m}^2$) ground footprint:
* **Propane Ceramic IR ($17.6\text{ kW}$):** Delivers $17,600\text{ Joules/second}$. Reaching the foliar threshold ($80\text{ kJ/m}^2 \times 0.21\text{ m}^2 = 16.8\text{ kJ}$) requires **$0.95\text{ seconds}$ of exposure**. This allows continuous walking glide speeds between **$0.8\text{ and }1.5\text{ mph}$**.
* **Microwave RF ($1.0\text{ kW}$):** Delivers $1,000\text{ Joules/second}$. Reaching that same foliar threshold requires **$17\text{ to }35\text{ seconds}$ of stationary dwell** per 18" patch. Cooking a taproot 2 inches deep requires a stationary dwell of **$90\text{ to }180\text{ seconds}$**.

---

## 4. Control, Modulation & Responsiveness

While power density favors propane, **control and modulation decisively favor microwave systems**.

```
PROPANE CERAMIC BURNER:
  [Deadman Released] ──> Gas shut off ──> Cordierite tile glows at 1,600°F for 30–60s ──> Thermal Lag
MICROWAVE INVERTER:
  [Deadman Released] ──> Gate drive pulled LOW ──> RF emission ceases in <10 microseconds ──> Zero Lag
```

### 4.1 Zero Thermal Inertia
* **Propane:** Cordierite ceramic tiles take 20 to 30 seconds to reach operating temperature ($1,800^\circ\text{F}$) and retain dangerous radiant heat for 1 to 2 minutes after fuel shutoff. If an operator stops moving or trips, the stationary hot plaque can scorch asphalt, crack concrete, or ignite dry debris.
* **Microwave:** Electromagnetic waves vanish immediately when cathode emission ceases. Releasing a deadman switch halts energy transfer within **microseconds**, leaving no residual glowing thermal mass.

### 4.2 Precision Digital Modulation
* Modern kitchen units utilizing **inverter power supplies** (e.g., Panasonic high-frequency switching inverters) do not use slow mechanical relays to cycle on and off; they modulate true continuous RF output from $10\%$ to $100\%$ via high-frequency DC pulse-width modulation.
* An onboard microcontroller (e.g., ESP32) tied to wheel rotary encoders can dynamically scale microwave power in direct closed-loop synchronization with the operator's rolling speed:
  $$\text{RF Power (Watts)} = k \cdot v_{\text{ground}}$$
* If the cart stops rolling, RF power automatically drops to zero, preventing localized soil overheating.

---

## 5. Heating Physics: Dielectric vs. Radiant Surface Transfer

The fundamental heating mechanism differs radically between the two technologies:

```
        CERAMIC INFRARED (3 to 5 µm)                  MICROWAVE RF (2.45 GHz / 12.2 cm)
  ──────────────────────────────────────────    ──────────────────────────────────────────
  • Surface Absorption: Radiation absorbed      • Volumetric Absorption: Waves penetrate
    by outer cuticle (<0.2 mm). Heat must         directly into the vascular bundles and
    conduct inward slowly via cell walls.         cambium, exciting polar water molecules.
  • Substrate Loss: Gravel and stones heat      • Dielectric Transparency: Dry gravel, sand,
    up first; stone conducts heat to weed.        and pavers have low dielectric loss factors.
  • Seedbank Limitation: Soil is an insulator;    Energy concentrates inside moist plants.
    IR cannot penetrate below the ground.       • Depth: Penetrates 1 to 3 inches into soil.
```

1. **Selective Heating Efficiency:**
   * Liquid water has a high dielectric loss factor ($\epsilon'' \approx 12$ at $20^\circ\text{C}$, $2.45\text{ GHz}$). Dry silica sand and river rocks have very low loss factors ($\epsilon'' \approx 0.01 - 0.05$).
   * Microwaves pass through dry gravel with minimal attenuation and deposit their energy directly into the moist plant core. In contrast, infrared rays are absorbed by the top surface of the gravel, requiring the rocks to heat up before conducting energy to the plant roots.
2. **Explosive Cellular Rupture:**
   * Dielectric heating generates instantaneous steam pressure inside intact plant cell walls. This internal pressure build-up creates violent cellular popping (lysis) at lower bulk leaf temperatures ($65^\circ\text{C} - 75^\circ\text{C}$) than convective drying requires.

---

## 6. Practical Fabrication Hazards: Repurposing Kitchen Microwave Units

Attempting to repurpose a consumer microwave oven on an open mobile chassis introduces three major engineering and safety hazards:

```
   CLOSED RESONANT CAVITY (Factory Design)         OPEN GROUND CONVERSION (DIY Sled)
  ┌──────────────────────────────────────┐       ┌──────────────────────────────────────┐
  │ ┌──────────┐                         │       │ ┌──────────┐                         │
  │ │Magnetron │   2.45 GHz Standing     │       │ │Magnetron │  Downward Launch Horn   │
  │ └───┬──────┘   Waves Contained       │       │ └───┬──────┘                         │
  │     ▼                                │       │     ▼                                │
  │  (Food Load)                         │       └─────┼────────────────────────────────┘
  │ ════════════════════════════════════ │             ▼    ▼    ▼    ▼    ▼    ▼
  │ Continuous Faraday Metal Enclosure   │       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  └──────────────────────────────────────┘       ◄── DANGEROUS RF LEAKAGE UNDER SKIRT ──►
```

### 6.1 RF Leakage & Human Exposure
* A kitchen microwave is a closed **Faraday cage cavity**. Removing the floor to direct energy toward the ground turns the unit into an **open-boundary slot antenna**.
* At $2.45\text{ GHz}$, the free-space wavelength is $\lambda = 12.2\text{ cm}$ ($4.8''$). Any irregular air gap between the sled skirt and uneven gravel larger than a quarter-wavelength ($\approx 1.2''$) will act as an efficient radiating aperture.
* **Biological Hazard:** High-power uncontained stray microwave radiation poses severe biological risks, particularly to the eyes (rapid cataract formation due to lack of vascular cooling in the ocular lens) and peripheral tissue.
* Commercial microwave weeders require elaborate **quarter-wave reactive choke channels** and flexible conductive mesh skirts (e.g., braided stainless or beryllium-copper fingerstock) maintaining continuous contact with the ground plane.

### 6.2 Reflected Power & Magnetron Destruction (VSWR)
* Domestic magnetrons are matched to a specific cavity impedance.
* When operated over dry ground with sparse weed coverage, there is insufficient dielectric water load to absorb the microwave energy.
* The unabsorbed RF energy reflects back into the launch waveguide and strikes the magnetron cathode/antenna. Without an expensive **three-port ferrite circulator and dummy load** (standard on industrial RF systems, but absent in consumer microwaves), the tube will arc, overheat, and suffer permanent filament failure within minutes.

### 6.3 Lethal High-Voltage DC Circuitry (MOT)
* Standard domestic microwave oven transformers (MOTs) step up 120V AC household power to **$2,100\text{V} - 4,200\text{V} \text{ DC}$ at $300\text{ to }500\text{ mA}$**.
* Unlike automotive ignition coils or stun guns (which operate at high voltage but negligible microamp currents), a microwave power supply delivers **lethal current** capable of causing instantaneous cardiac arrest and catastrophic electrical burns.
* Housing a 4kV transformer and high-voltage oil-filled capacitor on a mobile hand truck subjected to outdoor vibration, moisture, and rough gravel introduces an extreme shock hazard that is difficult to ruggedize safely in a DIY prototyping environment.

---

## 7. Strategic Synthesis: The Stationary "Spot Zap" Alternative

While unsuited for a continuous walking sled like the Road Roaster, microwave technology holds significant potential if reimagined as a **stationary, deep-root spot applicator**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE STATIONARY "SPOT ZAP" CONCEPT                               │
│                                                                                        │
│     • Enclosure: Cylindrical shielded bell with spring-loaded ground interlock         │
│     • RF Choke: Dual-perimeter conductive chainmail skirt sealing flat to gravel       │
│     • Interlock Logic: Magnetron fires ONLY when pressure switches confirm seal        │
│     • Target Application: Hardened invasive taproots (wild blackberries, thistles,    │
│       bindweed) requiring deep root-crown boiling without disturbing gravel beds      │
│     • Operation: Place bell over weed crown, dwell 30–45 seconds, step to next weed   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

For such an application:
1. The sealed bell eliminates RF leakage by forming a true closed chamber over the target.
2. A small, portable inverter generator ($1,800\text{ W}$) mounted to the hand truck can power the stationary probe without requiring continuous multi-kilowatt power during walking.

---

## 8. Conclusion & Road Roaster Platform Roadmap

For the primary mission of the Road Roaster—**rapid, continuous, chemical-free weed eradication across expansive gravel corridors at walking speed**:

1. **Ceramic Infrared Gas Combustion Remains the Superior Mobile Engine:**
   * Delivers $15\times - 18\times$ higher continuous thermal power ($60,000\text{ BTU/hr}$ vs. $3,412\text{ BTU/hr}$).
   * Weighs less than 5 lbs for fuel storage (vs. 45+ lbs for generator/batteries).
   * Operates with complete mechanical autonomy—zero electrical cords, high-voltage inverters, or RF containment hazards.
   * Produces zero aerodynamic blast pressure, preserving gravel placement and suppressing airborne embers.
2. **Microwave Integration Archived as Specialized Subsystem:**
   * Direct microwave prototyping via repurposed kitchen ovens is deemed unviable for the main chassis due to severe dwell time penalties ($30\text{s}+/\text{sq ft}$), magnetron reflection burnout, and 4kV electrical safety risks.
   * The concept is documented herein and archived for future investigation as an optional, tethered **Spot-Zap Deep Root Wand** accessory.
