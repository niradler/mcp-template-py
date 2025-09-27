"""Unit tests for server creation."""

import pytest

from mcp_template.server import create_server


def test_server_creation():
    """Test that server can be created successfully."""
    server = create_server()

    # Check that it's a FastMCP server with expected attributes
    assert hasattr(server, "run")
    assert hasattr(server, "name")
    assert server.name == "mcp-server"


@pytest.mark.asyncio
async def test_server_has_tools():
    """Test that server has tools registered."""
    server = create_server()

    # Check that tools are available
    tools = await server.list_tools()
    assert len(tools) > 0

    tool_names = {tool.name for tool in tools}
    expected_tools = {"echo", "advanced_calculator"}

    assert expected_tools.issubset(tool_names)


@pytest.mark.asyncio
async def test_server_has_prompts():
    """Test that server has prompts registered."""
    server = create_server()

    # Check that prompts are available
    prompts = await server.list_prompts()
    assert len(prompts) > 0

    prompt_names = {prompt.name for prompt in prompts}
    expected_prompts = {"hello_world", "code_review"}

    assert expected_prompts.issubset(prompt_names)


@pytest.mark.asyncio
async def test_server_has_resources():
    """Test that server has resources registered."""
    server = create_server()

    # Check that resources are available
    resources = await server.list_resources()
    assert len(resources) > 0

    resource_uris = {str(resource.uri) for resource in resources}
    expected_resources = {"server://info", "server://status"}

    assert expected_resources.issubset(resource_uris)
