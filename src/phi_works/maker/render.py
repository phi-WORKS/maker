import os
import time

try:
    import FreeCAD
    import FreeCADGui
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False


def export_orthogonal_views(gui_doc, base_prefix, master_dir=None, model_prefix="model", width=1920, height=1080, bg_type="White"):
    """
    Rotates the active model through 7 standard orthographic/isometric projections,
    fits the view, disables view transition animations, and exports high-resolution PNGs.
    """
    if not HAS_GUI or not gui_doc:
        return
    try:
        FreeCADGui.updateGui()
    except Exception:
        pass

    view = gui_doc.activeView()
    if not view:
        return

    # Disable view transition animations in FreeCAD preferences
    try:
        param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
        param.SetBool("EnableAnimation", False)
        param.SetInt("TransitionTime", 0)
    except Exception as e:
        print(f"Preference note: {e}")

    # 1. Force camera into Orthographic mode
    try:
        view.setCameraType("Orthographic")
    except Exception as e:
        print(f"Camera type note: {e}")

    # 2. Define standard orthogonal view methods
    back_fn = getattr(view, "viewRear", getattr(view, "viewBack", lambda: None))
    orthogonal_views = [
        ("front", view.viewFront, "Front Elevation View"),
        ("back", back_fn, "Rear Elevation View"),
        ("top", view.viewTop, "Top Plan View"),
        ("bottom", view.viewBottom, "Bottom Plan View"),
        ("left", view.viewLeft, "Left Side Elevation View"),
        ("right", view.viewRight, "Right Side Elevation View"),
        ("iso", view.viewIsometric, "Isometric (Home) View"),
    ]

    # Ensure target output directory exists
    out_dir = os.path.dirname(base_prefix)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # 3. Loop through views, re-fit bounding box, force GUI redraw, and export
    for name, set_view_func, label in orthogonal_views:
        if not set_view_func:
            continue
        try:
            # 1. Orient camera view angle
            set_view_func()

            # 2. Scene graph update and pause for camera rotation animation completion
            FreeCADGui.updateGui()
            time.sleep(0.3)
            FreeCADGui.updateGui()

            # 3. Fit bounding box to viewport on settled view angle
            view.fitAll()

            # 4. Scene graph update and pause for fitAll zoom animation completion
            FreeCADGui.updateGui()
            time.sleep(0.3)
            FreeCADGui.updateGui()

            # Save version-specific PNG image
            filepath = f"{base_prefix}_{name}.png"
            view.saveImage(filepath, width, height, bg_type)
            print(f"Exported {label}: {filepath}")

            # Save master copy if master_dir is provided
            if master_dir:
                os.makedirs(master_dir, exist_ok=True)
                master_png = os.path.join(master_dir, f"{model_prefix}_{name}.png")
                view.saveImage(master_png, width, height, bg_type)
        except Exception as e:
            print(f"Error rendering {name} view: {e}")


def render_single_view(gui_doc, png_path, view_type="Isometric", width=1920, height=1080, bg_type="White", hide_objs=[]):
    """
    Renders a single camera view projection to PNG.
    Inserts necessary GUI updates and pauses after camera rotation and after fitAll zoom
    to ensure full model framing without clipping or animation lag.
    """
    if not HAS_GUI or not gui_doc:
        return

    try:
        FreeCADGui.updateGui()
    except Exception:
        pass

    view = gui_doc.activeView()
    if not view:
        return

    # Disable view transition animations in FreeCAD preferences
    try:
        param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
        param.SetBool("EnableAnimation", False)
        param.SetInt("TransitionTime", 0)
    except Exception as e:
        print(f"Preference note: {e}")

    try:
        view.setCameraType("Orthographic")
    except Exception as e:
        print(f"Camera type note: {e}")

    # Orient camera
    if view_type == "Isometric":
        view.viewIsometric()
    elif view_type == "Top":
        view.viewTop()
    elif view_type == "Bottom":
        view.viewBottom()
    elif view_type == "Front":
        view.viewFront()
    elif view_type in ("Rear", "Back"):
        back_fn = getattr(view, "viewRear", getattr(view, "viewBack", lambda: None))
        if back_fn:
            back_fn()
    elif view_type == "Left":
        view.viewLeft()
    elif view_type in ("Right", "Side"):
        view.viewRight()

    # Pause 1: Allow camera rotation animation to settle before fitAll calculation
    FreeCADGui.updateGui()
    time.sleep(0.3)
    FreeCADGui.updateGui()

    hidden_objs_restored = []
    try:
        # Temporarily hide distant objects during fitAll framing
        for ho in hide_objs:
            g_ho = None
            if hasattr(ho, "Name"):
                g_ho = gui_doc.getObject(ho.Name)
            elif isinstance(ho, str):
                g_ho = gui_doc.getObject(ho)
            if g_ho and getattr(g_ho, "Visibility", False):
                g_ho.Visibility = False
                hidden_objs_restored.append(g_ho)

        # Fit bounding box to viewport
        view.fitAll()

        # Pause 2: Allow fitAll zoom animation to settle before snapshot capture
        FreeCADGui.updateGui()
        time.sleep(0.3)
        FreeCADGui.updateGui()

    finally:
        # Restore visibility after framing
        for g_ho in hidden_objs_restored:
            g_ho.Visibility = True

    # Ensure output directory exists
    out_dir = os.path.dirname(png_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    view.saveImage(png_path, width, height, bg_type)
    print(f"Rendered snapshot: {png_path}")

