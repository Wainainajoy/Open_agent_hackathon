"""Runs the tools in SAMPLE_MODE: no Zetaris, no Nightshift, no internet needed.
Usage:  python sample_demo.py
"""
import logging
import os

os.environ["SAMPLE_MODE"] = "true"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from google_search_on_nyeri_agent.tools import query_zetaris, read_nyeri_page  # noqa: E402

question = "Which department has the largest 2024/25 allocation?"
print("QUESTION:", question)
result = query_zetaris(
    "SELECT department, allocation_kes_millions FROM nyeri_budget "
    "WHERE financial_year = '2024/25'"
)
print(result["notice"])
top = max(result["rows"], key=lambda r: r[2])
print(f"ANSWER (template, no LLM in this script): {top[0]} has the largest sample "
      f"allocation, KES {top[2]} million. Source: Zetaris table nyeri_budget (SAMPLE).")
page = read_nyeri_page("budget")
print("Official source to check:", page["url"])
