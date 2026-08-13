"""
Component Loader & Assembly Import Utilities

Provides helpers to locate, import, and place pre-built 3D CAD component models (.FCStd)
from `components/` into project assembly documents.
"""

import os
import FreeCAD

def get_component_path(component_name):
    """
    Resolves the absolute path to `components/<component_name>/<component_name>.FCStd`.
    """
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    maker_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "..", ".."))
    
    comp_dir = os.path.join(maker_dir, "components", component_name)
    fcstd_path = os.path.join(comp_dir, f"{component_name}.FCStd")
    
    if not os.path.exists(fcstd_path):
        raise FileNotFoundError(f"Component CAD model not found: {fcstd_path}")
        
    return fcstd_path

def import_component(doc, component_name, placement=None, group_label=None):
    """
    Imports a pre-built component `.FCStd` document into `doc` and positions it.

    Parameters:
      doc: FreeCAD Document target assembly document
      component_name: String, directory name under `components/` (e.g., 'torch_hf91037')
      placement: FreeCAD.Placement (optional), spatial placement to position imported objects
      group_label: String (optional), custom label for the created App::DocumentObjectGroup container

    Returns:
      App::DocumentObjectGroup container containing the imported component objects.
    """
    fcstd_path = get_component_path(component_name)
    
    # Track existing objects in document before merging
    existing_objs = set(doc.Objects)
    
    # Merge component project into assembly document
    doc.mergeProject(fcstd_path)
    
    # Identify newly merged objects
    imported_objs = [o for o in doc.Objects if o not in existing_objs]
    
    # Create subassembly group container
    grp_name = f"{component_name}_subassembly"
    grp = doc.addObject("App::DocumentObjectGroup", grp_name)
    grp.Label = group_label or f"{component_name} Subassembly"
    
    # Add top-level imported objects to group
    for o in imported_objs:
        if o.InList:
            parent_in_imported = any(p in imported_objs for p in o.InList)
            if parent_in_imported:
                continue
        grp.addObject(o)

    # Apply Placement transformation if provided
    if placement is not None:
        if isinstance(placement, FreeCAD.Vector):
            placement = FreeCAD.Placement(placement, FreeCAD.Rotation())
            
        for o in imported_objs:
            if hasattr(o, "Placement"):
                o.Placement = placement.multiply(o.Placement)

    doc.recompute()
    return grp

__all__ = ["get_component_path", "import_component"]
