"""Kanuni Mfumo Scout: Nyeri County assistant.

Model: Meterless Nightshift (OpenAI-compatible) -> NVIDIA Nemotron.
Data:  Zetaris via query_zetaris, plus official nyeri.go.ke pages for context.
"""
import logging
import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .tools import query_zetaris, read_nyeri_page

load_dotenv()
log = logging.getLogger("kanuni.agent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

TABLE = os.getenv("ZETARIS_BUDGET_TABLE", "nyeri_budget")


def _model():
    """Use Nightshift when METERLESS_BASE_URL is set, otherwise a Gemini fallback."""
    base_url = os.getenv("METERLESS_BASE_URL")
    if not base_url:
        return os.getenv("FALLBACK_MODEL", "gemini-2.5-flash")
    from google.adk.models.lite_llm import LiteLlm

    return LiteLlm(
        model="openai/" + os.getenv("METERLESS_MODEL", "meterless/auto"),
        api_base=base_url,
        api_key=os.getenv("METERLESS_RUNTIME_TOKEN", "not-set"),
    )


def _before_tool(tool, args, tool_context):
    log.info("agent -> tool %s args=%s", tool.name, args)


def _after_tool(tool, args, tool_context, tool_response):
    log.info("tool %s -> agent (%s)", tool.name, str(tool_response)[:160])


root_agent = Agent(
    name="kanuni_mfumo_scout",
    model=_model(),
    description="Helps citizens and entrepreneurs find Nyeri County budgets, tenders, reports and Acts.",
    instruction=f"""You help citizens and local entrepreneurs of Nyeri County, Kenya, find budgets,
tenders, reports and Acts, in plain language.
1. For budget questions, call query_zetaris first. The table is {TABLE} with columns
   department, financial_year, allocation_kes_millions, category. Send one SELECT at a time.
2. Use read_nyeri_page (budget, tenders, reports, acts, home) for official context and links.
3. If a tool result says mode SAMPLE, say clearly that the figures are illustrative sample
   data, not official numbers.
4. Never invent figures. If the tools return nothing, say so and point to the official page.
5. Always cite the source: the Zetaris table or the nyeri.go.ke URL.""",
    tools=[query_zetaris, read_nyeri_page],
    before_tool_callback=_before_tool,
    after_tool_callback=_after_tool,
)
