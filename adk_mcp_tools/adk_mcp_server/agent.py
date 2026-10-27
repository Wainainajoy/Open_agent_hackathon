import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, \
                    StdioServerParameters, StdioConnectionParams

                    import os
from dotenv import load_dotenv

load_dotenv() # Add this line!

# IMPORTANT: Replace this with the ABSOLUTE path to your adk_server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adk_server.py")

if PATH_TO_YOUR_MCP_SERVER_SCRIPT == "None":
    print("WARNING: PATH_TO_YOUR_MCP_SERVER_SCRIPT is not set. Please update it in agent.py.")
    # Optionally, raise an error if the path is critical

root_agent = LlmAgent(
    model=os.getenv("METERLESS_MODEL", "meterless/auto"),
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    ## Add the MCPToolset below:
    tools=[
    MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3", # Command to run your MCP server script
            args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
        ),
        timeout=30,
        ),
        tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
    )
],

)
