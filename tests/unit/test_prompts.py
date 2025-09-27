"""Unit tests for prompts module."""

import pytest
from mcp.server.fastmcp import FastMCP

from mcp_template.prompts import register_prompts


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with prompts registered."""
    mcp = FastMCP("test-server")
    register_prompts(mcp)
    return mcp


@pytest.mark.asyncio
async def test_hello_world_prompt(mcp_server):
    """Test hello world prompt generation."""
    result = await mcp_server.get_prompt("hello_world", {"name": "Alice"})
    assert "Alice" in result.messages[0].content.text
    assert "hello" in result.messages[0].content.text.lower()

    # Test with default
    result = await mcp_server.get_prompt("hello_world", {})
    assert "World" in result.messages[0].content.text


@pytest.mark.asyncio
async def test_code_review_prompt(mcp_server):
    """Test code review prompt generation."""
    code = "def hello():\n    return 'Hello World'"
    result = await mcp_server.get_prompt(
        "code_review", {"code": code, "language": "python", "focus": "style"}
    )

    content = result.messages[0].content.text
    assert "def hello()" in content
    assert "python" in content
    assert "style" in content
