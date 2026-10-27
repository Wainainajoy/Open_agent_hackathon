from google.adk.agents import Agent
from google.adk.tools import google_search
import os 
import os

def query_zetaris(sql: str) -> str:
    """Query the Zetaris data layer for Nyeri County records."""
    if os.getenv("SAMPLE_MODE") == "true":
        print(f"[LOG] SAMPLE_MODE ON: Mocking Zetaris query: {sql}")
        return "SAMPLE DATA: Nyeri County Budget 2024: 1.2 Billion KES."
    
    print(f"[LOG] Querying Zetaris: {sql}")
    # Your actual Zetaris connection code goes here later
    return "Real Zetaris data would be here."
root_agent = Agent(
    name="google_search_on_nyeri_agent",
    model=os.getenv("METERLESS_MODEL", "meterless/auto"),
    instruction=" Answer questions using Google Search to help local entrepreneurs and citizens of the Nyeri County Goverment in Kenya to quickly navigate complex, lengthy county government websites to find documents and information about specific opportunities or services. Always cite sources.",
    description="""Professional helpful search assistant with Google Search capabilities to help local entrepreneurs and citizens of the Nyeri County Goverment in Kenya to quickly navigate complex, lengthy county government websites to find documents and information about specific opportunities or services.
    Below are all the important links that you can use to get most of the information
    - Here is the link to the Nyeri County Government Website: https://www.nyeri.go.ke/ 
    - Here is the link that contains all the Budgets for Nyeri County: https://www.nyeri.go.ke/budget-2024-2025/
    - Here is the link that contains all the Tenders for Nyeri County: https://www.nyeri.go.ke/cgntenders/ 
    - Here is the link that contains all the County Reports for Nyeri County: https://www.nyeri.go.ke/reports/
    - Here is a link on all the Nyeri Counties Acts and Bills : https://www.nyeri.go.ke/actsnbills/ 
    Use the above links to get most of the information about Nyeri County Government in Kenya.""",
    tools=[google_search, query_zetaris]
)
