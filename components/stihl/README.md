# STIHL Equipment Ecosystem Library

> **Commercial Power Units, Drive Modular Shafts & Kombi Attachments**  
> *phi-WORKS Maker Framework (`components/stihl/`)*

---

## Ecosystem Overview

The `components/stihl/` directory consolidates the 3D parametric CAD models for the user's complete fleet of STIHL professional landscaping equipment. Built according to FreeCAD 1.1 material property cards (`Plastic-StihlOrange`, `Plastic-StihlWhite`, `Aluminum-6061-T6`, `CastIron-Gray`, `Steel-A36`), each module provides accurate physical weights, 3D Center of Gravity (CoG), and 7-view render galleries.

```
components/stihl/
├── README.md                  # Master STIHL fleet index
├── kombi_shaft/               # Shared 25.4mm modular aluminum drive tube
├── stihl_kma200r/             # KMA 200 R AP-system cordless KombiEngine power head
└── tools/                     # KombiSystem attachment tools
    ├── README.md              # 7-attachment tool suite catalog
    ├── kombi_trimmer_fs/      # FS-KM straight shaft string trimmer (AutoCut 25-2)
    ├── kombi_brushcutter_fs/  # FS-KM brush cutter (3-tooth triangular steel blade)
    ├── kombi_blower_bg/       # BG-KM in-line coaxial axial blower
    ├── kombi_scythe_fh/       # FH-KM 145° articulating scrub scythe
    ├── kombi_pruner_ht/       # HT-KM 12" in-line pole pruner chainsaw
    ├── kombi_bed_redefiner_fbd/ # FBD-KM bed redefiner (4-tine scoop rotor + guide wheel)
    └── kombi_cultivator_bf/   # BF-KM mini-cultivator (4 starburst pick tine rotors)
```

---

## 1. Power Units & Drive Infrastructure

### [STIHL KMA 200 R AP-System KombiEngine](stihl_kma200r/)

| Power Unit Preview | Specifications & Role |
| :---: | :--- |
| [![STIHL KMA 200 R](stihl_kma200r/stihl_kma200r.png)](stihl_kma200r/) | • **Description**: Professional high-torque cordless KombiEngine power unit.<br>• **Features**: STIHL Orange EC brushless motor shroud, STIHL White rear electronics chassis, AP 500 S battery pack, ergonomic control grip with variable throttle trigger, rubberized loop handle (R) with barrier bar, and quick-release split clamp sleeve.<br>• **Interface**: $Z = 0$ tool coupling datum receiving any Kombi attachment.<br>• **Weight**: $14.16\text{ lbs}$ ($6.424\text{ kg}$) with AP 500 S battery.<br>• 📖 [**`stihl_kma200r/README.md`**](stihl_kma200r/README.md) |

### [STIHL Kombi Standard Modular Drive Shaft](kombi_shaft/)

| Drive Shaft Preview | Specifications & Role |
| :---: | :--- |
| [![STIHL Kombi Shaft](kombi_shaft/kombi_shaft.png)](kombi_shaft/) | • **Description**: Standard $25.4\text{ mm}$ ($1.0''$) OD drawn aluminum drive tube ($850\text{ mm}$ length).<br>• **Features**: Quick-connect coupler sleeve (`Plastic-ABS`), spring detent pin, rubber grip band, and internal driveshaft bore.<br>• **Role**: Shared modular drive tube foundation consumed across all straight-shaft KombiSystem attachments.<br>• **Weight**: $0.72\text{ lbs}$ ($0.325\text{ kg}$).<br>• 📖 [**`kombi_shaft/README.md`**](kombi_shaft/README.md) |

---

## 2. [KombiSystem Attachment Suite (`tools/`)](tools/)

The complete 7-tool attachment suite is housed in the [**`tools/`**](tools/) subfolder:

| Tool Attachment | Working Action | Weight | Master Model |
| :--- | :--- | :---: | :---: |
| **[FS-KM Line Trimmer](tools/kombi_trimmer_fs/)** | AutoCut 25-2 dual $2.4\text{ mm}$ line bump feed ($420\text{ mm}$ swath) | $4.17\text{ lbs}$ | [`kombi_trimmer_fs.FCStd`](tools/kombi_trimmer_fs/kombi_trimmer_fs.FCStd) |
| **[FS-KM Brush Cutter](tools/kombi_brushcutter_fs/)** | 3-tooth triangular hardened steel brush knife ($250\text{ mm}$) | $4.54\text{ lbs}$ | [`kombi_brushcutter_fs.FCStd`](tools/kombi_brushcutter_fs/kombi_brushcutter_fs.FCStd) |
| **[BG-KM In-Line Blower](tools/kombi_blower_bg/)** | Concentric $6.0''$ axial blower with two-stage tapered black nozzle | $2.59\text{ lbs}$ | [`kombi_blower_bg.FCStd`](tools/kombi_blower_bg/kombi_blower_bg.FCStd) |
| **[FH-KM Power Scythe](tools/kombi_scythe_fh/)** | $145^\circ$ articulating dual reciprocating scythe scrub cutters ($250\text{ mm}$) | $4.31\text{ lbs}$ | [`kombi_scythe_fh.FCStd`](tools/kombi_scythe_fh/kombi_scythe_fh.FCStd) |
| **[HT-KM 12" Pole Pruner](tools/kombi_pruner_ht/)** | In-line $12''$ ($300\text{ mm}$) Rollomatic E Mini guide bar & Picco saw chain | $6.67\text{ lbs}$ | [`kombi_pruner_ht.FCStd`](tools/kombi_pruner_ht/kombi_pruner_ht.FCStd) |
| **[FBD-KM Bed Redefiner](tools/kombi_bed_redefiner_fbd/)** | 4-tine bent scoop digging rotor ($200\text{ mm}$) + $180\text{ mm}$ guide wheel | $10.98\text{ lbs}$ | [`kombi_bed_redefiner_fbd.FCStd`](tools/kombi_bed_redefiner_fbd/kombi_bed_redefiner_fbd.FCStd) |
| **[BF-KM Mini-Cultivator](tools/kombi_cultivator_bf/)** | Center worm drive + 4 starburst pick tine rotors ($220\text{ mm}$ tilling width) | $8.38\text{ lbs}$ | [`kombi_cultivator_bf.FCStd`](tools/kombi_cultivator_bf/kombi_cultivator_bf.FCStd) |

*For full multi-view galleries, dimensional drawings, and material breakdowns, visit the [**Tools Subfolder Catalog (`tools/README.md`)**](tools/README.md).*

---

## Python Assembly Usage

All STIHL modules can be imported directly into project assemblies (such as the [Kombi Kaddy](../../projects/kombi-kaddy/)):

```python
from phi_works.maker.components import import_component

# Import power head
powerhead = import_component(doc, "stihl_kma200r", placement=pl_head)

# Import attachments
trimmer = import_component(doc, "kombi_trimmer_fs", placement=pl_slot1)
pruner  = import_component(doc, "kombi_pruner_ht",  placement=pl_slot2)
tiller  = import_component(doc, "kombi_cultivator_bf", placement=pl_slot3)
```
