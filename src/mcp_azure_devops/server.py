"""
Azure DevOps MCP Server

A simple MCP server that exposes Azure DevOps capabilities.
"""
import argparse
from mcp.server.fastmcp import FastMCP
from mcp_azure_devops.features import register_all
from dotenv import load_dotenv
load_dotenv()

# Create a FastMCP server instance with a name
mcp = FastMCP("Azure DevOps")

# Register all features
register_all(mcp)

def main():
    """Entry point for the command-line script."""
    parser = argparse.ArgumentParser(description="Run the Azure DevOps MCP server")
    # Add more command-line arguments as needed
    
    args = parser.parse_args()
    
    # Start the server
    mcp.run()

if __name__ == "__main__":
    main()
