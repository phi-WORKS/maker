import os
import time

try:
    import FreeCAD
    import FreeCADGui
    HAS_GUI = bool(getattr(FreeCAD, "GuiUp", False))
except Exception:
    FreeCADGui = None
    HAS_GUI = False

def is_gui_up():
    """Dynamically checks whether FreeCAD's GUI is running."""
    try:
        import FreeCAD
        import FreeCADGui
        return bool(getattr(FreeCAD, "GuiUp", False)) and FreeCADGui is not None
    except Exception:
        return False


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
    if not is_gui_up():
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


def _hide_kinematic_markers(gui_doc):
    """
    Hides FreeCAD 1.1 Assembly joint markers (padlocks, axes, coordinate systems)
    and coordinate origin features so presentation renders capture pure geometry.
    """
    if not gui_doc:
        return
    app_doc = getattr(gui_doc, "Document", None)
    if not app_doc:
        return
    for obj in app_doc.Objects:
        type_id = getattr(obj, "TypeId", "")
        type_lower = type_id.lower()
        name = getattr(obj, "Name", "")
        name_lower = name.lower()
        is_hidden = (
            "joint" in type_lower
            or "joint" in name_lower
            or "ground" in name_lower
            or "skeleton" in name_lower
            or type_lower == "assembly::jointgroup"
            or type_id in ("App::Origin", "App::Line", "App::Plane", "App::Point")
            or type_lower.startswith("app::origin")
            or "origin" in type_lower
            or name_lower.startswith("origin")
            or "_axis" in name_lower
            or "_plane" in name_lower
            or name_lower in ("x_axis", "y_axis", "z_axis", "xy_plane", "xz_plane", "yz_plane")
        )
        if is_hidden:
            try:
                obj.Visibility = False
                g_o = gui_doc.getObject(obj.Name)
                if g_o:
                    g_o.Visibility = False
            except Exception:
                pass


def export_orthogonal_views(gui_doc, base_prefix, master_dir=None, model_prefix="model",
                            width=1920, height=1080, bg_type="White", camera_type="Perspective"):
    """
    Rotates the active model through 7 standard projections (front, back, top, bottom, left, right, iso),
    fits the view, disables view transition animations, and exports high-resolution PNGs in Perspective mode.
    Leaves the active viewport oriented in Isometric Perspective with fitAll() applied so that subsequent
    document saves preserve this framed home view.
    """
    if not is_gui_up() or not gui_doc:
        return
    import FreeCADGui
    try:
        FreeCADGui.updateGui()
    except Exception:
        pass

    view = gui_doc.activeView()
    if not view:
        return

    configure_freecad_preferences()
    _hide_kinematic_markers(gui_doc)

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
    if not is_gui_up() or not gui_doc:
        return
    import FreeCADGui

    try:
        FreeCADGui.updateGui()
    except Exception:
        pass

    view = gui_doc.activeView()
    if not view:
        return

    configure_freecad_preferences()
    _hide_kinematic_markers(gui_doc)

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


def ensure_fcstd_gui_visibility(fc_path, doc=None):
    """
    Ensures that the .FCStd archive contains a valid GuiDocument.xml specifying
    Visibility = True for all physical objects, assemblies, parts, and links,
    and Visibility = False for kinematic joints and skeleton sketches.

    This guarantees that when the .FCStd file is opened in FreeCAD desktop GUI,
    all components and subassemblies appear visible immediately, even if the model
    was built or saved headlessly.
    """
    if not os.path.exists(fc_path):
        return

    import zipfile
    import xml.etree.ElementTree as ET

    try:
        with zipfile.ZipFile(fc_path, "r") as zin:
            file_names = set(zin.namelist())
            if "Document.xml" not in file_names:
                return
            doc_xml = zin.read("Document.xml").decode("utf-8")
            has_gui = "GuiDocument.xml" in file_names
            gui_xml = zin.read("GuiDocument.xml").decode("utf-8") if has_gui else None
            files = {item.filename: zin.read(item.filename) for item in zin.infolist()}

        root = ET.fromstring(doc_xml)
        all_objects = []
        hidden_names = set()

        for obj in root.iter("Object"):
            name = obj.get("name")
            type_id = obj.get("type", "")
            if not name:
                continue
            all_objects.append((name, type_id))

            name_lower = name.lower()
            type_lower = type_id.lower()
            if (
                "joint" in name_lower
                or "ground" in name_lower
                or "skeleton" in name_lower
                or "joint" in type_lower
                or type_id == "Assembly::JointGroup"
                or type_id in ("App::Origin", "App::Line", "App::Plane", "App::Point")
                or type_id.startswith("App::Origin")
                or "origin" in type_lower
                or name_lower.startswith("origin")
                or "_axis" in name_lower
                or "_plane" in name_lower
                or name_lower in ("x_axis", "y_axis", "z_axis", "xy_plane", "xz_plane", "yz_plane")
            ):
                hidden_names.add(name)

        if not has_gui:
            gui_root = ET.Element("Document", {"SchemaVersion": "1", "HasExpansion": "1"})
            ET.SubElement(gui_root, "Expand")
            vp_data = ET.SubElement(gui_root, "ViewProviderData", {"Count": str(len(all_objects))})

            for name, type_id in all_objects:
                vis_val = "false" if name in hidden_names else "true"
                vp = ET.SubElement(vp_data, "ViewProvider", {"name": name})
                props = ET.SubElement(vp, "Properties", {"Count": "1"})
                prop = ET.SubElement(props, "Property", {"name": "Visibility", "type": "App::PropertyBool", "status": "1"})
                ET.SubElement(prop, "Bool", {"value": vis_val})

            files["GuiDocument.xml"] = ET.tostring(gui_root, encoding="utf-8", xml_declaration=True)

            with zipfile.ZipFile(fc_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for fname, data in files.items():
                    zout.writestr(fname, data)
        else:
            gui_tree = ET.fromstring(gui_xml)
            vp_data = gui_tree.find("ViewProviderData")
            modified = False
            existing_vp_names = set()

            if vp_data is not None:
                for vp in vp_data.iter("ViewProvider"):
                    vp_name = vp.get("name")
                    if not vp_name:
                        continue
                    existing_vp_names.add(vp_name)
                    should_hide = vp_name in hidden_names

                    props = vp.find("Properties")
                    if props is None:
                        props = ET.SubElement(vp, "Properties", {"Count": "1"})

                    vis_prop = None
                    for p in props.iter("Property"):
                        if p.get("name") == "Visibility":
                            vis_prop = p
                            break

                    target_val = "false" if should_hide else "true"
                    if vis_prop is not None:
                        bool_tag = vis_prop.find("Bool")
                        if bool_tag is not None:
                            if bool_tag.get("value") != target_val:
                                bool_tag.set("value", target_val)
                                modified = True
                        else:
                            ET.SubElement(vis_prop, "Bool", {"value": target_val})
                            modified = True
                    else:
                        prop = ET.SubElement(props, "Property", {"name": "Visibility", "type": "App::PropertyBool", "status": "1"})
                        ET.SubElement(prop, "Bool", {"value": target_val})
                        modified = True

                for name, type_id in all_objects:
                    if name not in existing_vp_names:
                        vis_val = "false" if name in hidden_names else "true"
                        vp = ET.SubElement(vp_data, "ViewProvider", {"name": name})
                        props = ET.SubElement(vp, "Properties", {"Count": "1"})
                        prop = ET.SubElement(props, "Property", {"name": "Visibility", "type": "App::PropertyBool", "status": "1"})
                        ET.SubElement(prop, "Bool", {"value": vis_val})
                        modified = True

            if modified:
                files["GuiDocument.xml"] = ET.tostring(gui_tree, encoding="utf-8", xml_declaration=True)
                with zipfile.ZipFile(fc_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                    for fname, data in files.items():
                        zout.writestr(fname, data)
    except Exception as e:
        print(f"Note verifying GUI visibility for {fc_path}: {e}")


def save_model(doc, fc_path, camera_type="Perspective"):
    """
    Saves the FreeCAD document such that the active GUI viewport is set to
    Perspective Isometric view, fully framed with fitAll(), so opening the .FCStd file
    in FreeCAD GUI launches immediately in the home perspective view.
    Disables backup file creation, cleans up any stray .FCBak files, and guarantees
    GuiDocument.xml visibility properties are stored.
    """
    configure_freecad_preferences()

    try:
        from phi_works.maker.assembly import ensure_assembly_visible, hide_origins
        ensure_assembly_visible(doc)
        hide_origins(doc)
    except Exception:
        pass

    has_gui = bool(getattr(FreeCAD, "GuiUp", False)) and FreeCADGui is not None
    if has_gui and hasattr(FreeCADGui, "getDocument"):
        try:
            gui_d = FreeCADGui.getDocument(doc.Name)
            if gui_d:
                # Synchronize GUI ViewProvider visibility before saving
                for obj in doc.Objects:
                    vobj = gui_d.getObject(obj.Name)
                    if vobj:
                        type_id = getattr(obj, "TypeId", "")
                        type_lower = type_id.lower()
                        name_lower = getattr(obj, "Name", "").lower()
                        is_hidden = (
                            "joint" in type_lower
                            or "joint" in name_lower
                            or "ground" in name_lower
                            or "skeleton" in name_lower
                            or type_lower == "assembly::jointgroup"
                            or type_id in ("App::Origin", "App::Line", "App::Plane", "App::Point")
                            or type_id.startswith("App::Origin")
                            or "origin" in type_lower
                            or name_lower.startswith("origin")
                            or "_axis" in name_lower
                            or "_plane" in name_lower
                            or name_lower in ("x_axis", "y_axis", "z_axis", "xy_plane", "xz_plane", "yz_plane")
                        )
                        if is_hidden:
                            vobj.Visibility = False
                            if hasattr(obj, "Visibility"):
                                obj.Visibility = False
                        else:
                            vobj.Visibility = True
                            if hasattr(obj, "Visibility"):
                                obj.Visibility = True

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

    # Ensure GuiDocument.xml is present and sets physical subcomponents to visible
    ensure_fcstd_gui_visibility(fc_path, doc)


def close_model(doc_or_name):
    """
    Cleanly closes the FreeCAD document and flushes GUI events to ensure
    file locks and resources are completely released before process termination.
    """
    name = doc_or_name if isinstance(doc_or_name, str) else getattr(doc_or_name, "Name", str(doc_or_name))
    try:
        FreeCAD.closeDocument(name)
        if is_gui_up():
            import FreeCADGui
            FreeCADGui.updateGui()
            time.sleep(0.1)
    except Exception as e:
        print(f"Note closing document {name}: {e}")

