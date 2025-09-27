"""
Resources implementation for MCP template.

This is where you define your resources. Users mainly need to modify this file.
"""

import json
from datetime import datetime
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from .helpers.logging import get_logger

logger = get_logger(__name__)


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the FastMCP server."""

    @mcp.resource("template://info")
    def get_template_info() -> str:
        """Get basic information about this MCP template."""
        info = {
            "name": "MCP Template Python",
            "version": "0.1.0",
            "description": "A comprehensive MCP server template with all features",
            "author": "MCP Template",
            "license": "MIT",
            "created": datetime.now().isoformat(),
            "features": [
                "Prompts support",
                "Tools execution",
                "Resources access",
                "FastMCP framework",
                "Comprehensive testing",
                "Helper utilities",
            ],
            "capabilities": {
                "prompts": True,
                "tools": True,
                "resources": True,
                "logging": True,
            }
        }
        return json.dumps(info, indent=2)

    @mcp.resource("template://help")
    def get_help_documentation() -> str:
        """Get help documentation for this MCP server."""
        return """# MCP Template Help

This is a comprehensive MCP server template that provides examples of all MCP features.

## Available Prompts

- **hello_world**: A simple greeting prompt
- **code_review**: Generate code review prompts
- **explain_concept**: Create concept explanation prompts
- **debug_help**: Generate debugging assistance prompts
- **write_documentation**: Create documentation writing prompts

## Available Tools

- **echo**: Echo back text with optional repetition
- **calculate**: Perform basic mathematical calculations
- **timestamp**: Get current timestamp in various formats
- **text_stats**: Analyze text and provide statistics
- **json_format**: Format and validate JSON data
- **server_status**: Get server status and metrics

## Available Resources

- **template://info**: Basic template information
- **template://help**: This help documentation
- **template://status**: Server status and metrics
- **file://example.txt**: Example file resource

## Usage Examples

### Using Prompts
```
Get prompt "hello_world" with arguments {"name": "Alice"}
```

### Using Tools
```
Call tool "calculate" with {"expression": "2 + 2"}
Call tool "echo" with {"text": "Hello", "repeat": 3}
```

### Using Resources
```
Read resource "template://info"
Read resource "template://help"
```

## Development

To add your own features:

1. **Prompts**: Edit `src/mcp_template/prompts.py`
2. **Tools**: Edit `src/mcp_template/tools.py`  
3. **Resources**: Edit `src/mcp_template/resources.py`

See the implementation files for detailed examples and patterns.

## FastMCP Framework

This template uses the FastMCP framework which provides:
- Simple decorator-based API
- Automatic type validation
- Built-in error handling
- Easy development and testing
"""

    @mcp.resource("template://status")
    def get_server_status() -> str:
        """Get current server status and metrics."""
        # Access the global context from tools module
        from .tools import _server_context

        status = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_requests": _server_context["request_count"],
                "calculations_stored": len(_server_context["calculations"]),
                "last_echo": _server_context["last_echo"],
            },
            "server_info": {
                "framework": "FastMCP",
                "transport": "stdio",
                "version": "0.1.0",
            }
        }

        return json.dumps(status, indent=2)

    @mcp.resource("file://{filename}")
    def get_file(filename: str) -> str:
        """Serve example files."""
        # For security, only allow certain files
        allowed_files = {
            "example.txt": "This is an example text file resource.\n\nIt demonstrates how to serve file-based resources through MCP.\n\nYou can extend this to serve any type of file content.",
            "data.json": json.dumps({
                "message": "Example JSON data",
                "timestamp": datetime.now().isoformat(),
                "numbers": [1, 2, 3, 4, 5],
                "nested": {"key": "value", "active": True}
            }, indent=2),
            "config.ini": """[settings]
debug=true
max_connections=100
timeout=30

[features]
enable_cache=true
enable_logging=true
enable_metrics=true

[mcp]
transport=stdio
server_name=mcp-template
""",
        }

        if filename in allowed_files:
            return allowed_files[filename]
        else:
            raise ValueError(f"File not found or not allowed: {filename}")

    @mcp.resource("template://metrics")
    def get_metrics() -> str:
        """Get detailed server metrics."""
        from .tools import _server_context

        metrics = {
            "server": {
                "uptime": "Available in production deployment",
                "requests_processed": _server_context["request_count"],
                "framework": "FastMCP",
                "python_version": "3.10+",
            },
            "tools": {
                "total_calculations": len(_server_context["calculations"]),
                "last_calculation": _server_context["calculations"][-1] if _server_context["calculations"] else None,
                "echo_history": {"last_echo": _server_context["last_echo"]},
            },
            "resources": {
                "available_resources": [
                    "template://info",
                    "template://help",
                    "template://status",
                    "template://metrics",
                    "file://example.txt",
                    "file://data.json",
                    "file://config.ini",
                ],
                "dynamic_resources": ["file://{filename}"],
            },
            "timestamp": datetime.now().isoformat(),
        }

        return json.dumps(metrics, indent=2)


# Example of how to add your own resource:
"""
To add a new resource, just add a function with the @mcp.resource() decorator:

@mcp.resource("my://resource")
def get_my_resource() -> str:
    '''Description of what this resource provides.'''
    # Your resource logic here
    data = {"message": "Hello from my resource"}
    return json.dumps(data)

# For dynamic resources with parameters:
@mcp.resource("my://users/{user_id}")
def get_user(user_id: str) -> str:
    '''Get user information by ID.'''
    # Your logic here
    return f"User data for {user_id}"

The function signature automatically defines the resource parameters.
The docstring becomes the resource's description.
"""
