# GEMINI.md: Maker Agent Context & Operating Manual

**Workspace Root**: `/home/phi/PROJECTS/phi-WORKS/maker`  
**Organization Rule**: `RULE[user_global]` (`phiarchitect` / `phi-WORKS`)  
**FreeCAD AppImage Command**:  
`/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='<script_path>'; exec(open(__file__).read())"`  

---

## Workspace Purpose & Context

`maker` is the central repository for physical design, FreeCAD 3D parametric modeling, component library development, and DIY fabrication documentation. It consolidates all projects (`kombi-kaddy`, `road-roaster`) under a single folder structure for seamless single-agent context retention and handoff.

---

## Folder Layout

- `src/`: Primary Python package library (`src/phi_works/maker/`) for shared CAD helpers and rendering utilities.
- `components/`: Reusable commercial tools and hardware modules (e.g., `components/torch_hf91037/`, `components/kombi_tools/`).
- `projects/`: Physical assembly projects (`projects/kombi-kaddy/`, `projects/road-roaster/`), organized by self-contained version subdirectories (`v0.0.0/`, `v0.1.0/`, ..., `v0.9.0/`).
- `templates/`: Boilerplate starter scripts (`component_template.py`, `project_template.py`).
- `pyproject.toml`: Package metadata, dependencies, and build settings (`phi_works_maker`).
- `WORKFLOW.md`: Official Maker Collaboration & CAD Best Practices Guide.
- `README.md`: Master project suite overview and workspace navigation.
- `ROADMAP.md`: Strategic roadmap for future component modeling and physical projects.

---

## Agent Operating Directives

1. **Component Modularization & File Import**: Build commercial tools, burners, or attachments first as standalone CAD modules under `components/<component_name>/`. Running `components/<component_name>/build.py` generates `<component_name>.FCStd` and multi-view PNG snapshot renders. Project assemblies consume components by importing their pre-built `.FCStd` models via `import_component(doc, component_name, placement=...)` rather than housing component CAD geometry code inside `src/`.
2. **Semantic Versioning & Evolutionary Project Indices**: Store design iterations in self-contained version folders (`projects/<project>/v0.0.0/`, `v0.1.0/`, `v0.2.0/`), each housing its standalone `build.py`, `.FCStd` model, cut lists, and specs. Project root landing pages (`projects/<project>/README.md`) must display a reverse-chronological evolutionary version history featuring representative isometric snapshot thumbnails (`<model>_iso.png`) and standardized lifecycle status badges (`🟡 IN PROGRESS`, `🔵 FABRICATION READY`, `🟢 BUILT & VERIFIED`, `📦 SUPERSEDED`). Do not leave loose `.FCStd`, `.png`, or spec files in project root folders.
3. **Dynamic Pathing**: Resolve script paths dynamically relative to `__file__` (never hardcode local `/home/phi/...` workspace paths).
4. **No STEP Export Overhead**: Do not generate `.step` files during routine builds; generate STEP models only upon explicit user request.
5. **Vector Math Rule**: Use non-mutating vector addition (`v1 + v2`) in FreeCAD Python API. Never use `vec.add(other)` in a chained fashion as it mutates vectors in place.
6. **Tree View Part Containers**: Organize assembly models using `App::DocumentObjectGroup` or `App::Part` subassembly containers.
7. **Git Feature Branching**: Execute new features, refactors, and version iterations on dedicated Git branches (`feature/<name>` or `version/<name>`).
8. **Documentation Standard**: Keep `README.md`, `REQUIREMENTS.md`, `SPECIFICATION.md`, `CUT_LIST.md`, `FABRICATION_GUIDE.md`, and `BOM.md` updated for every project version.
9. **Shared Library Architecture (`src/`)**: Utilize `src/phi_works/maker` for shared Python infrastructure, CAD file import/placement helpers (`phi_works.maker.components.import_component`), and rendering exports (`phi_works.maker.render`). Keep `src/` free of component CAD geometry code.
