"""
Resources implementation for MCP server.

This is where you define your resources. Users mainly need to modify this file.
"""

import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from .helpers import logger
from .tools import _server_state


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the FastMCP server."""

    @mcp.resource("server://info")
    def get_server_info() -> str:
        """Get basic information about this MCP server."""
        info = {
            "name": "MCP Server",
            "version": "0.1.0",
            "description": "A simple MCP server template",
            "created": datetime.now().isoformat(),
            "features": [
                "Prompts support",
                "Tools execution",
                "Resources access",
                "FastMCP framework",
            ],
        }
        return json.dumps(info, indent=2)

    @mcp.resource("server://status")
    def get_server_status() -> str:
        """Get current server status and metrics."""
        # Access the global state from tools module

        status = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_requests": _server_state["request_count"],
                "calculations_stored": len(_server_state["calculations"]),
            },
        }

        return json.dumps(status, indent=2)
