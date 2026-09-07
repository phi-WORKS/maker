"""
Component Metadata Sourcing & Catalog Registry

Provides helpers to resolve commercial and technical metadata (vendor, SKU,
category, description, estimated/spec weight, URLs) for reusable components
in `components/<component_name>/`.
"""

import os
import re
import json

# Built-in catalog metadata for known maker components
CATALOG_METADATA = {
    "commercial_hand_truck": {
        "title": "Commercial Tubular Steel Hand Truck Chassis",
        "category": "Chassis / Running Gear",
        "acquisition": "commercial",
        "vendor": "Donor / Restored Commercial Equipment",
        "part_number": "HANDTRUCK-VINTAGE-01",
        "description": "1.0\" OD tubular steel frame, 12.5\" riser spacing, 9.5\" x 3.0\" wheels on 5/8\" solid axle",
        "spec_mass_lb": 24.5,
        "spec_mass_kg": 11.1,
        "reference_url": "components/commercial_hand_truck/README.md",
    },
    "platform_cart_24x36": {
        "title": "Commercial 24\" x 36\" Platform Truck / Dolly",
        "category": "Chassis / Rolling Platform",
        "acquisition": "commercial",
        "vendor": "Commercial Equipment / Harbor Freight / Uline",
        "part_number": "PLATFORM-24X36-1000LB",
        "description": "24\" W x 36\" L diamond plate steel deck, folding handle, dual 5\" rigid casters & dual 5\" swivel casters",
        "spec_mass_lb": 48.0,
        "spec_mass_kg": 21.8,
        "reference_url": "components/platform_cart_24x36/README.md",
    },
    "solaronics_infrared_burner": {
        "title": "Solaronics High-Intensity Ceramic Infrared Burner",
        "category": "Thermal Engine / Radiant Burner",
        "acquisition": "commercial",
        "vendor": "Solaronics USA",
        "part_number": "K-60 / 60,000 BTU",
        "description": "60,000 BTU/hr @ 11\" W.C. LP gas, 173 sq. in cordierite ceramic matrix, parabolic reflector, Inconel re-radiating face grid",
        "spec_mass_lb": 18.5,
        "spec_mass_kg": 8.4,
        "reference_url": "components/solaronics_infrared_burner/README.md",
    },
    "propane_cylinder_1lb": {
        "title": "1 lb Disposable / Refillable Propane Cylinder",
        "category": "Fuel System / Pressure Vessel",
        "acquisition": "commercial",
        "vendor": "Worthington / Flame King / Coleman",
        "part_number": "DOT-39 / 16.4 oz",
        "description": "Standard DOT-39 16.4 oz / 1 lb LP gas cylinder with 1\"-20 UNEF threaded valve connection",
        "spec_mass_lb": 1.9,
        "spec_mass_kg": 0.86,
        "reference_url": "components/propane_cylinder_1lb/README.md",
    },
    "propane_cylinder_20lb": {
        "title": "DOT 20 lb Steel Propane Cylinder",
        "category": "Fuel System / Pressure Vessel",
        "acquisition": "commercial",
        "vendor": "Worthington / Manchester Tank",
        "part_number": "DOT-4BA240 / 20 lb",
        "description": "Standard 20 lb (5 gal) LP gas tank with OPD valve, foot ring, and protective collar",
        "spec_mass_lb": 17.0,
        "spec_mass_kg": 7.7,
        "reference_url": "components/propane_cylinder_20lb/README.md",
    },
    "propane_harness": {
        "title": "1 lb Propane Bottle Retention Harness",
        "category": "Fuel System / Mounting",
        "acquisition": "commercial",
        "vendor": "Custom Fabricated / Commercial Quick-Release Bike Cage",
        "part_number": "BOTTLE-CAGE-1LB",
        "description": "Quick-release steel retention cage with base seat cup, side arms, and top knurled latch",
        "spec_mass_lb": 2.2,
        "spec_mass_kg": 1.0,
        "reference_url": "components/propane_harness/README.md",
    },
    "torch_hf91037": {
        "title": "Harbor Freight #91037 Propane Torch Assembly",
        "category": "Combustion / Auxiliary Torch",
        "acquisition": "commercial",
        "vendor": "Harbor Freight",
        "part_number": "ITEM 91037",
        "description": "500,000 BTU propane torch with brass valve, squeeze boost lever, 32\" wand, and piezo igniter",
        "spec_mass_lb": 4.1,
        "spec_mass_kg": 1.86,
        "reference_url": "components/torch_hf91037/README.md",
    },
    "caster_rigid_5in": {
        "title": "5\" Heavy-Duty Rigid Plate Caster",
        "category": "Running Gear / Hardware",
        "acquisition": "commercial",
        "vendor": "McMaster-Carr / Caster City",
        "part_number": "CASTER-5-RIGID-HD",
        "description": "5.0\" OD x 1.25\" wide polyurethane/rubber wheel, 10-gauge zinc-plated rigid horn, 4\" x 4.5\" plate",
        "spec_mass_lb": 3.2,
        "spec_mass_kg": 1.45,
        "reference_url": "components/caster_rigid_5in/README.md",
    },
    "caster_swivel_5in": {
        "title": "5\" 360-Degree Swivel Plate Caster with Brake",
        "category": "Running Gear / Hardware",
        "acquisition": "commercial",
        "vendor": "McMaster-Carr / Caster City",
        "part_number": "CASTER-5-SWIVEL-BRK",
        "description": "5.0\" OD x 1.25\" wide wheel, 360° swivel crown with double ball raceway and toe lock brake",
        "spec_mass_lb": 3.6,
        "spec_mass_kg": 1.63,
        "reference_url": "components/caster_swivel_5in/README.md",
    },
    "caster_wheel_5in": {
        "title": "5\" Industrial Caster Wheel",
        "category": "Running Gear / Hardware",
        "acquisition": "commercial",
        "vendor": "McMaster-Carr",
        "part_number": "WHEEL-5-IND",
        "description": "5.0\" OD polyurethane wheel with 3/8\" axle bore and rubber tread",
        "spec_mass_lb": 1.2,
        "spec_mass_kg": 0.54,
        "reference_url": "components/caster_wheel_5in/README.md",
    },
    "steel_caster_wheel": {
        "title": "4\" Solid Machined Cast Steel Wheel",
        "category": "Running Gear / High-Temp",
        "acquisition": "commercial",
        "vendor": "McMaster-Carr",
        "part_number": "WHEEL-4-STEEL",
        "description": "4.0\" OD x 1.5\" face machined cast steel wheel with 1/2\" axle bolt hardware",
        "spec_mass_lb": 3.8,
        "spec_mass_kg": 1.72,
        "reference_url": "components/steel_caster_wheel/README.md",
    },
}


def parse_readme_metadata(readme_path):
    """
    Parses title and top summary from a component's README.md file.
    """
    if not os.path.exists(readme_path):
        return {}

    info = {}
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line_s = line.strip()
            if line_s.startswith("# ") and "title" not in info:
                info["title"] = line_s[2:].strip()
            elif line_s.startswith("> ") and "description" not in info:
                info["description"] = line_s[2:].replace("*", "").strip()
            elif "title" in info and "description" in info:
                break
    except Exception:
        pass
    return info


def get_component_metadata(component_name):
    """
    Resolves comprehensive commercial and technical metadata for a component.

    Checks:
    1. Built-in CATALOG_METADATA registry.
    2. `components/<component_name>/metadata.json` if present.
    3. `components/<component_name>/README.md` parsing.
    4. Sane defaults based on component_name.
    """
    base_name = os.path.basename(component_name).replace(".FCStd", "")

    # Start with catalog entry if present
    data = CATALOG_METADATA.get(base_name, {}).copy()

    # Locate component directory
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    maker_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "..", ".."))
    comp_dir = os.path.join(maker_dir, "components", base_name)

    # Check for metadata.json
    json_path = os.path.join(comp_dir, "metadata.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                override = json.load(f)
                data.update(override)
        except Exception:
            pass

    # If title or description missing, check README.md
    if not data.get("title") or not data.get("description"):
        readme_path = os.path.join(comp_dir, "README.md")
        readme_meta = parse_readme_metadata(readme_path)
        if not data.get("title") and readme_meta.get("title"):
            data["title"] = readme_meta["title"]
        if not data.get("description") and readme_meta.get("description"):
            data["description"] = readme_meta["description"]

    # Sane fallbacks
    if not data.get("title"):
        data["title"] = base_name.replace("_", " ").title()
    if not data.get("category"):
        data["category"] = "Commercial Hardware"
    if not data.get("acquisition"):
        data["acquisition"] = "commercial"
    if not data.get("vendor"):
        data["vendor"] = "Commercial Supplier / COTS"
    if not data.get("part_number"):
        data["part_number"] = base_name.upper()

    return data
