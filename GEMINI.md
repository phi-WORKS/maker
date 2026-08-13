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
2. **Git-Native Versioning & Visual Transformation Changelogs**: Maintain only single active master product files at `projects/<project>/` root (`build.py`, `<model>.FCStd`, `<model>_iso.png`, `SPECIFICATION.md`, `CHANGELOG.md`). Historical CAD model versions are managed natively via Git tags (`v0.0.0`, `v0.1.0`, ...). Historical visual snapshot thumbnails are preserved under `projects/<project>/changelog/` (`vX.Y.Z_iso.png`). Project landing pages (`README.md`) and `CHANGELOG.md` display reverse-chronological evolutionary transformation tables featuring visual milestone thumbnails and release notes. Do not create separate version subdirectories (`v0.0.0/`, `v0.1.0/`).
3. **Dynamic Pathing**: Resolve script paths dynamically relative to `__file__` (never hardcode local `/home/phi/...` workspace paths).
4. **No STEP Export Overhead**: Do not generate `.step` files during routine builds; generate STEP models only upon explicit user request.
5. **Vector Math Rule**: Use non-mutating vector addition (`v1 + v2`) in FreeCAD Python API. Never use `vec.add(other)` in a chained fashion as it mutates vectors in place.
6. **Tree View Part Containers**: Organize assembly models using `App::DocumentObjectGroup` or `App::Part` subassembly containers.
7. **Git Feature Branching**: Execute new features, refactors, and version iterations on dedicated Git branches (`feature/<name>` or `version/<name>`).
8. **Streamlined Master Documentation**: Keep `README.md`, `SPECIFICATION.md`, and `CHANGELOG.md` updated as living master documents for each active project root. Derive material lists and cut dimensions parametrically from model parameters rather than maintaining static overworked spec files.
9. **Shared Library Architecture (`src/`)**: Utilize `src/phi_works/maker` for shared Python infrastructure, CAD file import/placement helpers (`phi_works.maker.components.import_component`), and rendering exports (`phi_works.maker.render`). Keep `src/` free of component CAD geometry code.
