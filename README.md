# UCREW — Commercial & Industrial Energy Efficiency Incentives

A self-updating database of **commercial & industrial (C&I)** energy efficiency
incentives, published as a public website for UCREW students and staff.

**Currently scoped to Utah** — the goal is to perfect one state first, then grow.
The scanner supports Utah, Montana, Idaho, and Nevada; coverage is controlled by a
single `ENABLED_STATES` list in [`fetch_incentives.py`](fetch_incentives.py). Add a
state code there (e.g. `["UT", "ID"]`) and the scrapers, the kept records, and every
site/Excel label update automatically.

**Live site:** https://jackurness13.github.io/IncentiveDatabase/

The scanner collects utility and program incentives, records the actual numbers used
in savings calculations (rebate rates, tiers, baselines, minimum project sizes), and
publishes a searchable, sortable web page with an **AR Finder** that maps an assessment
recommendation (e.g. "Install VFD on compressors") to the incentives that apply. It
refreshes **automatically every day** — no one has to run anything.

> Scope note: residential, multifamily, and new-home/builder programs are intentionally
> excluded. This tool is for **commercial, industrial, and agricultural** facilities.

---

## What you get

- **Web viewer** (`site/index.html`) — searchable, filterable, sortable table with a
  detail popup for each program. Each popup leads with a **Calculation Values** panel
  (incentive rate, rebate tiers, per-unit/project cap, baseline assumption, minimum
  project size) so the numbers behind the math are easy to find.
- **Excel workbook** (`incentives.xlsx`) — one sheet per state plus a **Details** sheet
  with the structured calculation values and long-form methodology/examples.
- **SQLite database** (`incentives.db`) — every field, queryable.
- A **"Last scanned" badge** and **download links** on the page so students always know
  the data is current and can grab an offline copy.

## How it works

```
fetch_incentives.py         Orchestrator: ENABLED_STATES scope, runs the in-scope
                            scrapers, dedupes, auto-expires, writes db/xlsx/html, stages site/
scrapers/                   One module per data source (each returns C&I programs only)
  base.py                     record() row factory + shared HTTP helper
  rocky_mountain.py           Rocky Mountain Power / PacifiCorp (UT)   [active]
                              -- all 11 wattsmart Business categories + wattsmart Battery,
                                 with a daily coverage self-audit (see below)
  dominion_ut.py              Dominion Energy / ThermWise Business (UT) [active]
  federal.py                  Federal C&I incentives -- ITC (battery/solar 30%),
                              MACRS, 179D, USDA REAP  [active, all states]
  discovery.py                Breadth discovery: scans utility index pages, adds any
                              uncovered program/category as a 'general' stub [active]
  nv_energy.py                NV Energy PowerShift Business (NV)        [disabled: not in ENABLED_STATES]
  northwestern.py             NorthWestern Energy Business (MT)         [disabled: not in ENABLED_STATES]
  idaho_power.py              Idaho Power C&I + Agricultural (ID)       [disabled: not in ENABLED_STATES]
  avista.py                   Avista Business (ID)                      [disabled: not in ENABLED_STATES]
  dsire.py                    DSIRE lookup [inactive: API now returns 403 and pages are
                              JS-rendered; federal.py carries the key federal incentives instead]
data/scan_state.json        Per-program source fingerprints (change detection); committed
data/needs_data.md          Auto-generated worklist of programs needing exact data; committed
site/                       Static site published to GitHub Pages (generated, gitignored)
.github/workflows/          Daily build + publish automation
```

Non-Utah scrapers stay in the repo but don't run until their state is added to
`ENABLED_STATES` — enabling more coverage is a one-line change, not a rewrite.

## Two-tier data model: broad by default, exact when verified

Because exact incentive amounts live in changing PDFs (see "Accuracy" below), every
program carries a **tier**:

- **`detailed`** — a human verified the exact values from the source; shown with a green
  **"✓ verified {date}"** badge and its Calculation Values panel populated.
- **`general`** — the program exists and is described broadly, but its exact per-unit
  values are **pending**; shown with an amber **"general · values pending"** badge.
- A `detailed` entry whose source document later changes flips to a red
  **"⚠ source changed · re-verify"** badge and its (now possibly stale) numbers are
  withheld until re-verified.

How each piece stays automatic:

- **Discovery keeps it broad.** `scrapers/discovery.py` scans each utility's live index
  and adds any program/category we don't already cover as a `general` stub — so new
  programs appear on their own, flagged for data. (Coverage is decided by URL, so there
  are never duplicate general + detailed rows for the same thing.)
- **Change detection keeps it honest.** Each run fingerprints every `detailed` entry's
  source document via a cheap HTTP `HEAD` (Content-Length; never downloads or parses the
  file) and compares it to the fingerprint captured when the values were verified. A
  mismatch flags the entry **and stays flagged every run** until a human re-verifies.
  State lives in `data/scan_state.json`, committed each run so `git log` is an audit trail
  of what changed when.
- **The worklist tells you what to do.** `data/needs_data.md` is regenerated every run
  listing all `general` + `changed` programs with their source links — your queue of what
  to curate next.

### Promoting a program (general → detailed)

1. Open the program's source PDF/page (linked in `data/needs_data.md`).
2. Paste it (or the key values) to Claude and ask it to draft the curated measure — exact
   `incentive_rate`, `rebate_tiers`, `unit_cap`, `baseline`, plus a `verified_date` and
   `source_doc`.
3. **Review the numbers** (a human always confirms the figures), then add/replace the
   measure in the relevant scraper's `MEASURES` list and add its key to that scraper's
   `DETAILED_KEYS`.
4. Commit. The next build shows it as **verified**, drops it from `needs_data.md`, and
   discovery stops stubbing that category.

To signal a **re-verification** after a "source changed" flag, bump the measure's
`verified_date` — the change detector re-baselines the fingerprint and clears the flag.

**Why some rates are "general / pending":** utilities publish exact per-unit amounts in
PDFs (not machine-readable HTML), and DSIRE — the would-be automated catch-all — now
blocks scraping. So exact rates are curated from the published lists (each measure links
to its authoritative page), while the scanner automatically keeps the list broad,
live-checks the pages, auto-expires lapsed programs, and flags changed sources.

Each scraper tries to read the live utility page and falls back to a curated set of
known programs (with full methodology and worked examples) if the page can't be parsed.

## Automatic daily refresh

`.github/workflows/update-incentives.yml` runs the scanner and republishes the site:

- **Daily** at 13:00 UTC (~6–7am Mountain) via cron.
- **On demand** — Actions tab → *Update incentives & publish site* → **Run workflow**.
- **On push** to `main` (so code changes rebuild immediately).

The workflow builds `site/` and deploys it straight to GitHub Pages (nothing is
committed back to the repo).

## Run it locally

Requires Python 3.12+.

```bash
pip install -r requirements.txt
python fetch_incentives.py
```

This regenerates `incentives.db`, `incentives.xlsx`, `incentives.html`, and `site/`.
To preview the site the way students see it:

```bash
python -m http.server 8000 --directory site
# then open http://localhost:8000/
```

(Opening `incentives.html` directly by double-clicking also works for a quick look.)

## Adding or editing programs

Program data lives in each scraper's fallback list. To add/adjust a program, edit the
relevant `scrapers/*.py` file and pass values through `record()`
([`scrapers/base.py`](scrapers/base.py)), including the structured calculation fields:

| Field             | Example                                        |
| ----------------- | ---------------------------------------------- |
| `incentive_rate`  | `"$0.10/kWh first-year savings"`               |
| `rebate_tiers`    | `"$300 (tier 1); $600 (tier 2); $900 (tier 3)"`|
| `unit_cap`        | `"$900/unit"`                                  |
| `baseline`        | `"ASHRAE 90.1 standard-efficiency HVAC"`       |
| `min_project`     | `"50,000 kWh/yr savings"`                      |

Blank structured fields are hidden gracefully in the UI. Push to `main` and the site
rebuilds automatically.

## One-time setup (already done for this repo)

1. Repo is **Public** (required for free GitHub Pages).
2. **Settings → Pages → Source: GitHub Actions** (the workflow also enables this
   automatically on first run).

## Accuracy: break measures apart, price them exactly

To keep the incentive **value** accurate, programs are broken out to the granularity
the utility actually publishes instead of one broad "custom" bucket. For example,
Rocky Mountain Power's Utah wattsmart Business program is split into specific measures
— *VFD Air Compressor (≤75 hp)* carries its exact published rate, **$0.15/kWh of annual
energy savings**, and links to RMP's compressed-air incentive page — rather than a
generic `$0.08–0.12/kWh` custom range. Searching an AR like "install VFD on compressor"
now surfaces that exact measure first.

How this stays maintainable and self-updating:

- **Granular measures live in the scrapers** (e.g. [`scrapers/rocky_mountain.py`](scrapers/rocky_mountain.py)),
  each with its precise `incentive_rate` and a link to the authoritative utility page.
- **The AR Finder ranks specific prescriptive measures above custom/whole-facility
  programs**, so the most accurate value leads; custom programs still appear as
  "also applies."
- **The daily scanner keeps running** — it live-checks the source pages and auto-expires
  lapsed programs. Utilities publish per-unit rates in PDFs (not machine-readable HTML),
  so exact amounts are curated from those published lists; when a utility revises a rate,
  update the matching entry and push.
- **To add or refine a measure:** edit the `MEASURES` list in the relevant scraper (name
  it specifically, e.g. "VFD Air Compressor (≤75 hp)", set `incentive_rate`, and point
  `url` at the utility's category page). Push to `main` and the site rebuilds.

Incentive programs change often and expiration dates lapse. Programs whose expiration
date has passed are automatically marked **Expired** with a note to verify renewal at
the administrator's website. **Always confirm current terms with the program
administrator before advising a client.**
