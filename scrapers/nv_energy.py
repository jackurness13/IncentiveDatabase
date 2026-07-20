"""
NV Energy -- PowerShift Business energy services, Nevada.
Commercial & Industrial programs only (UCREW scope).
Source: nvenergy.com/save-with-powershift/business-energy-services
"""
from .base import record

ADMIN = "NV Energy"
STATE = "NV"
SECTOR = "Commercial & Industrial"
BIZ_URL = "https://www.nvenergy.com/save-with-powershift/business-energy-services"


def fetch_all():
    rows = _business()
    print("  NV Energy [NV]: " + str(len(rows)) + " programs")
    return rows


def _business():
    programs = [
        (
            "NV Energy Business -- Commercial HVAC Efficiency", "Heat Pump / HVAC",
            "Varies by measure", "Varies",
            "~50-75% of first-year kWh savings value",
            "", "", "ASHRAE 90.1 baseline efficiency", "Custom analysis (large projects)",
            "Custom analysis for large commercial projects; contact NV Energy Business Energy Services",
            "1. Contact NV Energy Business Energy Services. 2. Request a free energy assessment. 3. Receive custom rebate offer based on projected kWh savings. 4. Install qualifying equipment with pre-approval. 5. Submit post-installation documentation.",
            "Commercial HVAC rebates calculated on kWh savings vs. ASHRAE 90.1 baseline. Nevada commercial rate: ~$0.073-0.095/kWh. Rebate typically 50-75% of first-year savings value to achieve 3-5 year payback target.",
            "Example: A 50,000 sq ft Las Vegas strip mall replaces 10 rooftop units (SEER 10) with SEER2 18 units. Annual cooling savings: 85,000 kWh. Rebate: ~$8,500. Equipment cost: $60,000. Annual electric savings: 85,000 x $0.085 = $7,225. Payback: ~7.2 years after rebate.",
        ),
        (
            "NV Energy Business -- LED Lighting (Small Business)", "LED Lighting",
            "Varies per kWh saved", "Varies",
            "$0.05-0.10/kWh first-year savings (prescriptive by fixture type)",
            "", "", "Existing fluorescent/incandescent wattage", "",
            "Simplified application for small businesses; prescriptive rebates by fixture type",
            "1. Contact a NV Energy Trade Ally contractor for a free lighting assessment. 2. Select qualifying LED replacements from approved product list. 3. Contractor can submit rebate application directly. 4. Rebate paid within 6-8 weeks of completion.",
            "LED lighting uses 50-70% less energy than fluorescent/incandescent. Commercial lighting operates 3,000-5,000 hrs/yr. Rebate = watts saved x hours/yr / 1,000 x incentive rate (typically $0.05-0.10/kWh first-year savings).",
            "Example: A small restaurant in Carson City, NV replaces 40 T8 fluorescent fixtures (32W each) with LED tubes (15W each). Savings: 40 x 17W x 4,000 hrs / 1,000 = 2,720 kWh/yr. Rebate: ~$272. Material cost: $480. Annual savings: 2,720 x $0.09 = $245. Payback: ~0.9 years after rebate.",
        ),
    ]
    return [
        record(STATE, name, ADMIN, SECTOR, "Rebate", tech, value, max_b,
               "Commercial & industrial NV Energy customers in Nevada", "Ongoing", BIZ_URL,
               notes=notes, implementation=impl, methodology=meth, example=ex,
               incentive_rate=rate, rebate_tiers=tiers, unit_cap=cap,
               baseline=baseline, min_project=minp)
        for (name, tech, value, max_b, rate, tiers, cap, baseline, minp,
             notes, impl, meth, ex) in programs
    ]
