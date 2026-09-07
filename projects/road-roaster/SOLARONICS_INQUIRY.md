# Engineering Collaboration & OEM Application Inquiry
## Integrating High-Intensity Infrared Radiant Heating into the Road Roaster Hardscape Weed Management Platform

**To:** Solaronics, Inc. — Engineering & OEM Application Sales (`sales@solaronicsusa.com`)  
**From:** phi ARCHITECT / phi-WORKS (`maker` physical design & CAD fabrication studio)  
**Subject:** OEM Technical Collaboration: Downward-Firing Infrared Radiant Burner for Mobile Hardscape Weed Eradication  
**Date:** September 7, 2026  
**Document Reference:** `RR-SOLARONICS-INQUIRY-v0.8.0`  
**Digital Models & Project Repository:** [github.com/phiarchitect/maker](https://github.com/phiarchitect/maker)  

---

## 1. Executive Summary & Purpose of Inquiry

We are developing the **Road Roaster** platform family—an innovative, chemical-free physical weed management system engineered specifically for non-agricultural hardscapes, including gravel driveways, paver walkways, cobblestone corridors, roadside curbs, and agricultural headlands.

### The Problem with Conventional Open-Flame Weed Torches
Traditional high-output open-flame propane torches (such as weed dragon torches) fail severely in hardscape environments:
* **Severe Aerodynamic Air Blast**: High-velocity open gas jets act like leaf blowers, blasting loose gravel, sand, and burning plant embers into the air.
* **Massive Convective Heat Loss**: In outdoor ambient breezes, over 80% to 85% of convective heat is lost to the wind before conducting into the ground.
* **Fire & Safety Hazards**: Uncontrolled open flames create intolerable fire ignition risks along dry borders, fences, and mulch beds.

### The Infrared Radiant Solution
Through extensive thermodynamic analysis, we have identified **gas-fired high-intensity infrared radiant technology** as the ideal thermal engine for non-contact hardscape weed eradication:
* **Targeted Biological Shock**: Weed eradication does not require incinerating vegetation to ash. Heating plant foliage and root crowns to **$140^\circ\text{F} - 180^\circ\text{F}$ ($60^\circ\text{C} - 82^\circ\text{C}$)** causes intracellular moisture to boil instantaneously, rupturing cellular membranes. Deprived of moisture retention, the plant desiccates and dies within 24 to 48 hours without chemicals.
* **Zero Aerodynamic Blast Pressure**: Silent, gentle micro-pore surface combustion produces pure electromagnetic radiant energy with zero dynamic air pressure, preventing stone and debris displacement.
* **Directional Radiant Penetration**: Focused downward infrared radiation directly penetrates the foliar canopy and heats the gravel/soil interface without relying on convective air transfer.

### Purpose of Reaching Out
We have developed high-fidelity 3D CAD assemblies of our mobile platforms integrating the **Solaronics K-30** as a **concept / reference model**. We are reaching out to Solaronics engineering to:
1. Introduce our platform concepts and operational requirements.
2. Solicit your engineering critique and recommendations regarding the ideal burner device, burner media, and sizing for this application.
3. Explore procurement options for sample burner hardware, gas train components, and ignition controls for prototype field validation.

---

## 2. The Road Roaster Platform Family

We have engineered two distinct mobile platform architectures to cover residential and commercial operational envelopes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE ROAD ROASTER PLATFORM SUITE                           │
├────────────────────────────────────────┬───────────────────────────────────────────────┤
│ 1. Road Roaster (2-Wheel Compact Cart) │ 2. Road Roaster 4W (Commercial Platform Cart) │
├────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Nimble walk-behind hand-truck frame  │ • Heavy-duty 24" × 36" 4-wheel platform dolly │
│ • 1 lb or 11 lb portable LP cylinder   │ • Full 20 lb propane cylinder (~14.4 hr run)  │
│ • Floating radiant sled on ground skids│ • 2.5 gal pressurized water safety reservoir  │
│ • Sled tilts back on 9.5" wheels       │ • Cantilevered forward hover suspension       │
│ • Residential paths, patios & curbs    │ • 180° flip-back burner transit stowage       │
│ • Low mass, single-operator agility    │ • Commercial driveways & agricultural headland│
└────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### 2.1 Road Roaster 4W (Commercial Platform Cart — Active Baseline v0.2.0)
* **Chassis**: Industrial 24" × 36" platform cart with two 5" front rigid casters, two 5" rear swivel casters with foot brakes, and an ergonomic 29" push handle.
* **Cantilevered Burner Suspension**: The burner engine is mounted on forward cantilever drop-arms pivoting on a continuous $3/4''$ cold-rolled steel pivot axle supported by arched brackets on the front skirt.
* **Operational Hover & Transit**: The burner hovers at an adjustable operating height of **$1.5'' - 2.0''$ ($38 - 50\text{ mm}$)** above the ground. For rolling transport over curbs and obstacles, the entire burner assembly rotates **$180^\circ$ backward** onto the front stow zone of the cart deck, shifting weight safely inboard over the wheelbase.
* **Payload**: Carries a vertical 20 lb LP cylinder, dual-outlet manifold regulator, and a 2.5-gallon pressurized water spray tank for perimeter dampening.

### 2.2 Road Roaster 2W (Compact Hand-Truck Platform — Baseline v0.7.0)
* **Chassis**: Tubular steel walk-behind hand-truck chassis with heavy-duty 9.5" all-terrain rubber wheels.
* **Floating Sled**: Forward radiant sled with perimeter ground skirts and 3/16" steel skids gliding with 0.5" ground clearance, holding the burner face ~2.0" above ground.
* **Common Axle Pivot**: Sled suspension ties concentrically to the main wheel axle, allowing the operator to tilt the unit back like an upright vacuum for rapid wheeled transit.

---

## 3. The Role of the Solaronics K-30 as a 3D CAD Concept Model

In our engineering CAD repository (`components/solaronics_infrared_burner/`), we built a comprehensive parametric 3D CAD model of the **Solaronics K-30** high-intensity ceramic infrared heater (plaque matrix, cast iron venturi, plenum chamber, flared specular reflector hood, and gas train controls) derived directly from Solaronics architectural specifications and plan-view DWG drawings.

```
                  [SOLARONICS K-30 CAD CONCEPT MODEL]
        ┌───────────────────────────────────────────────────────┐
        │  • 30,000 BTU/hr rated input (LP Gas @ 10"-11" W.C.)  │
        │  • 173 sq. in radiating face (Cordierite matrix)      │
        │  • 16.75" W × 23.9" L flared reflector mouth         │
        │  • Total Mass: ~29.6 lbs                              │
        │  • Modeled in downward-firing horizontal orientation  │
        └───────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Clarification on K-30 Status**:  
> The Solaronics K-30 integration in our current CAD models represents a **proof-of-concept reference baseline**. We selected the K-30 because of its well-documented dimensional envelope, robust industrial build quality, and outstanding radiant efficiency.
> 
> However, because standard K-series heaters are primarily engineered for building space heating (hung overhead and angled $0^\circ - 30^\circ$), **we do not assume an unmodified K-30 is necessarily the final production device for our mobile ground-weeding application**. We actively seek Solaronics' guidance on the best burner configuration from your product lines or custom OEM manufacturing capabilities.

---

## 4. Key Engineering Questions for Solaronics

We would greatly value the technical guidance of Solaronics applications engineering on the following four core questions:

### Question 1: Burner Sizing & Heat Flux (Target: 180°F In-Ground)
* **Thermal Objective**: Our target is raising the weed foliar canopy and the immediate top soil / gravel layer to **$180^\circ\text{F}$ ($82^\circ\text{C}$)** to ensure complete cellular lysis and destroy the root crown.
* **Operational Kinematics**:
  - *Continuous Walking Pace*: $0.8 - 1.5\text{ mph}$ (yielding an exposure dwell time of approximately **$1.0 - 2.5\text{ seconds}$** over a given ground patch).
  - *Slow Crawl / Spot Dwell*: $0.2 - 0.4\text{ mph}$ or stationary dwell (**$5 - 15\text{ seconds}$**) for dense perennial taproots.
* **Engineering Inquiries**:
  1. What thermal heat release rate (BTU/hr) and radiant flux density ($\text{BTU/hr}\cdot\text{in}^2$ or $\text{kW/m}^2$) does Solaronics recommend to reliably achieve $180^\circ\text{F}$ in ground media at these speeds?
  2. Is a **30,000 BTU/hr** unit (e.g. K-30 footprint) adequate for this thermal dose, or would a higher-output array (e.g. **40,000 – 60,000 BTU/hr**, such as the K-50 / K-60 footprint) be required for continuous walking speeds?
  3. What emitter face hover distance (currently modeled at **$1.5'' - 2.0''$**) provides the optimal balance of radiant energy concentration versus combustion air entrainment?

### Question 2: Best Burner Type for this Scenario
* **Operational Environment**: The burner will be deployed in an outdoor mobile vehicle, operating in a **continuous downward-firing orientation ($90^\circ$ horizontal, facing the ground)**, and subject to continuous vibrations, bumps, and minor mechanical shocks from rolling over gravel driveways and uneven ground.
* **Engineering Inquiries**:
  1. **Ceramic Plaque Resilience**: How do Solaronics cordierite ceramic plaques and refractory cement gaskets perform under continuous mechanical vibration and outdoor thermal cycling? Is special shock-isolated mounting recommended, or are ceramic plaques robust enough for cart-mounted service?
  2. **Alternative Burner Media**: Does Solaronics manufacture or recommend alternative burner surface media—such as **woven metallic fiber (FeCrAlloy / Inconel)**, sintered porous metal, or radiant ribbon matrices—for close-proximity ground process heating? How do they compare in terms of shock resistance, thermal turn-down, and draft resistance?
  3. **Downward Firing & Combustion Air Clearance**: When firing directly downward at a $1.5'' - 2.0''$ hover height, how is primary air aspiration at the venturi and secondary air at the burner face maintained? Does Solaronics recommend specific perimeter exhaust relief gaps, draft diverters, or chimney vents to prevent flame smothering?

### Question 3: Thermostatic & Overheating Controls (Could it get too hot?)
* **Operational Concern**: When operating close to the ground, significant radiant energy is reflected back upward from gravel and hardscapes, while hot flue gases rise around the hood.
* **Engineering Inquiries**:
  1. **Cavity Heat Trap & Back-Radiation**: Is there a risk of overheating the burner plenum box, venturi tube, gas orifice, or control enclosure due to trapped heat in the ground cavity? What are the maximum safe operating temperatures for the plenum and gas train?
  2. **Substrate Overheating / Scorching**: If the operator pauses motion or travels very slowly, could ground temperatures spike excessively, posing scorching or ignition hazards?
  3. **Control Strategies**:
     - Does Solaronics offer or recommend **modulating control valves** (e.g., 2:1 or wider turndown) or **dual-stage (high/low)** firing to tailor heat input to ground speed and weed density?
     - What thermal hi-limit safety switches are standard or recommended on the burner plenum?
     - Have you integrated **non-contact infrared pyrometer sensors** or thermocouples in OEM equipment to monitor surface temperature and automatically throttle gas flow when the target ground temperature ($180^\circ\text{F}$) is reached?

### Question 4: Field Ignition & Safety Requirements for an Off-Grid Mobile Cart
* **Operational Reality**: Stationary Solaronics commercial heaters typically utilize building AC power ($24\text{ VAC}$ or $115\text{ VAC}$) for direct spark ignition (DSI) and flame rectification sensing, or a millivolt standing pilot (`TAL` series). On an autonomous outdoor mobile cart, 120VAC line power is unavailable.
* **Engineering Inquiries**:
  1. **Low-Voltage DC Ignition Packages**: Does Solaronics offer or support **12V DC battery-powered Direct Spark Ignition (DSI)** modules with 100% safety shutoff for portable / OEM equipment?
  2. **Millivolt Standing Pilot in Outdoor Wind**: Is a self-powered millivolt standing pilot (`TAL` package) practical and reliable in outdoor mobile environments, or do ambient wind gusts and movement cause nuisance pilot flame outages?
  3. **Flame Supervision Under Wind**: What flame rectification probe or sensor configuration is most reliable against outdoor wind turbulence when firing downward?
  4. **Emergency Gas Shutoff**: What deadman switch or safety valve configuration does Solaronics recommend to instantly cut fuel supply in the event of an operator tip-over, cart release, or loss of flame?

---

## 5. Summary Technical Specification Comparison

| Parameter | CAD Concept Baseline (Solaronics K-30) | Application Requirement / Query Envelope |
| :--- | :--- | :--- |
| **Thermal Input Rating** | $30,000\text{ BTU/hr}$ ($8.8\text{ kW}$) | $30,000 - 60,000\text{ BTU/hr}$ (seeking sizing recommendation) |
| **Fuel Supply** | Propane (LP Gas) @ $10.0'' - 11.0''\text{ W.C.}$ | 20 lb cylinder (4W) or 1 lb/11 lb cylinder (2W) w/ low-pressure regulator |
| **Operating Orientation** | Suspended overhead ($0^\circ - 30^\circ$) | **Direct horizontal downward firing ($90^\circ$ to ground)** |
| **Ground Clearance** | N/A (Indoor factory ceiling mount) | **$1.5'' - 2.0''$ ($38 - 50\text{ mm}$)** hover height above soil/gravel |
| **Target Workpiece Temp**| Indoor ambient comfort ($65^\circ - 72^\circ\text{F}$) | **$180^\circ\text{F}$ ($82^\circ\text{C}$)** ground / foliage weed root shock |
| **Operating Medium** | Cordierite grooved ceramic tiles ($1,800^\circ\text{F}$) | Cordierite ceramic vs. metallic fiber mesh vs. ribbon burner |
| **Ignition / Electrical**| $24\text{ VAC}$, $115\text{ VAC}$, or Millivolt Pilot | **12V DC Battery DSI, Piezo, or Wind-Resistant Millivolt** |
| **Transit / Mobility** | Stationary suspended | Mobile wheeled platform subject to outdoor terrain vibration |

---

## 6. Digital CAD Assets & Next Steps

### 6.1 Available 3D Engineering Data
We maintain complete, open parametric 3D CAD assemblies of both platforms in FreeCAD and can provide standard **STEP / IGES** digital models, dimensioned drawings, and clearance diagrams:
* **`road-roaster-4w.FCStd` / `road-roaster-4w.png`**: Commercial 4W platform dolly showing cantilever suspension, pivot axle, 180° flip stowage, and gas/water payload zoning.
* **`road-roaster.FCStd` / `road-roaster.png`**: Compact 2W hand-truck sled with Concentric Axle pivot and perimeter draft skirts.
* **`solaronics_infrared_burner.FCStd`**: Detailed parametric representation of the K-30 burner core, plenum diffuser, venturi horn, and flared reflector hood.

### 6.2 Proposed Path to Collaboration
We welcome the opportunity to discuss this application directly with a Solaronics OEM Application Engineer. Specifically, we would like to:
1. Schedule a brief technical call to review your recommendations on burner sizing, media, and combustion clearances.
2. Discuss options for purchasing a prototype evaluation burner assembly, appropriate gas orifice, and ignition controls.
3. Explore potential OEM supply arrangements as we move from prototype trials to low-rate initial production.

---

**Primary Engineering Contact:**  
phi ARCHITECT  
`phi-WORKS` Physical Design & AI-Augmented CAD Laboratory  
Website: [github.com/phiarchitect/maker](https://github.com/phiarchitect/maker)  
Repository: `phi-WORKS/maker`  
Project Directories: [`projects/road-roaster/`](.) & [`projects/road-roaster-4w/`](../road-roaster-4w/)  
Email: `phi@phiarchitect.com`  
Attachments: 3D Perspective & Orthogonal CAD Renders of Road Roaster 4W and Solaronics K-30 Concept Assembly.
