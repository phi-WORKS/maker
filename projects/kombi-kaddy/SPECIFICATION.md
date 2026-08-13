# Kombi Kaddy — Master Technical Specification

> **Mobile STIHL KombiSystem Attachment Rack**  
> *Single-Source Architectural & Engineering Specification*

---

## 1. Executive Summary & Design Purpose

The **Kombi Kaddy** is a mobile vertical storage system designed specifically for the STIHL KombiSystem attachment ecosystem (trimmers, edgers, hedge trimmers, tillers, pole saws, blowers).

### Core Design Objectives
1. **Vertical Storage Density**: Holds 4 full-length Kombi attachments upright in spring clips.
2. **Mobility & Ergonomics**: Integrated rear 5" fixed rubber casters for tilt-and-roll transport across shop floors and job sites.
3. **Garage Alignment**: 24.0 in post spacing aligns with standard 16"/24" wall stud centers.
4. **Cantilever Deck & Rail Expansion**: 36.0 in overall rail width provides 6.0 in cantilever overhangs on each side, eliminating clip crowding for wide tool heads.
5. **Calibrated Standing Height**: 44.5 in post height places clip grab centers at 42.75 in, matching standard 39.5 in attachment standing heights.

---

## 2. Parametric VarSet (`dims`) Specification

All dimensions are managed parametrically in FreeCAD via `App::VarSet` (`dims`):

| Parameter Name | Value (Metric / Imperial) | Description |
| :--- | :--- | :--- |
| `LumberWidth` | $88.9\text{ mm}$ ($3.5\text{ in}$) | Actual width of 2x4 and 1x4 dimensional lumber |
| `LumberThickness` | $38.1\text{ mm}$ ($1.5\text{ in}$) | Actual thickness of 2x4 vertical post stock |
| `RailThickness` | $19.05\text{ mm}$ ($0.75\text{ in}$) | Actual thickness of 1x4 cross rails and floor deck slats |
| `CaddyWidth` | $914.4\text{ mm}$ ($36.0\text{ in}$) | Overall width of top/bottom rails and floor deck |
| `CaddyHeight` | $1130.3\text{ mm}$ ($44.5\text{ in}$) | Overall frame post height |
| `PostSpan` | $609.6\text{ mm}$ ($24.0\text{ in}$) | Outside spacing between vertical 2x4 posts |
| `RailOverhang` | $152.4\text{ mm}$ ($6.0\text{ in}$) | Cantilever overhang of 1x4 rails past vertical posts |
| `BaseLength` | $381.0\text{ mm}$ ($15.0\text{ in}$) | Base foot depth |
| `LapDepth` | $19.05\text{ mm}$ ($0.75\text{ in}$) | Half-lap cut depth for base foot joinery |
| `PostOffset` | $215.9\text{ mm}$ ($8.5\text{ in}$) | Rearward offset of posts from front foot toe |

---

## 3. Structural Joinery & Assembly Tree

The assembly document `caddy.FCStd` consists of the following components:

```
caddy.FCStd (Kombi Kaddy Assembly)
├── dims (App::VarSet)
├── Base_Foot_Left (Part::Feature - 2x4 Foot with sloped toe & half-lap notch)
├── Base_Foot_Right (Part::Feature - 2x4 Foot with sloped toe & half-lap notch)
├── Post_Left (Part::Feature - 2x4 Post with top/rear 0.75" dado pockets)
├── Post_Right (Part::Feature - 2x4 Post with top/rear 0.75" dado pockets)
├── Upper_Top_Rail_1x4 (Part::Feature - 36" 1x4 cross rail)
├── Lower_Cross_Rail_Rear_1x4 (Part::Feature - 36" 1x4 cross rail)
├── Tool_Deck_Slat_Front_1x4 (Part::Feature - 36" 1x4 floor slat)
├── Tool_Deck_Slat_Rear_1x4 (Part::Feature - 36" 1x4 floor slat)
├── Plywood_Gusset_Left (Part::Feature - 3/4" rear triangular corner gusset)
├── Plywood_Gusset_Right (Part::Feature - 3/4" rear triangular corner gusset)
├── Wheel_Left (Part::Feature - 5" Fixed Caster)
├── Wheel_Right (Part::Feature - 5" Fixed Caster)
├── Spring_Clip_[1..4] (Part::Feature - Spring clip holders)
└── Kombi_Shaft_[1..4] (Part::Feature - Visual tool shaft representations)
```

---

## 4. Materials & Automated Property Integration

- **Primary Frame**: Softwood Lumber (SPF 2x4 & 1x4).
- **Bracing**: 3/4" Exterior Plywood.
- **Hardware**: 5" Fixed Caster Wheels (Rubber/Steel), Heavy-Duty Spring Clips ($25\text{--}35\text{ mm}$ diameter grab range).
- **Fasteners**: 2-1/2" Wood Screws (frame), 1-1/4" Pocket/Wood Screws (slats & gussets).
