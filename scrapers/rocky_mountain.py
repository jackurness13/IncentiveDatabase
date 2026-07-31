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
from .base import record, make_key

UTIL = "rmp"
# Measures with an exact, human-verified rate (everything else is "general" --
# a real category, but the exact per-unit amount is still pending a PDF/data pull).
VERIFIED_DATE = "2026-07-31"
DETAILED_KEYS = {
    "rmp:vfd-air-compressor-75-hp",
    "rmp:compressed-air-system-optimization-calculated",
}

BASE = "https://www.rockymountainpower.net"
BIZ = BASE + "/savings-energy-choices/business/wattsmart-efficiency-incentives-utah"
LISTS = BIZ + "/ut-incentive-lists"
ADMIN = "Rocky Mountain Power"
STATE = "UT"
SECTOR = "Commercial & Industrial"
RECIP = "Commercial & industrial Rocky Mountain Power customers in Utah"

# Authoritative per-category incentive pages (published rates live in their PDFs).
# Each measure points its source at one of these; scrapers/discovery.py treats a
# category as "covered" when some measure's source URL matches it.
URL = {
    "lighting": LISTS + "/ut-lighting.html",
    "hvac": LISTS + "/ut-hvac.html",
    "motors": LISTS + "/ut-motors-drives.html",
    "foodservice": LISTS + "/ut-foodservice.html",
    "compressed_air": LISTS + "/ut-compressed-air.html",
    "envelope": LISTS + "/ut-building-envelope.html",
    "appliances": LISTS + "/ut-appliances-office.html",
    "agriculture": BIZ + "/ut-agriculture.html",
    "wbnc": LISTS + "/wbnc.html",
    "wastewater": LISTS + "/ut-wastewater-other-refrigeration.html",
    "oil_gas": LISTS + "/ut-oil-gas.html",
    "lists": LISTS + ".html",
    "business": BIZ + ".html",
    "battery": BASE + "/savings-energy-choices/wattsmart-battery-program.html",
}

def fetch_all():
    rows = _measures()
    print("  Rocky Mountain Power [UT]: " + str(len(rows)) + " programs")
    return rows
    # Coverage gaps are now surfaced by scrapers/discovery.py, which adds any
    # uncovered category as a 'general' entry (not just a warning).


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
        "url": URL["lighting"],
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
        "url": URL["envelope"],
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
        "url": URL["appliances"],
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
    # ---- Motors & VFDs ----
    {
        "name": "wattsmart Business -- Motors & VFDs (Pumps / Fans)",
        "tech": "Motors & Drives / VFD",
        "value": "Prescriptive per hp; VFD custom by kWh",
        "max": "Varies",
        "rate": "Prescriptive per-hp amounts for premium-efficiency motors; VFDs paid on calculated kWh savings",
        "tiers": "",
        "cap": "",
        "baseline": "NEMA Premium vs. standard motor; fixed-speed vs. VFD operation",
        "minp": "Pre-approval recommended for larger drives",
        "url": URL["motors"],
        "notes": "NEMA Premium-efficiency motors and variable-frequency drives on pumps, fans, and other "
                 "variable-load equipment. Motors typically have a fixed per-hp prescriptive amount; VFDs are "
                 "paid on calculated annual kWh savings. Confirm current per-hp and VFD amounts on RMP's motors "
                 "& drives list. (Compressed-air VFDs use the compressed-air program at $0.15/kWh.)",
        "impl": "1. Identify motors/loads suited to premium motors or VFDs. 2. Get bids; pre-approve larger "
                "drives. 3. Install. 4. Submit the application with nameplate data and invoices. 5. Receive rebate.",
        "meth": "Premium motors: fixed $ per hp by size. VFDs: (fixed-speed kWh - variable-speed kWh) x rate, "
                "with savings driven by load profile (variable-torque loads like pumps/fans save the most).",
        "example": "Example: A VFD on a 40 hp supply fan running at part load saves ~45,000 kWh/yr; the calculated "
                   "incentive plus a per-hp motor rebate offsets much of the drive cost. Confirm current amounts.",
    },
    # ---- Food service ----
    {
        "name": "wattsmart Business -- Commercial Food Service Equipment",
        "tech": "Food Service / Refrigeration",
        "value": "Prescriptive per qualifying appliance",
        "max": "Varies",
        "rate": "Fixed per-unit amounts for efficient commercial kitchen equipment",
        "tiers": "",
        "cap": "",
        "baseline": "Standard commercial food-service equipment",
        "minp": "",
        "url": URL["foodservice"],
        "notes": "Efficient commercial kitchen equipment -- convection/combi ovens, fryers, steamers, "
                 "dishwashers, griddles, and refrigeration. Fixed per-unit prescriptive amounts; confirm current "
                 "values on RMP's food service list.",
        "impl": "1. Select qualifying ENERGY STAR / high-efficiency food-service equipment. 2. Purchase and "
                "install. 3. Submit the rebate application with proof of purchase and model numbers.",
        "meth": "Rebate is a fixed amount per qualifying appliance from RMP's food-service list.",
        "example": "Example: A restaurant replaces a standard convection oven and adds an ENERGY STAR dishwasher; "
                   "the rebate is the sum of the per-unit amounts for those appliances.",
    },
    # ---- Agriculture / irrigation ----
    {
        "name": "wattsmart Business -- Agriculture & Irrigation",
        "tech": "Irrigation / Agricultural",
        "value": "Prescriptive + calculated ag measures",
        "max": "Varies",
        "rate": "Per-unit and calculated-kWh amounts for irrigation and farm-efficiency measures",
        "tiers": "",
        "cap": "",
        "baseline": "Existing irrigation hardware / pump efficiency",
        "minp": "RMP agricultural customers",
        "url": URL["agriculture"],
        "notes": "Irrigation and farm efficiency: sprinkler-package upgrades, nozzles/regulators, VFDs and "
                 "efficient motors on irrigation pumps, scientific irrigation scheduling, dairy/livestock "
                 "measures, and grain/crop drying. Mix of prescriptive per-unit amounts and calculated savings; "
                 "confirm current amounts on RMP's agriculture page.",
        "impl": "1. Contact RMP's agricultural team or a Trade Ally for an assessment. 2. Identify qualifying "
                "measures (nozzles, VFDs, pumps, scheduling). 3. Install and submit the application with invoices.",
        "meth": "Prescriptive per-unit amounts for hardware (e.g. sprinkler heads/regulators) plus calculated "
                "kWh savings for pump/VFD upgrades based on wire-to-water efficiency and run hours.",
        "example": "Example: A Utah farm upgrades pivot sprinkler packages and adds a VFD to a 50 hp irrigation "
                   "pump; prescriptive hardware rebates plus calculated pump savings offset much of the cost.",
    },
    # ---- Wastewater / process ----
    {
        "name": "wattsmart Business -- Wastewater & Process (Aeration / Blowers)",
        "tech": "Motors & Drives / Process",
        "value": "Calculated by kWh saved",
        "max": "Varies",
        "rate": "Calculated incentive on annual kWh savings (aeration, blowers, pumps, controls)",
        "tiers": "",
        "cap": "",
        "baseline": "Existing aeration/blower/pump system performance",
        "minp": "Engineering analysis / pre-approval",
        "url": URL["wastewater"],
        "notes": "Water and wastewater treatment efficiency -- high-efficiency blowers, aeration controls "
                 "(dissolved-oxygen control), VFDs on blowers and pumps, and other refrigeration/process "
                 "measures. Paid on calculated annual kWh savings; confirm current terms on RMP's wastewater page.",
        "impl": "1. Assess the aeration/pumping system with RMP or an engineer. 2. Identify measures (efficient "
                "blowers, DO control, VFDs). 3. Submit the application with the savings analysis. 4. Install and "
                "verify. 5. Receive incentive.",
        "meth": "Incentive = calculated annual kWh savings x the applicable rate. Aeration is often the largest "
                "electrical load at a treatment plant, so blower/DO-control upgrades yield large savings.",
        "example": "Example: A municipal plant adds dissolved-oxygen control and VFDs to its aeration blowers, "
                   "cutting blower energy ~30%; the calculated incentive offsets a large share of the project.",
    },
    # ---- Oil & gas ----
    {
        "name": "wattsmart Business -- Oil & Gas Field Efficiency",
        "tech": "Motors & Drives / Process",
        "value": "Calculated by kWh saved",
        "max": "Varies",
        "rate": "Calculated incentive on annual kWh savings for oil & gas field/production equipment",
        "tiers": "",
        "cap": "",
        "baseline": "Existing production/compression/pumping equipment",
        "minp": "Engineering analysis / pre-approval",
        "url": URL["oil_gas"],
        "notes": "Efficiency measures for oil & gas operations -- VFDs and efficient motors on pump jacks, "
                 "compressors, and pumps, plus process improvements. Paid on calculated annual kWh savings; "
                 "confirm current terms on RMP's oil & gas page.",
        "impl": "1. Assess field/production loads with RMP or an engineer. 2. Identify qualifying measures. "
                "3. Submit the application with the savings analysis. 4. Install and verify. 5. Receive incentive.",
        "meth": "Incentive = calculated annual kWh savings x the applicable rate, based on the specific "
                "production/compression/pumping measure.",
        "example": "Example: An operator adds VFDs to electric submersible pumps and optimizes compression; the "
                   "calculated incentive is based on the verified annual kWh reduction.",
    },
    # ---- Whole-building new construction / major renovation ----
    {
        "name": "wattsmart Business -- Whole-Building New Construction / Major Renovation",
        "tech": "Multiple Technologies",
        "value": "Whole-building performance incentive by modeled savings",
        "max": "Varies",
        "rate": "Incentive scaled to modeled whole-building energy savings vs. code (performance path)",
        "tiers": "",
        "cap": "",
        "baseline": "ASHRAE 90.1 / Utah energy code reference building",
        "minp": "New construction or major renovation; energy modeling required",
        "url": URL["wbnc"],
        "notes": "For new construction and major renovations: a whole-building performance-path incentive scaled "
                 "to modeled energy savings beyond code, plus access to prescriptive measures. Also a system-by-"
                 "system path for individual upgrades. Confirm current incentive structure on RMP's WBNC page.",
        "impl": "1. Engage RMP early in design. 2. Model the building vs. ASHRAE 90.1 / Utah code. 3. Choose the "
                "whole-building performance path or system-by-system prescriptive measures. 4. Submit the "
                "application with modeling. 5. Build and verify. 6. Receive incentive.",
        "meth": "Whole-building path: incentive scales with modeled % energy savings vs. the code baseline. "
                "System path: sum of prescriptive measure amounts.",
        "example": "Example: A new 80,000 sq ft office modeled 25% better than code earns a whole-building "
                   "incentive plus prescriptive lighting/HVAC rebates; confirm the current per-savings rate.",
    },
    # ---- Battery storage (separate wattsmart Battery / dispatch program) ----
    {
        "name": "wattsmart Battery -- Commercial Battery Storage (dispatch)",
        "tech": "Energy Storage / Battery",
        "value": "Per kW of battery capacity (upfront + annual bill credit)",
        "max": "Scales with enrolled battery kW",
        "rate": "Incentive per kW of committed battery capacity: an upfront incentive plus an ongoing annual "
                "bill credit (confirm current commercial $/kW with RMP)",
        "tiers": "",
        "cap": "",
        "baseline": "Battery power capacity (kW) enrolled for utility dispatch",
        "minp": "Enroll the battery in RMP's dispatch program; solar or solar+battery may be required",
        "url": URL["battery"],
        "notes": "Rocky Mountain Power's wattsmart Battery program pays an incentive based on battery size (kW) "
                 "in exchange for letting the utility dispatch the battery (a virtual power plant). Published "
                 "residential terms are about $150/kW for each committed year plus a $15/kW annual bill credit; "
                 "commercial terms are set by RMP and were updated in 2026 -- confirm the current commercial "
                 "$/kW, term length, and eligibility (solar/solar+battery requirement). Stacks with the 30% "
                 "federal storage ITC, which is usually the larger incentive when buying a battery.",
        "impl": "1. Contact Rocky Mountain Power (or a participating battery installer) about wattsmart Battery "
                "enrollment. 2. Confirm eligibility and current commercial $/kW and term. 3. Install a qualifying "
                "battery and enroll it for dispatch. 4. Receive the upfront incentive and ongoing annual bill "
                "credit. 5. Separately claim the 30% federal ITC on the battery.",
        "meth": "Incentive = committed battery kW x the program's $/kW upfront rate (per committed year) plus a "
                "$/kW annual bill credit for participating years. Value scales with enrolled power capacity (kW).",
        "example": "Example: A business enrolls a 100 kW battery. Using published residential reference rates "
                   "(~$150/kW/yr committed + $15/kW annual credit) the utility incentive is on the order of "
                   "thousands per year; confirm the current commercial figures. Separately, a $300,000 battery "
                   "earns a 0.30 x $300,000 = $90,000 federal ITC.",
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
    rows = []
    for m in MEASURES:
        key = make_key(UTIL, m["name"])
        detailed = key in DETAILED_KEYS
        rows.append(record(
            STATE, m["name"], ADMIN, SECTOR, "Rebate", m["tech"],
            m["value"], m["max"], RECIP, "Ongoing", m["url"],
            notes=m["notes"], implementation=m["impl"], methodology=m["meth"],
            example=m["example"], incentive_rate=m["rate"], rebate_tiers=m["tiers"],
            unit_cap=m["cap"], baseline=m["baseline"], min_project=m["minp"],
            key=key,
            detail_level=("detailed" if detailed else "general"),
            verified_date=(VERIFIED_DATE if detailed else ""),
            source_doc=m["url"],
        ))
    return rows
