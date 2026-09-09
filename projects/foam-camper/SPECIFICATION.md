# Compact Foam Camper - Technical Specification

> **Physical Dimensions, Station Geometry, and Volumetric Comparison**  
> *Project Version: v0.1.0*

---

## 1. Master Envelope & Baseline Dimensions

The models are parameterized via FreeCAD's native `App::VarSet` (`Vars`) container inside `foam-camper.FCStd`:

| Parameter Name | Value (Metric) | Value (Imperial) | Description |
| :--- | :--- | :--- | :--- |
| `CamperLength` | 3,658.0 mm | 12'-0" (144.0") | Overall length of the camper body (front prow to rear transom) |
| `CamperWidth` | 1,981.0 mm | 6'-6" (78.0") | Maximum outer width at shoulder station |
| `CamperHeight` | 1,750.0 mm | 5'-9" (68.9") | Maximum outer height above trailer deck |
| `FoamThickness` | 50.8 mm | 2.0" | Standard commercial Extruded Polystyrene (XPS) sheet thickness |
| `AxleStation` | 2,194.8 mm | 7'-2.4" (86.4") | 60% rearward trailer axle balance reference line |
| `TrailerTongue` | 900.0 mm | 35.4" | Front triangular coupler tongue extension |
| `DisplaySpacing`| 3,200.0 mm | 10'-6" (126.0") | Lateral offset between comparative 3D showcase models |

---

## 2. Volumetric & Mass Engineering Properties

Using material card [`materials/polymers/Polymer-XPS-Foam.FCMat`](../../materials/polymers/Polymer-XPS-Foam.FCMat) with nominal density $\rho = 32\ \text{kg/m}^3$ ($2.0\ \text{lb/cu.ft}$):

| Form Model | Solid Volume (m³) | Solid Volume (cu.ft) | Est. Surface Area (m²) | Est. 2" Foam Shell Weight |
| :--- | :---: | :---: | :---: | :---: |
| **Form A (Carved Aero)** | **6.94 m³** | 245.0 cu.ft | ~28.5 m² (306 sq.ft) | **~123 lbs** (56 kg) |
| **Form B (Faceted Chine)** | **8.41 m³** | 297.1 cu.ft | ~32.8 m² (353 sq.ft) | **~142 lbs** (64 kg) |
| **Form C (Lofted Organic)** | **8.53 m³** | 301.2 cu.ft | ~33.4 m² (360 sq.ft) | **~145 lbs** (66 kg) |

*Note: Solid volume represents the total enclosed displacement. Foam shell weight is calculated based on a 2.0" (50.8 mm) continuous perimeter foam wall over floor, walls, and roof.*

---

## 3. Station Rib & Geometry Breakdown

### Form A: Dual-Axis Carved Aero Capsule
- **Elevation Curve (XZ)**:
  - Nose prow: Extends from floor $(X=180, Z=0)$ through bullet nose $(X=0, Z=650)$ to windshield $(X=400, Z=1400)$.
  - Roof crown: Apex at $(X=1200, Z=1750)$, sloping smoothly rearward to $(X=3000, Z=1420)$.
  - Kamm tail: Slopes down to rear transom $(X=3658, Z=480)$ with vertical drop to floor.
- **Plan Curve (XY)**:
  - Nose tip: Pointed prow at $X=0, Y=0$.
  - Shoulder beam: Expands to full half-width $Y = \pm 990.5\ \text{mm}$ at $X=1300\ \text{mm}$.
  - Boat-tail taper: Tapers inward to $Y = \pm 752.8\ \text{mm}$ at the rear transom ($X=3658\ \text{mm}$).
- **Shoulder Roll**: 180 mm compound edge blend along the top perimeter.

### Form B: Multi-Chine Faceted Hull (Kerf-Score Angles)
Form B is defined by 4 stations with 8 faceted segments per station:
- **Station 0 (Nose Wedge, $X=0\ \text{mm}$)**: Width 1,288 mm, Height 1,100 mm.
- **Station 1 (Shoulder Apex, $X=1100\ \text{mm}$)**: Width 1,981 mm, Height 1,750 mm.
- **Station 2 (Mid-Cabin, $X=2400\ \text{mm}$)**: Width 1,862 mm, Height 1,645 mm.
- **Station 3 (Rear Transom, $X=3658\ \text{mm}$)**: Width 1,505 mm, Height 750 mm.

**Chine Dihedral Fold Angles**:
1. **Floor to Plinth**: 90° vertical plinth ($Z = 0$ to $480\ \text{mm}$).
2. **Plinth to Lower Tumblehome Chine**: $\sim 12^\circ$ inward fold ($168^\circ$ interior angle).
3. **Lower Chine to Shoulder Chine**: $\sim 28^\circ$ inward fold ($152^\circ$ interior angle).
4. **Shoulder Chine to Roof Crown**: $\sim 35^\circ$ fold ($145^\circ$ interior angle).
5. **Roof Cap**: Flat/crowned center panel spanning the top centerline.

### Form C: Multi-Station Arched Loft
- **Station 0 ($X=0\ \text{mm}$)**: Nose entry arch, $W = 1,307\ \text{mm}$, $H = 1,050\ \text{mm}$.
- **Station 1 ($X=1100\ \text{mm}$)**: Master cabin peak, $W = 1,981\ \text{mm}$, $H = 1,750\ \text{mm}$, tumblehome ratio $0.84$.
- **Station 2 ($X=2400\ \text{mm}$)**: Galley transition, $W = 1,862\ \text{mm}$, $H = 1,610\ \text{mm}$, tumblehome ratio $0.86$.
- **Station 3 ($X=3658\ \text{mm}$)**: Rear transom arch, $W = 1,466\ \text{mm}$, $H = 900\ \text{mm}$, tumblehome ratio $0.90$.
