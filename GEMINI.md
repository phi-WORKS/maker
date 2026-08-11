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
- `projects/`: Physical assembly projects (`projects/kombi-kaddy/`, `projects/road-roaster/`), organized by self-contained version subdirectories (`v01/`, `v02/`, ..., `v10/`).
- `templates/`: Boilerplate starter scripts (`component_template.py`, `project_template.py`).
- `pyproject.toml`: Package metadata, dependencies, and build settings (`phi_works_maker`).
- `WORKFLOW.md`: Official Maker Collaboration & CAD Best Practices Guide.
- `README.md`: Master project suite overview and workspace navigation.
- `ROADMAP.md`: Strategic roadmap for future component modeling and physical projects.

---

## Agent Operating Directives

1. **Component Modularization**: When modeling commercial tools, burners, or attachments, build them first as standalone 3D modules in `components/` before placing them into project assemblies.
2. **Self-Contained Versioning & Evolutionary Project Indices**: Store design iterations in self-contained version folders (`projects/<project>/v01/`, `v02/`, ..., `vXX/`), each housing its standalone `build.py`, `.FCStd` model, cut lists, and specs. The project root folder `projects/<project>/` contains **only a single `README.md` as the project landing page** (Title, Subtitle, Description of Utility, and a reverse-chronological evolutionary version history featuring representative snapshot images for each version). Do not leave loose `.FCStd`, `.png`, or spec files in project root folders.
3. **Dynamic Pathing**: Resolve script paths dynamically relative to `__file__` (never hardcode local `/home/phi/...` workspace paths).
4. **No STEP Export Overhead**: Do not generate `.step` files during routine builds; generate STEP models only upon explicit user request.
5. **Vector Math Rule**: Use non-mutating vector addition (`v1 + v2`) in FreeCAD Python API. Never use `vec.add(other)` in a chained fashion as it mutates vectors in place.
6. **Tree View Part Containers**: Organize assembly models using `App::DocumentObjectGroup` or `App::Part` subassembly containers.
7. **Git Feature Branching**: Execute new features, refactors, and version iterations on dedicated Git branches (`feature/<name>` or `version/<name>`).
8. **Documentation Standard**: Keep `README.md`, `REQUIREMENTS.md`, `SPECIFICATION.md`, `CUT_LIST.md`, `FABRICATION_GUIDE.md`, and `BOM.md` updated for every project version.
9. **Shared Library Architecture (`src/`)**: Utilize `src/phi_works/maker` for shared Python utilities, CAD routines, and rendering exports (`phi_works.maker.render`) rather than duplicating helper code in individual build scripts.
