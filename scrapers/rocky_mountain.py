"""
Rocky Mountain Power (PacifiCorp) -- Utah wattsmart(R) Business incentives.
Commercial & Industrial energy efficiency only (UCREW scope).

Accuracy note: rather than one broad "custom" bucket, measures are broken out to
the granularity RMP actually publishes, with the exact rate for each. RMP posts
its Utah incentive amounts in per-category pages/PDFs (linked per measure below);
the daily scanner keeps the pages live-checked and auto-expires stale ones. When
RMP revises a rate, update the matching entry here.

Sources:
  Incentive lists (all categories): .../ut-incentive-lists.html
  Compressed air:                   .../ut-incentive-lists/ut-compressed-air.html
  Motors & drives:                  .../ut-incentive-lists/ut-motors-drives.html
  HVAC:                             .../ut-incentive-lists/ut-hvac.html
"""
from .base import record

BASE = "https://www.rockymountainpower.net"
BIZ = BASE + "/savings-energy-choices/business/wattsmart-efficiency-incentives-utah"
LISTS = BIZ + "/ut-incentive-lists"
ADMIN = "Rocky Mountain Power"
STATE = "UT"
SECTOR = "Commercial & Industrial"
RECIP = "Commercial & industrial Rocky Mountain Power customers in Utah"

# Authoritative per-category incentive pages (published rates live in their PDFs).
URL = {
    "compressed_air": LISTS + "/ut-compressed-air.html",
    "motors": LISTS + "/ut-motors-drives.html",
    "hvac": LISTS + "/ut-hvac.html",
    "lists": LISTS + ".html",
    "business": BIZ + ".html",
}


def fetch_all():
    rows = _measures()
    print("  Rocky Mountain Power [UT]: " + str(len(rows)) + " programs")
    return rows


# Each dict is one measure. Keep names specific ("VFD Air Compressor (<=75 hp)")
# so the AR Finder matches them precisely and shows the right rate. Rates that RMP
# calculates from an engineering estimate are still exact per-kWh figures -- the
# *rate* is fixed, only the annual-kWh input varies.
MEASURES = [
    # ---- Compressed air (rate confirmed from the RMP wattsmart application) ----
    {
        "name": "wattsmart Business -- VFD Air Compressor (<=75 hp)",
        "tech": "Compressed Air / VFD",
        "value": "$0.15/kWh of annual energy savings",
        "max": "By estimated annual savings",
        "rate": "$0.15 per kWh of annual energy savings (savings estimated by Rocky Mountain Power)",
        "tiers": "",
        "cap": "",
        "baseline": "Total system compressor capacity <=75 hp (all compressors combined, excluding backup)",
        "minp": "VFD must be the primary means of capacity control; savings estimate subject to RMP approval",
        "url": URL["compressed_air"],
        "notes": "Incentive is paid at $0.15 per kWh of annual energy savings. Program staff provide "
                 "the energy savings estimate; subject to Rocky Mountain Power approval. Qualifying unit "
                 "is a variable-frequency-drive oil-injected screw compressor in a system of <=75 hp total "
                 "(all compressors combined, not counting backup capacity) that adjusts speed as the "
                 "primary means of capacity control.",
        "impl": "1. Get an incentive application package from Rocky Mountain Power (1-866-870-3419) or a "
                "wattsmart Business Trade Ally. 2. Confirm the system qualifies (<=75 hp total, VFD primary "
                "capacity control). 3. Purchase and install the qualifying VFD screw compressor. 4. Submit "
                "the application package with IRS Form W-9. 5. Program staff estimate annual kWh savings and "
                "approve. 6. Receive incentive check (typically within 45 days).",
        "meth": "Incentive = estimated annual energy savings (kWh) x $0.15/kWh. Rocky Mountain Power "
                "determines the annual kWh savings estimate for the specific system; the $0.15/kWh rate is "
                "fixed. Applies only when total compressor capacity is <=75 hp and the VFD is the primary "
                "capacity-control method.",
        "example": "Example: A Salt Lake City shop replaces a 50 hp load/no-load screw compressor (its only "
                   "production unit, plus a small backup) with a 50 hp VFD screw compressor. RMP estimates "
                   "38,000 kWh/yr savings from matching output to demand. Incentive: 38,000 x $0.15 = $5,700. "
                   "Incremental cost of the VFD unit: ~$9,000. Payback after incentive: well under 2 years.",
    },
    {
        "name": "wattsmart Business -- Compressed Air System Optimization (calculated)",
        "tech": "Compressed Air",
        "value": "$0.15/kWh of annual energy savings",
        "max": "By estimated annual savings",
        "rate": "$0.15 per kWh of annual energy savings (calculated/estimated by Rocky Mountain Power)",
        "tiers": "",
        "cap": "",
        "baseline": "Existing compressed-air system performance (measured or engineering-estimated)",
        "minp": "Savings estimate subject to RMP approval",
        "url": URL["compressed_air"],
        "notes": "For compressed-air efficiency measures beyond the <=75 hp VFD compressor -- e.g. VFD on "
                 "larger systems, added storage, sequencing/pressure controls, no-loss condensate drains, "
                 "engineered (high-efficiency) nozzles, and leak surveys/repair. Paid at $0.15 per kWh of "
                 "annual energy savings as determined by Rocky Mountain Power.",
        "impl": "1. Contact Rocky Mountain Power or a Trade Ally for a compressed-air assessment. 2. Identify "
                "qualifying measures (controls, storage, drains, nozzles, leak repair, larger VFD). 3. Submit "
                "the incentive application with the savings analysis. 4. RMP reviews/approves the estimate. "
                "5. Install and submit invoices. 6. Receive incentive.",
        "meth": "Incentive = estimated annual kWh savings x $0.15/kWh. Savings are calculated per measure "
                "(leak repair, storage, controls, drains, nozzles) or via a system model for larger VFD "
                "projects, then verified/approved by Rocky Mountain Power.",
        "example": "Example: A manufacturer repairs compressed-air leaks and adds sequencing controls across a "
                   "120 hp system; RMP estimates 90,000 kWh/yr savings. Incentive: 90,000 x $0.15 = $13,500. "
                   "Project cost: ~$22,000. Payback after incentive: ~1.5 years (before ongoing energy savings).",
    },
    # ---- HVAC ----
    {
        "name": "wattsmart Business -- HVAC / Heat Pump",
        "tech": "Heat Pump / HVAC",
        "value": "Prescriptive per unit; custom $0.08-0.12/kWh",
        "max": "Varies",
        "rate": "Prescriptive per-unit amounts (see RMP HVAC list); custom measures ~$0.08-0.12/kWh",
        "tiers": "",
        "cap": "",
        "baseline": "ASHRAE 90.1 standard-efficiency HVAC baseline",
        "minp": "Pre-approval recommended for projects over $2,000",
        "url": URL["hvac"],
        "notes": "High-efficiency rooftop units, heat pumps, chillers, controls/economizers and tune-ups. "
                 "Many measures have fixed per-unit or $/ton prescriptive amounts on RMP's HVAC incentive "
                 "list; non-listed measures go through custom at roughly $0.08-0.12/kWh first-year savings. "
                 "Confirm the current per-unit amount on the linked RMP HVAC page.",
        "impl": "1. Contact Rocky Mountain Power (1-866-870-3419) or a Trade Ally; pre-approve projects over "
                "$2,000. 2. Get bids from licensed HVAC contractors. 3. Install qualifying equipment. "
                "4. Submit the application with invoices and equipment specs. 5. Receive rebate.",
        "meth": "Prescriptive measures pay a fixed amount per unit/ton from the RMP HVAC list. Custom measures "
                "pay (baseline kWh - new kWh) x incentive rate, baseline per ASHRAE 90.1.",
        "example": "Example: A 10,000 sq ft Salt Lake City office replaces a 20-ton rooftop unit (11 EER) with "
                   "a 14 EER unit. Custom savings ~18,000 kWh/yr; rebate at $0.10/kWh = $1,800. Confirm whether "
                   "a fixed $/ton prescriptive amount applies instead on RMP's current HVAC list.",
    },
    # ---- Lighting ----
    {
        "name": "wattsmart Business -- LED Lighting (Prescriptive + Calculated)",
        "tech": "LED Lighting",
        "value": "Prescriptive per fixture; custom $0.08-0.15/kWh",
        "max": "Varies",
        "rate": "Prescriptive per-fixture/lamp amounts (see RMP lighting list); custom ~$0.08-0.15/kWh",
        "tiers": "",
        "cap": "",
        "baseline": "Existing fixture wattage x operating hours by building type",
        "minp": "Pre-approval recommended for projects over $2,000",
        "url": URL["lists"],
        "notes": "Interior/exterior LED fixtures, high-bays, troffers, and networked lighting controls. RMP "
                 "publishes fixed per-fixture/per-lamp prescriptive amounts; larger or non-listed jobs use "
                 "custom at roughly $0.08-0.15/kWh first-year savings. Confirm current per-fixture amounts on "
                 "RMP's lighting incentive list.",
        "impl": "1. Contact Rocky Mountain Power or an authorized Trade Ally for a lighting assessment. 2. Get "
                "a contractor quote; pre-approve projects over $2,000. 3. Install qualifying LEDs/controls. "
                "4. Submit the final application with fixture counts and invoices. 5. Receive rebate.",
        "meth": "Prescriptive: fixed $ per qualifying fixture/lamp. Custom: (watts saved x annual hours x "
                "quantity / 1,000) x incentive rate. Operating hours by building type (retail ~4,000; office "
                "~2,500; warehouse ~3,000 hrs/yr).",
        "example": "Example: An Ogden warehouse replaces 200 x 400W metal-halide fixtures with 150W LED "
                   "high-bays. Savings: 200 x 250W x 3,000 hrs / 1,000 = 150,000 kWh/yr. Custom rebate at "
                   "$0.10/kWh = $15,000 (or the sum of per-fixture prescriptive amounts, whichever applies).",
    },
    # ---- Building envelope ----
    {
        "name": "wattsmart Business -- Building Envelope (Insulation / Cool Roof)",
        "tech": "Insulation / Weatherization",
        "value": "Prescriptive per sq ft; custom by model",
        "max": "Varies",
        "rate": "Prescriptive per-sq-ft amounts (insulation, cool roofs); custom via energy model",
        "tiers": "",
        "cap": "",
        "baseline": "DOE-2 modeling or Utah climate-zone-5 prescriptive estimates",
        "minp": "Pre-approval recommended for projects over $5,000",
        "url": URL["lists"],
        "notes": "Roof/wall insulation and cool roofs. Prescriptive $/sq ft amounts apply for common upgrades; "
                 "larger scopes use custom energy modeling. Confirm current per-sq-ft amounts on RMP's "
                 "incentive lists.",
        "impl": "1. Obtain contractor bids. 2. Pre-approve projects over $5,000. 3. Complete installation. "
                "4. Submit the application with invoices, photos, and R-value documentation.",
        "meth": "Prescriptive: fixed $/sq ft by measure. Custom: DOE-2 modeling or climate-zone prescriptive "
                "savings estimates; Utah climate zone 5 baselines apply.",
        "example": "Example: A 20,000 sq ft retail building adds roof insulation from R-11 to R-30. At a "
                   "representative $0.07/sq ft the rebate is ~$1,400; confirm the current per-sq-ft amount.",
    },
    # ---- Appliances / plug load ----
    {
        "name": "wattsmart Business -- Commercial Refrigeration & Equipment",
        "tech": "Refrigeration / Appliances",
        "value": "Prescriptive per qualifying product",
        "max": "Varies",
        "rate": "Prescriptive per-unit amounts for qualifying commercial refrigeration/food-service equipment",
        "tiers": "",
        "cap": "",
        "baseline": "Standard (non-high-efficiency) commercial equipment",
        "minp": "",
        "url": URL["lists"],
        "notes": "Commercial refrigeration (ECM evaporator-fan motors, night covers, anti-sweat controls, "
                 "door gaskets, cases) and efficient commercial food-service/office equipment. Fixed per-unit "
                 "prescriptive amounts; confirm current values on RMP's incentive lists.",
        "impl": "1. Select qualifying equipment/measures from RMP's list. 2. Purchase and install. 3. Submit "
                "the rebate application with proof of purchase and model numbers within the program window.",
        "meth": "Rebate is a fixed amount per qualifying unit/measure from RMP's incentive list. Refrigeration "
                "controls and ECM fan motors typically cut case energy 10-30% vs. standard.",
        "example": "Example: A grocery adds ECM evaporator-fan motors and night covers to 20 refrigerated "
                   "cases; the rebate is the sum of the per-unit prescriptive amounts for those measures.",
    },
    # ---- Custom catch-all (only for measures with no prescriptive rate) ----
    {
        "name": "wattsmart Business -- Custom / Calculated Projects (Industrial)",
        "tech": "Multiple Technologies",
        "value": "$0.08-0.12/kWh verified first-year savings",
        "max": "Custom",
        "rate": "~$0.08-0.12/kWh of verified first-year savings (measure-specific)",
        "tiers": "",
        "cap": "",
        "baseline": "IPMVP Option A/B/C measured baseline",
        "minp": "Typically ~$5,000 in annual energy savings",
        "url": URL["business"],
        "notes": "For non-prescriptive measures not covered by a published per-unit/per-kWh amount -- ideal "
                 "for industrial process loads and whole-system projects. If a measure has a prescriptive "
                 "rate (e.g. the $0.15/kWh compressed-air program), use that instead for a more accurate value.",
        "impl": "1. Contact the Rocky Mountain Power business team. 2. Submit a pre-approval application with "
                "an energy-savings analysis (modeling or M&V plan). 3. Await approval (2-4 weeks). 4. Implement. "
                "5. Submit post-installation M&V. 6. Receive rebate.",
        "meth": "Custom projects use IPMVP Option A/B/C. Rebate = verified first-year kWh savings x the "
                "measure's custom rate (~$0.08-0.12/kWh). Minimum project size ~ $5,000 in energy savings.",
        "example": "Example: A food plant installs VFDs on 15 pump motors; M&V confirms 350,000 kWh/yr. Rebate "
                   "at $0.10/kWh = $35,000. (A compressed-air VFD instead would use the $0.15/kWh program.)",
    },
]


def _measures():
    return [
        record(
            STATE, m["name"], ADMIN, SECTOR, "Rebate", m["tech"],
            m["value"], m["max"], RECIP, "Ongoing", m["url"],
            notes=m["notes"], implementation=m["impl"], methodology=m["meth"],
            example=m["example"], incentive_rate=m["rate"], rebate_tiers=m["tiers"],
            unit_cap=m["cap"], baseline=m["baseline"], min_project=m["minp"],
        )
        for m in MEASURES
    ]
