# Vintage Commercial Hand Truck Chassis (Restored Red Frame)

> **Standalone 3D CAD Component Module**  
> *phi-WORKS Maker Component Library (`components/commercial_hand_truck/`)*

---

## 1. Overview & Donor Frame Restoration

This module models an authentic vintage tubular steel hand truck donor frame (restored in industrial Red) adapted as the mobile structural base for the **Road Roaster** directional radiant weed shock sled:

- **Inverted U-Frame**: Single continuous $1.0''\text{ OD}$ tubular steel pipe forming both vertical side risers and a smooth 180° semi-circular top arc.
- **Center Handle Spine Pipe**: $1.0''\text{ OD}$ round steel tube welded to the top of the U-bend, curving backward into a high-back loop handle ($Y \approx +160\text{ mm}$), then bending down to meet the cross-straps and running straight down the vertical centerline ($X = 0$).
- **Authentic Triangular Axle Trusses**: Dual-strut triangular truss brackets welded to the vertical uprights and converging at the wheel axle sleeves.
- **Common-Axis Wheel Pivot**: $\varnothing 9.5''$ wheels on a $5/8''$ continuous steel axle centered at **$4.75''$ from the floor and $4.75''$ from the side rail plane**.

---

## 2. Technical Specifications & Verified Dimensions

| Feature | Value (Metric / Imperial) | Description |
| :--- | :--- | :--- |
| **Upright Tubing** | $\varnothing 25.4\text{ mm}$ ($1.0\text{ in}$) | Steel tubing with $1.0''\text{ OD}$ ($25.4\text{ mm}$) |
| **Riser Spacing** | $317.5\text{ mm}$ ($12.5\text{ in}$) | Center-to-center upright spacing ($X = \pm 158.75\text{ mm}$) |
| **Total Height (Top of U)** | $1168.4\text{ mm}$ ($46.0\text{ in}$) | Ground to top outer edge of semi-circular U-bend |
| **Top U-Bend Radius** | $158.75\text{ mm}$ ($6.25\text{ in}$) | 180° semi-circular bend transitioning at $Z = 996.95\text{ mm}$ |
| **Center Spine Pipe** | $\varnothing 25.4\text{ mm}$ ($1.0\text{ in}$) | Loop handle reach $Y = +160\text{ mm}$, vertical run along $X = 0$ |
| **Horizontal Straps** | 3x $25.4\text{ mm} \times 4.76\text{ mm}$ ($1.0'' \times 3/16''$) | Flat steel straps; top edges at **$12.0''$, $22.0''$, and $31.0''$** |
| **Wheels** | $\varnothing 241.3\text{ mm} \times 76.2\text{ mm}$ ($9.5'' \times 3.0''$) | Heavy-duty all-terrain rubber tires with stamped steel rims |
| **Axle Shaft** | $\varnothing 15.875\text{ mm}$ ($5/8\text{ in}$) | Solid steel continuous axle ($L = 540\text{ mm} / 21.25\text{ in}$) |
| **Axle Datum Center** | $Y = 120.65\text{ mm}, Z = 120.65\text{ mm}$ | Centered at **$4.75''$ from floor and $4.75''$ behind side rails** |
| **Track Width** | $440.0\text{ mm}$ ($17.3\text{ in}$) | Center-to-center wheel stance |
| **Axle Trusses** | Dual $1.0'' \times 3/16''$ Steel Straps | Lower strut from $Z = 30\text{ mm}$; upper strut from Strap 1 ($Z = 292\text{ mm}$) |

---

## 3. Build & Visual Renders

To build the standalone `.FCStd` CAD model and regenerate all 7 orthogonal/isometric renders:

```bash
/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='components/commercial_hand_truck/build.py'; exec(open(__file__).read())"
```
