"""Unit tests for tools module."""

import asyncio

import pytest
from mcp.server.fastmcp import FastMCP

from mcp_template.tools import register_tools


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with tools registered."""
    mcp = FastMCP("test-server")
    register_tools(mcp)
    return mcp


@pytest.mark.asyncio
async def test_echo_tool(mcp_server):
    """Test echo tool."""
    result = await mcp_server.call_tool("echo", {"text": "Hello World"})
    # Result is a tuple: (content_list, metadata)
    content = result[0][0].text
    assert "Hello World" in content


@pytest.mark.asyncio
async def test_echo_tool_with_repeat(mcp_server):
    """Test echo tool with repeat."""
    result = await mcp_server.call_tool("echo", {"text": "Test", "repeat": 3})
    # Result is a tuple: (content_list, metadata)
    content = result[0][0].text
    assert content.count("Test") == 3


@pytest.mark.asyncio
async def test_advanced_calculator_tool(mcp_server):
    """Test advanced calculator tool."""
    result = await mcp_server.call_tool("advanced_calculator", {"expression": "2 + 2"})
    # Result is a tuple: (content_list, metadata)
    content = result[0][0].text
    assert "Result: 4" in content


@pytest.mark.asyncio
async def test_advanced_calculator_tool_complex(mcp_server):
    """Test advanced calculator tool with complex expression."""
    result = await mcp_server.call_tool("advanced_calculator", {"expression": "(10 + 5) * 2 - 3"})
    # Result is a tuple: (content_list, metadata)
    content = result[0][0].text
    assert "Result: 27" in content


@pytest.mark.asyncio
async def test_advanced_calculator_tool_invalid_expression(mcp_server):
    """Test advanced calculator tool with invalid expression."""
    result = await mcp_server.call_tool("advanced_calculator", {"expression": "import os"})
    # Result is a tuple: (content_list, metadata)
    content = result[0][0].text
    assert "Error:" in content
