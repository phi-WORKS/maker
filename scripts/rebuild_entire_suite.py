"""
Master CAD Suite Rebuild Pipeline
Builds the entire repository from atomic components up to top-level assemblies
in topological dependency order, ensuring:
1. Zero 'Material not found' errors
2. Native App::Part and App::Link hierarchies
3. GuiDocument.xml present with Visibility = True for all physical parts
4. Multi-view PNG renders and mass engineering reports
"""

import os
import sys
import time
import subprocess
import zipfile
import xml.etree.ElementTree as ET

MAKER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FREECAD_APPIMAGE = "/home/phi/AppImages/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"

LEVEL_0_ATOMIC = [
    "components/caster_wheel_5in/build.py",
    "components/steel_caster_wheel/build.py",
    "components/torch_burner_head/build.py",
    "components/torch_control_handle/build.py",
    "components/torch_hf91037/build.py",
    "components/propane_cylinder_1lb/build.py",
    "components/propane_cylinder_20lb/build.py",
    "components/propane_harness/build.py",
    "components/solaronics_infrared_burner/build.py",
    "components/water_tank/build.py",
    "components/commercial_hand_truck/build.py",
    "components/stihl/kombi_shaft/build.py",
    "components/stihl/stihl_kma200r/build.py",
    "components/stihl/tools/kombi_trimmer_fs/build.py",
    "components/stihl/tools/kombi_bed_redefiner_fbd/build.py",
    "components/stihl/tools/kombi_blower_bg/build.py",
    "components/stihl/tools/kombi_scythe_fh/build.py",
    "components/stihl/tools/kombi_pruner_ht/build.py",
    "components/stihl/tools/kombi_cultivator_bf/build.py",
    "components/stihl/tools/kombi_brushcutter_fs/build.py",
]

LEVEL_1_COMPOUND = [
    "components/caster_rigid_5in/build.py",
    "components/caster_swivel_5in/build.py",
    "components/platform_cart_24x36/build.py",
]

LEVEL_2_SUBASSEMBLIES = [
    "projects/road-roaster-4w/subassemblies/cantilever_burner/build.py",
    "projects/road-roaster-4w/subassemblies/fuel_system/build.py",
    "projects/road-roaster-4w/subassemblies/aux_torch_safety/build.py",
]

LEVEL_3_MASTER = [
    "projects/road-roaster-4w/build.py",
    "projects/kombi-kaddy/build.py",
    "projects/road-roaster/build.py",
]

ALL_BUILDS = [
    ("Level 0: Atomic Commercial Components", LEVEL_0_ATOMIC),
    ("Level 1: Compound Components & Cart Foundation", LEVEL_1_COMPOUND),
    ("Level 2: Road Roaster 4W Subassemblies", LEVEL_2_SUBASSEMBLIES),
    ("Level 3: Master Integrated Assemblies", LEVEL_3_MASTER),
]

def run_build_script(rel_path):
    abs_path = os.path.join(MAKER_ROOT, rel_path)
    if not os.path.exists(abs_path):
        print(f"  ERROR: File does not exist: {abs_path}")
        return False, 0.0

    t0 = time.time()
    cmd = [
        "xvfb-run",
        "-a",
        FREECAD_APPIMAGE,
        "-c",
        f"__file__='{abs_path}'; exec(open(__file__).read())",
    ]

    env = os.environ.copy()
    src_dir = os.path.join(MAKER_ROOT, "src")
    env["PYTHONPATH"] = f"{src_dir}:{env.get('PYTHONPATH', '')}"

    try:
        proc = subprocess.run(
            cmd,
            cwd=os.path.dirname(abs_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
            env=env,
        )
        elapsed = time.time() - t0

        if proc.returncode != 0:
            print(f"  FAILED (exit code {proc.returncode}) in {elapsed:.1f}s")
            lines = proc.stdout.strip().split("\n")
            print("  --- Traceback / Tail Output ---")
            for l in lines[-15:]:
                print(f"    {l}")
            print("  ------------------------------")
            return False, elapsed

        return True, elapsed
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after 120s")
        return False, 120.0
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False, 0.0

def audit_suite():
    print("\n================================================================================")
    print(" POST-BUILD VERIFICATION AUDIT")
    print("================================================================================")

    all_fcstd = []
    for root, dirs, files in os.walk(MAKER_ROOT):
        if ".git" in root or ".gemini" in root:
            continue
        for f in files:
            if f.endswith(".FCStd"):
                all_fcstd.append(os.path.join(root, f))

    all_fcstd.sort()
    print(f"Total .FCStd files inspected: {len(all_fcstd)}\n")

    issues = 0
    for fpath in all_fcstd:
        rel = os.path.relpath(fpath, MAKER_ROOT)
        try:
            with zipfile.ZipFile(fpath, "r") as z:
                namelist = set(z.namelist())
                has_gui = "GuiDocument.xml" in namelist
                doc_xml = z.read("Document.xml").decode("utf-8")

            root = ET.fromstring(doc_xml)
            mat_objs = [o.get("name") for o in root.iter("Object") if o.get("type") == "App::MaterialObject"]
            shape_mats = []
            for o in root.iter("Object"):
                for p in o.iter("Property"):
                    if p.get("name") == "ShapeMaterial":
                        shape_mats.append(o.get("name"))

            status_notes = []
            if not has_gui:
                status_notes.append("MISSING GuiDocument.xml")
                issues += 1
            if len(shape_mats) > 0 and len(mat_objs) == 0:
                status_notes.append(f"MISSING MaterialObjects (has {len(shape_mats)} ShapeMaterials)")
                issues += 1

            if status_notes:
                print(f"  [!] {rel}: {', '.join(status_notes)}")
            else:
                print(f"  [OK] {rel} (Materials: {len(mat_objs)}, Shapes: {len(shape_mats)}, GUI: Yes)")
        except Exception as e:
            print(f"  [ERROR] {rel}: {e}")
            issues += 1

    if issues == 0:
        print("\nAUDIT RESULT: 100% PASS - All models have GuiDocument.xml and embedded materials!")
    else:
        print(f"\nAUDIT RESULT: {issues} issues identified.")
    return issues == 0

def test_load_models():
    print("\n================================================================================")
    print(" TESTING DIRECT LOAD OF ROAD ROASTER 4W AND KOMBI KADDY IN FREECAD")
    print("================================================================================")

    test_script = os.path.join(MAKER_ROOT, "scripts", "_test_load.py")
    code = f"""
import FreeCAD
import FreeCADGui
FreeCADGui.showMainWindow()

sys_path = '{MAKER_ROOT}/src'
import sys
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from phi_works.maker.materials import init_materials
init_materials()

models = [
    '{MAKER_ROOT}/projects/road-roaster-4w/road-roaster-4w.FCStd',
    '{MAKER_ROOT}/projects/kombi-kaddy/caddy.FCStd',
    '{MAKER_ROOT}/projects/road-roaster/road-roaster.FCStd',
]

for m in models:
    print(f'\\n>>> Opening model: {{m}}')
    doc = FreeCAD.openDocument(m)
    gui_doc = FreeCADGui.getDocument(doc.Name)
    
    hidden_physical = []
    visible_joints = []
    visible_origins = []
    
    for obj in doc.Objects:
        vobj = gui_doc.getObject(obj.Name) if gui_doc else None
        vis = vobj.Visibility if vobj else False
        t = obj.TypeId
        n = obj.Name.lower()
        is_joint = "joint" in n or "ground" in n or "skeleton" in n or "joint" in t.lower()
        is_origin = (
            t in ("App::Origin", "App::Line", "App::Plane", "App::Point")
            or t.startswith("App::Origin")
            or "origin" in t.lower()
            or n.startswith("origin")
            or "_axis" in n
            or "_plane" in n
            or n in ("x_axis", "y_axis", "z_axis", "xy_plane", "xz_plane", "yz_plane")
        )
        
        if is_origin and vis:
            visible_origins.append(obj.Name)
        elif is_joint and vis:
            visible_joints.append(obj.Name)
        elif not is_joint and not is_origin and not vis:
            if hasattr(obj, "Shape") or t in ("App::Part", "App::Link", "Assembly::AssemblyObject"):
                hidden_physical.append((obj.Name, t))
                
    print(f'    Document Name: {{doc.Name}} (Objects: {{len(doc.Objects)}})')
    if hidden_physical:
        print(f'    [FAIL] Hidden physical objects ({{len(hidden_physical)}}): {{hidden_physical[:5]}}')
    else:
        print(f'    [PASS] All physical components and links are VISIBLE in GUI!')
        
    if visible_origins:
        print(f'    [FAIL] Visible origin objects ({{len(visible_origins)}}): {{visible_origins[:5]}}')
    else:
        print(f'    [PASS] All origin coordinate systems, axes, planes, and points are HIDDEN!')

    if visible_joints:
        print(f'    [NOTE] Visible joints: {{visible_joints}}')
    else:
        print(f'    [PASS] All kinematic joint glyphs are hidden!')
        
    FreeCAD.closeDocument(doc.Name)

print('\\nVerification test completed successfully.')
import os
os._exit(0)
"""
    with open(test_script, "w") as f:
        f.write(code)

    cmd = [
        "xvfb-run",
        "-a",
        FREECAD_APPIMAGE,
        "-c",
        f"__file__='{test_script}'; exec(open(__file__).read())",
    ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(proc.stdout)

    if os.path.exists(test_script):
        os.remove(test_script)

def main():
    print("================================================================================")
    print(" STARTING COMPLETE CAD SUITE TOPOLOGICAL REBUILD")
    print(f" Root: {MAKER_ROOT}")
    print(f" FreeCAD: {FREECAD_APPIMAGE}")
    print("================================================================================")

    total_start = time.time()
    total_scripts = sum(len(scripts) for _, scripts in ALL_BUILDS)
    completed = 0
    failed = []

    for level_title, scripts in ALL_BUILDS:
        print(f"\n--- {level_title} ({len(scripts)} models) ---")
        for rel_path in scripts:
            completed += 1
            print(f"[{completed:02d}/{total_scripts:02d}] Building {rel_path} ...", end="", flush=True)
            success, elapsed = run_build_script(rel_path)
            time.sleep(0.5)
            if success:
                print(f" OK ({elapsed:.1f}s)")
            else:
                failed.append(rel_path)

    total_time = time.time() - total_start
    print("\n================================================================================")
    print(f" BUILD COMPLETE: {completed - len(failed)}/{total_scripts} succeeded in {total_time:.1f}s")
    if failed:
        print(f" FAILED SCRIPTS ({len(failed)}):")
        for f in failed:
            print(f"   - {f}")
    print("================================================================================")

    audit_suite()
    test_load_models()

if __name__ == "__main__":
    main()
