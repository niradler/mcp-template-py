"""Unit tests for resources module."""

import pytest
import json
from mcp.server.fastmcp import FastMCP
from mcp_template.resources import register_resources


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with resources registered."""
    mcp = FastMCP("test-server")
    register_resources(mcp)
    return mcp


def test_template_info_resource(mcp_server):
    """Test template info resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "template://info":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func()
    
    # Parse JSON content
    data = json.loads(result)
    assert data["name"] == "MCP Template Python"
    assert data["version"] == "0.1.0"
    assert "features" in data
    assert "capabilities" in data


def test_help_documentation_resource(mcp_server):
    """Test help documentation resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "template://help":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func()
    
    # Check that help content contains expected sections
    assert "# MCP Template Help" in result
    assert "## Available Prompts" in result
    assert "## Available Tools" in result
    assert "## Available Resources" in result


def test_server_status_resource(mcp_server):
    """Test server status resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "template://status":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func()
    
    # Parse JSON content
    data = json.loads(result)
    assert data["status"] == "running"
    assert "timestamp" in data
    assert "metrics" in data


def test_metrics_resource(mcp_server):
    """Test metrics resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "template://metrics":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func()
    
    # Parse JSON content
    data = json.loads(result)
    assert "server" in data
    assert "tools" in data
    assert "resources" in data
    assert "timestamp" in data


def test_example_file_resource(mcp_server):
    """Test example file resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "file://{filename}":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func(filename="example.txt")
    assert "This is an example text file resource" in result


def test_json_file_resource(mcp_server):
    """Test JSON file resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "file://{filename}":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func(filename="data.json")
    
    # Parse JSON content
    data = json.loads(result)
    assert data["message"] == "Example JSON data"
    assert "timestamp" in data


def test_config_file_resource(mcp_server):
    """Test config file resource."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "file://{filename}":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    result = resource_func(filename="config.ini")
    
    assert "[settings]" in result
    assert "[features]" in result
    assert "[mcp]" in result


def test_file_not_found(mcp_server):
    """Test file not found error."""
    # Get the resource function directly
    resource_func = None
    for handler in mcp_server._resource_handlers.values():
        if handler.template == "file://{filename}":
            resource_func = handler.handler
            break
    
    assert resource_func is not None
    
    with pytest.raises(ValueError, match="File not found or not allowed"):
        resource_func(filename="nonexistent.txt")
