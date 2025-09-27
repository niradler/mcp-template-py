"""Unit tests for server creation."""

import pytest
from mcp_template.server import create_server


def test_server_creation():
    """Test that server can be created successfully."""
    server = create_server()
    
    # Check that it's a FastMCP server
    assert hasattr(server, '_tool_handlers')
    assert hasattr(server, '_prompt_handlers')
    assert hasattr(server, '_resource_handlers')
    
    # Check that handlers are registered
    assert len(server._tool_handlers) > 0
    assert len(server._prompt_handlers) > 0
    assert len(server._resource_handlers) > 0


def test_server_has_expected_tools():
    """Test that server has the expected tools registered."""
    server = create_server()
    
    tool_names = {handler.name for handler in server._tool_handlers.values()}
    expected_tools = {"echo", "calculate", "timestamp", "text_stats", "json_format", "server_status"}
    
    assert expected_tools.issubset(tool_names)


def test_server_has_expected_prompts():
    """Test that server has the expected prompts registered."""
    server = create_server()
    
    prompt_names = {handler.name for handler in server._prompt_handlers.values()}
    expected_prompts = {"hello_world", "code_review", "explain_concept", "debug_help"}
    
    assert expected_prompts.issubset(prompt_names)


def test_server_has_expected_resources():
    """Test that server has the expected resources registered."""
    server = create_server()
    
    resource_templates = {handler.template for handler in server._resource_handlers.values()}
    expected_resources = {"template://info", "template://help", "template://status", "template://metrics", "file://{filename}"}
    
    assert expected_resources.issubset(resource_templates)
