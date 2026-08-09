# Changelog

All notable changes to the **Maker** repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.3.0] - 2026-08-09

### Added
- **Multi-View Camera Projections (`render_all_camera_views`)**: Implemented complete 7-projection FreeCAD camera setup (Isometric Home, Top Plan, Front Elevation, Right Side Elevation, Left Side Elevation, Bottom Plan, Rear/Back Elevation) in `projects/caddy/v10/build.py`.
- **View-Framing Safety (`view.fitAll()`)**: Guaranteed exact bounding framing on every camera view transition to eliminate model clipping.
- **Caddy 7-View Visual Galleries**: Embedded complete 7-projection CAD visual gallery tables into [`projects/caddy/v10/README.md`](projects/caddy/v10/README.md) and [`projects/caddy/README.md`](projects/caddy/README.md).
- **Master Visual Gallery Upgrade**: Updated root [`README.md`](README.md) to feature Caddy Front & Side projections alongside Isometric views.

---

## [0.2.0] - 2026-08-09

### Added
- **Deep Markdown Navigation & Indexing**: Added multi-level README indices across root, component libraries (`components/torch_hf91037/README.md`, `components/kombi_tools/README.md`), master projects (`projects/caddy/README.md`, `projects/flame-weeding-sled/README.md`), and version subdirectories (`projects/caddy/v10/README.md`, `projects/flame-weeding-sled/v04/README.md`).
- **Embedded 3D Visual Galleries**: Integrated high-resolution side-by-side CAD render snapshots (`caddy_v10.png`, `flame_sled_iso.png`, `trimmer_iso.png`, `kombi_tools.png`) directly into README documents across all folder levels.
- **Direct Document Links**: Established deep cross-links from master project hubs directly to `REQUIREMENTS.md`, `SPECIFICATION.md`, `CUT_LIST.md`, `FABRICATION_GUIDE.md`, `BOM.md`, and `build.py` scripts.

---

## [0.1.0] - 2026-08-09

### Added
- **Engelbart AI-Human Collaboration Framework**: Integrated Douglas Engelbart's 1962 vision (*Augmenting Human Intellect*) into root [`README.md`](README.md) detailing the human-agent pair-designing loop.
- **Living Requirements Lifecycle**: Introduced [`REQUIREMENTS.md`](WORKFLOW.md#3-fabrication-documentation-standard) at project roots and version-specific subdirectories (`projects/caddy/REQUIREMENTS.md`, `projects/caddy/v10/REQUIREMENTS.md`, `projects/flame-weeding-sled/REQUIREMENTS.md`, `projects/flame-weeding-sled/v04/REQUIREMENTS.md`).
- **Git Feature Branching Workflow Policy**: Documented standard operating directive requiring dedicated feature/version branches (`feature/<name>`, `version/<name>`) before merging into `main`.
- **Master Repository Changelog**: Created root [`CHANGELOG.md`](CHANGELOG.md) to log framework releases and project milestone history.

### Changed
- **Commercial Tool Isolation**: Isolated purchased tools into standalone 3D modules in `components/` ([`components/torch_hf91037/`](components/torch_hf91037/), [`components/kombi_tools/`](components/kombi_tools/)).
- **Self-Contained Version Subdirectories**: Refactored physical projects into zero-padded version folders (`v01/`..`v10/` for Caddy, `v01/`..`v04/` for Flame Weeding Sled). Each folder houses its own `build.py`, `.FCStd` CAD model, render images, cut lists, and specs.
- **Dynamic Path Resolution**: Converted all hardcoded workspace paths in Python scripts to dynamic relative resolution using `os.path.dirname(os.path.abspath(__file__))`.
- **Updated Operating Manuals**: Refreshed [`WORKFLOW.md`](WORKFLOW.md), [`GEMINI.md`](GEMINI.md), and project `README.md` files to reflect the updated architecture.

### Fixed
- **FreeCAD Headless Teardown**: Updated scripts to safely resolve output paths when run via AppImage `-c "__file__='...'; exec(open(__file__).read())"`.
