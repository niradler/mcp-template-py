"""Test fixtures and utilities."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_server_state():
    """Create a mock server state for testing."""
    return {
        "request_count": 0,
        "calculations": [],
    }


@pytest.fixture
def sample_prompts_data():
    """Sample data for prompt testing."""
    return {
        "hello_world": {"args": {"name": "Test User"}, "expected_content": "Test User"},
        "code_review": {
            "args": {
                "code": "def hello():\n    print('Hello World')",
                "language": "python",
                "focus": "style",
            },
            "expected_content": "def hello()",
        },
    }


@pytest.fixture
def sample_tools_data():
    """Sample data for tool testing."""
    return {
        "echo": {"args": {"text": "Hello World", "repeat": 2}, "expected_result": "Hello World"},
        "advanced_calculator": {"args": {"expression": "2 + 2"}, "expected_result": "4"},
    }


@pytest.fixture
def sample_resources_data():
    """Sample data for resource testing."""
    return {
        "server://info": {
            "expected_content": "MCP Server",
            "mime_type": "application/json",
        },
        "server://status": {"expected_content": "running", "mime_type": "application/json"},
    }


@pytest.fixture
def invalid_inputs():
    """Invalid inputs for testing error handling."""
    return {
        "prompts": {
            "missing_required": {
                "name": "code_review",
                "args": {},  # Missing required 'code' argument
            },
            "unknown_prompt": {"name": "nonexistent_prompt", "args": {}},
        },
        "tools": {
            "missing_required": {"name": "echo", "args": {}},  # Missing required 'text' argument
            "invalid_expression": {
                "name": "advanced_calculator",
                "args": {"expression": "import os; os.system('ls')"},
            },
            "unknown_tool": {"name": "nonexistent_tool", "args": {}},
        },
        "resources": {
            "unknown_resource": "unknown://resource",
            "invalid_uri": "not-a-valid-uri",
        },
    }


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    logger = MagicMock()
    logger.debug = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    return logger


class AsyncContextManager:
    """Helper for testing async context managers."""

    def __init__(self, return_value=None):
        self.return_value = return_value

    async def __aenter__(self):
        return self.return_value

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


@pytest.fixture
def async_context_manager():
    """Factory for creating async context managers."""
    return AsyncContextManager


def async_mock(*args, **kwargs):
    """Create an async mock function."""
    m = MagicMock(*args, **kwargs)

    async def async_func(*args, **kwargs):
        return m(*args, **kwargs)

    async_func.mock = m
    return async_func


@pytest.fixture
def create_async_mock():
    """Factory for creating async mocks."""
    return async_mock
