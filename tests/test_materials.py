import FreeCAD
import Part
import sys

# Ensure src/ is in sys.path
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from phi_works.maker.materials import (
    init_materials,
    list_materials,
    get_material,
    apply_material,
    get_mass_properties,
    format_mass_report,
)

print("--- 1. Testing init_materials & list_materials ---")
init_materials()
all_mats = list_materials()
print(f"Total materials found: {len(all_mats)}")
expected_mats = [
    "Steel-A36",
    "Steel-304Stainless",
    "Steel-ZincPlated",
    "Aluminum-6061-T6",
    "Brass-C360",
    "CastIron-Gray",
    "Rubber-Solid",
    "Plastic-ABS",
    "Polyurethane",
    "PowderCoat-IndustrialRed",
    "PowderCoat-SafetyYellow",
]
for em in expected_mats:
    assert em in all_mats, f"Expected material '{em}' not found in list_materials!"
    mat = all_mats[em]
    dens = mat.getPhysicalValue("Density")
    assert dens is not None, f"Material '{em}' has no Density physical property!"
    diffuse = mat.getAppearanceValue("DiffuseColor")
    assert diffuse is not None, f"Material '{em}' has no DiffuseColor appearance property!"
    print(f"  [OK] {em:<25} Density: {dens.UserString:<16} Diffuse: {diffuse}")

print("\n--- 2. Testing apply_material & mass properties ---")
doc = FreeCAD.newDocument("AutomatedMatTest")

# 100mm cube of Steel-A36 (Volume = 1,000,000 mm^3 = 0.001 m^3 -> Mass = 7.85 kg)
b1 = doc.addObject("Part::Box", "SteelFrameMember")
b1.Length = 100
b1.Width = 100
b1.Height = 100
apply_material(b1, "Steel-A36")

# 100mm cube of Aluminum-6061-T6 (Mass = 2.70 kg), placed at X=200
b2 = doc.addObject("Part::Box", "AluminumDeckPlate")
b2.Length = 100
b2.Width = 100
b2.Height = 100
b2.Placement.Base = FreeCAD.Vector(200, 0, 0)
apply_material(b2, "Aluminum-6061-T6")

# 100mm cube of Rubber-Solid (Mass = 1.15 kg), placed at Y=200
b3 = doc.addObject("Part::Box", "RubberBumper")
b3.Length = 100
b3.Width = 100
b3.Height = 100
b3.Placement.Base = FreeCAD.Vector(0, 200, 0)
apply_material(b3, "Rubber-Solid")

doc.recompute()

res = get_mass_properties(doc)
print(format_mass_report(res, title="Automated Material Test Report"))

# Assertions
expected_total_kg = 7.85 + 2.70 + 1.15 # 11.70 kg
assert abs(res["total_mass_kg"] - expected_total_kg) < 1e-3, f"Expected mass ~{expected_total_kg} kg, got {res['total_mass_kg']}"
print("\n--- 3. Testing FCStd Persistence ---")
persist_path = "/home/phi/.gemini/antigravity/brain/6e7b222c-60a6-438b-ae3a-ed0709600fb0/scratch/test_persist_full.FCStd"
doc.saveAs(persist_path)
FreeCAD.closeDocument("AutomatedMatTest")

doc2 = FreeCAD.openDocument(persist_path)
b1_reopen = doc2.getObject("SteelFrameMember")
assert b1_reopen.ShapeMaterial is not None, "ShapeMaterial lost on reopen!"
assert b1_reopen.ShapeMaterial.Name == "Steel-A36", f"Expected Steel-A36, got {b1_reopen.ShapeMaterial.Name}"
assert b1_reopen.ShapeMaterial.getPhysicalValue("Density") is not None, "Density lost on reopen!"
print("  [OK] Saved and re-opened FCStd retains ShapeMaterial Steel-A36 with density!")
FreeCAD.closeDocument(doc2.Name)

print("\n[SUCCESS] All material tests passed successfully!")
