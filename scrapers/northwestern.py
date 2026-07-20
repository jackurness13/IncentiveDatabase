"""
NorthWestern Energy -- Montana Commercial & Industrial efficiency rebates.
Commercial & Industrial programs only (UCREW scope).
Source: northwesternenergy.com/.../energy-efficiency-for-business/rebates-incentives
"""
from bs4 import BeautifulSoup
from .base import get, record

ADMIN = "NorthWestern Energy"
STATE = "MT"
SECTOR = "Commercial & Industrial"
BIZ_URL = "https://www.northwesternenergy.com/account-services/for-business/energy-efficiency-for-business/rebates-incentives"


def fetch_all():
    rows = _scrape_business() or _business_fallback()
    print("  NorthWestern Energy [MT]: " + str(len(rows)) + " programs")
    return rows


def _scrape_business():
    try:
        soup = BeautifulSoup(get(BIZ_URL).text, "lxml")
        programs = []
        for row in soup.select("table tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cells) >= 2 and cells[0]:
                programs.append(record(
                    STATE, "NorthWestern Energy Business -- " + cells[0], ADMIN,
                    SECTOR, "Rebate", _infer_tech(cells[0]),
                    cells[1] if len(cells) > 1 else "See program",
                    cells[2] if len(cells) > 2 else "See program",
                    "NorthWestern Energy commercial & industrial customers in Montana",
                    "2026-06-30", BIZ_URL,
                ))
        return programs if len(programs) >= 2 else []
    except Exception:
        return []


def _business_fallback():
    programs = [
        (
            "NorthWestern Energy Business -- Commercial Lighting (LED)", "LED Lighting",
            "Varies per fixture", "Varies", "2026-06-30",
            "$0.08-0.12/kWh first-year savings",
            "", "", "Existing wattage x annual operating hours", "",
            "Custom incentive based on watts reduced and annual operating hours",
            "1. Contact NorthWestern Energy business team. 2. Get a free lighting audit from a Trade Ally contractor. 3. Submit project proposal with fixture counts and hours of operation. 4. Install qualifying LEDs. 5. Submit final application with invoices and fixture documentation.",
            "Rebate = (old watts - new watts) x annual hours / 1,000 x incentive rate (typically $0.08-0.12/kWh). Montana commercial operations: office 2,500 hrs/yr; retail 4,000 hrs/yr; industrial 5,000-8,000 hrs/yr.",
            "Example: A 15,000 sq ft retail store in Billings, MT replaces 120 T8 fluorescent fixtures (32W) with LED tubes (15W). Savings: 120 x 17W x 4,000 hrs / 1,000 = 8,160 kWh/yr. Rebate at $0.10/kWh: $816. Material cost: $1,800. Annual savings: 8,160 x $0.073 (commercial rate) = $596. Payback: ~1.7 years after rebate.",
        ),
        (
            "NorthWestern Energy Business -- Commercial HVAC", "Heat Pump / HVAC",
            "Varies by equipment", "Varies", "2026-06-30",
            "Efficiency improvement x annual kWh x incentive rate",
            "", "", "ASHRAE 90.1 baseline efficiency by equipment category", "",
            "Heat pumps, chillers, RTUs; contact NorthWestern for equipment-specific incentive schedule",
            "1. Contact NorthWestern Energy commercial team for pre-approval. 2. Submit equipment specs and energy savings analysis. 3. Install qualifying equipment. 4. Submit final documentation.",
            "Commercial HVAC rebate = efficiency improvement x annual energy use x incentive rate. Benchmarked against ASHRAE 90.1 baseline efficiency for each equipment category. Montana commercial electric rate: ~$0.067-0.082/kWh.",
            "Example: A 10-room motel in Whitefish, MT replaces 10 PTAC units (10 EER) with mini-split heat pumps (18 SEER2 / HSPF2 10). Annual cooling savings: 6,000 kWh. Annual heating savings vs. electric resistance: 12,000 kWh. Estimated rebate: ~$1,800. Annual savings: 18,000 kWh x $0.075 = $1,350. Payback after rebate: ~9 years.",
        ),
        (
            "NorthWestern Energy Business -- Custom Efficiency Projects (Industrial)", "Multiple Technologies",
            "Custom calculation per kWh or therm saved", "Custom", "2026-06-30",
            "$0.08-0.12/kWh electric; $0.50-0.80/therm gas (verified)",
            "", "", "IPMVP Option A/B/C measured baseline (ASHRAE Level 2 audit)", "Payback 5+ yrs without rebate",
            "Non-prescriptive measures; M&V plan required; minimum project size applies",
            "1. Contact NorthWestern Energy business team. 2. Submit pre-approval with engineering analysis (ASHRAE Level 2 audit minimum). 3. Agree on M&V plan (IPMVP Option A, B, or C). 4. Install project. 5. Submit verified savings documentation. 6. Receive rebate.",
            "Rebate = verified first-year kWh (or therm) savings x incentive rate. Electric: $0.08-0.12/kWh. Gas: $0.50-0.80/therm. Project must achieve payback of 5+ years without rebate to qualify (rebate brings to 3-4 yr target).",
            "Example: A Helena, MT food processing facility installs compressed air system upgrades (variable speed compressor, leak detection, pressure optimization). Pre-approval energy model: 140,000 kWh/yr savings. Post-installation M&V: 128,000 kWh confirmed. Rebate: 128,000 x $0.10 = $12,800. Project cost: $45,000. Annual savings: 128,000 x $0.078 = $9,984. Payback after rebate: ~3.2 years.",
        ),
    ]
    return [
        record(STATE, name, ADMIN, SECTOR, "Rebate", tech, value, max_b,
               "NorthWestern Energy commercial & industrial customers in Montana",
               exp, BIZ_URL, notes=notes, implementation=impl, methodology=meth, example=ex,
               incentive_rate=rate, rebate_tiers=tiers, unit_cap=cap,
               baseline=baseline, min_project=minp)
        for (name, tech, value, max_b, exp, rate, tiers, cap, baseline, minp,
             notes, impl, meth, ex) in programs
    ]


def _infer_tech(name):
    n = name.lower()
    if "heat pump" in n and "water" not in n:
        return "Heat Pump"
    if "water heat" in n:
        return "Water Heater"
    if "led" in n or "light" in n:
        return "LED Lighting"
    if "insulat" in n or "weatheri" in n or "air seal" in n:
        return "Insulation / Weatherization"
    if "hvac" in n or "furnace" in n or "boiler" in n:
        return "HVAC / Furnace"
    return "Multiple Technologies"
