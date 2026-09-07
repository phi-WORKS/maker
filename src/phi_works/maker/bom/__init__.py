"""
Maker Bill of Materials (BOM) & Fabrication Cut List Engine

Provides automated physical assembly extraction, atomic commercial component
boundary enforcement, custom part cut list derivation, and multi-format exports
(Markdown, CSV, JSON) with conditional filtering.
"""

import os
from phi_works.maker.bom.models import (
    BOMItemType,
    CommercialItem,
    FabricatedPart,
    HardwareItem,
    StockSummaryItem,
    BOMReport,
)
from phi_works.maker.bom.extractor import extract_bom
from phi_works.maker.bom.filters import (
    filter_bom,
    create_procurement_list,
    create_fabrication_cut_list,
)
from phi_works.maker.bom.formatters import (
    generate_bom_markdown,
    export_bom_markdown,
    export_bom_csv,
    export_bom_json,
)


def export_bom(
    doc,
    output_dir: str,
    formats=("markdown", "csv", "json"),
    config: dict = None,
    md_filename: str = "BOM.md",
    json_filename: str = "bom.json",
) -> BOMReport:
    """
    Extracts the BOM from a FreeCAD document and writes specified export artifacts.

    Parameters:
      doc: FreeCAD Document
      output_dir: Target folder (e.g. project directory)
      formats: Iterable of strings ("markdown", "csv", "json")
      config: Optional dictionary with extraction options
      md_filename: Name of the output Markdown file (default 'BOM.md')
      json_filename: Name of the output JSON file (default 'bom.json')

    Returns:
      Extracted BOMReport instance
    """
    report = extract_bom(doc, config=config)

    formats_set = set(f.lower() for f in formats)

    if "markdown" in formats_set or "md" in formats_set:
        md_path = os.path.join(output_dir, md_filename)
        export_bom_markdown(report, md_path)
        print(f"Generated Bill of Materials Markdown: {md_path}")

    if "csv" in formats_set:
        export_bom_csv(report, output_dir)
        print(f"Exported CSV tables (bom_commercial.csv, cut_list.csv, hardware.csv) to: {output_dir}")

    if "json" in formats_set:
        json_path = os.path.join(output_dir, json_filename)
        export_bom_json(report, json_path)
        print(f"Exported BOM JSON: {json_path}")

    return report


__all__ = [
    "BOMItemType",
    "CommercialItem",
    "FabricatedPart",
    "HardwareItem",
    "StockSummaryItem",
    "BOMReport",
    "extract_bom",
    "filter_bom",
    "create_procurement_list",
    "create_fabrication_cut_list",
    "generate_bom_markdown",
    "export_bom_markdown",
    "export_bom_csv",
    "export_bom_json",
    "export_bom",
]
