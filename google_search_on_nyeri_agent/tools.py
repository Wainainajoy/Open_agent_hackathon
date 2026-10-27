"""Tools for the Kanuni Mfumo Scout agent.

Kept free of google-adk imports so SAMPLE_MODE can run anywhere.
Every call is logged so judges can see agent -> tool -> Zetaris activity.
"""
import logging
import os
import re
import uuid
from urllib.parse import urlparse

log = logging.getLogger("kanuni.tools")

NYERI_SECTIONS = {
    "home": "https://www.nyeri.go.ke/",
    "budget": "https://www.nyeri.go.ke/budget-2024-2025/",
    "tenders": "https://www.nyeri.go.ke/cgntenders/",
    "reports": "https://www.nyeri.go.ke/reports/",
    "acts": "https://www.nyeri.go.ke/actsnbills/",
}
ALLOWED_HOSTS = {"www.nyeri.go.ke", "nyeri.go.ke"}

SAMPLE_NOTICE = (
    "ILLUSTRATIVE SAMPLE DATA for SAMPLE_MODE. These are NOT official "
    "Nyeri County figures."
)
SAMPLE_COLUMNS = ["department", "financial_year", "allocation_kes_millions", "category"]
SAMPLE_ROWS = [
    ["Health Services", "2024/25", 100, "recurrent"],
    ["Roads and Public Works", "2024/25", 200, "development"],
    ["Agriculture", "2024/25", 150, "development"],
    ["Education", "2024/25", 120, "recurrent"],
]


def sample_mode() -> bool:
    return os.getenv("SAMPLE_MODE", "false").strip().lower() in ("1", "true", "yes")


def query_zetaris(sql: str) -> dict:
    """Run ONE read-only Lightning SQL statement (SELECT, SHOW or DESCRIBE) on the
    Zetaris data layer and return the rows.

    Args:
        sql: a single SQL statement, for example
             SELECT department, allocation_kes_millions FROM nyeri_budget
    """
    statement = (sql or "").strip().rstrip(";").strip()
    if ";" in statement or not re.match(r"^(select|show|describe)\b", statement, re.I):
        log.warning("[zetaris] rejected statement: %s", statement[:120])
        return {"error": "Only one read-only SELECT, SHOW or DESCRIBE statement is allowed."}

    if sample_mode():
        log.info("[zetaris] SAMPLE_MODE=true, returning sample rows for: %s", statement)
        return {"mode": "SAMPLE", "notice": SAMPLE_NOTICE,
                "columns": SAMPLE_COLUMNS, "rows": SAMPLE_ROWS}

    import requests  # imported here so SAMPLE_MODE needs no network libraries

    url = os.environ["ZETARIS_REST_URL"].rstrip("/") + "/sql-editor/sqls/run"
    log.info("[zetaris] LIVE query: %s", statement)
    response = requests.post(
        url,
        headers={
            "Authorization": "Bearer " + os.environ["ZETARIS_API_KEY"],
            "X-Org-ID": os.environ.get("ZETARIS_ORG_ID", "1"),
            "X-Request-ID": str(uuid.uuid4()),
        },
        json={"queryId": str(uuid.uuid4()), "sql": statement,
              "source": "SqlEditor", "limit": 50},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    rows = body.get("data") or []
    log.info("[zetaris] LIVE result: %d rows", len(rows))
    return {"mode": "LIVE", "row_count": len(rows), "rows": rows[:50]}


def read_nyeri_page(section_or_url: str) -> dict:
    """Read text from an official Nyeri County Government web page, for context.

    Args:
        section_or_url: one of home, budget, tenders, reports, acts, or a full
            URL on nyeri.go.ke.
    """
    url = NYERI_SECTIONS.get((section_or_url or "").strip().lower(), section_or_url)
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_HOSTS:
        log.warning("[web] blocked non-Nyeri URL: %s", url)
        return {"error": "Only nyeri.go.ke pages can be read."}

    if sample_mode():
        log.info("[web] SAMPLE_MODE=true, skipping fetch of %s", url)
        return {"mode": "SAMPLE", "url": url,
                "text": "Page fetch skipped in SAMPLE_MODE. Official source: " + url}

    import requests
    from bs4 import BeautifulSoup

    log.info("[web] fetching %s", url)
    response = requests.get(url, timeout=30, headers={"User-Agent": "KanuniMfumoScout/0.1"})
    response.raise_for_status()
    text = BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True)
    return {"mode": "LIVE", "url": url, "text": text[:6000]}
