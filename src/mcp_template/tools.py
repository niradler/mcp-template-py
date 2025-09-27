"""
Tools implementation for MCP server.

This is where you define your tools. Users mainly need to modify this file.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from .helpers import logger, safe_int, sanitize_string

# Global context for storing server state
_server_state = {
    "request_count": 0,
    "calculations": [],
}


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the FastMCP server."""

    @mcp.tool()
    async def echo(text: str, repeat: int = 1, ctx: Context[ServerSession, Any] = None) -> str:
        """Echo back the input text, optionally repeated.

        This demonstrates basic tool functionality with input validation and logging.
        """
        # Validate and sanitize inputs
        text = sanitize_string(text, max_length=1000)
        repeat = safe_int(repeat, default=1, min_val=1, max_val=10)

        # Update state
        _server_state["request_count"] += 1

        # Use singleton logger (handles initialization and errors internally)
        await logger.info(f"Echo called with text='{text[:50]}...', repeat={repeat}", component="echo", ctx=ctx)
        await logger.debug(f"Generated {repeat} repetitions", component="echo", ctx=ctx)

        # Generate result
        result = "\n".join([text] * repeat)
        return result

    @mcp.tool()
    async def advanced_calculator(
        expression: str,
        show_steps: bool = False,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Advanced calculator with progress tracking and structured logging.

        This demonstrates advanced MCP features like progress tracking, 
        structured logging with extra data, and error handling.
        """
        # Validate input first
        expression = sanitize_string(expression, max_length=100)

        # Log with structured data using singleton logger
        await logger.info(
            "Starting calculation",
            component="calculator",
            extra={
                "expression": expression,
                "show_steps": show_steps,
                "request_id": _server_state["request_count"]
            },
            ctx=ctx
        )

        try:
            # Show progress for demonstration (with fallback for tests)
            if ctx:
                try:
                    await ctx.info("Validating expression...")
                    await asyncio.sleep(0.1)  # Simulate work
                except ValueError:
                    # Context not available in tests - continue
                    pass

            # Safe evaluation of mathematical expressions
            allowed_chars = set("0123456789+-*/().,eE ")
            if not all(c in allowed_chars for c in expression):
                await logger.error(
                    "Invalid characters in expression",
                    component="calculator",
                    extra={"invalid_chars": [
                        c for c in expression if c not in allowed_chars]},
                    ctx=ctx
                )
                return "Error: Expression contains invalid characters"

            if ctx:
                try:
                    await ctx.info("Calculating result...")
                    await asyncio.sleep(0.1)  # Simulate work
                except ValueError:
                    # Context not available in tests - continue
                    pass

            # Use eval with limited builtins for safety
            safe_dict = {"__builtins__": {}}
            result = eval(expression, safe_dict, {})

            # Store calculation with timestamp
            calculation = {
                "expression": expression,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "request_id": _server_state["request_count"]
            }
            _server_state["calculations"].append(calculation)

            # Keep only last 10 calculations
            if len(_server_state["calculations"]) > 10:
                _server_state["calculations"] = _server_state["calculations"][-10:]

            _server_state["request_count"] += 1

            # Log success with structured data using singleton logger
            await logger.info(
                "Calculation completed successfully",
                component="calculator",
                extra={
                    "expression": expression,
                    "result": result,
                    "calculation_time": "simulated"
                },
                ctx=ctx
            )

            if show_steps:
                return json.dumps({
                    "expression": expression,
                    "result": result,
                    "steps": [
                        "1. Validated input characters",
                        "2. Parsed mathematical expression",
                        "3. Evaluated safely",
                        "4. Stored result"
                    ],
                    "timestamp": calculation["timestamp"]
                }, indent=2)
            else:
                return f"Result: {result}"

        except Exception as e:
            await logger.error(
                "Calculation failed",
                component="calculator",
                extra={
                    "expression": expression,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                },
                ctx=ctx
            )
            return f"Error: Invalid mathematical expression - {str(e)}"
