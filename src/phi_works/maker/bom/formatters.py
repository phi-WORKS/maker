"""
BOM and Cut List Formatters

Exports BOMReport into:
- GitHub-Flavored Markdown (BOM.md)
- Procurement and Cut List CSV files
- Structured JSON for automation
"""

import os
import csv
import json
from dataclasses import asdict
from phi_works.maker.bom.models import BOMReport


def generate_bom_markdown(report: BOMReport, title_prefix: str = "") -> str:
    """
    Renders a clean, comprehensive GitHub Flavored Markdown document from a BOMReport.
    """
    lines = []
    title = f"{title_prefix}{report.project_name} — Master Bill of Materials & Fabrication Cut List"
    lines.append(f"# {title.strip()}\n")
    lines.append(f"> **Automated Physical Design & Procurement Specification (v{report.version})**  ")
    lines.append(f"> *Generated on {report.date_str} via `phi_works.maker.bom`*\n")
    lines.append("---\n")

    # Executive Summary Table
    lines.append("## Executive Summary & Weight Rollup\n")
    lines.append("| Classification | Line Items | Total Weight (lb) | Weight Share | Role / Scope |")
    lines.append("| :--- | :---: | :---: | :---: | :--- |")

    tot_mass = report.total_assembly_mass_lb or 1.0
    c_mass = report.total_commercial_mass_lb
    f_mass = report.total_fabricated_mass_lb
    h_mass = report.total_hardware_mass_lb

    lines.append(f"| **Commercial / Acquired (COTS)** | {len(report.commercial_items)} | {c_mass:.2f} lb | {c_mass/tot_mass*100:.1f}% | Complete donor chassis, burner engines, pressure vessels |")
    lines.append(f"| **Custom Fabricated Parts** | {len(report.fabricated_parts)} | {f_mass:.2f} lb | {f_mass/tot_mass*100:.1f}% | Formed sheet metal, welded flat bar skids & linkages |")
    lines.append(f"| **Hardware, Fluid & Electrical** | {len(report.hardware_items)} | {h_mass:.2f} lb | {h_mass/tot_mass*100:.1f}% | Valves, LP hoses, wiring, retention hardware |")
    lines.append(f"| **Total Assembly Machine** | **{len(report.commercial_items) + len(report.fabricated_parts) + len(report.hardware_items)}** | **{tot_mass:.2f} lb** | **100.0%** | **Operating machine weight (empty fuel)** |\n")

    lines.append("---\n")

    # Section 1: Commercial & Acquired Components
    if report.commercial_items:
        lines.append("## 1. Commercial & Acquired Components (COTS Procurement List)\n")
        lines.append("Commercial off-the-shelf assemblies acquired as complete units. **Do not fabricate in-house**.\n")
        lines.append("| Item Description | Component ID | Category | Qty | Vendor / Source | Part / Model # | Unit Wt | Subassembly / Reference |")
        lines.append("| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |")
        for item in report.commercial_items:
            ref_link = f"[`{item.component_id}`]({item.reference_url})" if item.reference_url else f"`{item.component_id}`"
            lines.append(
                f"| **{item.name}** | {ref_link} | {item.category} | {item.qty} | {item.vendor} | `{item.part_number}` | {item.mass_lb:.1f} lb | {item.subassembly} |"
            )
        lines.append(f"\n*Subtotal Commercial Hardware Weight: **{c_mass:.2f} lb***\n")
        lines.append("---\n")

    # Section 2: Custom Fabricated Parts & Cut List
    if report.fabricated_parts:
        lines.append("## 2. Custom Fabricated Parts & Machine Shop Cut List\n")
        lines.append("Custom metal components fabricated in the shop from raw stock materials.\n")
        lines.append("| Mark | Part Name | Subassembly | Material | Raw Stock Profile | Cut Dimensions (L × W × T) | Qty | Unit Wt | Primary Operations |")
        lines.append("| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |")
        for p in report.fabricated_parts:
            # Format imperial and metric dimensions
            dim_str = f"{p.length_in:.2f}\" × {p.width_in:.2f}\" × {p.thickness_in:.3f}\"<br>({p.length_mm:.1f} × {p.width_mm:.1f} × {p.thickness_mm:.2f} mm)"
            lines.append(
                f"| **{p.part_mark}** | **{p.name}** | {p.subassembly} | `{p.material}` | {p.stock_spec} | {dim_str} | {p.qty} | {p.mass_lb:.2f} lb | {p.operations} |"
            )
        lines.append(f"\n*Subtotal Custom Fabricated Parts Weight: **{f_mass:.2f} lb***\n")
        lines.append("---\n")

    # Section 3: Raw Stock Requisition Summary
    if report.stock_summary:
        lines.append("## 3. Raw Stock Requisition & Material Nesting Summary\n")
        lines.append("Consolidated raw stock material requirements for inventory purchasing and shop prep.\n")
        lines.append("| Raw Material Grade | Stock Specification | Profile Type | Total Required | Piece Count | Total Wt | Member Part Marks |")
        lines.append("| :---: | :--- | :---: | :---: | :---: | :---: | :--- |")
        for s in report.stock_summary:
            if s.stock_type in ("Sheet Metal", "Steel Plate"):
                req_str = f"**{s.total_area_sq_ft:.2f} sq ft** ({s.total_area_sq_in:.1f} sq in)"
            else:
                req_str = f"**{s.total_linear_ft:.2f} ft** ({s.total_linear_in:.1f} in)"
            marks_str = ", ".join(f"`{m}`" for m in s.pieces)
            lines.append(
                f"| `{s.material}` | **{s.stock_spec}** | {s.stock_type} | {req_str} | {s.piece_count} | {s.total_mass_lb:.2f} lb | {marks_str} |"
            )
        lines.append("\n---\n")

    # Section 4: Hardware, Fluid & Electrical Train
    if report.hardware_items:
        lines.append("## 4. Hardware, Fluid Lines & Electrical Controls\n")
        lines.append("Fittings, regulation valves, reinforced fuel hoses, retention brackets, and ignition wiring.\n")
        lines.append("| Item Description | Category | Material | Specification / Model | Qty | Total Wt | Subassembly / Location |")
        lines.append("| :--- | :--- | :---: | :--- | :---: | :---: | :--- |")
        for h in report.hardware_items:
            lines.append(
                f"| **{h.name}** | {h.category} | `{h.material}` | {h.specification} | {h.qty} | {h.mass_lb:.2f} lb | {h.subassembly} |"
            )
        lines.append(f"\n*Subtotal Hardware & Controls Weight: **{h_mass:.2f} lb***\n")
        lines.append("---\n")

    return "\n".join(lines)


def export_bom_markdown(report: BOMReport, file_path: str, title_prefix: str = ""):
    """
    Writes BOMReport to a Markdown file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    content = generate_bom_markdown(report, title_prefix=title_prefix)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def export_bom_csv(report: BOMReport, output_dir: str):
    """
    Exports clean, spreadsheet-ready CSV files:
    1. `bom_commercial.csv`: Procurement list for commercial components
    2. `cut_list.csv`: Shop fabrication cut list
    3. `hardware.csv`: Fasteners and fluid train items
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Commercial CSV
    c_path = os.path.join(output_dir, "bom_commercial.csv")
    with open(c_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item Name", "Component ID", "Category", "Qty", "Vendor", "Part Number", "Unit Weight (lb)", "Subassembly", "Description"])
        for item in report.commercial_items:
            writer.writerow([item.name, item.component_id, item.category, item.qty, item.vendor, item.part_number, f"{item.mass_lb:.2f}", item.subassembly, item.description])

    # 2. Cut List CSV
    cut_path = os.path.join(output_dir, "cut_list.csv")
    with open(cut_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mark", "Part Name", "Subassembly", "Material", "Stock Spec", "Length (in)", "Width (in)", "Thickness (in)", "Length (mm)", "Width (mm)", "Thickness (mm)", "Qty", "Unit Weight (lb)", "Operations"])
        for p in report.fabricated_parts:
            writer.writerow([
                p.part_mark, p.name, p.subassembly, p.material, p.stock_spec,
                f"{p.length_in:.3f}", f"{p.width_in:.3f}", f"{p.thickness_in:.3f}",
                f"{p.length_mm:.1f}", f"{p.width_mm:.1f}", f"{p.thickness_mm:.2f}",
                p.qty, f"{p.mass_lb:.2f}", p.operations
            ])

    # 3. Hardware CSV
    hw_path = os.path.join(output_dir, "hardware.csv")
    with open(hw_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item Name", "Category", "Material", "Specification", "Qty", "Weight (lb)", "Subassembly"])
        for h in report.hardware_items:
            writer.writerow([h.name, h.category, h.material, h.specification, h.qty, f"{h.mass_lb:.2f}", h.subassembly])


def export_bom_json(report: BOMReport, file_path: str):
    """
    Exports BOMReport to structured JSON.
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    data = {
        "project_name": report.project_name,
        "version": report.version,
        "date": report.date_str,
        "total_mass_lb": round(report.total_assembly_mass_lb, 2),
        "commercial_mass_lb": round(report.total_commercial_mass_lb, 2),
        "fabricated_mass_lb": round(report.total_fabricated_mass_lb, 2),
        "hardware_mass_lb": round(report.total_hardware_mass_lb, 2),
        "commercial_items": [asdict(item) for item in report.commercial_items],
        "fabricated_parts": [asdict(part) for part in report.fabricated_parts],
        "hardware_items": [asdict(hw) for hw in report.hardware_items],
        "stock_summary": [asdict(s) for s in report.stock_summary],
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
