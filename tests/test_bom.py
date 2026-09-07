import os
import sys
import FreeCAD
import Part

# Ensure src/ is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from phi_works.maker.materials import init_materials, apply_material
from phi_works.maker.bom import (
    extract_bom,
    filter_bom,
    create_procurement_list,
    create_fabrication_cut_list,
    generate_bom_markdown,
    export_bom,
)

print("--- 1. Testing BOM Extraction on Synthetic Assembly ---")
init_materials()
doc = FreeCAD.newDocument("BOM_Test_Doc")

# Create a fabricated part (14-ga sheet box)
cowl = doc.addObject("Part::Box", "Radiant_Cowl")
cowl.Label = "14-Gauge Protective Steel Cowl"
cowl.Length = 400
cowl.Width = 300
cowl.Height = 100
apply_material(cowl, "Steel-A36")

# Create a fabricated flat bar skid runner
skid = doc.addObject("Part::Box", "Skid_Runner")
skid.Label = "1-1/2\" x 3/16\" Stainless Flat Bar Skid"
skid.Length = 500
skid.Width = 38.1
skid.Height = 4.76
apply_material(skid, "Steel-304Stainless")

# Create a hardware item
valve = doc.addObject("Part::Cylinder", "Regulator_Valve")
valve.Label = "Flow Control Valve & LP Regulator"
valve.Radius = 15
valve.Height = 50
apply_material(valve, "Brass-C360")

doc.recompute()

report = extract_bom(doc, config={"project_name": "Synthetic Test", "version": "1.0.0"})
assert len(report.fabricated_parts) == 2, f"Expected 2 fabricated parts, got {len(report.fabricated_parts)}"
assert len(report.hardware_items) == 1, f"Expected 1 hardware item, got {len(report.hardware_items)}"
assert len(report.commercial_items) == 0, f"Expected 0 commercial items in synthetic doc, got {len(report.commercial_items)}"
print("  [OK] Successfully categorized fabricated parts and hardware.")

# Check stock specs
cowl_part = [p for p in report.fabricated_parts if "cowl" in p.name.lower()][0]
assert "14-Ga" in cowl_part.stock_spec, f"Expected 14-Ga stock spec, got {cowl_part.stock_spec}"
skid_part = [p for p in report.fabricated_parts if "skid" in p.name.lower()][0]
assert "1-1/2\"" in skid_part.stock_spec, f"Expected 1-1/2\" stock spec, got {skid_part.stock_spec}"
print("  [OK] Stock specifications derived correctly.")

print("\n--- 2. Testing Conditional Filtering ---")
# Procurement filter
procurement = create_procurement_list(report)
assert len(procurement.fabricated_parts) == 0, "Procurement list must not contain fabricated parts"
assert len(procurement.hardware_items) == 1, "Procurement list should contain hardware"
print("  [OK] Procurement filter passed.")

# Cut list filter
cutlist = create_fabrication_cut_list(report)
assert len(cutlist.fabricated_parts) == 2, "Cut list must contain fabricated parts"
assert len(cutlist.hardware_items) == 0, "Cut list must not contain hardware"
assert len(cutlist.commercial_items) == 0, "Cut list must not contain commercial items"
print("  [OK] Cut list filter passed.")

# Material filter
steel_only = filter_bom(report, materials=["Steel-304Stainless"])
assert len(steel_only.fabricated_parts) == 1, "Filtered report should contain 1 stainless part"
assert steel_only.fabricated_parts[0].material == "Steel-304Stainless"
print("  [OK] Material-specific filter passed.")

print("\n--- 3. Testing Markdown Output ---")
md_text = generate_bom_markdown(report)
assert "# Synthetic Test" in md_text
assert "Executive Summary & Weight Rollup" in md_text
assert "Machine Shop Cut List" in md_text
assert "Raw Stock Requisition" in md_text
print("  [OK] Markdown generation verified.")

print("\nALL BOM UNIT TESTS PASSED SUCCESSFULLY!")
os._exit(0)
