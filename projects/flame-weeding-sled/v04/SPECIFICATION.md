# Project Specification: Towable Flame Weeding Sled

**Document Version**: 1.3  
**Project Lead**: DIY Fabricator / CAD Designer  
**Primary Application**: Gravel driveway weed suppression via targeted thermal shock  
**Key Goal**: Lightweight, heat-concentrating drag hood for efficient 1 lb propane torch operation  
**Torch Unit**: Harbor Freight Propane Torch with Push-Button Igniter (Item #91037)  

---

## 1. System Architecture & Operating Principles

The system consists of a ground-contact drag hood pulled ahead of the operator via a hinged rigid tow bar extending forward. The Harbor Freight #91037 torch burner is mounted in an overhead steel frame above the pyramidal hood. The burner nozzle points down and rearward ($35^\circ$ toward $+Y$), while the torch wand shaft and blue handle lean **180° forward towards the operator pulling at the front** for effortless control and ignition access.

```
   (Direction of Travel <--- Operator Pulls Forward)

                             [ Torch Handle Leans Forward ]
   [ Tow Handle Grip ]             /
            |                     / (Harbor Freight #91037 Torch Mounted)
            |-- (Tow Bar 5 ft)   / 
            |                   /
            +-------------\    /
                           \ (Single-Axis Vertical Hinge @ Front)
                            \
                    +--------v-------------------------------+
                    | Front Skirt (Low Clearance)            |
                    |                                        |
                    |       [ Pyramidal Hood / Flange ]      |
                    |     (14-gauge Mild Steel)              |
                    |                                        |
                    |         \ (Flame Directed Rearward @ 35°)|
                    |          v                             |  [ Rear Exhaust Vent ]
                    +========================================+=======================>
                      \____________________________________/ (Steel Skid Runners)
```

### Thermal Mechanics

- **Target Mechanism**: Thermal disruption of plant cellular walls ($150^\circ\text{F}$–$180^\circ\text{F}$ / $65^\circ\text{C}$–$80^\circ\text{C}$) rather than complete combustion to ash. Heating cell sap causes cell walls to burst, interrupting photosynthesis and starving root systems.
- **Flame Orientation & Heat Containment**: The burner nozzle is angled $35^\circ$ down and rearward (away from the puller). The pyramidal hood acts as a large heat-concentrating flange, trapping superheated air ($1,000^\circ\text{F}+$ exhaust gases) over the ground and driving hot exhaust out the rear vent.

---

## 2. Mechanical Design & Geometric Specs

### 2.1 Hood & Heat Flange Geometry (Pyramidal Design)
- **Base Footprint**: $18.0'' \times 18.0''$ square ($457.2\text{ mm} \times 457.2\text{ mm}$).
- **Top Apex Opening**: $4.0'' \times 4.0''$ square flat top ($101.6\text{ mm} \times 101.6\text{ mm}$) centered under the overhead torch frame.
- **Vertical Height (Hood Rise)**: $6.0''$ ($152.4\text{ mm}$) from base flange to apex top.
- **Facet Slant Height**: $\approx 9.6''$ ($243.9\text{ mm}$) along face centerline.
- **Material**: 14-gauge ($0.075''$ / $1.9\text{ mm}$) A36 Hot Rolled Mild Steel Sheet.

### 2.2 Side Skirts & Rear Exhaust Venting
- **Front & Side Skirts**: $2.0''$ ($50.8\text{ mm}$) vertical extension below the pyramid base. Maintained at approximately $0.5''$ ($12.7\text{ mm}$) clearance above gravel surface.
- **Rear Exhaust Venting**: $1.5'' \times 12.0''$ ($38.1\text{ mm} \times 304.8\text{ mm}$) horizontal cutout along the top of the rear skirt panel. Directs hot flame exhaust away from the operator pulling at the front.

### 2.3 Runners / Skids (Ground Contact)
- **Configuration**: Dual skid runners mounted along left and right lower skirt edges.
- **Material**: $1.5'' \text{ wide} \times 3/16'' \text{ thick}$ ($38.1\text{ mm} \times 4.76\text{ mm}$) mild steel flat bar.
- **Profile**: Tips turned upward at $30^\circ$ angles ($2.0''$ rise) on both front and rear ends to glide over loose gravel aggregate without plowing.

---

## 3. Burner Subsystem & Ergonomic Forward-Leaning Torch Frame

### 3.1 Harbor Freight #91037 Torch Interface
- **Torch Model**: Harbor Freight Propane Torch with Push Button Igniter (Item #91037).
- **Overhead Mounting Frame**: Fabricated steel bridge frame mounted over the top apex opening with a $3/16''$ clamp sleeve angled $35^\circ$ forward towards the operator.
- **Nozzle Orientation**: Torch nozzle recessed $1.5''$ inside the apex chamber, tilted $35^\circ$ rearward (flame points toward the rear exhaust vent, away from the operator).
- **Forward Handle Ergonomics**: The torch wand shaft curves $180^\circ$ forward so the blue handle, brass flow control knob, squeeze trigger lever, and red piezo igniter button lean forward towards the puller for instant access while walking ahead.

### 3.2 Fuel Delivery Setup
- **Propane Tank**: Single 1 lb disposable or refillable propane tank carried in a shoulder holster or backpack rig.
- **Extension Line**: Flexible high-pressure propane extension hose connecting 1 lb cylinder to the torch handle.

---

## 4. Towing & Rigging System

### 4.1 Forward Tow Bar Assembly
- **Length**: $5.0\text{ ft}$ ($60''$) rigid steel tube ($3/4'' \times 3/4'' \times 1/16''$ square wall tubing).
- **Orientation**: Extends forward from the front skirt clevis hitch (away from the hood). Operator pulls the sled walking forward.
- **Handle**: T-handle grip ($8''$ cross bar) at comfortable pulling height ($\approx 35''$ above ground).

### 4.2 Hinged Hitch Interface & 20° Drop-Stop Tab
- **Coupling Construction**: Double-ear clevis hitch bracket ($3/16''$ steel plate) welded to front center hood skirt with a $3/8''$ clevis pin.
- **Pivot Mechanical Stop**: Weld a $1'' \times 1''$ angle iron rest tab on the hitch bracket to catch the tow bar at a $20^\circ$ minimum angle. This prevents the dropped tow bar from falling onto the ground when released.

---

## 5. Bill of Materials (BOM)

| Item # | Description | Spec / Dimensions | Qty | Est. Weight | Sourcing Source |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **01** | Hood Sheet Metal | 14-ga A36 Mild Steel ($24'' \times 24''$ sheet) | 1 | 9.0 lbs | Steel Service Center / Scrap Drop |
| **02** | Skid Runners & Frame | $1.5'' \times 3/16''$ Mild Steel Flat Bar | 6 ft | 5.5 lbs | MetalsDepot / Home Depot |
| **03** | Tow Bar Tube | $3/4''$ Square Steel Tubing (16-ga) | 5 ft | 2.5 lbs | Local Metal Supply |
| **04** | Propane Torch Unit | Harbor Freight Torch w/ Piezo Igniter (Item #91037) | 1 | 2.5 lbs | Harbor Freight Tools |
| **05** | Reinforcement Angles | $1'' \times 1'' \times 1/8''$ Angle Iron | 3 ft | 1.2 lbs | Metal Supply |
| **06** | Propane Tank Rig | 1 lb Propane Cylinder & Shoulder Harness | 1 | 1.0 lb | Camping / Propane Retailer |
| **07** | Clevis Hardware & Stop Tab | $3/8''$ Clevis Pin, Cotter Clip & $3/16''$ Bracket | 1 kit | 0.5 lbs | Hardware Store / Scrap Flat Bar |
| **TOTAL** | **Estimated Sled Weight** | *(Excluding Fuel Cylinder)* | | **~22.2 lbs** | |
