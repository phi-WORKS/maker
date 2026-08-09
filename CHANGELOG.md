# Changelog

All notable changes to the **Maker** repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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
