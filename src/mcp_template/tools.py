"""
Tools implementation for MCP template.

This is where you define your tools. Users mainly need to modify this file.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from .helpers.logging import create_mcp_logger
from .helpers.mcp_features import (AuthenticationHelper, ElicitationHelper,
                                   MCPPatterns, NotificationHelper,
                                   SamplingHelper, SessionHelper)
from .helpers.validation import safe_int, sanitize_string

# Global context for storing server state
# In a real application, you might use a proper state management solution
_server_context = {
    "request_count": 0,
    "calculations": [],
    "last_echo": None,
    "user_preferences": {},
}


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the FastMCP server."""

    # === Basic Tools ===

    @mcp.tool()
    async def echo(text: str, repeat: int = 1, ctx: Context[ServerSession, Any] = None) -> str:
        """Echo back the input text, optionally repeated."""
        # Use MCP context logging instead of regular logger
        if ctx:
            logger = create_mcp_logger(ctx, "echo")
            await logger.info(f"Echo tool called with text='{text}', repeat={repeat}")

        # Validate and sanitize inputs
        text = sanitize_string(text, max_length=1000)
        repeat = safe_int(repeat, default=1, min_val=1, max_val=10)

        # Update context
        _server_context["request_count"] += 1
        _server_context["last_echo"] = text

        # Generate result
        result = "\n".join([text] * repeat)
        return f"Echo: {result}"

    @mcp.tool()
    async def calculate(expression: str, ctx: Context[ServerSession, Any] = None) -> str:
        """Perform basic mathematical calculations with MCP logging."""
        if ctx:
            logger = create_mcp_logger(ctx, "calculator")
            await logger.info(f"Calculating expression: {expression}")

        expression = sanitize_string(expression, max_length=100)

        try:
            # Safe evaluation of mathematical expressions
            allowed_chars = set("0123456789+-*/().,eE ")
            if not all(c in allowed_chars for c in expression):
                if ctx:
                    await logger.error("Expression contains invalid characters")
                return "Error: Expression contains invalid characters"

            # Use eval with limited builtins for safety
            safe_dict = {"__builtins__": {}}
            result = eval(expression, safe_dict, {})

            # Store calculation in context
            calculation = {
                "expression": expression,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            _server_context["calculations"].append(calculation)

            # Keep only last 10 calculations
            if len(_server_context["calculations"]) > 10:
                _server_context["calculations"] = _server_context["calculations"][-10:]

            _server_context["request_count"] += 1

            if ctx:
                await logger.info(f"Calculation successful: {expression} = {result}")

            return f"Result: {result}"

        except Exception as e:
            if ctx:
                await logger.error(f"Calculation failed: {str(e)}")
            return f"Error: Invalid mathematical expression - {str(e)}"

    # === Advanced MCP Features Demonstrations ===

    @mcp.tool()
    async def interactive_processor(
        data: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate elicitation by asking user how to process data."""
        if not ctx:
            return "Error: Context required for interactive features"

        logger = create_mcp_logger(ctx, "interactive")
        await logger.info("Starting interactive data processing")

        # Use the elicitation helper
        result = await MCPPatterns.interactive_data_processing(ctx, data)

        # Notify about completion
        await NotificationHelper.notify_tool_list_changed(ctx)

        return result

    @mcp.tool()
    async def ai_analyzer(
        text: str,
        analysis_type: str = "general",
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate AI completions by analyzing text with AI assistance."""
        if not ctx:
            return "Error: Context required for AI features"

        logger = create_mcp_logger(ctx, "ai_analyzer")
        await logger.info(f"Starting AI analysis of type: {analysis_type}")

        try:
            # Use AI-assisted analysis
            result = await MCPPatterns.ai_assisted_analysis(ctx, text)

            # Log success
            logger = create_mcp_logger(ctx, "tool.ai_analyzer")
            await logger.info(f"Executing with args: text={text[:50]}..., type={analysis_type}")
            await logger.debug("Result: Success")
            return result

        except Exception as e:
            logger = create_mcp_logger(ctx, "error")
            await logger.error(f"Error in ai_analyzer: {str(e)}")
            await logger.debug(f"Error details: {type(e).__name__}: {e}")
            return f"AI analysis failed: {str(e)}"

    @mcp.tool()
    async def preferences_manager(
        action: str,
        key: str = "",
        value: str = "",
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Manage user preferences with elicitation for missing values."""
        if not ctx:
            return "Error: Context required for preference management"

        logger = create_mcp_logger(ctx, "preferences")

        if action == "get":
            if not key:
                # Show all preferences
                return json.dumps(_server_context["user_preferences"], indent=2)
            else:
                # Get specific preference
                value = _server_context["user_preferences"].get(key, "Not set")
                await logger.info(f"Retrieved preference {key}: {value}")
                return f"{key}: {value}"

        elif action == "set":
            if not key:
                confirmed = await ElicitationHelper.elicit_simple_confirmation(
                    ctx, "No key provided. Would you like to clear all preferences?"
                )
                if confirmed:
                    _server_context["user_preferences"].clear()
                    await logger.info("All preferences cleared")
                    return "All preferences cleared"
                return "Operation cancelled"

            if not value:
                # Ask user for the value
                class ValueSchema(BaseModel):
                    preference_value: str = Field(
                        description="The value to set for this preference")

                result = await ElicitationHelper.elicit_user_input(
                    ctx, f"Please provide a value for preference '{key}':", ValueSchema
                )

                if result.action.value == "accept" and result.data:
                    value = result.data.preference_value
                else:
                    return "Operation cancelled by user"

            # Set the preference
            _server_context["user_preferences"][key] = value
            await logger.info(f"Set preference {key} to: {value}")

            # Notify about changes
            await NotificationHelper.notify_resource_list_changed(ctx)

            return f"Set {key} = {value}"

        elif action == "delete":
            if key in _server_context["user_preferences"]:
                del _server_context["user_preferences"][key]
                await logger.info(f"Deleted preference: {key}")
                return f"Deleted preference: {key}"
            return f"Preference '{key}' not found"

        return "Invalid action. Use 'get', 'set', or 'delete'"

    @mcp.tool()
    async def session_inspector(ctx: Context[ServerSession, Any] = None) -> str:
        """Inspect current MCP session properties and capabilities."""
        if not ctx:
            return "Error: Context required for session inspection"

        logger = create_mcp_logger(ctx, "session_inspector")
        await logger.info("Inspecting session properties")

        # Get session info
        session_info = SessionHelper.get_session_info(ctx)
        context_info = SessionHelper.get_request_context_info(ctx)
        capabilities = await SessionHelper.check_client_capabilities(ctx)

        inspection_result = {
            "session_info": session_info,
            "context_info": context_info,
            "client_capabilities": capabilities,
            "server_context": {
                "total_requests": _server_context["request_count"],
                "calculations_stored": len(_server_context["calculations"]),
                "preferences_set": len(_server_context["user_preferences"]),
            }
        }

        return json.dumps(inspection_result, indent=2)

    @mcp.tool()
    async def notification_demo(
        notification_type: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate different types of MCP notifications."""
        if not ctx:
            return "Error: Context required for notifications"

        logger = create_mcp_logger(ctx, "notifications")

        try:
            if notification_type == "resource_changed":
                await NotificationHelper.notify_resource_changed(ctx, "template://status")
                await logger.info("Sent resource changed notification")
                return "Sent resource changed notification for template://status"

            elif notification_type == "resource_list":
                await NotificationHelper.notify_resource_list_changed(ctx)
                await logger.info("Sent resource list changed notification")
                return "Sent resource list changed notification"

            elif notification_type == "tool_list":
                await NotificationHelper.notify_tool_list_changed(ctx)
                await logger.info("Sent tool list changed notification")
                return "Sent tool list changed notification"

            elif notification_type == "prompt_list":
                await NotificationHelper.notify_prompt_list_changed(ctx)
                await logger.info("Sent prompt list changed notification")
                return "Sent prompt list changed notification"

            elif notification_type == "progress":
                # Send a series of progress notifications
                for i in range(0, 101, 20):
                    await NotificationHelper.send_progress_notification(ctx, i, 100)
                    await asyncio.sleep(0.1)  # Small delay for demo
                await logger.info("Sent progress notification sequence")
                return "Sent progress notification sequence (0-100%)"

            else:
                available_types = [
                    "resource_changed", "resource_list", "tool_list", "prompt_list", "progress"]
                return f"Unknown notification type. Available: {', '.join(available_types)}"

        except Exception as e:
            await logger.error(f"Notification failed: {str(e)}")
            return f"Notification failed: {str(e)}"

    @mcp.tool()
    async def logging_demo(
        log_level: str,
        message: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate different MCP logging levels."""
        if not ctx:
            return "Error: Context required for logging demo"

        logger = create_mcp_logger(ctx, "logging_demo")

        # Demonstrate different log levels
        if log_level == "debug":
            await logger.debug(message)
        elif log_level == "info":
            await logger.info(message)
        elif log_level == "warning":
            await logger.warning(message)
        elif log_level == "error":
            await logger.error(message)
        elif log_level == "notice":
            await logger.notice(message)
        else:
            await logger.error(f"Unknown log level: {log_level}")
            return f"Unknown log level: {log_level}. Available: debug, info, warning, error, notice"

        return f"Logged message at {log_level} level: {message}"

    # === Legacy Tools (kept for compatibility) ===

    @mcp.tool()
    def timestamp(format: str = "iso") -> str:
        """Get current timestamp in various formats."""
        now = datetime.now()

        if format == "iso":
            result = now.isoformat()
        elif format == "unix":
            result = str(int(now.timestamp()))
        elif format == "human":
            result = now.strftime("%Y-%m-%d %H:%M:%S")
        elif format == "utc":
            result = datetime.utcnow().isoformat() + "Z"
        else:
            result = now.isoformat()

        _server_context["request_count"] += 1
        return f"Timestamp ({format}): {result}"

    @mcp.tool()
    def text_stats(text: str, include_words: bool = False) -> str:
        """Analyze text and provide statistics."""
        if not text:
            return "Error: Text is required"

        # Basic statistics
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.splitlines())
        paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

        result_lines = [
            "Text Statistics:",
            f"Characters: {char_count}",
            f"Words: {word_count}",
            f"Lines: {line_count}",
            f"Paragraphs: {paragraph_count}",
        ]

        # Word frequency analysis
        if include_words and word_count > 0:
            words = text.lower().split()
            word_freq = {}
            for word in words:
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word:
                    word_freq[clean_word] = word_freq.get(clean_word, 0) + 1

            top_words = sorted(word_freq.items(),
                               key=lambda x: x[1], reverse=True)[:10]
            if top_words:
                result_lines.append("\nTop 10 most frequent words:")
                for word, count in top_words:
                    result_lines.append(f"  {word}: {count}")

        _server_context["request_count"] += 1
        return "\n".join(result_lines)

    @mcp.tool()
    def json_format(json_data: str, indent: int = 2) -> str:
        """Format and validate JSON data."""
        if not json_data:
            return "Error: JSON data is required"

        indent = safe_int(indent, default=2, min_val=0, max_val=8)

        try:
            parsed = json.loads(json_data)
            formatted = json.dumps(parsed, indent=indent,
                                   ensure_ascii=False, sort_keys=True)

            result_lines = [
                "Formatted JSON:",
                "```json",
                formatted,
                "```",
                f"\nJSON is valid ✓",
                f"Indentation: {indent} spaces",
            ]

            _server_context["request_count"] += 1
            return "\n".join(result_lines)

        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON - {str(e)}"

    @mcp.tool()
    def server_status(include_cache: bool = False) -> str:
        """Get server status and metrics."""
        status_lines = [
            "Server Status:",
            f"Total requests: {_server_context['request_count']}",
            f"Calculations stored: {len(_server_context['calculations'])}",
            f"User preferences: {len(_server_context['user_preferences'])}",
        ]

        if _server_context['last_echo']:
            status_lines.append(f"Last echo: {_server_context['last_echo']}")

        if include_cache and _server_context['calculations']:
            status_lines.append("\nRecent calculations:")
            for calc in _server_context['calculations'][-3:]:
                status_lines.append(
                    f"  {calc['expression']} = {calc['result']}")

        if _server_context['user_preferences']:
            status_lines.append(
                f"\nUser preferences: {list(_server_context['user_preferences'].keys())}")

        _server_context["request_count"] += 1
        return "\n".join(status_lines)


# Example of how to add your own advanced tool:
"""
@mcp.tool()
async def my_advanced_tool(
    input_data: str, 
    ctx: Context[ServerSession, Any] = None
) -> str:
    '''My advanced tool with full MCP features.'''
    
    if not ctx:
        return "Error: Context required"
    
    # Use MCP logging
    logger = create_mcp_logger(ctx, "my_tool")
    await logger.info("Tool execution started")
    
    # Use elicitation if needed
    confirmation = await ElicitationHelper.elicit_simple_confirmation(
        ctx, "Do you want to proceed with processing?"
    )
    
    if not confirmation:
        await logger.info("Operation cancelled by user")
        return "Operation cancelled"
    
    # Process data
    result = f"Processed: {input_data}"
    
    # Send notifications
    await NotificationHelper.notify_resource_changed(ctx, "my://resource")
    
    await logger.info("Tool execution completed")
    return result
"""
