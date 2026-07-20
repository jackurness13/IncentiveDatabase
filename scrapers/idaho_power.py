"""
Idaho Power -- Commercial, Industrial & Agricultural efficiency programs.
Commercial & Industrial scope (UCREW): residential programs excluded.
Source: idahopower.com/energy-environment/ways-to-save/savings-for-your-business
"""
from .base import record

ADMIN = "Idaho Power"
STATE = "ID"
BIZ_URL = "https://www.idahopower.com/energy-environment/ways-to-save/savings-for-your-business/"
AG_URL = "https://www.idahopower.com/energy-environment/ways-to-save/savings-for-your-business/agricultural/"


def fetch_all():
    rows = _business()
    print("  Idaho Power [ID]: " + str(len(rows)) + " programs")
    return rows


def _business():
    programs = [
        (
            "Idaho Power -- Flex Peak Program (Commercial Demand Response)",
            "Commercial & Industrial", "HVAC / AC",
            "$5-$7/kW per event", "Varies",
            "$5-$7/kW per demand-response event",
            "", "", "Enrolled controllable load (kW)", "Qualified controllable load required",
            "Idaho Power commercial customers with qualified controllable load", BIZ_URL,
            "Commercial equivalent of residential demand response; reduces peak demand charges",
            "1. Contact Idaho Power commercial team to assess controllable load (HVAC, lighting, refrigeration, etc.). 2. Install smart controls or enroll existing BMS. 3. Participate in demand response events (typically June-September, 2-6 PM, max 10 events/summer). 4. Receive per-kW bill credit for each event.",
            "Demand response value = controllable kW x events x $/kW/event. Additional benefit: reducing peak demand reduces monthly demand charges (Idaho Power commercial demand charge: ~$8-12/kW/month). Reducing 20 kW of peak demand can save $160-240/month on demand charges.",
            "Example: A 30,000 sq ft office in Boise, ID enrolls 25 kW of pre-cooling capable HVAC load. Peak demand credit: 25 kW x 10 events x $6 = $1,500/yr. Plus avoids 25 kW demand charge increase: 25 x $10 x 4 months = $1,000/yr. Total annual benefit: ~$2,500.",
        ),
        (
            "Idaho Power -- Custom Efficiency (Commercial & Industrial)",
            "Commercial & Industrial", "Multiple Technologies",
            "Custom calculation per kWh saved", "Custom",
            "$0.08-0.12/kWh verified first-year savings",
            "", "", "ASHRAE Level 2 audit measured baseline (M&V)", "50,000 kWh/yr savings",
            "Idaho Power commercial and industrial customers", BIZ_URL,
            "Large C&I projects; includes new construction, major retrofits, custom measures; M&V required",
            "1. Contact Idaho Power's Custom Efficiency team. 2. Complete ASHRAE Level 2 energy audit. 3. Submit custom project application with engineering analysis. 4. Pre-approve project (3-6 weeks). 5. Implement with M&V plan. 6. Submit post-installation verified savings. 7. Receive rebate.",
            "Rebate = verified first-year kWh savings x $0.08-0.12/kWh. Projects must show incremental cost payback > 3 years without rebate (rebate brings payback to 2-3 yr target). Minimum savings: 50,000 kWh/yr.",
            "Example: A 200,000 sq ft manufacturing facility in Twin Falls, ID upgrades compressed air system, variable frequency drives on conveyor motors, and lighting. Energy model predicts 850,000 kWh/yr savings. M&V confirms 810,000 kWh. Rebate: 810,000 x $0.10 = $81,000. Project cost: $280,000. Annual savings: 810,000 x $0.075 = $60,750. Payback after rebate: ~3.3 years.",
        ),
        (
            "Idaho Power -- Irrigation Efficiency Rewards",
            "Agricultural", "Irrigation / Pumping",
            "Varies by measure", "Varies",
            "Per kWh saved (pump/motor/VFD upgrades)",
            "", "", "Existing pump wire-to-water efficiency", "Free audit; measure-dependent",
            "Idaho Power agricultural customers with irrigation systems", AG_URL,
            "VFDs, motor replacements, pump efficiency upgrades, irrigation scheduling controls",
            "1. Contact Idaho Power's agricultural team. 2. Schedule a free irrigation system audit. 3. Receive recommendations and incentive estimate. 4. Implement qualifying measures (VFD, efficient pump, scheduling controls). 5. Submit application with invoices within 90 days of installation.",
            "Irrigation pumping is Idaho's largest agricultural electricity end-use. Rebate = (old pump efficiency - new pump efficiency) x annual kWh x incentive rate. VFDs on variable-load pumps typically save 30-50% on pump energy. Idaho agricultural rate: ~$0.063/kWh (off-peak irrigation schedule).",
            "Example: A Kimberly, ID farm replaces an 80% wire-to-water efficiency pump motor on a 50 hp irrigation pump with a 92% efficiency motor + VFD. Annual pump run: 1,200 hours. Old: 50 hp x 0.746 kW/hp / 0.80 x 1,200 = 55,950 kWh. New: 50 x 0.746 / 0.92 x 0.70 (VFD load factor) x 1,200 = 34,350 kWh. Savings: 21,600 kWh x $0.063 = $1,361/yr. Estimated rebate: ~$3,000. VFD + motor: $8,500. Payback after rebate: ~4 years.",
        ),
    ]
    return [
        record(
            STATE, name, ADMIN, sector, "Rebate", tech, value, max_b,
            recip, "Ongoing", url,
            notes=notes, implementation=impl, methodology=meth, example=ex,
            incentive_rate=rate, rebate_tiers=tiers, unit_cap=cap,
            baseline=baseline, min_project=minp,
        )
        for (name, sector, tech, value, max_b, rate, tiers, cap, baseline, minp,
             recip, url, notes, impl, meth, ex) in programs
    ]
