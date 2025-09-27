"""Test fixtures and utilities."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from mcp_template.context import ServerContext


@pytest.fixture
def mock_context():
    """Create a mock server context for testing."""
    context = MagicMock(spec=ServerContext)
    context.get_state = MagicMock(return_value=None)
    context.set_state = MagicMock()
    context.get_cache = MagicMock(return_value=None)
    context.set_cache = MagicMock()
    context.get_config = MagicMock(return_value=None)
    context.get_metrics = MagicMock(return_value={
        "uptime_seconds": 100.0,
        "total_requests": 5,
        "active_requests": 1,
        "cache_size": 2,
        "state_keys": ["session_id", "active_requests"],
    })
    context.increment_request_count = MagicMock()
    context.decrement_active_requests = MagicMock()
    return context


@pytest.fixture
def sample_prompts_data():
    """Sample data for prompt testing."""
    return {
        "hello_world": {
            "args": {"name": "Test User"},
            "expected_content": "Test User"
        },
        "code_review": {
            "args": {
                "code": "def hello():\n    print('Hello World')",
                "language": "python",
                "focus": "style"
            },
            "expected_content": "def hello()"
        },
        "explain_concept": {
            "args": {
                "concept": "recursion",
                "audience": "beginner",
                "include_examples": "true"
            },
            "expected_content": "recursion"
        },
        "debug_help": {
            "args": {
                "error_message": "IndexError: list index out of range",
                "context": "Accessing array elements",
                "language": "python"
            },
            "expected_content": "IndexError"
        }
    }


@pytest.fixture
def sample_tools_data():
    """Sample data for tool testing."""
    return {
        "echo": {
            "args": {"text": "Hello World", "repeat": 2},
            "expected_result": "Hello World"
        },
        "calculate": {
            "args": {"expression": "2 + 2"},
            "expected_result": "4"
        },
        "timestamp": {
            "args": {"format": "iso"},
            "expected_content": "Timestamp (iso):"
        },
        "text_stats": {
            "args": {"text": "Hello world hello", "include_words": True},
            "expected_content": "Text Statistics:"
        },
        "json_format": {
            "args": {"json_data": '{"key": "value"}', "indent": 2},
            "expected_content": "Formatted JSON:"
        },
        "server_status": {
            "args": {"include_cache": True},
            "expected_content": "Server Status:"
        }
    }


@pytest.fixture
def sample_resources_data():
    """Sample data for resource testing."""
    return {
        "template://info": {
            "expected_content": "MCP Template Python",
            "mime_type": "application/json"
        },
        "template://status": {
            "expected_content": "running",
            "mime_type": "application/json"
        },
        "template://config": {
            "expected_content": "server_config",
            "mime_type": "application/json"
        },
        "template://logs/recent": {
            "expected_content": "Total requests processed:",
            "mime_type": "text/plain"
        },
        "template://help": {
            "expected_content": "# MCP Template Help",
            "mime_type": "text/markdown"
        },
        "file://example.txt": {
            "expected_content": "This is an example text file",
            "mime_type": "text/plain"
        }
    }


@pytest.fixture
def invalid_inputs():
    """Invalid inputs for testing error handling."""
    return {
        "prompts": {
            "missing_required": {
                "name": "code_review",
                "args": {}  # Missing required 'code' argument
            },
            "unknown_prompt": {
                "name": "nonexistent_prompt",
                "args": {}
            }
        },
        "tools": {
            "missing_required": {
                "name": "echo",
                "args": {}  # Missing required 'text' argument
            },
            "invalid_expression": {
                "name": "calculate",
                "args": {"expression": "import os; os.system('ls')"}
            },
            "unknown_tool": {
                "name": "nonexistent_tool",
                "args": {}
            }
        },
        "resources": {
            "unknown_resource": "unknown://resource",
            "invalid_uri": "not-a-valid-uri",
            "file_not_found": "file://nonexistent.txt"
        }
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
