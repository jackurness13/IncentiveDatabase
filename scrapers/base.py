"""Shared utilities for all scrapers."""
import requests
from datetime import date

TODAY = date.today().isoformat()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}

def get(url, timeout=15, **kwargs):
    resp = requests.get(url, headers=HEADERS, timeout=timeout, **kwargs)
    resp.raise_for_status()
    return resp

def record(
    state, name, administrator, sector, incentive_type,
    technology, value, max_benefit, eligible_recipients,
    expiration, url, status="Active", notes="",
    implementation="", methodology="", example="",
    incentive_rate="", rebate_tiers="", unit_cap="", baseline="", min_project=""
):
    return {
        "State": state,
        "Program Name": name,
        "Administrator": administrator,
        "Sector": sector,
        "Incentive Type": incentive_type,
        "Technology": technology,
        "Incentive Value": value,
        "Max Benefit": max_benefit,
        "Eligible Recipients": eligible_recipients,
        "Expiration Date": expiration,
        "Application URL": url,
        "Last Scraped": TODAY,
        "Status": status,
        "Notes": notes,
        # Detail page fields (not shown in Excel summary columns)
        "_implementation": implementation,
        "_methodology": methodology,
        "_example": example,
        # Structured calculation values (surfaced in the "Calculation Values" panel).
        # All optional -- blank values are hidden gracefully in the UI.
        "_incentive_rate": incentive_rate,   # e.g. "$0.10/kWh first-year savings"
        "_rebate_tiers": rebate_tiers,       # e.g. "$300 (tier 1); $600 (tier 2)"
        "_unit_cap": unit_cap,               # e.g. "$900/unit" or "$14,000/household"
        "_baseline": baseline,               # e.g. "ASHRAE 90.1 standard-efficiency HVAC"
        "_min_project": min_project,         # e.g. "50,000 kWh/yr savings"
    }
