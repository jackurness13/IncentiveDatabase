"""
Avista Utilities -- Idaho Commercial & Industrial efficiency rebates.
Commercial & Industrial programs only (UCREW scope). Commercial schedule updated Jan 1, 2026.
Source: myavista.com/energy-savings/energy-saving-programs-services-for-your-business
"""
from .base import record

ADMIN = "Avista Utilities"
STATE = "ID"
SECTOR = "Commercial & Industrial"
BIZ_URL = "https://www.myavista.com/energy-savings/energy-saving-programs-services-for-your-business/rebates-idaho"


def fetch_all():
    rows = _business()
    print("  Avista [ID]: " + str(len(rows)) + " programs")
    return rows


def _business():
    programs = [
        (
            "Avista Business -- Commercial Lighting (LED)", "LED Lighting",
            "Varies per fixture (updated Jan 1, 2026)", "Varies",
            "$0.07-0.12/kWh first-year savings",
            "", "", "Existing fixture wattage x operating hours", "$2,000 project (pre-approval)",
            "Updated commercial program effective January 1, 2026; pre-approval recommended for projects > $2,000",
            "1. Contact Avista's commercial team or an Avista Trade Ally contractor for a free lighting audit. 2. Get a proposal showing fixture counts, wattage reduction, and estimated rebate. 3. Submit pre-approval for projects over $2,000. 4. Install qualifying LEDs. 5. Submit final application with invoices and fixture documentation.",
            "Rebate = kWh saved/yr x incentive rate (typically $0.07-0.12/kWh). Commercial lighting hours: office 2,500 hr/yr, retail 4,000 hr/yr, 24-hr operations 8,760 hr/yr. Updated Jan 1, 2026 schedule may differ from prior rates -- verify with Avista before project.",
            "Example: A retail store in Spokane Valley (Avista ID territory) replaces 80 T8 fluorescent fixtures with LED tubes. Savings: 80 x 17W x 4,000 hrs / 1,000 = 5,440 kWh/yr. Rebate at $0.09: $490. Material cost: $1,200. Annual savings: 5,440 x $0.097 = $528. Payback after rebate: ~1.4 years.",
        ),
        (
            "Avista Business -- Commercial HVAC / Heat Pump", "Heat Pump / HVAC",
            "Varies by equipment (updated Jan 1, 2026)", "Varies",
            "$0.07-0.10/kWh first-year savings",
            "", "", "Baseline equipment efficiency (per category)", "$5,000 project (pre-approval)",
            "Updated Jan 1, 2026; pre-approval required for projects > $5,000",
            "1. Contact Avista commercial energy team. 2. Get bids from licensed HVAC contractors. 3. Submit pre-approval with equipment specs and efficiency comparison. 4. Install qualifying equipment. 5. Submit final documentation within 90 days.",
            "Commercial HVAC rebates calculated on efficiency improvement vs. baseline. Avista commercial rate: ~$0.063-0.082/kWh. Incentive rate typically $0.07-0.10/kWh first-year savings.",
            "Example: A 12,000 sq ft office in Coeur d'Alene, ID replaces an aging rooftop unit (SEER 10) with a new heat pump RTU (SEER2 16). Annual cooling savings: 12,000 kWh. Estimated rebate: ~$900-1,200. Equipment delta cost: $5,000. Annual savings: 12,000 x $0.075 = $900. Payback after rebate: ~4-5 years.",
        ),
        (
            "Avista Business -- Custom Commercial Projects (Industrial)", "Multiple Technologies",
            "Custom calculation per kWh or therm saved", "Custom",
            "$0.07-0.10/kWh; $0.40-0.70/therm (verified)",
            "", "", "IPMVP Option A/B/C measured baseline (ASHRAE Level 2)", "Payback > 3 yrs without rebate",
            "Measurement & verification required; pre-approval mandatory; no excluded measure types",
            "1. Contact Avista's commercial team to discuss project scope. 2. Submit project proposal with engineering analysis (ASHRAE Level 2 minimum). 3. Agree on M&V methodology (IPMVP Option A, B, or C). 4. Pre-approve project. 5. Implement measures. 6. Submit M&V report. 7. Receive rebate.",
            "Rebate = verified first-year energy savings x incentive rate ($0.07-0.10/kWh; $0.40-0.70/therm). Custom projects must show payback > 3 years without rebate, < 3 years with rebate.",
            "Example: A manufacturing facility in Sandpoint, ID installs VFDs on 8 cooling tower fan motors. Energy model: 95,000 kWh/yr savings. M&V confirms 88,000 kWh. Rebate: 88,000 x $0.09 = $7,920. Project cost: $28,000. Annual savings: 88,000 x $0.078 = $6,864. Payback after rebate: ~2.9 years.",
        ),
    ]
    return [
        record(STATE, name, ADMIN, SECTOR, "Rebate", tech, value, max_b,
               "Avista commercial & industrial customers in Idaho", "Ongoing", BIZ_URL,
               notes=notes, implementation=impl, methodology=meth, example=ex,
               incentive_rate=rate, rebate_tiers=tiers, unit_cap=cap,
               baseline=baseline, min_project=minp)
        for (name, tech, value, max_b, rate, tiers, cap, baseline, minp,
             notes, impl, meth, ex) in programs
    ]
