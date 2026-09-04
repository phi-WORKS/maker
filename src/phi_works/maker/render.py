import os
import time

try:
    import FreeCAD
    import FreeCADGui
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False


import os
import time

try:
    import FreeCAD
    import FreeCADGui
    HAS_GUI = True
except Exception:
    FreeCADGui = None
    HAS_GUI = False


def cleanup_backup_files(path_or_dir):
    """
    Removes any stray .FCBak files in the specified file path or directory.
    """
    if os.path.isfile(path_or_dir):
        directory = os.path.dirname(path_or_dir)
        basename = os.path.splitext(os.path.basename(path_or_dir))[0]
    else:
        directory = path_or_dir
        basename = None

    if not directory or not os.path.exists(directory):
        return

    try:
        for fname in os.listdir(directory):
            if fname.endswith(".FCBak"):
                if basename is None or fname.startswith(basename):
                    fpath = os.path.join(directory, fname)
                    try:
                        os.remove(fpath)
                    except Exception:
                        pass
    except Exception:
        pass


def configure_freecad_preferences():
    """
    Applies performance and lifecycle preferences to FreeCAD:
    - Disables view transition animations to prevent frame lag during snapshot capture.
    - Disables backup file generation (CreateBackupFiles = False) to prevent .FCBak clutter.
    """
    if not HAS_GUI or not FreeCAD:
        return

    # 1. Disable view transition animations
    try:
        param_view = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
        param_view.SetBool("EnableAnimation", False)
        param_view.SetInt("TransitionTime", 0)
    except Exception as e:
        print(f"Preference note (View): {e}")

    # 2. Disable automatic .FCBak backup file creation
    try:
        param_doc = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Document")
        param_doc.SetBool("CreateBackupFiles", False)
        param_doc.SetInt("CountBackupFiles", 0)
    except Exception as e:
        print(f"Preference note (Document): {e}")


def export_orthogonal_views(gui_doc, base_prefix, master_dir=None, model_prefix="model",
                            width=1920, height=1080, bg_type="White", camera_type="Perspective"):
    """
    Rotates the active model through 7 standard projections (front, back, top, bottom, left, right, iso),
    fits the view, disables view transition animations, and exports high-resolution PNGs in Perspective mode.
    Leaves the active viewport oriented in Isometric Perspective with fitAll() applied so that subsequent
    document saves preserve this framed home view.
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

    configure_freecad_preferences()

    # 1. Apply requested camera projection mode (Perspective or Orthographic)
    try:
        view.setCameraType(camera_type)
    except Exception as e:
        print(f"Camera type note: {e}")

    # 2. Define standard view methods (home view is last to leave viewport framed for doc save)
    back_fn = getattr(view, "viewRear", getattr(view, "viewBack", lambda: None))
    views_to_export = [
        ("front", view.viewFront, "Front Elevation View"),
        ("back", back_fn, "Rear Elevation View"),
        ("top", view.viewTop, "Top Plan View"),
        ("bottom", view.viewBottom, "Bottom Plan View"),
        ("left", view.viewLeft, "Left Side Elevation View"),
        ("right", view.viewRight, "Right Side Elevation View"),
        ("home", view.viewIsometric, "Home Perspective View"),
    ]

    # Ensure target output directory exists
    out_dir = os.path.dirname(base_prefix)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # 3. Loop through views, re-fit bounding box, force GUI redraw, and export
    for name, set_view_func, label in views_to_export:
        if not set_view_func:
            continue
        try:
            # Orient camera view angle
            set_view_func()

            # Scene graph update and pause for camera orientation completion
            FreeCADGui.updateGui()
            time.sleep(0.3)
            FreeCADGui.updateGui()

            # Fit bounding box to viewport on settled view angle
            view.fitAll()

            # Scene graph update and pause for fitAll zoom completion
            FreeCADGui.updateGui()
            time.sleep(0.3)
            FreeCADGui.updateGui()

            # Save PNG image: home view is saved without underscore modifier (<model>.png)
            if name == "home":
                filepath = f"{base_prefix}.png"
                master_png = os.path.join(master_dir, f"{model_prefix}.png") if master_dir else None
            else:
                filepath = f"{base_prefix}_{name}.png"
                master_png = os.path.join(master_dir, f"{model_prefix}_{name}.png") if master_dir else None

            view.saveImage(filepath, width, height, bg_type)
            print(f"Exported {label}: {filepath}")

            # Save master copy if master_dir is provided
            if master_png:
                os.makedirs(master_dir, exist_ok=True)
                view.saveImage(master_png, width, height, bg_type)
        except Exception as e:
            print(f"Error rendering {name} view: {e}")

    # Ensure viewport remains settled in Isometric Perspective view
    try:
        view.setCameraType(camera_type)
        view.viewIsometric()
        FreeCADGui.updateGui()
        time.sleep(0.2)
        view.fitAll()
        FreeCADGui.updateGui()
    except Exception:
        pass


def render_single_view(gui_doc, png_path, view_type="Isometric", width=1920, height=1080,
                       bg_type="White", hide_objs=[], camera_type="Perspective"):
    """
    Renders a single camera view projection to PNG in Perspective mode.
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

    configure_freecad_preferences()

    try:
        view.setCameraType(camera_type)
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


def save_model(doc, fc_path, camera_type="Perspective"):
    """
    Saves the FreeCAD document such that the active GUI viewport is set to
    Perspective Isometric view, fully framed with fitAll(), so opening the .FCStd file
    in FreeCAD GUI launches immediately in the home perspective view.
    Disables backup file creation and cleans up any stray .FCBak files.
    """
    configure_freecad_preferences()

    if HAS_GUI and FreeCADGui and FreeCADGui.getDocument(doc.Name):
        gui_d = FreeCADGui.getDocument(doc.Name)
        view = gui_d.activeView()
        if view:
            try:
                view.setCameraType(camera_type)
            except Exception:
                pass
            try:
                view.viewIsometric()
                FreeCADGui.updateGui()
                time.sleep(0.2)
                view.fitAll()
                FreeCADGui.updateGui()
                time.sleep(0.2)
            except Exception:
                pass

    doc.recompute()
    out_dir = os.path.dirname(fc_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    doc.saveAs(fc_path)
    print(f"Saved model with perspective home view: {fc_path}")

    # Remove any stray .FCBak files created by FreeCAD
    cleanup_backup_files(fc_path)


def close_model(doc_or_name):
    """
    Cleanly closes the FreeCAD document and flushes GUI events to ensure
    file locks and resources are completely released before process termination.
    """
    name = doc_or_name if isinstance(doc_or_name, str) else getattr(doc_or_name, "Name", str(doc_or_name))
    try:
        FreeCAD.closeDocument(name)
        if HAS_GUI and FreeCADGui:
            FreeCADGui.updateGui()
            time.sleep(0.1)
    except Exception as e:
        print(f"Note closing document {name}: {e}")

