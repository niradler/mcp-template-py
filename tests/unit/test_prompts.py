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


def test_hello_world_prompt(mcp_server):
    """Test hello world prompt generation."""
    # Get the prompt function directly
    prompt_func = None
    for handler in mcp_server._prompt_handlers.values():
        if handler.name == "hello_world":
            prompt_func = handler.handler
            break
    
    assert prompt_func is not None
    
    # Test with name
    result = prompt_func(name="Alice")
    assert "Alice" in result
    assert "hello" in result.lower()
    
    # Test with default
    result = prompt_func()
    assert "World" in result


def test_code_review_prompt(mcp_server):
    """Test code review prompt generation."""
    # Get the prompt function directly
    prompt_func = None
    for handler in mcp_server._prompt_handlers.values():
        if handler.name == "code_review":
            prompt_func = handler.handler
            break
    
    assert prompt_func is not None
    
    code = "def hello():\n    return 'Hello World'"
    result = prompt_func(code=code, language="python", focus="style")
    
    assert "def hello()" in result
    assert "python" in result
    assert "style" in result


def test_explain_concept_prompt(mcp_server):
    """Test explain concept prompt generation."""
    # Get the prompt function directly
    prompt_func = None
    for handler in mcp_server._prompt_handlers.values():
        if handler.name == "explain_concept":
            prompt_func = handler.handler
            break
    
    assert prompt_func is not None
    
    result = prompt_func(concept="recursion", audience="beginner", include_examples="true")
    
    assert "recursion" in result
    assert "beginner" in result
    assert "examples" in result


def test_debug_help_prompt(mcp_server):
    """Test debug help prompt generation."""
    # Get the prompt function directly
    prompt_func = None
    for handler in mcp_server._prompt_handlers.values():
        if handler.name == "debug_help":
            prompt_func = handler.handler
            break
    
    assert prompt_func is not None
    
    result = prompt_func(
        error_message="AttributeError: 'str' object has no attribute 'append'",
        context="Working with lists",
        language="python"
    )
    
    assert "AttributeError" in result
    assert "Working with lists" in result
    assert "python" in result
