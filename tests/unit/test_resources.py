"""Unit tests for resources module."""

import json

import pytest
from mcp.server.fastmcp import FastMCP

from mcp_template.resources import register_resources


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with resources registered."""
    mcp = FastMCP("test-server")
    register_resources(mcp)
    return mcp


@pytest.mark.asyncio
async def test_server_info_resource(mcp_server):
    """Test server info resource."""
    result = await mcp_server.read_resource("server://info")
    # The result is a list of content items
    data = json.loads(result[0].content)

    assert "name" in data
    assert "version" in data
    assert "description" in data
    assert data["name"] == "MCP Server"


@pytest.mark.asyncio
async def test_server_status_resource(mcp_server):
    """Test server status resource."""
    result = await mcp_server.read_resource("server://status")
    # The result is a list of content items
    data = json.loads(result[0].content)

    assert "status" in data
    assert "timestamp" in data
    assert "metrics" in data
    assert data["status"] == "running"
