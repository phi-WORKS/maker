"""
Parametric skeleton and VarSet helpers for FreeCAD 1.1.

Enables master 2D skeleton layout modeling with unified App::VarSet
parameter binding and downstream feature reactivity.
"""
import FreeCAD
import Part
import Sketcher


def create_varset(doc, name: str = "Vars", label: str = "Parameters", properties: dict = None):
    """
    Create or retrieve an App::VarSet parameter container.

    Args:
        doc: FreeCAD Document
        name: Object name (default 'Vars')
        label: Tree view label (default 'Parameters')
        properties: Dict of {param_name: value} or {param_name: (prop_type, value, group)}
                    Example: {"Length": 914.4, "Width": 609.6}
                    Example: {"Angle": ("App::PropertyAngle", 45.0, "Angles")}

    Returns:
        App::VarSet object
    """
    existing = doc.getObject(name)
    if existing and existing.isDerivedFrom("App::VarSet"):
        varset = existing
    else:
        varset = doc.addObject("App::VarSet", name)
        varset.Label = label

    if properties:
        for key, val in properties.items():
            if isinstance(val, tuple):
                prop_type = val[0]
                val_data = val[1]
                group = val[2] if len(val) > 2 else "Dimensions"
            elif isinstance(val, (int, float)):
                prop_type = "App::PropertyLength"
                val_data = float(val)
                group = "Dimensions"
            elif isinstance(val, bool):
                prop_type = "App::PropertyBool"
                val_data = val
                group = "Parameters"
            else:
                prop_type = "App::PropertyString"
                val_data = str(val)
                group = "Parameters"

            if not hasattr(varset, key):
                varset.addProperty(prop_type, key, group)
            setattr(varset, key, val_data)

    doc.recompute()
    return varset


def create_skeleton_sketch(doc, name: str = "Skeleton", plane: str = "XY", offset: float = 0.0, label: str = None):
    """
    Create a 2D Skeleton sketch on a specified plane.

    Args:
        doc: FreeCAD Document
        name: Object name
        plane: Coordinate plane ('XY', 'XZ', 'YZ')
        offset: Normal offset distance along the perpendicular axis
        label: Display label (defaults to name)

    Returns:
        Sketcher::SketchObject
    """
    sketch = doc.addObject("Sketcher::SketchObject", name)
    sketch.Label = label or name

    # Map to standard planes
    if plane.upper() == "XY":
        sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, offset), FreeCAD.Rotation())
    elif plane.upper() == "XZ":
        # Rotated 90 deg around X
        sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0, offset, 0), FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90))
    elif plane.upper() == "YZ":
        # Rotated 90 deg around Y
        sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(offset, 0, 0), FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), -90))

    sketch.MapMode = "Deactivated"
    doc.recompute()
    return sketch


def bind_expression(obj, property_name: str, expression: str):
    """
    Bind an object property to an expression (e.g. referencing a VarSet).

    Args:
        obj: DocumentObject
        property_name: Target property name (e.g. 'Length' or 'Constraints[0]')
        expression: Expression formula string (e.g. 'Vars.Length')
    """
    obj.setExpression(property_name, expression)
    if hasattr(obj, "Document") and obj.Document:
        obj.Document.recompute()


def build_box_skeleton(
    sketch,
    length_expr: str,
    width_expr: str,
    centered: bool = False,
):
    """
    Construct a rectangular boundary skeleton in a sketch and bind its dimensions
    to VarSet expressions.

    Args:
        sketch: Sketcher::SketchObject
        length_expr: Expression string for length along local X (e.g. 'Vars.ChassisLength')
        width_expr: Expression string for width along local Y (e.g. 'Vars.ChassisWidth')
        centered: If True, center rectangle on local (0, 0); if False, anchor corner at (0, 0)
    """
    p1 = FreeCAD.Vector(0, 0, 0)
    p2 = FreeCAD.Vector(100, 0, 0)
    p3 = FreeCAD.Vector(100, 50, 0)
    p4 = FreeCAD.Vector(0, 50, 0)

    sketch.addGeometry(Part.LineSegment(p1, p2))
    sketch.addGeometry(Part.LineSegment(p2, p3))
    sketch.addGeometry(Part.LineSegment(p3, p4))
    sketch.addGeometry(Part.LineSegment(p4, p1))

    sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 0, 1))
    sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
    sketch.addConstraint(Sketcher.Constraint("Vertical", 1))
    sketch.addConstraint(Sketcher.Constraint("Horizontal", 2))
    sketch.addConstraint(Sketcher.Constraint("Vertical", 3))

    if centered:
        # Symmetric to X and Y axes
        sketch.addConstraint(Sketcher.Constraint("Symmetric", 0, 1, 0, 2, -2, 1))  # X-symmetric
        sketch.addConstraint(Sketcher.Constraint("Symmetric", 1, 1, 1, 2, -1, 1))  # Y-symmetric
    else:
        # Anchor bottom-left corner to origin (0, 0)
        sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 1, -1, 1))

    idx_len = sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, 0, 2, 100.0))
    idx_wid = sketch.addConstraint(Sketcher.Constraint("DistanceY", 1, 1, 1, 2, 50.0))

    sketch.setExpression(f"Constraints[{idx_len}]", length_expr)
    sketch.setExpression(f"Constraints[{idx_wid}]", width_expr)

    if hasattr(sketch, "Document") and sketch.Document:
        sketch.Document.recompute()
