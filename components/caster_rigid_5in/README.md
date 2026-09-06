# 5.0" Commercial Rigid Plate Caster Assembly

**Component Type**: Commercial Off-The-Shelf (COTS) Running Gear Subassembly  
**Target Applications**: Commercial Platform Dollies, Workshop Equipment Carts, Kombi Kaddy

---

## Component Overview

This module provides a standalone 3D CAD model for a heavy-duty industrial **5.0" (127 mm) rigid plate caster**:
* **Mounting Plate**: Heavy-gauge stamped steel top plate ($85.0\text{ mm} \times 100.0\text{ mm} \times 4.0\text{ mm}$) with 4 Grade 5 mounting fasteners.
* **Fork Bracket**: Dual formed $3.5\text{ mm}$ stamped steel upright fork legs in corrosion-resistant `Steel-ZincPlated` finish.
* **Axle Hardware**: Grade 5 $3/8''$ ($9.525\text{ mm}$) axle bolt, dual zinc-plated flat washers, and locking hex nut.
* **Running Gear**: Directly consumes the [5.0" Caster Wheel](../caster_wheel_5in/) component (`Rubber-Solid` tread on `Polyurethane` safety yellow hub).

---

![5.0" Rigid Caster](caster_rigid_5in.png)

---

## Specifications

| Parameter | Metric (mm) | Imperial (in) | Material |
| :--- | :--- | :--- | :--- |
| **Overall Height** | $150.0\text{ mm}$ | $5.91''$ | `Steel-ZincPlated` |
| **Wheel Diameter** | $127.0\text{ mm}$ | $5.00''$ | Composite |
| **Tread Face Width** | $35.0\text{ mm}$ | $1.38''$ | `Rubber-Solid` |
| **Top Plate Dimensions** | $85.0 \times 100.0\text{ mm}$ | $3.35 \times 3.94''$ | `Steel-ZincPlated` |
| **Plate Thickness** | $4.0\text{ mm}$ | $0.16''$ | `Steel-ZincPlated` |
| **Axle Bolt Size** | $\varnothing 9.525\text{ mm}$ | $3/8''$ Grade 5 | `Steel-ZincPlated` |
| **Total Weight** | $1.150\text{ kg}$ | $2.54\text{ lbs}$ | Composite |

---

## 3D CAD Multi-View Gallery

| Front Elevation | Rear Elevation | Top Plan |
| :---: | :---: | :---: |
| ![Front](caster_rigid_5in_front.png) | ![Back](caster_rigid_5in_back.png) | ![Top](caster_rigid_5in_top.png) |
| **Bottom Plan** | **Left Side** | **Right Side** |
| ![Bottom](caster_rigid_5in_bottom.png) | ![Left](caster_rigid_5in_left.png) | ![Right](caster_rigid_5in_right.png) |

---

## Python Usage

```python
from phi_works.maker.components import import_component
# Import rigid caster into any assembly
caster = import_component(doc, "caster_rigid_5in", placement=placement)
```
