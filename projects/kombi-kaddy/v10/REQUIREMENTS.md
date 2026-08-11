# Version 10 Requirement Refinements — Kombi Kaddy

## 1. Iteration Objectives

Version 10 resolves final ergonomics and spacing constraints discovered during v09 physical testing:
1. **Cantilever Rail Overhangs**: Expand top and lower 1x4 cross rails from 24" to 36" (6.0 in overhang on each side) to mount Spring Clip 1 and 4 on the overhangs, leaving ample space for 4 full-sized attachments.
2. **Stud Alignment**: Keep vertical 2x4 posts spaced at 24.0 in outer span for alignment with shop wall studs and hand-truck wheel track stability.
3. **Tool Deck Slats**: Position 2x 1x4 slats horizontally over base feet at Z = 3.5" to support tool gearboxes.

---

## 2. Requirement Delta & Verification Matrix

| Req ID | Target Requirement | v09 Baseline | v10 Specification | Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| **V10-REQ-1** | **Overall Rail Width** | 24.0 in (Posts flush at rail ends) | 36.0 in (914.4 mm) with 6.0 in cantilever overhangs | PASSED in CAD |
| **V10-REQ-2** | **Outside Post Span** | 24.0 in (609.6 mm) | 24.0 in (609.6 mm) centered under 36" rails | PASSED in CAD |
| **V10-REQ-3** | **Clip Grab Height** | 42.75 in (1085.85 mm) | 42.75 in (1085.85 mm) centered on 1x4 top rail | PASSED in CAD |
| **V10-REQ-4** | **Deck Drainage** | 0.5 in gap between slats | 2x 1x4 slats @ Y=12mm & Y=114mm | PASSED in CAD |
| **V10-REQ-5** | **App::VarSet (`dims`)** | Parametric FreeCAD table | All 10 parametric dimensions updated | PASSED in CAD |
