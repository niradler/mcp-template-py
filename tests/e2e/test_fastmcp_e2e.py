"""Simple E2E tests for FastMCP server."""

import pytest
from mcp_template.server import create_server


def test_fastmcp_server_creation():
    """Test that the FastMCP server can be created."""
    server = create_server()
    assert server is not None
    assert server.name == "mcp-template"


def test_server_tool_registration():
    """Test that tools are properly registered."""
    server = create_server()
    
    # Check tool handlers are registered
    tool_names = {handler.name for handler in server._tool_handlers.values()}
    expected_tools = {"echo", "calculate", "timestamp", "text_stats", "json_format", "server_status"}
    assert expected_tools.issubset(tool_names)


def test_server_prompt_registration():
    """Test that prompts are properly registered."""
    server = create_server()
    
    # Check prompt handlers are registered
    prompt_names = {handler.name for handler in server._prompt_handlers.values()}
    expected_prompts = {"hello_world", "code_review", "explain_concept", "debug_help"}
    assert expected_prompts.issubset(prompt_names)


def test_server_resource_registration():
    """Test that resources are properly registered."""
    server = create_server()
    
    # Check resource handlers are registered
    resource_templates = {handler.template for handler in server._resource_handlers.values()}
    expected_resources = {"template://info", "template://help", "template://status"}
    assert expected_resources.issubset(resource_templates)


# Note: More comprehensive E2E tests would require setting up actual MCP client connections
# For now, these basic tests ensure the server structure is correct
