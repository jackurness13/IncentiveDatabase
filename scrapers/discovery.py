"""
Breadth discovery: scan utility incentive *index* pages and emit a "general"
stub for any program/category we don't already cover with a curated measure.

This is the automated half of the two-tier model: it keeps the database broad and
self-updating (a newly published category shows up on its own, flagged "values
pending"), while exact rates only ever come from human-verified curated measures.
Coverage is decided by URL: a category page is "covered" if some curated measure
already points its source at that page, so there are no duplicate general+detailed
rows for the same thing.

Generalizes the old rocky_mountain._audit_coverage() check into something that
actually adds the gaps to the list rather than just logging them.
"""
from urllib.parse import urljoin, urldefrag

from bs4 import BeautifulSoup

from . import rocky_mountain as rmp
from .base import get, record, slugify


def fetch_all(states=None):
    states = states or ["UT"]
    rows = []
    if "UT" in states:
        rows += _discover_rmp("UT")
        rows += _discover_dominion("UT")
    print("  Discovery (index scan): " + str(len(rows)) + " new/uncovered program stub(s)")
    return rows


def _norm(url):
    """Normalize a URL for comparison: drop fragment, trailing slash, lowercase."""
    return urldefrag(str(url))[0].rstrip("/").lower()


# Index links are often generic buttons ("See details"); fall back to the slug then.
_GENERIC_LABELS = {"", "see details", "details", "learn more", "more", "view", "apply", "link", "read more"}


def _title_from_slug(slug):
    s = slug[3:] if slug.startswith("ut-") else slug
    s = s.replace("-", " ").strip()
    return s.title() if s else slug


def _stub(state, util, slug, label, url, admin, sector, recip):
    """A 'general' breadth entry: the program exists, exact values pending."""
    label = (label or "").strip()
    base = label if (label.lower() not in _GENERIC_LABELS and len(label) > 3) else _title_from_slug(slug)
    name = base + " (auto-discovered)"
    return record(
        state, name, admin, sector, "See program", "",
        "See program -- exact incentive values pending", "See program",
        recip, "Ongoing", url,
        notes="Auto-discovered from the utility's incentive index. This program is listed "
              "so it isn't missed; its exact incentive values are pending -- provide the "
              "program PDF/data to add verified figures.",
        implementation="See the linked program page to apply, then confirm current terms "
                       "with the program administrator.",
        key=util + ":" + slugify(slug),
        detail_level="general", verified_date="", source_doc=url,
    )


def _discover_rmp(state):
    """Scan RMP's Utah incentive-lists index; stub any category page not already
    covered by a curated measure's source URL."""
    index = rmp.URL["lists"]
    covered = {_norm(m["url"]) for m in rmp.MEASURES}
    covered.add(_norm(index))
    stubs, seen = [], set()
    try:
        soup = BeautifulSoup(get(index, timeout=15).text, "lxml")
    except Exception as exc:
        print("    [DISCOVERY] RMP index fetch failed: " + str(exc))
        return stubs
    for a in soup.find_all("a", href=True):
        href = urljoin(index, a["href"])
        n = _norm(href)
        # Category detail pages live under /ut-incentive-lists/ and end in .html.
        if "/ut-incentive-lists/" not in n or not n.endswith(".html"):
            continue
        if n in covered or n in seen:
            continue
        seen.add(n)
        slug = n.rsplit("/", 1)[-1][:-5]  # strip ".html"
        stubs.append(_stub(state, "rmp", slug, a.get_text(strip=True), href,
                           rmp.ADMIN, rmp.SECTOR, rmp.RECIP))
    if stubs:
        print("    [DISCOVERY] RMP: " + str(len(stubs)) + " uncovered category(ies) added as general: "
              + ", ".join(s["Program Name"] for s in stubs))
    return stubs


def _discover_dominion(state):
    """Placeholder: the Utah gas program (ThermWise) is migrating from Dominion to
    Enbridge Gas and its index structure is in flux, so automated discovery is
    disabled here to avoid emitting noise. Wire up once the index stabilizes -- add
    an index URL + a covered-URL set and reuse the same pattern as _discover_rmp."""
    return []
