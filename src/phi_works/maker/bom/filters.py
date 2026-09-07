"""
Conditional Filtering Engine for Bill of Materials & Cut Lists

Enables generating specialized, targeted reports:
- Purchasing / Procurement List (Commercial COTS items & hardware only)
- Machine Shop Cut List (Custom fabricated metal & wood parts only)
- Material-Specific Lists (e.g. Steel only, Stainless only, Wood only)
- Subassembly-Specific Reports
"""

import copy
from typing import List, Optional, Callable, Any
from phi_works.maker.bom.models import BOMReport, CommercialItem, FabricatedPart, HardwareItem, StockSummaryItem


def filter_bom(
    report: BOMReport,
    include_commercial: bool = True,
    include_fabricated: bool = True,
    include_hardware: bool = True,
    categories: Optional[List[str]] = None,
    materials: Optional[List[str]] = None,
    subassemblies: Optional[List[str]] = None,
    min_mass_lb: Optional[float] = None,
    custom_predicate: Optional[Callable[[Any], bool]] = None,
) -> BOMReport:
    """
    Applies conditional filtering rules to a BOMReport and returns a new filtered BOMReport.
    """
    new_report = BOMReport(
        project_name=report.project_name,
        version=report.version,
        date_str=report.date_str,
        commercial_items=[],
        fabricated_parts=[],
        hardware_items=[],
        stock_summary=[],
    )

    cat_set = set(c.lower() for c in categories) if categories else None
    mat_set = set(m.lower() for m in materials) if materials else None
    sub_set = set(s.lower() for s in subassemblies) if subassemblies else None

    # 1. Commercial Items
    if include_commercial:
        for item in report.commercial_items:
            if cat_set and item.category.lower() not in cat_set:
                continue
            if sub_set and not any(s in item.subassembly.lower() for s in sub_set):
                continue
            if min_mass_lb is not None and item.mass_lb < min_mass_lb:
                continue
            if custom_predicate and not custom_predicate(item):
                continue
            new_report.commercial_items.append(copy.deepcopy(item))

    # 2. Fabricated Parts
    if include_fabricated:
        for part in report.fabricated_parts:
            if mat_set and part.material.lower() not in mat_set:
                continue
            if sub_set and not any(s in part.subassembly.lower() for s in sub_set):
                continue
            if min_mass_lb is not None and part.mass_lb < min_mass_lb:
                continue
            if custom_predicate and not custom_predicate(part):
                continue
            new_report.fabricated_parts.append(copy.deepcopy(part))

    # 3. Hardware Items
    if include_hardware:
        for hw in report.hardware_items:
            if cat_set and hw.category.lower() not in cat_set:
                continue
            if mat_set and hw.material.lower() not in mat_set:
                continue
            if sub_set and not any(s in hw.subassembly.lower() for s in sub_set):
                continue
            if custom_predicate and not custom_predicate(hw):
                continue
            new_report.hardware_items.append(copy.deepcopy(hw))

    # 4. Recompute Stock Summary for the remaining fabricated parts
    stock_groups = {}
    for part in new_report.fabricated_parts:
        key = (part.material, part.stock_spec, part.stock_type)
        if key not in stock_groups:
            stock_groups[key] = {
                "count": 0,
                "linear_in": 0.0,
                "area_sq_in": 0.0,
                "mass_lb": 0.0,
                "pieces": [],
            }
        g = stock_groups[key]
        g["count"] += part.qty
        g["mass_lb"] += part.mass_lb * part.qty
        g["pieces"].append(part.part_mark or part.name)

        if part.stock_type in ("Sheet Metal", "Steel Plate"):
            area = part.length_in * part.width_in * part.qty
            g["area_sq_in"] += area
        else:
            g["linear_in"] += part.length_in * part.qty

    new_stock = []
    for (mat, spec, stype), vals in sorted(stock_groups.items()):
        item = StockSummaryItem(
            stock_spec=spec,
            material=mat,
            stock_type=stype,
            piece_count=vals["count"],
            total_linear_in=vals["linear_in"],
            total_linear_ft=vals["linear_in"] / 12.0,
            total_area_sq_in=vals["area_sq_in"],
            total_area_sq_ft=vals["area_sq_in"] / 144.0,
            total_mass_lb=vals["mass_lb"],
            pieces=vals["pieces"],
        )
        new_stock.append(item)

    new_report.stock_summary = new_stock
    return new_report


def create_procurement_list(report: BOMReport) -> BOMReport:
    """
    Filters report to only items requiring commercial acquisition or hardware purchase.
    """
    return filter_bom(report, include_commercial=True, include_fabricated=False, include_hardware=True)


def create_fabrication_cut_list(report: BOMReport) -> BOMReport:
    """
    Filters report to only custom fabricated parts and raw stock requisitions.
    """
    return filter_bom(report, include_commercial=False, include_fabricated=True, include_hardware=False)
