"""Unit tests for tools module."""

import pytest
from mcp.server.fastmcp import FastMCP
from mcp_template.tools import register_tools


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with tools registered."""
    mcp = FastMCP("test-server")
    register_tools(mcp)
    return mcp


def test_echo_tool(mcp_server):
    """Test echo tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "echo":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(text="Hello World")
    assert "Echo: Hello World" in result


def test_echo_tool_with_repeat(mcp_server):
    """Test echo tool with repeat."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "echo":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(text="Test", repeat=3)
    assert result.count("Test") == 3


def test_calculate_tool(mcp_server):
    """Test calculate tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "calculate":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(expression="2 + 2")
    assert "Result: 4" in result


def test_calculate_tool_complex(mcp_server):
    """Test calculate tool with complex expression."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "calculate":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(expression="(10 + 5) * 2 - 3")
    assert "Result: 27" in result


def test_calculate_tool_invalid_expression(mcp_server):
    """Test calculate tool with invalid expression."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "calculate":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(expression="import os")
    assert "Error:" in result


def test_timestamp_tool(mcp_server):
    """Test timestamp tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "timestamp":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(format="iso")
    assert "Timestamp (iso):" in result


def test_timestamp_tool_unix(mcp_server):
    """Test timestamp tool with unix format."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "timestamp":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(format="unix")
    assert "Timestamp (unix):" in result


def test_text_stats_tool(mcp_server):
    """Test text stats tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "text_stats":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    text = "Hello world. This is a test text with multiple sentences."
    result = tool_func(text=text)
    
    assert "Text Statistics:" in result
    assert "Characters:" in result
    assert "Words:" in result


def test_text_stats_tool_with_words(mcp_server):
    """Test text stats tool with word frequency."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "text_stats":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    text = "hello world hello test hello"
    result = tool_func(text=text, include_words=True)
    
    assert "Top 10 most frequent words:" in result
    assert "hello: 3" in result


def test_json_format_tool(mcp_server):
    """Test JSON format tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "json_format":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    json_data = '{"name":"test","value":123,"nested":{"key":"value"}}'
    result = tool_func(json_data=json_data)
    
    assert "Formatted JSON:" in result
    assert "JSON is valid ✓" in result
    assert "```json" in result


def test_json_format_tool_invalid(mcp_server):
    """Test JSON format tool with invalid JSON."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "json_format":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func(json_data="invalid json{")
    assert "Error: Invalid JSON" in result


def test_server_status_tool(mcp_server):
    """Test server status tool."""
    # Get the tool function directly
    tool_func = None
    for handler in mcp_server._tool_handlers.values():
        if handler.name == "server_status":
            tool_func = handler.handler
            break
    
    assert tool_func is not None
    
    result = tool_func()
    
    assert "Server Status:" in result
    assert "Total requests:" in result
