from mcp.server.fastmcp import FastMCP
import logging
import os
import sys
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)20s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables
load_dotenv()

# Create MCP server instance
mcp = FastMCP("basic_mcp_for_wherobots")

# Import tools after creating mcp instance to avoid circular import
import tools

# Register the tools with the MCP instance
tools.register_tools(mcp)

if __name__ == "__main__":
    # Run the server
    mcp.run()