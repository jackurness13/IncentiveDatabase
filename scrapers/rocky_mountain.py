"""
Rocky Mountain Power (PacifiCorp) -- Utah Wattsmart(R) Business programs.
Commercial & Industrial energy efficiency incentives only (UCREW scope).
Source: rockymountainpower.net/savings-energy-choices/business
"""
from .base import record

BASE = "https://www.rockymountainpower.net"
ADMIN = "Rocky Mountain Power"
STATE = "UT"
SECTOR = "Commercial & Industrial"


def fetch_all():
    rows = _business()
    print("  Rocky Mountain Power [UT]: " + str(len(rows)) + " programs")
    return rows


def _business():
    url = BASE + "/savings-energy-choices/business/wattsmart-efficiency-incentives-utah.html"
    programs = [
        (
            "Wattsmart(R) Business -- HVAC / Heat Pump", "Heat Pump / HVAC",
            "Varies by equipment", "Varies",
            "$0.08-0.12/kWh first-year savings; standard HVAC ~$50-300/ton",
            "", "", "ASHRAE 90.1 standard-efficiency HVAC baseline", "$2,000 project (pre-approval)",
            "Custom incentive based on efficiency vs. baseline; standard HVAC typically $50-300/ton",
            "1. Contact Rocky Mountain Power business team at 1-866-870-3419 for pre-approval on projects over $2,000. 2. Get bids from licensed HVAC contractors. 3. Install qualifying equipment. 4. Submit application with invoices and equipment specs. 5. Receive rebate check in 6-8 weeks.",
            "Rebate = (baseline kWh - new equipment kWh) x incentive rate. Baseline is standard-efficiency HVAC per ASHRAE 90.1. Incentive rate typically $0.08-0.12/kWh first-year savings. Simple payback target: 3-5 years for standard projects.",
            "Example: A 10,000 sq ft office in Salt Lake City replaces a 20-ton rooftop unit (11 EER) with a 14 EER unit. Annual cooling savings: 18,000 kWh. Rebate at $0.10/kWh = $1,800. Equipment cost delta: ~$4,000. Net payback: ~1.2 years after rebate.",
        ),
        (
            "Wattsmart(R) Business -- LED Lighting Retrofit", "LED Lighting",
            "Varies by kWh saved", "Varies",
            "$0.08-0.15/kWh first-year savings (prescriptive per fixture also available)",
            "", "", "Existing fixture wattage x operating hours by building type", "$2,000 project (pre-approval)",
            "Typically $0.08-$0.15/kWh first-year savings; prescriptive rebates also available per fixture type",
            "1. Contact Rocky Mountain Power or authorized trade ally for a free lighting audit. 2. Get quote from lighting contractor. 3. Submit pre-approval for projects over $2,000. 4. Install qualifying LEDs. 5. Submit final application with fixture counts and invoices.",
            "Rebate = (watts saved per fixture x operating hours/yr x number of fixtures) / 1,000 x incentive rate. Operating hours based on building type (retail: 4,000 hrs/yr; office: 2,500 hrs/yr; warehouse: 3,000 hrs/yr).",
            "Example: A warehouse in Ogden replaces 200 x 400W metal halide fixtures with 200 x 150W LED high-bays. Savings: 200 x 250W x 3,000 hrs / 1,000 = 150,000 kWh/yr. Rebate at $0.10/kWh = $15,000. Installation cost: $30,000. Annual energy savings: 150,000 x $0.073 (commercial rate) = $10,950. Simple payback after rebate: ~1.4 years.",
        ),
        (
            "Wattsmart(R) Business -- Building Envelope (Insulation)", "Insulation / Weatherization",
            "Varies by measure", "Varies",
            "Attic insulation ~$0.05-0.10/sq ft; cool roofs ~$0.10/sq ft",
            "", "", "DOE-2 modeling or climate zone 5 prescriptive estimates", "$5,000 project (pre-approval)",
            "Prescriptive rebates: attic insulation ~$0.05-0.10/sq ft; cool roofs ~$0.10/sq ft",
            "1. Obtain contractor bids. 2. Submit pre-approval for projects over $5,000. 3. Complete installation. 4. Submit application with invoices, photos, and R-value documentation.",
            "Savings calculated using DOE-2 energy modeling or prescriptive savings estimates based on climate zone and building type. Utah's climate zone 5 baseline assumptions apply.",
            "Example: A 20,000 sq ft retail building adds roof insulation from R-11 to R-30 (20,000 sq ft). Rebate: 20,000 x $0.07 = $1,400. Material + labor: $14,000. Annual HVAC savings: ~$2,100 (15% of $14,000 annual energy spend). Payback after rebate: ~6 years.",
        ),
        (
            "Wattsmart(R) Business -- Custom Projects (Industrial)", "Multiple Technologies",
            "Custom calculation", "Custom",
            "$0.08-0.12/kWh verified first-year savings",
            "", "", "IPMVP Option A/B/C measured baseline", "$5,000 in annual energy savings",
            "Available for non-prescriptive measures not covered by standard rebate schedule; ideal for industrial process loads",
            "1. Contact Rocky Mountain Power business team. 2. Submit pre-approval application with energy savings analysis (DOE-2 modeling or M&V plan). 3. Await approval (2-4 weeks). 4. Implement project. 5. Submit post-installation M&V data. 6. Receive rebate.",
            "Custom projects use International Performance Measurement and Verification Protocol (IPMVP) Option A, B, or C. Rebate = verified first-year kWh savings x $0.08-0.12. Minimum project size: $5,000 in energy savings.",
            "Example: A food processing plant in Lindon, UT installs variable frequency drives (VFDs) on 15 pump motors. Pre-installation energy audit shows 380,000 kWh/yr savings potential. Post-installation M&V confirms 350,000 kWh. Rebate: 350,000 x $0.10 = $35,000. Project cost: $85,000. Net payback: ~2.3 years.",
        ),
        (
            "Wattsmart(R) Business -- Appliances & Office Equipment", "Appliances",
            "Varies by product", "Varies",
            "Prescriptive per ENERGY STAR qualified product",
            "", "", "Standard (non-ENERGY STAR) commercial equipment", "",
            "Prescriptive: ENERGY STAR commercial refrigeration, commercial food service equipment, office equipment",
            "1. Select ENERGY STAR qualified commercial equipment. 2. Purchase and install. 3. Submit rebate application with proof of purchase and equipment model number within 90 days.",
            "Rebate amounts based on ENERGY STAR qualified product list savings estimates. Commercial refrigeration savings: 10-30% vs. standard. Vending machines: 30-50% vs. standard.",
            "Example: A restaurant in Provo, UT replaces a standard reach-in refrigerator (1,800 kWh/yr) with an ENERGY STAR model (1,200 kWh/yr). Annual savings: 600 kWh x $0.073 = $44/yr. Rebate: ~$75. Unit cost delta: $200. Total payback: ~2.8 years.",
        ),
    ]
    return [
        record(STATE, name, ADMIN, SECTOR, "Rebate", tech, value, max_b,
               "Commercial & industrial Rocky Mountain Power customers in Utah", "Ongoing", url,
               notes=notes, implementation=impl, methodology=meth, example=ex,
               incentive_rate=rate, rebate_tiers=tiers, unit_cap=cap,
               baseline=baseline, min_project=minp)
        for (name, tech, value, max_b, rate, tiers, cap, baseline, minp,
             notes, impl, meth, ex) in programs
    ]
