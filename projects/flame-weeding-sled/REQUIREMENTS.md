# Master Requirements Specification — Towable Flame Weeding Sled

## 1. Vision & Purpose

Design and build a lightweight, heat-concentrating drag hood pulled ahead of an operator via a 5 ft rigid steel tow bar. Designed for gravel driveway weed management, it utilizes an overhead steel frame mounting a **Harbor Freight #91037 Propane Torch** above an enclosed 14-gauge mild steel pyramidal hood.

Target application: Gravel driveway weed suppression via targeted thermal shock ($150^\circ\text{F}$–$180^\circ\text{F}$).

---

## 2. Functional Requirements

| Req ID | Requirement Statement | Priority | Verification Method |
| :--- | :--- | :---: | :--- |
| **FR-01** | **Heat Concentration**: Enclose thermal output inside an $18'' \times 18''$ 14-gauge steel pyramidal hood with 2.0" vertical skirts and 0.5" ground clearance. | High | Thermal & CAD Inspection |
| **FR-02** | **Exhaust Venting**: Incorporate a $1.5'' \times 12.0''$ rear exhaust vent to direct hot gases away from the operator while maintaining heat trap. | High | CFD & CAD Model |
| **FR-03** | **Torch Clamp**: Mount Harbor Freight #91037 propane torch overhead at a 35-degree forward incline recessed 1.5" into the apex chamber. | High | Assembly Test |
| **FR-04** | **Tow Rigging**: Provide a 5 ft rigid square tube tow bar connected via a front clevis hitch pin with a 20-degree drop-stop rest tab. | High | Mechanical Test |
| **FR-05** | **Tree View Subassemblies**: Structure the 3D model into 4 clean FreeCAD `App::DocumentObjectGroup` subassembly containers. | Medium | FreeCAD Inspection |

---

## 3. Physical Fabrication Constraints

| Constraint | Value | Rationale |
| :--- | :--- | :--- |
| **Sheet Metal** | 14-Gauge Mild Steel (0.075 in / 1.905 mm) | Resists thermal distortion under torch flame; weldable with flux-core MIG. |
| **Skids** | Dual $1.5'' \times 3/16''$ Flat Bar Skids | Turned-up 30-degree tips allow smooth gliding over loose gravel. |
| **Tow Bar Tube** | $3/4''$ Square Steel Tubing (5.0 ft) | Lightweight rigid pull bar; maintains 5 ft safety clearance for operator. |
| **Weight Target** | $< 25$ lbs dry weight (~22.2 lbs actual) | Ensures single-operator hand towing without fatigue. |
