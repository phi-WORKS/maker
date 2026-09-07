"""
Data Models for Bill of Materials & Fabrication Cut Lists
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any


class BOMItemType(str, Enum):
    COMMERCIAL = "commercial"
    FABRICATED = "fabricated"
    HARDWARE = "hardware"
    CONSUMABLE = "consumable"


@dataclass
class CommercialItem:
    """
    Commercial Off-The-Shelf (COTS) or acquired entity (e.g. hand truck chassis,
    gas cylinder, Solaronics burner, casters). Treated as an atomic procurement unit.
    """
    name: str
    component_id: str
    category: str = "General"
    qty: int = 1
    vendor: str = "Commercial Supplier"
    part_number: str = ""
    description: str = ""
    subassembly: str = ""
    mass_kg: float = 0.0
    mass_lb: float = 0.0
    reference_url: str = ""
    notes: str = ""


@dataclass
class FabricatedPart:
    """
    Custom in-house fabricated part produced from raw stock materials
    (sheet metal, flat bar, tube, structural angle, wood).
    """
    name: str
    part_mark: str = ""
    subassembly: str = ""
    material: str = "Steel-A36"
    stock_type: str = "Flat Bar"      # Sheet Metal, Flat Bar, Round Tube, Structural Angle, Plate
    stock_spec: str = ""              # e.g. "14-Ga (0.075\")", "1-1/2\" x 3/16\""
    length_mm: float = 0.0
    width_mm: float = 0.0
    thickness_mm: float = 0.0
    qty: int = 1
    mass_kg: float = 0.0
    mass_lb: float = 0.0
    operations: str = ""              # e.g. "Cut, 30° cold tip bend, weld"
    bounding_box_mm: tuple = (0.0, 0.0, 0.0)

    @property
    def length_in(self) -> float:
        return self.length_mm / 25.4

    @property
    def width_in(self) -> float:
        return self.width_mm / 25.4

    @property
    def thickness_in(self) -> float:
        return self.thickness_mm / 25.4


@dataclass
class HardwareItem:
    """
    Standard hardware, fasteners, fittings, hoses, and electrical lines.
    """
    name: str
    category: str = "Hardware & Fasteners"  # Fasteners, Plumbing, Electrical, Running Gear
    subassembly: str = ""
    material: str = "Steel-ZincPlated"
    specification: str = ""
    qty: int = 1
    mass_kg: float = 0.0
    mass_lb: float = 0.0
    vendor_sku: str = ""
    notes: str = ""


@dataclass
class StockSummaryItem:
    """
    Aggregated raw stock material requirements for shop requisition.
    """
    stock_spec: str
    material: str
    stock_type: str
    piece_count: int = 0
    total_linear_in: float = 0.0
    total_linear_ft: float = 0.0
    total_area_sq_in: float = 0.0
    total_area_sq_ft: float = 0.0
    total_mass_lb: float = 0.0
    pieces: List[str] = field(default_factory=list)


@dataclass
class BOMReport:
    """
    Master report containing all procurement, fabrication, and stock data.
    """
    project_name: str
    version: str = "1.0.0"
    date_str: str = ""
    commercial_items: List[CommercialItem] = field(default_factory=list)
    fabricated_parts: List[FabricatedPart] = field(default_factory=list)
    hardware_items: List[HardwareItem] = field(default_factory=list)
    stock_summary: List[StockSummaryItem] = field(default_factory=list)
    
    @property
    def total_commercial_mass_lb(self) -> float:
        return sum(item.mass_lb * item.qty for item in self.commercial_items)

    @property
    def total_fabricated_mass_lb(self) -> float:
        return sum(part.mass_lb * part.qty for part in self.fabricated_parts)

    @property
    def total_hardware_mass_lb(self) -> float:
        return sum(hw.mass_lb * hw.qty for hw in self.hardware_items)

    @property
    def total_assembly_mass_lb(self) -> float:
        return (
            self.total_commercial_mass_lb
            + self.total_fabricated_mass_lb
            + self.total_hardware_mass_lb
        )
