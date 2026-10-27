# Kanuni Mfumo Scout: Nyeri County assistant (Open Agent Hackathon 2026, Wildcard track)

Helps citizens and local entrepreneurs in Nyeri County, Kenya, find budgets, tenders, reports
and Acts without digging through long government web pages. It answers from a data layer
first (Zetaris), adds context from official `nyeri.go.ke` pages, and cites its sources.

## Existing before the hackathon vs built during it
- **Before:** an earlier Google ADK project, [The_Kanuni_Mfumo_Scout](https://github.com/Wainainajoy/The_Kanuni_Mfumo_Scout): a Gemini + Google Search agent for Nyeri County pages, a Google Maps agent and a web-page MCP server.
- **Built during the hackathon:** the model now runs through **Meterless Nightshift** (NVIDIA Nemotron); a **Zetaris** `query_zetaris` tool; an official-pages reader restricted to nyeri.go.ke; **SAMPLE_MODE**; tool-call logging; this README.

## Honest status
| Item | Status |
|---|---|
| Nightshift connected to NVIDIA, Nemotron 3.5 Lightning 30B A3B enabled | Verified in Nightshift's Diagnose screen |
| Agent calls the model through Nightshift (`METERLESS_BASE_URL`) | Implemented |
| `query_zetaris` against a live Zetaris install | Implemented using the documented REST call; **no official Nyeri budget data has been loaded into Zetaris** |
| SAMPLE_MODE (no Zetaris, no Nightshift, no internet) | Works: `python sample_demo.py` |
| **Meterless Engine (H-MEM, Markovian, World Model, Scout Intent)** | **Not integrated at submission time.** The Build requirement is not met. |
| Sample figures | Illustrative only, labelled as such in every result. They are not official county numbers. |

The folders `adk_mcp_tools/` come from the earlier project and are not part of the demonstrated flow.

## Run it (SAMPLE_MODE, no accounts needed)
```bash
python -m venv venv
venv\Scripts\activate        # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python sample_demo.py
```
This prints the query sent to the data layer, the sample rows, a labelled answer and the official source link.

## Run the agent with live services
1. Install and start **Meterless Nightshift**. In Setup > Providers add your NVIDIA key (stored by Nightshift, never in this repo) and enable a Nemotron model. In the Console copy the Base URL and API key.
2. Optional: install **Zetaris** locally with Docker (participant guide), create an API key and register a table named `nyeri_budget` (columns `department`, `financial_year`, `allocation_kes_millions`, `category`).
3. `copy .env.example .env`, then fill in the values and set `SAMPLE_MODE=false`.
4. `pip install -r requirements.txt`, then from the repo root run `adk web` and pick `google_search_on_nyeri_agent`.

## Environment variables
| Variable | Meaning |
|---|---|
| `SAMPLE_MODE` | `true` returns labelled sample data and skips network calls |
| `METERLESS_BASE_URL` | Nightshift URL, usually `http://127.0.0.1:8088/v1` |
| `METERLESS_RUNTIME_TOKEN` | Nightshift API key |
| `METERLESS_MODEL` | `meterless/auto` by default; pin a Nemotron lane if you want to be sure Nemotron answers |
| `ZETARIS_REST_URL`, `ZETARIS_ORG_ID`, `ZETARIS_API_KEY` | Zetaris REST settings |
| `ZETARIS_BUDGET_TABLE` | Table name, default `nyeri_budget` |

## Logs and traces
Every call is logged: `agent -> tool ...`, `[zetaris] SAMPLE_MODE ... / LIVE query ...`, `[web] fetching ...`, and `tool ... -> agent`.
The tool only accepts one read-only `SELECT`, `SHOW` or `DESCRIBE` statement and only reads nyeri.go.ke pages.

## Limitations
- No Meterless Engine yet (see status table).
- Answers are only as good as the data loaded into Zetaris and the pages available on nyeri.go.ke.
- `meterless/auto` can route to a non-NVIDIA model unless a Nemotron lane is pinned.
- Not an official county service.
