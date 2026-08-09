# Master Requirements Specification — STIHL Kombi Attachment Caddy

## 1. Vision & Purpose

Design and build a mobile, heavy-duty wooden storage caddy to organize and store STIHL KombiSystem powerheads and attachments (line trimmer, hedge trimmer, pole pruner, mini-cultivator tiller, leaf blower, rubber power sweep, curved lawn edger).

The caddy must provide vertical tool storage, allow rapid attachment access, prevent tool tip-overs, and offer smooth mobility across shop floors and yard terrain.

---

## 2. Functional Requirements

| Req ID | Requirement Statement | Priority | Verification Method |
| :--- | :--- | :---: | :--- |
| **FR-01** | **Vertical Storage**: Store up to 4 STIHL Kombi attachments vertically using wall-mount spring clips. | High | Physical Test & CAD Model |
| **FR-02** | **Tool Head Clearance**: Provide at least 8.5 inches of front toe overhang space so heavy tool heads (tiller tines, hedge trimmer blades, blower nozzles) do not hit the frame posts. | High | FreeCAD Collision Inspection |
| **FR-03** | **Floor Deck Slats**: Provide horizontal 1x4 deck slats across base feet so attachment shafts sit vertically supported off the floor with 0.5" drainage gaps. | Medium | Physical Assembly |
| **FR-04** | **Mobility**: Mount 2x 5-inch fixed rubber casters at the rear heel of base feet for tilt-and-roll transport. | High | Mechanical Test |
| **FR-05** | **Anti-Racking Stability**: Incorporate 3/4" plywood corner gussets to prevent lateral frame racking when fully loaded. | High | Load Test |

---

## 3. Dimensional & Shop Constraints

| Constraint | Value | Rationale |
| :--- | :--- | :--- |
| **Post Spacing (`PostSpan`)** | 24.0 in (609.6 mm) | Aligns with standard 24" garage/shop wall stud spacing & wheel tracks. |
| **Overall Rail Width (`CaddyWidth`)** | 36.0 in (914.4 mm) | Provides 6.0 in cantilever rail overhangs on each side to space 4 clips without crowding. |
| **Post Height (`CaddyHeight`)** | 44.5 in (1130.3 mm) | Calibrated so clip grab point sits at 42.75 in, matching 39.5" standing Kombi shaft height off deck. |
| **Base Foot Length (`BaseLength`)** | 15.0 in (381.0 mm) | Compact foot depth to maximize shop floor space while preventing forward tipping. |
| **Stock Lumber** | 2x4 and 1x4 Dimensional Lumber | Standard construction lumber workable with miter saw, table saw, and drill press. |

---

## 4. Requirement Evolutionary Traceability

- **v01–v03**: Initial flat 2x4 frame and compact 15" foot.
- **v04–v05**: Full top rail, sloped front toe, and 3/4" rear plywood gussets.
- **v06**: Offset vertical posts 8.5" rearward to grant front tool head clearance.
- **v07–v08**: Housed 1x4 cross rails in dado post pockets and added 1x4 tool head deck slats.
- **v09**: Calibrated overall height to 44.5" based on 39.5" real-world Kombi tool standing height.
- **v10**: Expanded overall rail width to 36.0" with 24.0" post span and 6.0" cantilever overhangs (Optimal Version).
