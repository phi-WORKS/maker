"""
Component Loader & Assembly Import Utilities

Provides helpers to locate, import, and place pre-built 3D CAD component models (.FCStd)
from `components/` into project assembly documents.
"""

import os
import FreeCAD

def get_component_path(component_name):
    """
    Resolves the absolute path to `<component_name>.FCStd` under `components/`.
    Supports direct names ('torch_hf91037', 'kombi_shaft'), relative subpaths
    ('stihl/kombi_shaft', 'stihl/tools/kombi_trimmer_fs'), and recursive lookup.
    """
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    maker_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "..", ".."))
    components_root = os.path.join(maker_dir, "components")

    # 0. Direct file path check (absolute or relative)
    if os.path.exists(component_name):
        return os.path.abspath(component_name)

    base_name = os.path.basename(component_name)
    
    # 1. Direct path check under components/
    direct_path = os.path.join(components_root, component_name, f"{base_name}.FCStd")
    if os.path.exists(direct_path):
        return direct_path
        
    # 2. Check if component_name was passed with .FCStd extension
    if component_name.endswith(".FCStd"):
        direct_file = os.path.join(components_root, component_name)
        if os.path.exists(direct_file):
            return direct_file

    # 3. Recursive directory search under components/
    target_filename = f"{base_name}.FCStd"
    for root, dirs, files in os.walk(components_root):
        if target_filename in files and os.path.basename(root) == base_name:
            return os.path.join(root, target_filename)
            
    # 4. Fallback search for any matching filename in case directory != filename
    for root, dirs, files in os.walk(components_root):
        if target_filename in files:
            return os.path.join(root, target_filename)
            
    raise FileNotFoundError(f"Component CAD model not found: '{component_name}' in {components_root}")

def import_component(doc, component_name, placement=None, label=None, as_link=True, group_label=None):
    """
    Imports a pre-built component `.FCStd` document into `doc` and positions it.
    When `as_link=True` (default), creates a native FreeCAD `App::Link` pointing to the component's
    root `App::Part` or `Assembly::AssemblyObject`, keeping the assembly document clean, modular,
    and solver-compatible.

    Parameters:
      doc: FreeCAD Document target assembly document (must be saved via saveAs() first for relative paths)
      component_name: String, directory name or path under `components/` (e.g., 'torch_hf91037', 'kombi_trimmer_fs')
      placement: FreeCAD.Placement (optional), spatial placement to position imported objects
      label: String (optional), custom label for the created App::Link
      as_link: Boolean (default True), whether to link to external component or merge project
      group_label: String (optional), legacy alias for label if as_link=False

    Returns:
      App::Link DocumentObject (if as_link=True) or App::DocumentObjectGroup (if as_link=False).
    """
    from phi_works.maker.materials import init_materials

    # Ensure material library paths are registered before loading component
    init_materials()

    fcstd_path = get_component_path(component_name)
    base_name = os.path.basename(component_name).replace(".FCStd", "")
    final_label = label or group_label

    if as_link:
        if not getattr(doc, "FileName", None):
            # Auto-save target document to current working directory so FreeCAD can resolve relative link paths
            auto_path = os.path.abspath(f"{doc.Name}.FCStd")
            doc.saveAs(auto_path)

        # Check if component document is already open
        comp_doc = None
        for dname, d in FreeCAD.listDocuments().items():
            if getattr(d, "FileName", None) and os.path.abspath(d.FileName) == os.path.abspath(fcstd_path):
                comp_doc = d
                break
        if not comp_doc:
            comp_doc = FreeCAD.openDocument(fcstd_path)

        # Locate root Part/Assembly container in component document
        # Note: Do not use comp_doc.RootObjects because FreeCAD removes objects from RootObjects
        # as soon as another open document links to them via App::Link!
        root_candidates = comp_doc.Objects
        root_obj = None
        for o in root_candidates:
            if o.Name == "Materials" or o.isDerivedFrom("App::MaterialObject"):
                continue
            # Only consider unparented objects within its own document
            in_doc_parents = [p for p in getattr(o, "InList", []) if getattr(p, "Document", None) == comp_doc]
            if o.TypeId in ("Assembly::AssemblyObject", "App::Part") and not in_doc_parents:
                root_obj = o
                break
        if not root_obj:
            for o in root_candidates:
                if o.Name == "Materials" or o.isDerivedFrom("App::MaterialObject"):
                    continue
                in_doc_parents = [p for p in getattr(o, "InList", []) if getattr(p, "Document", None) == comp_doc]
                if not in_doc_parents and hasattr(o, "Shape"):
                    root_obj = o
                    break

        if not root_obj:
            raise RuntimeError(f"No linkable root Part or Assembly found in '{fcstd_path}'")

        # Find target Assembly object if present
        assy = None
        for o in doc.Objects:
            if o.TypeId == "Assembly::AssemblyObject":
                assy = o
                break

        link_name = f"Link_{base_name}"
        if assy:
            link = assy.newObject("App::Link", link_name)
        else:
            link = doc.addObject("App::Link", link_name)

        link.setLink(root_obj)
        link.Label = final_label or getattr(root_obj, "Label", base_name)

        if placement is not None:
            if isinstance(placement, FreeCAD.Vector):
                placement = FreeCAD.Placement(placement, FreeCAD.Rotation())
            link.Placement = placement

        # Ensure link and all subcomponents are explicitly set to visible, and origins are hidden
        from phi_works.maker.assembly import ensure_assembly_visible, hide_origins
        ensure_assembly_visible(link)
        ensure_assembly_visible(root_obj)
        hide_origins(comp_doc)
        hide_origins(doc)

        doc.recompute()
        return link

    # Fallback: legacy mergeProject implementation
    existing_objs = set(doc.Objects)
    doc.mergeProject(fcstd_path)
    imported_objs = [o for o in doc.Objects if o not in existing_objs]

    grp_name = f"{base_name}_subassembly"
    grp = doc.addObject("App::DocumentObjectGroup", grp_name)
    grp.Label = final_label or f"{base_name} Subassembly"

    for o in imported_objs:

        if o.InList:
            parent_in_imported = any(p in imported_objs for p in o.InList)
            if parent_in_imported:
                continue
        grp.addObject(o)

    if placement is not None:
        if isinstance(placement, FreeCAD.Vector):
            placement = FreeCAD.Placement(placement, FreeCAD.Rotation())
        for o in imported_objs:
            if not o.isDerivedFrom("App::MaterialObject") and hasattr(o, "Placement"):
                o.Placement = placement.multiply(o.Placement)

    doc.recompute()
    return grp

__all__ = ["get_component_path", "import_component"]
