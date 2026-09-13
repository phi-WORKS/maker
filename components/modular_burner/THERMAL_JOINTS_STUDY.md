# Thermal Joints & Mechanical Interconnect Study (`modular_burner`)

> **Engineering Analysis: Thermal Expansion Compliance, Clamping Mechanics, and Radiant Heat Mitigation for Modular Ceramic Infrared Burner Arrays**  
> *phi-WORKS Maker Component Library (`components/modular_burner/`)*

---

## 1. Executive Summary & Problem Definition

Operating ceramic infrared burners in multi-cassette arrays introduces severe thermal and mechanical stresses that do not exist in single-burner appliances:
1. **Extreme Thermal Gradients**: Radiant cordierite ceramic plaques operate at **$1,600^\circ\text{F} - 1,800^\circ\text{F}$ ($870^\circ\text{C} - 980^\circ\text{C}$)**, while the deep-drawn 304 stainless steel plenum casings reach **$400^\circ\text{F} - 650^\circ\text{F}$ ($200^\circ\text{C} - 345^\circ\text{C}$)**. Meanwhile, the fuel distribution manifold, gas orifices, and shutoff valves must remain below **$140^\circ\text{F}$ ($60^\circ\text{C}$)** to prevent vapor density drop, lean surging, and seal degradation.
2. **Coefficient of Thermal Expansion (CTE) Mismatch**: Brittle cordierite ceramic has an exceptionally low CTE ($\alpha \approx 2.0 \times 10^{-6}/\text{K}$), whereas the surrounding 304 stainless steel expands nearly **nine times faster** ($\alpha \approx 17.3 \times 10^{-6}/\text{K}$).
3. **Array Scaling Constraints**: When coupling 2 cassettes ($1 \times 2$ inline) or 4 cassettes ($2 \times 2$ grid), rigid bolting causes differential expansion of up to **$2.0\text{ mm}$**, creating immense shear forces that buckle plenum flanges, shatter ceramic plaques, and loosen fasteners.

This study documents the mathematical models, joint kinematics, materials selection, and thermal isolation strategies engineered into the `modular_burner` component ecosystem.

---

## 2. Thermal Expansion Mathematics & Failure Modes

### 2.1 Governing Differential Expansion Formula
Thermal elongation along any axis $L$ is governed by:
$$\Delta L = L_0 \cdot \alpha \cdot \Delta T$$

Where:
- $L_0$ = Nominal dimension at ambient ($20^\circ\text{C}$ / $68^\circ\text{F}$)
- $\alpha$ = Linear coefficient of thermal expansion ($\text{m}/\text{m}\cdot\text{K}$)
- $\Delta T$ = Temperature differential from ambient ($\text{K}$ or $^\circ\text{C}$)

### 2.2 Material Properties Matrix

| Material | Component Role | Operating Temp ($T$) | CTE ($\alpha$) | Thermal Conduct. ($k$) |
| :--- | :--- | :--- | :--- | :--- |
| **Cordierite Ceramic** | Radiant Plaques | $900^\circ\text{C}$ ($1,650^\circ\text{F}$) | $2.2 \times 10^{-6}/\text{K}$ | $1.5\text{ W/m}\cdot\text{K}$ |
| **304 Stainless Steel** | Plenums, Bezels, Rails | $300^\circ\text{C}$ ($572^\circ\text{F}$) | $17.3 \times 10^{-6}/\text{K}$ | $16.2\text{ W/m}\cdot\text{K}$ |
| **6061-T6 Aluminum** | Gas Manifold Rails | $50^\circ\text{C}$ ($122^\circ\text{F}$) | $23.1 \times 10^{-6}/\text{K}$ | $167.0\text{ W/m}\cdot\text{K}$ |
| **Steatite / Mica** | Thermal Break Washers | $400^\circ\text{C}$ ($752^\circ\text{F}$) | $7.5 \times 10^{-6}/\text{K}$ | $2.0\text{ W/m}\cdot\text{K}$ |
| **Superwool 607** | Expansion Gasket Strips | $1,000^\circ\text{C}$ ($1,832^\circ\text{F}$) | $0.0$ (Compliant fiber) | $0.08\text{ W/m}\cdot\text{K}$ |

---

### 2.3 Quantitative Expansion by Array Configuration

#### Configuration A: 2-Burner Inline Array ($1 \times 2$ for Road Roaster 2W)
- Nominal overall span: $L_0 = 380\text{ mm}$ across the transverse X-axis (width of two $170\text{ mm}$ cassettes plus mounting flange tabs and gap).
- Operational $\Delta T \approx 250^\circ\text{C}$ on the stainless steel plenum casing:
$$\Delta L_{X,\text{steel}} = 380\text{ mm} \times (17.3 \times 10^{-6}/\text{K}) \times 250\text{ K} = \mathbf{1.64\text{ mm}}$$
- Ceramic plaque expansion over the same span:
$$\Delta L_{X,\text{ceramic}} = 340\text{ mm} \times (2.2 \times 10^{-6}/\text{K}) \times 880\text{ K} = \mathbf{0.66\text{ mm}}$$
- **Net Differential Shear Travel**: $\Delta L_{\text{diff}} = 1.64 - 0.66 \approx \mathbf{0.98\text{ mm}}$ relative slip between ceramic tile bed and stainless outer tray; $\mathbf{1.64\text{ mm}}$ absolute expansion along the mounting rails.

#### Configuration B: 4-Burner Grid Array ($2 \times 2$ for Road Roaster 4W)
- Transverse X span ($2 \times 220\text{ mm}$ cassette length + center cruciform gap): $L_{0,X} = 460\text{ mm}$.
$$\Delta L_{X} = 460\text{ mm} \times (17.3 \times 10^{-6}/\text{K}) \times 250\text{ K} = \mathbf{1.99\text{ mm}}$$
- Longitudinal Y span ($2 \times 170\text{ mm}$ cassette width + center cruciform gap): $L_{0,Y} = 360\text{ mm}$.
$$\Delta L_{Y} = 360\text{ mm} \times (17.3 \times 10^{-6}/\text{K}) \times 250\text{ K} = \mathbf{1.56\text{ mm}}$$
- **Net Area Dilation**: $\Delta A \approx 1,740\text{ mm}^2$ ($2.7\text{ sq. in.}$) thermal area growth of the burner tray relative to the cold chassis!

### 2.4 Mechanics of Rigid Joint Failure
If two or four burners are rigidly bolted together with standard clearance holes ($\varnothing 5.5\text{ mm}$ for M5 bolts):
1. **Plenum Flange Buckling**: The compressive thermal stress in the restrained stainless steel exceeds the yield strength ($\sigma_{\text{th}} = E \cdot \alpha \cdot \Delta T = 193\text{ GPa} \times 17.3 \times 10^{-6} \times 250 = \mathbf{835\text{ MPa}}$, exceeding $304\text{ SS}$ yield strength of $\approx 205\text{ MPa}$). The sheet metal will crimp and buckle.
2. **Ceramic Fracture**: Compressive pinch loads at inter-cassette boundaries transmit directly to the perimeter ceramic bezels, causing spalling and tile cracking.
3. **Fastener Loosening**: Cyclic expansion and contraction yields standard bolt threads, causing fasteners to vibrate loose in mobile trailer/cart service.

---

## 3. The 5-Point Thermal Joint Architecture

To mitigate these failure modes, the `modular_burner` ecosystem introduces a standardized 5-point thermal joint system:

```
                  [ 5-POINT THERMAL JOINT SYSTEM ]

   [Belleville Spring Pack] ◄── Maintains 40 lbs continuous clamping preload
             │
             ▼
   [Slotted Slip Tabs]     ◄── 8.0 x 5.5 mm slots absorb ±2.5 mm thermal float
             │
             ▼
   [Ceramic Fiber Gasket]  ◄── Superwool 607 cushions 5 mm inter-cassette gap
             │
             ▼
   [Thermal Break Washers] ◄── Steatite spacers stop conductive heat to manifold
             │
             ▼
   [Radiant Baffle Plate]  ◄── 304 SS deflector shields manifold from IR radiation
```

---

### 3.1 Point 1: Slotted Slip Mount Tabs
- **Slot Geometry**: All cassette perimeter mounting tabs and tray angle rails feature **$8.0\text{ mm} \times 5.5\text{ mm}$ obround slots** oriented along the primary thermal expansion vectors (X-axis for inline arrays; radial outward vectors for $2 \times 2$ grid arrays).
- **Slip Clearance**: Fastener shanks ($\varnothing 5.0\text{ mm}$ M5 studs) have $\pm 2.5\text{ mm}$ unobstructed axial travel, easily accommodating the maximum computed $1.99\text{ mm}$ thermal growth with $>25\%$ safety factor.

### 3.2 Point 2: Belleville Disc Spring Washer Packs
In high-temperature environments, rigid bolted joints undergo thermal relaxation: bolts heat and expand, losing clamping preload, or over-tighten and crush components.
- **Spring Element**: Conical Belleville disc spring washers (DIN 2093, Inconel 718 or 17-7 PH stainless steel) stacked under each knurled brass thumb nut.
- **Preload Profile**:
  - Uncompressed height: $1.5\text{ mm}$
  - Deflection at working load: $0.6\text{ mm}$ ($40\% - 50\%$ stroke)
  - Clamping force: $180 - 220\text{ N}$ ($40 - 50\text{ lbf}$) per stud
- **Dynamic Action**: As the stainless chassis heats and expands in thickness, the Belleville washer deflects while maintaining near-constant clamping friction ($F = \mu N \approx 0.2 \times 200\text{ N} = 40\text{ N}$), preventing rattling while permitting frictionless thermal sliding along the slot.

### 3.3 Point 3: Inter-Cassette Ceramic Fiber Expansion Gaskets
- **Material**: Superwool 607 or Kaowool high-temperature soluble ceramic fiber blanket ($2,300^\circ\text{F} / 1,260^\circ\text{C}$ classification).
- **Dimensions**: $5.0\text{ mm}$ thickness uncompressed; compressed to $3.0\text{ mm}$ during cassette insertion into the slide rails.
- **Functions**:
  1. **Thermal Cushion**: Allows adjacent metal plenums to expand toward each other without metal-to-metal collision or pinch stress.
  2. **Acoustic / Vibration Damper**: Eliminates metal-to-metal buzzing during cart transit over gravel or cobblestone.
  3. **Secondary Air Baffle**: Prevents parasitic draft air from bypassing through the gaps between tiles, preserving burner thermal efficiency.

---

### 3.4 Point 4: Manifold Thermal Break Spacers (Conductive Insulation)
Heat travels from the combustion chamber to the gas manifold via conduction through mounting brackets:
$$Q_{\text{cond}} = \frac{k \cdot A \cdot \Delta T}{L}$$

Without insulation, with stainless brackets ($k \approx 16.2\text{ W/m}\cdot\text{K}$), heat conducts rapidly into the aluminum manifold rail ($k \approx 167\text{ W/m}\cdot\text{K}$), elevating fuel temperatures to $>200^\circ\text{F}$.
- **Thermal Isolator**: A $3.0\text{ mm}$ thick machinable steatite ceramic or Muscovite mica thermal barrier washer installed at every fastener interface between the burner tray and the manifold standoff brackets.
- **Conductivity Reduction**: Steatite ($k \approx 2.0\text{ W/m}\cdot\text{K}$) provides an **$88\%$ reduction in thermal conductivity**, keeping conductive heat transfer to $<5\text{ Watts}$ per bracket.

---

### 3.5 Point 5: Radiant Heat Shield Baffle Plate (Radiative Insulation)
Thermal radiation from the top of the hot stainless plenum casing radiates upward toward the overhead manifold rail according to the Stefan-Boltzmann law:
$$q_{\text{rad}} = \epsilon \sigma (T_{\text{plenum}}^4 - T_{\text{manifold}}^4)$$

- **Shield Design**: A $1.2\text{ mm}$ polished 304 stainless steel radiant baffle plate positioned horizontally $15\text{ mm}$ above the plenum tops and $20\text{ mm}$ below the gas manifold.
- **Reflectivity**: Polished stainless ($\epsilon \approx 0.15$) reflects $>80\%$ of upward infrared radiation back down away from the gas rail.
- **Ventilation Gap**: Natural convective air channels between the plenum, shield, and cowl chimney flush radiant heat out through top cowl vents, maintaining manifold rail temperatures at a safe **$105^\circ\text{F} - 125^\circ\text{F}$ ($40^\circ\text{C} - 52^\circ\text{C}$)** during continuous operation.

---

## 4. Flame Crossover Bridge Kinematics

### 4.1 2-Burner Inline Crossover Bridge
- **Architecture**: A formed 304 SS inverted U-channel ($24\text{ mm}$ wide, $10\text{ mm}$ rise) spanning the $5\text{ mm}$ inter-cassette gap across the radiant face.
- **Thermal Slip Mounting**: The bridge foot flanges are retained under the outer tile retention bezels using elongated slots. As the cassettes expand $1.6\text{ mm}$, the bridge feet slip smoothly inside the retention pocket without buckling or popping off.
- **Perforations**: $3.5\text{ mm}$ laser-cut slots spaced at $15\text{ mm}$ pitch along the bridge crown ensure flame front propagation velocity of $>1.2\text{ m/s}$ ($<0.25\text{ seconds}$ total propagation time across plaques).

### 4.2 4-Burner $2 \times 2$ Cruciform Crossover Hub
- **Architecture**: A 4-way orthogonal cruciform star bridge centered at the intersection of all four cassettes ($X = 0, Y = 0$).
- **Multi-Axis Expansion Compliance**: The cruciform hub features four independent telescoping slip wings that slide into the adjacent perimeter bezels of all four quadrants. Thermal growth along X and Y moves the wings outward by up to $1.0\text{ mm}$ per quadrant while maintaining continuous flame tunnel overlap.
- **Fail-Safe Ignition**: Spark discharge on Quadrant 1 lights Quadrant 2, 3, and 4 in $<0.30\text{ seconds}$ symmetrically through the central cross chamber.

---

## 5. Implementation Summary & Maintenance Protocol

1. **Tool-Free Field Replacement**:
   - Back off 4 knurled brass thumb nuts by hand (no wrenches required).
   - Belleville springs expand and release clamping pressure.
   - Slide out damaged cassette along the angle rails.
   - Insert new cassette with pre-fitted ceramic gasket.
   - Tighten thumb nuts hand-tight until Belleville springs are $\approx 50\%$ compressed ($1.5 - 2\text{ turns}$ past first contact). Total swap time: **under 90 seconds**.
2. **Hardware Standardization**:
   - Fasteners: Standard metric M5 $\times 0.8\text{ mm}$ 304 SS captive studs.
   - Washers: DIN 2093 Belleville disc springs ($10\text{ mm OD} \times 5.2\text{ mm ID} \times 0.6\text{ mm}$ thickness, Inconel or 17-7 PH SS).
   - Nuts: M5 knurled brass C360 thumb nuts with collar.
   - Insulators: Steatite ceramic flat washers ($15\text{ mm OD} \times 5.5\text{ mm ID} \times 3.0\text{ mm}$ thick).
