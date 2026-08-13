# Engineering Specification — Kombi Kaddy Version 10 (Master Optimal Version)

## 1. Executive Overview

Version 10 represents the optimal design iteration of the STIHL Kombi Tool Caddy. It incorporates:
- **24-inch Outside Post Spacing**: Fits standard 24" workbench/garage stud spacing and fits standard hand-truck wheel tracks.
- **36-inch 1x4 Cantilever Rails**: 6.0-inch overhang on each side provides storage capacity for 4 Kombi attachments without overcrowding.
- **Calibrated Standing Height**: Overall post height of 44.5 inches (1130.3 mm) places tool spring clips at 42.75 inches, matching the standing height of Kombi shafts resting on the 1x4 deck.
- **1x4 Tool Deck Slats**: 2x 1x4 slats mounted across front toe overhang create a stable floor for attachment gearboxes while allowing debris/water drainage.

---

## 2. Parametric Dimension Matrix (`dims`)

| Parameter | Nominal Imperial | Metric Value | Description |
| :--- | :--- | :--- | :--- |
| `LumberWidth` | 3.5 in | 88.9 mm | Actual 2x4 and 1x4 lumber width |
| `LumberThickness` | 1.5 in | 38.1 mm | Actual 2x4 post/foot thickness |
| `RailThickness` | 0.75 in | 19.05 mm | Actual 1x4 rail and deck slat thickness |
| `CaddyHeight` | 44.5 in | 1130.3 mm | Total frame vertical height |
| `CaddyWidth` | 36.0 in | 914.4 mm | Total width of upper/lower 1x4 cross rails and deck |
| `PostSpan` | 24.0 in | 609.6 mm | Outside width between vertical side posts |
| `RailOverhang` | 6.0 in | 152.4 mm | Cantilever overhang distance on left/right sides |
| `BaseLength` | 15.0 in | 381.0 mm | Length of base foot |
| `LapDepth` | 0.75 in | 19.05 mm | Half-lap cut depth for post-to-foot joint |
| `PostOffset` | 8.5 in | 215.9 mm | Rearward post offset from front toe (provides 8.5" front clearance) |

---

## 3. Structural Analysis & Joints

1. **Base Half-Lap Joint**:
   - 2x4 vertical posts join 2x4 base feet via 3.5" x 3.5" x 0.75" half-lap dado cuts secured with 4x #10 x 2-1/2" screws per side.
2. **Flush Dado Rail Mounts**:
   - Upper top rail (1x4) and lower rear rail (1x4) sit in 0.75" deep dado pockets in vertical posts for a flush structural fit.
3. **Anti-Racking Plywood Gussets**:
   - 3/4" Plywood triangular gussets (8.75" x 8.75") mounted across the rear lower post/rail joint prevent lateral sway.
4. **Mobility**:
   - 5-inch fixed rubber casters mounted at the rear heel of base feet enable easy tilt-and-roll transport.
