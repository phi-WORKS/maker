# Woodworking Cut List & Bill of Materials (BOM) - Kombi Caddy (Version 8 Master)

## 1. Stock Timber Requirements

- **2x4 Dimensional Construction Lumber**: **1 board @ 10 Feet (120 inches)** OR **2 boards @ 8 Feet (96 inches)**
  - *Actual Cross-Section*: 1.5" x 3.5" (38.1 mm x 88.9 mm)
  - *Used For*: 2x Base Feet (15") + 2x Vertical Side Posts (42")
- **1x4 Dimensional Construction Lumber**: **2 boards @ 8 Feet (96 inches)**
  - *Actual Cross-Section*: 0.75" x 3.5" (19.05 mm x 88.9 mm)
  - *Used For*: 1x Upper Top Rail (36") + 1x Lower Rear Cross Rail (36") + 2x Tool Head Deck Slats (36")
- **3/4" Plywood Scrap**: **1 piece @ 9" x 18"** (for 2x 8.75" x 8.75" right-triangle anti-racking corner gussets)

---

## 2. Cut Diagram & Board Allocation

```
2x4 BOARD 1 [96 inches]:
[=== Base Foot Left (15.0") ===][=== Post Left (42.0") ===][=== Base Foot Right (15.0") ===][Waste 24.0"]

2x4 BOARD 2 [96 inches]:
[=== Post Right (42.0") ===][Waste 54.0"]

1x4 BOARD 1 [96 inches]:
[=== Upper Top Rail (36.0") ===][=== Lower Rear Rail (36.0") ===][Waste 24.0"]

1x4 BOARD 2 [96 inches]:
[=== Deck Slat Front (36.0") ===][=== Deck Slat Rear (36.0") ===][Waste 24.0"]
```

---

## 3. Detailed Parts List

| Part Name | Qty | Thickness | Width | Length | Material | Joint Notes |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Base Feet** | 2 | 1.5" (38 mm) | 3.5" (89 mm) | 15.0" (381 mm) | 2x4 Lumber | Standing on 1.5" edge; 3.5"x3.5" half-lap dado centered at `Y = 8.5"`; underside sloped 30mm upward behind post |
| **Vertical Side Posts** | 2 | 1.5" (38 mm) | 3.5" (89 mm) | 42.0" (1067 mm) | 2x4 Lumber | Narrow 1.5" face forward; 3.5"x3.5"x0.75" bottom half-lap; 0.75"x3.5"x0.75" top front pocket; 0.75"x3.5"x0.75" flush rear lower rail dado |
| **Upper Top Rail** | 1 | 0.75" (19 mm) | 3.5" (89 mm) | 36.0" (914 mm) | 1x4 Lumber | Housed flush into 0.75" top front post pockets |
| **Lower Rear Cross Rail** | 1 | 0.75" (19 mm) | 3.5" (89 mm) | 36.0" (914 mm) | 1x4 Lumber | Housed flush into 0.75" rear post pockets (~9.5" above floor) |
| **Tool Head Deck Slats** | 2 | 0.75" (19 mm) | 3.5" (89 mm) | 36.0" (914 mm) | 1x4 Lumber | Fastened flat on top of base feet (Z = 3.5") across front overhang; 0.5" drainage gap |
| **Rear Plywood Gussets** | 2 | 0.75" (19 mm) | 8.75" (220 mm) | 8.75" (220 mm) | 3/4" Plywood | Right-triangle plates mounted flat across rear post/rail flush joint |

---

## 4. Hardware & Tool Mounts

| Item | Specification | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **Base Half-Lap Screws** | #10 x 2-1/2" Flat Head Wood Screws | 8 | 4 per 3.5"x3.5" half-lap joint |
| **Top Rail Screws** | #10 x 1-1/2" Flat Head Wood Screws | 4 | Fasten 1x4 top rail into 0.75" post pockets |
| **Rear Rail & Gusset Screws** | #10 x 1-1/2" Flat Head Wood Screws | 12 | Secure 1x4 lower rail & flat rear gussets |
| **Tool Deck Slat Screws** | #8 x 1-1/4" Wood Screws | 8 | Fasten 1x4 deck slats down to base feet |
| **Hand-Truck Wheels** | 5" Rubber Fixed Caster Wheels | 2 | Mounted at rear heel of base feet |
| **Wheel Axle Bolts** | 1/4" x 1-1/2" Lag Screws / Axle Pins | 8 | Fasten 5" wheels to base feet |
| **Spring Tool Holder Clips** | Rubber Roller Wall-Mount Clips | 4 | Mounted on top front rail (spaced ~9.5" apart) |
| **Wood Glue** | High-Strength PVA Wood Glue | 1 bottle | All wood-to-wood joint surfaces |

---

## 5. FreeCAD Parametric VarSet (`dims`)

The master model `caddy.FCStd` includes an `App::VarSet` named **`dims`** containing all parametric dimensions:
- `LumberWidth`: `88.9 mm` (3.5 in)
- `LumberThickness`: `38.1 mm` (1.5 in)
- `RailThickness`: `19.05 mm` (0.75 in — 1x4 cross rails & deck)
- `CaddyHeight`: `1066.8 mm` (42 in)
- `CaddyWidth`: `914.4 mm` (36 in)
- `BaseLength`: `381.0 mm` (15 in)
- `LapDepth`: `19.05 mm` (0.75 in)
- `PostOffset`: `215.9 mm` (8.5 in from front toe)
- `DeckSlatCount`: `2` (1x4 tool head resting slats)
