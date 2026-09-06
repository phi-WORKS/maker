"""
Assembly helpers for FreeCAD 1.1 Assembly Workbench.

Provides programmatic wrappers for:
- Assembly::AssemblyObject containers
- Grounded and kinematic joints (Fixed, Revolute, Slider, etc.)
- Programmatic Exploded Views and translation steps
"""
import FreeCAD

try:
    from PySide import QtCore
    import builtins
    if not hasattr(builtins, "QtCore"):
        builtins.QtCore = QtCore
except Exception:
    pass

try:
    import UtilsAssembly
    import JointObject
    import CommandCreateView
    HAS_ASSEMBLY = True
except (ImportError, NameError):
    HAS_ASSEMBLY = False


def create_assembly(doc, name: str = "Assembly", label: str = "Assembly"):
    """
    Create or retrieve an Assembly::AssemblyObject root container.

    Args:
        doc: FreeCAD Document
        name: Internal object name
        label: Tree view label

    Returns:
        Assembly::AssemblyObject
    """
    existing = doc.getObject(name)
    if existing and existing.isDerivedFrom("Assembly::AssemblyObject"):
        return existing

    assy = doc.addObject("Assembly::AssemblyObject", name)
    assy.Label = label
    doc.recompute()
    return assy


def create_ground_joint(doc, assembly, obj, name: str = "GroundJoint"):
    """
    Anchor / ground a base part to assembly space.

    Args:
        doc: FreeCAD Document
        assembly: Assembly::AssemblyObject
        obj: DocumentObject to ground
        name: Name of ground joint object

    Returns:
        The created GroundedJoint object
    """
    if not HAS_ASSEMBLY:
        raise RuntimeError("Assembly workbench modules (JointObject, UtilsAssembly) not available")

    target_obj = obj
    if not hasattr(target_obj, "Placement") and hasattr(target_obj, "Group"):
        for child in target_obj.Group:
            if hasattr(child, "Placement"):
                target_obj = child
                break
            elif hasattr(child, "Group"):
                for sub in child.Group:
                    if hasattr(sub, "Placement"):
                        target_obj = sub
                        break

    joint_grp = UtilsAssembly.getJointGroup(assembly)
    ground = joint_grp.newObject("App::FeaturePython", name)
    ground.Label = f"Ground ({target_obj.Label})"
    JointObject.GroundedJoint(ground, target_obj)
    ground.Visibility = False
    
    if hasattr(ground, "ViewObject") and ground.ViewObject:
        try:
            JointObject.ViewProviderGroundedJoint(ground.ViewObject)
            ground.ViewObject.Visibility = False
        except Exception:
            pass

    joint_grp.Visibility = False
    doc.recompute()
    return ground


def _normalize_subelements(sub):
    """
    Ensures a joint reference subelements list contains at least 2 string elements [elt, vtx].
    This prevents FreeCAD's JointObject.py migrationScript4 from raising:
    'IndexError: list index out of range' when indexing ref[1][0] and ref[1][1].
    """
    if not sub:
        return ["", ""]
    if isinstance(sub, str):
        return [sub, ""]
    if isinstance(sub, (list, tuple)):
        if len(sub) == 0:
            return ["", ""]
        elif len(sub) == 1:
            return [str(sub[0]), ""]
        else:
            return [str(sub[0]), str(sub[1])]
    return ["", ""]


def create_joint(
    doc,
    assembly,
    joint_type: str,
    obj1,
    sub1: str = "",
    obj2=None,
    sub2: str = "",
    name: str = None,
    placement1=None,
    placement2=None,
    offset1=None,
    offset2=None,
    angle: float = None,
    distance: float = None,
):
    """
    Create a kinematic joint between two components or between a component and ground.

    Supported types: 'Fixed', 'Revolute', 'Cylindrical', 'Slider', 'Ball',
                     'Distance', 'Parallel', 'Perpendicular', 'Angle',
                     'RackPinion', 'Screw', 'Gears', 'Belt'

    Args:
        doc: FreeCAD Document
        assembly: Assembly::AssemblyObject
        joint_type: One of JointObject.JointTypes
        obj1: First DocumentObject
        sub1: Sub-element of obj1 (e.g. "Face1", "Edge1", or "")
        obj2: Second DocumentObject (optional)
        sub2: Sub-element of obj2 (optional)
        name: Joint name
        placement1: FreeCAD.Placement for coordinate system 1
        placement2: FreeCAD.Placement for coordinate system 2
        offset1: FreeCAD.Placement attachment offset 1
        offset2: FreeCAD.Placement attachment offset 2
        angle: Angle value in degrees (if applicable)
        distance: Distance value in mm (if applicable)

    Returns:
        The created Joint object
    """
    if not HAS_ASSEMBLY:
        raise RuntimeError("Assembly workbench modules not available")

    if joint_type not in JointObject.JointTypes:
        raise ValueError(f"Unknown joint type '{joint_type}'. Available: {JointObject.JointTypes}")

    if name is None:
        name = f"{joint_type}Joint"

    joint_grp = UtilsAssembly.getJointGroup(assembly)
    joint = joint_grp.newObject("App::FeaturePython", name)
    
    type_idx = JointObject.JointTypes.index(joint_type)
    JointObject.Joint(joint, type_idx)
    joint.Visibility = False

    if hasattr(joint, "ViewObject") and joint.ViewObject:
        try:
            JointObject.ViewProviderJoint(joint.ViewObject)
            joint.ViewObject.Visibility = False
        except Exception:
            pass

    # Assign references
    if obj1:
        joint.Reference1 = (obj1, _normalize_subelements(sub1))
    if obj2:
        joint.Reference2 = (obj2, _normalize_subelements(sub2))

    # Detach & custom placements if provided
    if placement1 is not None:
        joint.Detach1 = True
        joint.Placement1 = placement1
    if placement2 is not None:
        joint.Detach2 = True
        joint.Placement2 = placement2

    if offset1 is not None:
        joint.Offset1 = offset1
    if offset2 is not None:
        joint.Offset2 = offset2

    if angle is not None and hasattr(joint, "Angle"):
        joint.Angle = angle
    if distance is not None and hasattr(joint, "Distance"):
        joint.Distance = distance

    doc.recompute()
    return joint


def solve_assembly(assembly):
    """
    Solve assembly constraints.

    Args:
        assembly: Assembly::AssemblyObject

    Returns:
        int: 0 on solver success, non-zero on failure
    """
    return assembly.solve()


def create_exploded_view(doc, assembly, name: str = "ExplodedView", label: str = "Exploded View"):
    """
    Create an ExplodedView container nested under assembly Views.

    Args:
        doc: FreeCAD Document
        assembly: Assembly::AssemblyObject
        name: Object name
        label: User-facing label

    Returns:
        App::FeaturePython ExplodedView object
    """
    if not HAS_ASSEMBLY:
        raise RuntimeError("Assembly workbench modules not available")

    exp_view = doc.addObject("App::FeaturePython", name)
    exp_view.Label = label
    CommandCreateView.ExplodedView(exp_view)

    if hasattr(exp_view, "ViewObject") and exp_view.ViewObject:
        try:
            CommandCreateView.ViewProviderExplodedView(exp_view.ViewObject)
        except Exception:
            pass

    v_grp = UtilsAssembly.getViewGroup(assembly)
    if v_grp:
        v_grp.addObject(exp_view)

    doc.recompute()
    return exp_view


def add_exploded_step(
    doc,
    exploded_view,
    target_obj,
    offset_vector: FreeCAD.Vector,
    sub: str = "",
    name: str = None,
    label: str = None,
):
    """
    Add a translation step to an ExplodedView.

    Args:
        doc: FreeCAD Document
        exploded_view: ExplodedView object
        target_obj: Object to translate in exploded state
        offset_vector: FreeCAD.Vector offset [X, Y, Z]
        sub: Sub-element string (default empty string "")
        name: Step object name
        label: Step label

    Returns:
        The created ExplodedViewStep object
    """
    if not HAS_ASSEMBLY:
        raise RuntimeError("Assembly workbench modules not available")

    step_count = len(exploded_view.Group) + 1 if hasattr(exploded_view, "Group") else 1
    if name is None:
        name = f"Step{step_count:03d}"
    if label is None:
        label = f"Step {step_count}: {target_obj.Label}"

    step = doc.addObject("App::FeaturePython", name)
    step.Label = label
    CommandCreateView.ExplodedViewStep(step)

    step.References = (target_obj, sub)
    step.MovementTransform = FreeCAD.Placement(offset_vector, FreeCAD.Rotation())

    exploded_view.addObject(step)
    doc.recompute()
    return step


def is_origin_object(target):
    """
    Check if an object is an origin coordinate system container, axis, plane, or point.
    """
    type_id = getattr(target, "TypeId", "")
    name = getattr(target, "Name", "").lower()
    return (
        type_id in ("App::Origin", "App::Line", "App::Plane", "App::Point")
        or type_id.startswith("App::Origin")
        or "origin" in type_id.lower()
        or name.startswith("origin")
        or "_axis" in name
        or "_plane" in name
        or name in ("x_axis", "y_axis", "z_axis", "xy_plane", "xz_plane", "yz_plane")
    )


def hide_origins(target):
    """
    Recursively hides all origin features (coordinate axes, planes, center points) on target.
    Can accept a FreeCAD.Document, AssemblyObject, Part, Group, Link, or list of objects.
    """
    if isinstance(target, FreeCAD.Document):
        for o in target.Objects:
            if is_origin_object(o):
                hide_origins(o)
        return

    if isinstance(target, (list, tuple, set)):
        for o in target:
            hide_origins(o)
        return

    if is_origin_object(target):
        if hasattr(target, "Visibility"):
            target.Visibility = False
        if hasattr(target, "ViewObject") and target.ViewObject:
            try:
                target.ViewObject.Visibility = False
            except Exception:
                pass

    if hasattr(target, "Origin") and target.Origin:
        hide_origins(target.Origin)
        for child in getattr(target.Origin, "OutList", []):
            hide_origins(child)

    if hasattr(target, "LinkedObject") and target.LinkedObject:
        hide_origins(target.LinkedObject)

    if hasattr(target, "Group"):
        for child in target.Group:
            hide_origins(child)


def ensure_assembly_visible(target):
    """
    Recursively ensures all assemblies, subassemblies, parts, and linked components
    are explicitly set to Visibility = True, while keeping joints, origin features,
    and helper markers hidden.
    Can accept a FreeCAD.Document, AssemblyObject, Part, Group, Link, or list/collection of objects.
    """
    if isinstance(target, FreeCAD.Document):
        for o in target.Objects:
            ensure_assembly_visible(o)
        hide_origins(target)
        return

    if isinstance(target, (list, tuple, set)):
        for o in target:
            ensure_assembly_visible(o)
        return

    # Check if object is a joint, helper origin, or skeleton sketch intended to be hidden
    type_id = getattr(target, "TypeId", "")
    name = getattr(target, "Name", "").lower()

    is_hidden_type = (
        type_id.startswith("Assembly::Joint")
        or type_id == "Assembly::JointGroup"
        or "joint" in name
        or "ground" in name
        or "skeleton" in name
        or is_origin_object(target)
    )

    if is_hidden_type:
        if hasattr(target, "Visibility"):
            target.Visibility = False
        if hasattr(target, "ViewObject") and target.ViewObject:
            try:
                target.ViewObject.Visibility = False
            except Exception:
                pass
        return

    # For all physical parts, links, assemblies, and groups: make explicitly visible
    if hasattr(target, "Visibility"):
        target.Visibility = True
    if hasattr(target, "ViewObject") and target.ViewObject:
        try:
            target.ViewObject.Visibility = True
        except Exception:
            pass

    # Ensure Part or Assembly origin remains hidden
    if hasattr(target, "Origin") and target.Origin:
        hide_origins(target.Origin)

    # Recurse into App::Link
    if hasattr(target, "LinkedObject") and target.LinkedObject:
        ensure_assembly_visible(target.LinkedObject)

    # Recurse into Containers (Assembly, Part, Group)
    if hasattr(target, "Group"):
        for child in target.Group:
            ensure_assembly_visible(child)
