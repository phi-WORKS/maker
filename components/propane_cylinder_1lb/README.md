# 1 lb Disposable/Refillable Propane Cylinder Component

**Commercial Product Standard**: Standard 16.4 oz / 1 lb Disposable or Refillable Propane Cylinder (Coleman / Flame King / Worthington standard $3.875'' \times 7.8''$).

---

## Technical Specifications

- **Outer Diameter (Body)**: $3.875''$ ($98.4\text{ mm}$)
- **Total Vertical Height**: $7.8''$ ($198\text{ mm}$)
- **Body Shell Height**: $5.5''$ ($140\text{ mm}$)
- **Base Seat Collar Diameter**: $3.46''$ ($88\text{ mm}$)
- **Base Seat Collar Height**: $0.47''$ ($12\text{ mm}$)
- **Valve Threading**: Standard $1''\text{--}20\text{ UNEF}$ Male Brass Connection
- **Weight (Full)**: $\approx 2.0\text{ lbs}$ ($0.91\text{ kg}$)
- **Tare Weight (Empty)**: $\approx 1.0\text{ lb}$ ($0.45\text{ kg}$)

---

## Model Usage & Insertion Origin

- **Insertion Origin $(0,0,0)$**: Base of the bottom recessed seat collar rim along the central $Z$-axis.
- **Orientation**: Cylinder extends upwards along $+Z$. Valve stem center at top $+Z = 198\text{ mm}$.
- **Python Import**:
  ```python
  from phi_works.maker.components.propane_cylinder_1lb import create_propane_cylinder_component

  tank_grp = create_propane_cylinder_component(doc, placement)
  ```
