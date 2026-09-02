# Engineering Collaboration & Application Inquiry
## Integrating Solaronics High-Intensity Ceramic Infrared Technology into the Road Roaster Hardscape Weed Management Platform

**To:** Solaronics, Inc. — Engineering & OEM Application Sales  
**From:** phi ARCHITECT / phi-WORKS (`maker` physical design & CAD fabrication lab)  
**Subject:** Technical Collaboration, OEM Component Inquiry, and Downward-Firing Ceramic Infrared Application  
**Date:** September 2, 2026  
**Document Reference:** `RR-SOLARONICS-INQUIRY-v0.7.0`  

---

## 1. Executive Summary & Purpose of Inquiry

We are developing the **Road Roaster**, an innovative, chemical-free physical weed management tool designed for non-agricultural hardscapes—including gravel driveways, paver patios, cobblestone corridors, and roadside curbs. 

Conventional open-flame propane torches fail severely in these environments: their high-velocity open gas jets blow dangerous gravel, sand, and embers into the air while losing over 80% of their heat convectively to ambient wind. 

Through extensive thermodynamic research, we have identified **Solaronics high-intensity gas-fired ceramic infrared technology** as the premier thermal solution for our application. We are reaching out to introduce our platform, discuss the technical integration of Solaronics ceramic plaque and reflector assemblies into our downward-firing mobile sled, and explore options for procuring components or collaborating on build-to-spec OEM burner arrays.

---

## 2. The Road Roaster Concept: Why High-Intensity Infrared?

### 2.1 The Biological Mechanism of Thermal Weed Eradication
Weed eradication does not require burning vegetation to ash. Heating plant foliage to **$140^\circ\text{F} – 180^\circ\text{F}$ ($60^\circ\text{C} – 82^\circ\text{C}$)** for **1 to 2 seconds** causes intracellular sap to boil instantaneously, rupturing cellular membranes. Deprived of water retention, the plant desiccates and dies within 24 to 48 hours, destroying the root crown without chemicals.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               CONVENTIONAL WEED TORCH vs. SOLARONICS CERAMIC INFRARED                  │
├────────────────────────────────────────┬───────────────────────────────────────────────┤
│ Conventional Open-Flame Torch Wand     │ Road Roaster / Solaronics Radiant Sled        │
├────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • High-velocity turbulent air blast    │ • Zero dynamic air blast pressure             │
│ • Blown gravel, dirt, and projectiles  │ • Flameless surface micro-pore combustion     │
│ • Convective heat lost to wind (>80%)  │ • Direct 3–5 µm electromagnetic radiant flux  │
│ • 300,000 – 500,000 BTU/hr (wasteful)  │ • 40,000 – 60,000 BTU/hr (concentrated shock) │
│ • 1 lb bottle runtime: 5–8 minutes     │ • 1 lb bottle runtime: 35–50 minutes          │
│ • Cannot dwell without fire hazard     │ • 15–30s deep heat-soak for root crowns       │
└────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### 2.2 Why Solaronics?
1. **Targeted Radiant Spectrum**: Solaronics cordierite grooved ceramic plaques operate at **$1,600^\circ\text{F} – 1,800^\circ\text{F}$**, emitting infrared energy peaked at **$3 - 5\,\mu\text{m}$**, which directly matches the absorption spectrum of water molecules within plant cell walls.
2. **True Parabolic Focus**: Solaronics deep parabolic specular aluminum reflectors achieve over **$90\%$ directional radiant reflection efficiency**, focusing radiant energy downward into the weed canopy.
3. **Whisper-Quiet Surface Combustion**: Atmospheric premix through the venturi manifold produces gentle micro-pore surface combustion with **zero positive blast pressure**, eliminating gravel displacement and operator noise fatigue.
4. **Re-Radiating Inconel Grid Shield**: The front Inconel wire mesh increases radiant emissivity while providing a built-in impact shield against rocks and debris.

---

## 3. Physical Chassis Architecture & System Integration

The Road Roaster integrates the Solaronics radiant burner module into an ergonomic walk-behind chassis:

```
                                  [LOOP HANDLE]
                                        │
                                        │ (Vertical Center Spine Pipe)
                                        │
                               [UPRIGHT U-FRAME]
                                        │
                          [PROPANE BOTTLE & REGULATOR]
                                (Rear Mounted)
                                        │
                         [FLEXIBLE GAS HOSE & IGNITER]
                         (Secured to Center Spine)
                                        │
        [SLED SUSPENSION TOWER]         │
                  ▲                     │
                  │              [COMMON AXLE] ─── (9.5" All-Terrain Wheels)
       (Triangular Sled Straps)         │
                  │        (Triangular Frame Trusses)
                  ▼
    ┌───────────────────────────┐
    │  SOLARONICS INFRARED SLED │ ══► [Glides on 3/16" Steel Skids, 2.0" Clearance]
    │  - Cordierite Plaque Grid │
    │  - Parabolic Reflector    │
    │  - Perimeter Ground Skirt │
    └───────────────────────────┘
```

### Key Mechanical Design Features
* **Restored Vintage Hand Truck Frame**: Constructed from $1.0''\text{ OD}$ tubular steel ($12.5''$ upright centerline spacing, $46.0''$ top of U-bend) with 3 horizontal cross-straps.
* **Common Wheel Axle Datum ($9.5''$ Wheels)**: The $5/8''$ continuous steel wheel axle $(Y = 4.75'', Z = 4.75'')$ serves as the unified structural datum.
* **Triangular Axle Trusses**: Authentic dual-strut steel trusses weld to the vertical pipes and converge at the wheel axle sleeves.
* **Concentric Sled Suspension**: The forward radiant sled connects directly to the same wheel axle via matching triangular straps, allowing the sled to glide flat on ground runners or swing upward when tilted back for rolling transit.
* **Enclosed Radiant Sled**: A $15.0''\text{ W} \times 18.0''\text{ L} \times 5.12''\text{ H}$ 14-gauge steel cowl with perimeter ground skirts houses the Solaronics ceramic burner, maintaining a constant $2.0''$ emitter face distance from the soil.
* **Rear-Mounted Onboard LP Gas Train**: 1 lb disposable or 11 lb/20 lb refillable propane cylinder clamped to the middle horizontal cross-strap behind the frame. Direct needle flow control valve and $11''\text{ W.C.}$ low-pressure regulator with push-button piezo igniter.
* **Center-Support Conduit**: A flexible reinforced LP gas hose and silicone spark wire travel down the center support pipe directly into the Solaronics brass venturi gas connector.

---

## 4. Target Thermal Specifications

We have provisionally modeled a custom Solaronics radiant array sized to fit our forward sled enclosure:

| Parameter | Target Specification | Notes / Operating Context |
| :--- | :--- | :--- |
| **Plaque Array Dimensions** | $\approx 11.5''\text{ W} \times 15.0''\text{ L}$ ($173\text{ sq. in}$) | Rectangular array sized for our $15'' \times 18''$ outer sled cowl |
| **Thermal Input Rating** | **$40,000 – 60,000\text{ BTU/hr}$** | Surface power density $\sim 230 - 340\text{ BTU/sq. in}$ |
| **Fuel Type & Supply** | Propane (LP Gas) | $11''\text{ W.C.}$ regulated low-pressure supply |
| **Operating Surface Temp** | **$1,600^\circ\text{F} – 1,800^\circ\text{F}$** | Cherry-red incandescence ($3 - 5\,\mu\text{m}$ peak infrared flux) |
| **Combustion Type** | 100% Primary Aerated Premix | Atmospheric aspirating venturi tube with air shutter |
| **Reflector Geometry** | Deep Parabolic Aluminum Hood | Specular mirror finish, focused downward |
| **Face Protection** | Inconel / 304 SS Wire Mesh | Emissivity booster and physical rock guard |
| **Firing Angle** | **Horizontal Downward Firing** | Radiant plaque oriented facing ground ($2.0'' – 3.5''$ above surface) |

---

## 5. Technical Questions for Solaronics Engineers

We would greatly value the guidance of Solaronics engineering team on the following operational questions:

1. **Downward Horizontal Firing Orientation**:
   - Solaronics high-intensity heaters are commonly installed at angles from horizontal up to $30^\circ$ or downward in ceiling suspensions. Are standard K-series ceramic plaques and housings rated for continuous, direct downward ($90^\circ$) horizontal firing at a $2.0'' – 3.5''$ ground clearance?
   - What top/side ventilation clearances do you recommend to ensure adequate secondary aspiration and exhaust of combustion products without overheating the reflector hood or venturi tube?

2. **Mechanical Vibration & Shock Resistance**:
   - The Road Roaster traverses rough outdoor terrain (gravel, expansion joints, stone paths).
   - How resilient are Solaronics cordierite ceramic plaques and cement gaskets to mechanical vibration and shock? Do you recommend special shock-damped mounting brackets or perimeter elastomeric/ceramic-fiber isolation gaskets?

3. **Off-the-Shelf vs. Custom OEM Manifold Options**:
   - Could our dimensional envelope ($11.5'' \times 15.0''$ active face, $\sim 50,000 - 60,000\text{ BTU/hr}$) be achieved by arranging standard modular replacement plaques/reflectors (e.g., from the K-30 or K-60 product lines), or would an engineered OEM manifold be recommended?
   - What are the minimum order quantities or NRE expectations for custom OEM plaque manifolds?

4. **Venturi & Gas Orifice Sizing**:
   - Given a small portable LP gas delivery system operating at $11''\text{ W.C.}$ manifold pressure, what orifice size and venturi throat configuration does Solaronics recommend for optimal primary aeration and flame stability?

5. **CAD Models & Submittals**:
   - We maintain a fully parametric 3D FreeCAD/STEP digital model of the Road Roaster. Could Solaronics provide 3D CAD models (STEP/IGES) or dimensioned engineering drawings of standard K-series plaque assemblies, reflectors, and venturi manifolds to facilitate our digital assembly refinement?

6. **Prototype Evaluation & Parts Procurement**:
   - How can we proceed with purchasing a sample burner head, reflector assembly, and orifice fitting for bench testing and field prototype validation?

---

## 6. Closing & Next Steps

We believe this downward-firing hardscape weed management application presents an exciting demonstration of Solaronics technology expanding beyond industrial space heating into sustainable, chemical-free land stewardship.

We welcome the opportunity to discuss this project with an applications engineer, review your recommendations, and arrange for sample component procurement.

**Contact:**  
phi ARCHITECT  
`phi-WORKS` Physical Design & AI-Augmented CAD Laboratory  
Website: [github.com/phiarchitect/maker](https://github.com/phiarchitect/maker)  
Repository: `phi-WORKS/maker`  
Project: `projects/road-roaster`  
Email / Phone: *(Provided upon submission)*  
Attachments: Full 3D Multi-View Orthogonal CAD Renders (`road-roaster_iso.png`, `road-roaster_right.png`, `road-roaster_back.png`)
