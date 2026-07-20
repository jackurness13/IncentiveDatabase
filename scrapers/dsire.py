"""
DSIRE scraper — tries the internal JSON API first, falls back to HTML tables.
DSIRE is the federally-funded authoritative database at dsireusa.org.
"""
import json
from bs4 import BeautifulSoup
from .base import get, record, TODAY

STATES = ["UT", "MT", "ID", "NV"]

STATE_NAMES = {"UT": "Utah", "MT": "Montana", "ID": "Idaho", "NV": "Nevada"}

# Known DSIRE internal API paths (reverse-engineered from browser network tab)
_API_URLS = [
    "https://programs.dsireusa.org/api/programs?state={state}&type=program&active=true",
    "https://programs.dsireusa.org/system/program/data?state={state}&fromSir=0",
]

def fetch(state):
    """Return list of incentive records for a state code."""
    rows = _try_api(state)
    if not rows:
        rows = _try_html(state)
    return rows


def _try_api(state):
    for url_tpl in _API_URLS:
        url = url_tpl.format(state=state)
        try:
            resp = get(url, timeout=12)
            data = resp.json()
            programs = data if isinstance(data, list) else data.get("data", data.get("programs", []))
            if programs:
                return [_parse_api_program(p, state) for p in programs if isinstance(p, dict)]
        except Exception:
            continue
    return []


def _parse_api_program(p, state):
    name = p.get("name") or p.get("programName") or "Unknown Program"
    admin = p.get("implementingOrganization") or p.get("administrator") or "See link"
    sector = _join(p.get("sectors") or p.get("sectorTypes") or [])
    itype = p.get("typeCategory") or p.get("programType") or p.get("type") or "Incentive"
    tech = _join(p.get("technologies") or [])
    value = p.get("amount") or p.get("incentiveValue") or "See program"
    max_b = p.get("maxIncentive") or p.get("maxAmount") or "See program"
    recip = _join(p.get("eligibleRecipients") or [])
    exp = p.get("endDate") or p.get("expirationDate") or "Ongoing"
    pid = p.get("id") or p.get("programId") or ""
    url = f"https://programs.dsireusa.org/system/program/detail/{pid}" if pid else "https://dsireusa.org"
    status = "Active" if p.get("active", True) else "Expired"
    return record(state, name, admin, sector, itype, tech, value, max_b, recip, exp, url, status)


def _try_html(state):
    """Scrape the DSIRE public summary tables page for a state."""
    url = f"https://programs.dsireusa.org/system/program?fromSir=0&state={state}"
    try:
        resp = get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        rows = []
        for row in soup.select("table tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cells) >= 3:
                link = row.find("a")
                href = link["href"] if link and link.get("href") else url
                if not href.startswith("http"):
                    href = "https://programs.dsireusa.org" + href
                rows.append(record(
                    state=state,
                    name=cells[0] or "Unknown",
                    administrator=cells[1] if len(cells) > 1 else "See link",
                    sector=cells[2] if len(cells) > 2 else "",
                    incentive_type=cells[3] if len(cells) > 3 else "Incentive",
                    technology="",
                    value="See program",
                    max_benefit="See program",
                    eligible_recipients="",
                    expiration="Ongoing",
                    url=href,
                ))
        return rows
    except Exception:
        return []


def _join(lst):
    if isinstance(lst, list):
        return ", ".join(str(x.get("name", x) if isinstance(x, dict) else x) for x in lst)
    return str(lst) if lst else ""


# UCREW scope: keep only commercial & industrial (and adjacent non-residential) programs.
_CI_TERMS = (
    "commercial", "industrial", "agricultural", "nonprofit", "non-profit",
    "government", "institutional", "school", "construction", "utility",
    "manufacturing", "business",
)


def _is_ci(sector):
    """True if the program serves commercial/industrial sectors (or sector is unspecified).

    DSIRE often blanks the sector on broad federal incentives that apply to C&I, so
    blank is kept. Residential-only rows (sector names no C&I term) are dropped.
    """
    s = (sector or "").lower()
    if not s.strip():
        return True
    return any(term in s for term in _CI_TERMS)


def fetch_all():
    all_rows = []
    for state in STATES:
        rows = [r for r in fetch(state) if _is_ci(r.get("Sector", ""))]
        print(f"  DSIRE [{state}]: {len(rows)} commercial/industrial programs")
        all_rows.extend(rows)
    return all_rows
