"""Maker library package for 3D parametric CAD modeling and DIY fabrication."""

__version__ = "0.3.0"

from phi_works.maker.render import (
    export_orthogonal_views,
    render_single_view,
    save_model,
    close_model,
    HAS_GUI,
)
from phi_works.maker.components import import_component
from phi_works.maker.materials import (
    get_materials_dir,
    init_materials,
    list_materials,
    get_material,
    apply_material,
    get_mass_properties,
    format_mass_report,
)

__all__ = [
    "export_orthogonal_views",
    "render_single_view",
    "save_model",
    "close_model",
    "HAS_GUI",
    "import_component",
    "get_materials_dir",
    "init_materials",
    "list_materials",
    "get_material",
    "apply_material",
    "get_mass_properties",
    "format_mass_report",
]

