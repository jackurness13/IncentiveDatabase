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
  dominion_ut.py              Dominion Energy / ThermWise Business (UT) [active]
  nv_energy.py                NV Energy PowerShift Business (NV)        [disabled: not in ENABLED_STATES]
  northwestern.py             NorthWestern Energy Business (MT)         [disabled: not in ENABLED_STATES]
  idaho_power.py              Idaho Power C&I + Agricultural (ID)       [disabled: not in ENABLED_STATES]
  avista.py                   Avista Business (ID)                      [disabled: not in ENABLED_STATES]
  dsire.py                    DSIRE federal database (filtered to C&I + ENABLED_STATES)
site/                       Static site published to GitHub Pages (generated, gitignored)
.github/workflows/          Daily build + publish automation
```

Non-Utah scrapers stay in the repo but don't run until their state is added to
`ENABLED_STATES` — enabling more coverage is a one-line change, not a rewrite.

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

## Data accuracy

Incentive programs change often and expiration dates lapse. Programs whose expiration
date has passed are automatically marked **Expired** with a note to verify renewal at
the administrator's website. **Always confirm current terms with the program
administrator before advising a client.**
