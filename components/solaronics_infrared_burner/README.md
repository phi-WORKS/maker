# Solaronics High-Intensity Ceramic Infrared Burner & Parabolic Reflector

> **Standalone 3D CAD Component Module**  
> *phi-WORKS Maker Component Library (`components/solaronics_infrared_burner/`)*

---

## 1. Overview & Thermal Physics

This module models the **Solaronics USA** high-intensity ceramic infrared burner and deep parabolic reflector assembly adapted as the primary downward-firing radiant thermal engine for the **Road Roaster** platform.

### Core Features:
1. **Grooved Cordierite Ceramic Plaque Matrix**: $173\text{ sq. in}$ ($315\text{ mm} \times 355\text{ mm}$) active glowing radiant surface operating at **$1,600^\circ\text{F} - 1,800^\circ\text{F}$** ($870^\circ\text{C} - 980^\circ\text{C}$).
2. **Flameless Surface Micro-Pore Combustion**: Operates at standard $11''\text{ W.C.}$ low-pressure LP gas ($60,000\text{ BTU/hr}$) with **zero dynamic air blast pressure** (completely eliminating the blown gravel, dust, and flying spark hazards of open blast torches).
3. **Deep Parabolic Aluminum Reflector**: Specially contoured mirror-bright aluminum reflector concentrating $>90\%$ of infrared radiation straight downward into the weed root zone with a tight $90^\circ$ conical spread.
4. **Inconel Re-Radiating Wire Grid**: High-emissivity mesh screen positioned across the ceramic face that elevates surface radiant temperatures while protecting the ceramic tiles from gravel impact.
5. **Premix Venturi Induction Manifold**: Rear-mounted atmospheric air mixer with precision brass orifice jet ($1/2''\text{ FPT}$ gas connection).

---

## 2. Technical Specifications & Dimensions

| Parameter | Metric / Imperial | Description |
| :--- | :--- | :--- |
| **Radiating Surface** | $173\text{ sq. in}$ ($315\text{ mm} \times 355\text{ mm}$) | Cordierite grooved ceramic plaque array |
| **Thermal Input** | $60,000\text{ BTU/hr}$ ($17.6\text{ kW}$) | Propane (LP) / Natural Gas @ 11" W.C. |
| **Reflector Base** | $345.0\text{ mm} \times 385.0\text{ mm}$ ($13.6'' \times 15.2''$) | Mirror-bright parabolic aluminum reflector mouth |
| **Reflector Height** | $110.0\text{ mm}$ ($4.33\text{ in}$) | Parabolic reflector depth |
| **Plaque Thickness** | $12.7\text{ mm}$ ($0.5\text{ in}$) | Standard cordierite ceramic thickness |
| **Gas Connection** | $1/2''\text{ FPT}$ | Brass orifice nozzle & manifold block |
| **Operating Temp** | $1,600^\circ\text{F} - 1,800^\circ\text{F}$ | Surface radiant emission |

---

## 3. Build & Visual Renders

To build the standalone `.FCStd` CAD model and regenerate orthogonal/isometric renders:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='components/solaronics_infrared_burner/build.py'; exec(open(__file__).read())"
```
