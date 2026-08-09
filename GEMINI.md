# GEMINI.md: Maker Agent Context & Operating Manual

**Workspace Root**: `/home/phi/PROJECTS/phi-WORKS/maker`  
**Organization Rule**: `RULE[user_global]` (`phiarchitect` / `phi-WORKS`)  
**FreeCAD AppImage Command**:  
`/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage -c "__file__='<script_path>'; exec(open(__file__).read())"`  

---

## Workspace Purpose & Context

`maker` is the central repository for physical design, FreeCAD 3D parametric modeling, component library development, and DIY fabrication documentation. It consolidates all projects (`caddy`, `flame-weeding-sled`) under a single folder structure for seamless single-agent context retention and handoff.

---

## Folder Layout

- `components/`: Reusable commercial tools and hardware modules (e.g., `components/torch_hf91037/`, `components/kombi_tools/`).
- `projects/`: Physical assembly projects (`projects/caddy/`, `projects/flame-weeding-sled/`), organized by self-contained version subdirectories (`v01/`, `v02/`, ..., `v10/`).
- `templates/`: Boilerplate starter scripts (`component_template.py`, `project_template.py`).
- `sketches/`: Raw user freehand sketches, dimension photos, and field notes.
- `WORKFLOW.md`: Official Maker Collaboration & CAD Best Practices Guide.
- `README.md`: Master project suite overview and workspace navigation.
- `ROADMAP.md`: Strategic roadmap for future component modeling and physical projects.

---

## Agent Operating Directives

1. **Component Modularization**: When modeling commercial tools, burners, or attachments, build them first as standalone 3D modules in `components/` before placing them into project assemblies.
2. **Self-Contained Versioning**: Store design iterations in self-contained version folders (`projects/<project>/v01/`, `v02/`, ..., `v10/`), each housing its standalone `build.py`, `.FCStd` model, cut lists, and specs. Keep the project root `.FCStd` updated to the latest master version.
3. **Dynamic Pathing**: Resolve script paths dynamically relative to `__file__` (never hardcode local `/home/phi/...` workspace paths).
4. **No STEP Export Overhead**: Do not generate `.step` files during routine builds; generate STEP models only upon explicit user request.
5. **Vector Math Rule**: Use non-mutating vector addition (`v1 + v2`) in FreeCAD Python API. Never use `vec.add(other)` in a chained fashion as it mutates vectors in place.
6. **Tree View Part Containers**: Organize assembly models using `App::DocumentObjectGroup` or `App::Part` subassembly containers.
7. **Documentation Standard**: Keep `README.md`, `SPECIFICATION.md`, `CUT_LIST.md`, `FABRICATION_GUIDE.md`, and `BOM.md` updated for every project version.
