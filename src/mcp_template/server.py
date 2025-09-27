"""Core MCP server implementation using FastMCP."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession

from . import prompts, resources, tools
from .helpers.logging import get_logger, setup_file_logging

logger = get_logger(__name__)


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Any]:
    """Manage application lifecycle with startup and shutdown hooks."""
    logger.info("🚀 MCP server starting up...")

    # Initialize any resources here
    # e.g., database connections, cache, etc.
    startup_context = {
        "startup_time": "2024-01-01T12:00:00Z",
        "version": "0.1.0",
        "features_enabled": ["completions", "elicitation", "sampling", "logging", "auth"]
    }

    try:
        yield startup_context
    finally:
        # Cleanup resources here
        logger.info("🛑 MCP server shutting down...")


def create_server() -> FastMCP:
    """Create and configure the MCP server with all features."""
    # Create FastMCP server with lifespan management
    mcp = FastMCP(
        name="mcp-template",
        lifespan=app_lifespan
    )

    # Register all handlers with the mcp instance
    prompts.register_prompts(mcp)
    tools.register_tools(mcp)
    resources.register_resources(mcp)

    logger.info("FastMCP server created successfully with all features")
    return mcp
