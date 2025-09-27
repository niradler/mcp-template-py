"""
Comprehensive examples showcasing all MCP advanced features.

This file demonstrates:
- Completions and AI integration
- Elicitation (asking users for input)  
- Sampling and model interaction
- Logging through MCP context
- Notifications
- Authentication patterns
- Session management
- Request context handling
"""

import asyncio
import json
from datetime import datetime
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from mcp_template.helpers import (AuthenticationHelper, ElicitationHelper,
                                  MCPPatterns, NotificationHelper,
                                  SamplingHelper, SessionHelper,
                                  create_mcp_logger)


def create_example_server() -> FastMCP:
    """Create an example server showcasing all MCP features."""

    mcp = FastMCP(name="MCP Advanced Features Demo")

    # === 1. LOGGING AND NOTIFICATIONS EXAMPLE ===

    @mcp.tool()
    async def process_data_with_logging(
        data: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Process data with comprehensive MCP logging."""
        if not ctx:
            return "Error: Context required for MCP features"

        # Create component-specific logger
        logger = create_mcp_logger(ctx, "data_processor")

        # Different log levels
        await logger.debug(f"Debug: Processing data '{data[:20]}...'")
        await logger.info("Info: Starting data processing")
        await logger.warning("Warning: This is experimental feature")

        try:
            # Simulate processing
            await asyncio.sleep(0.1)
            result = data.upper()

            # Log success
            await logger.info(f"Successfully processed {len(data)} characters")

            # Send notifications
            await NotificationHelper.notify_resource_list_changed(ctx)
            await NotificationHelper.send_progress_notification(ctx, 100, 100)

            return f"Processed: {result}"

        except Exception as e:
            # Log error directly
            logger = create_mcp_logger(ctx, "error")
            await logger.error(f"Error in process_data: {str(e)}")
            await logger.debug(f"Error details: {type(e).__name__}: {e}")
            return f"Processing failed: {str(e)}"

    # === 2. ELICITATION EXAMPLES ===

    @mcp.tool()
    async def interactive_file_processor(
        filename: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate elicitation for user input."""
        if not ctx:
            return "Error: Context required"

        logger = create_mcp_logger(ctx, "file_processor")
        await logger.info(f"Processing file: {filename}")

        # Simple confirmation
        confirmed = await ElicitationHelper.elicit_simple_confirmation(
            ctx, f"Are you sure you want to process '{filename}'?"
        )

        if not confirmed:
            await logger.info("Operation cancelled by user")
            return "Operation cancelled by user"

        # Choice selection
        operation = await ElicitationHelper.elicit_choice(
            ctx,
            "What operation would you like to perform?",
            ["compress", "encrypt", "backup", "analyze"],
            allow_other=True
        )

        if not operation:
            return "No operation selected"

        # Complex input elicitation
        class ProcessingOptions(BaseModel):
            quality: int = Field(
                description="Quality level (1-10)", ge=1, le=10)
            include_metadata: bool = Field(
                description="Include metadata in output")
            output_format: str = Field(
                description="Output format (json, xml, csv)")

        options_result = await ElicitationHelper.elicit_user_input(
            ctx,
            f"Please provide options for {operation} operation:",
            ProcessingOptions
        )

        if options_result.action.value == "accept" and options_result.data:
            options = options_result.data
            await logger.info(f"Processing with options: {options}")

            result = {
                "file": filename,
                "operation": operation,
                "options": options.dict(),
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }

            return json.dumps(result, indent=2)

        return "Processing cancelled - no options provided"

    # === 3. AI COMPLETIONS AND SAMPLING ===

    @mcp.tool()
    async def ai_writing_assistant(
        prompt: str,
        style: str = "professional",
        max_tokens: int = 200,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate AI completions and sampling."""
        if not ctx:
            return "Error: Context required"

        logger = create_mcp_logger(ctx, "ai_assistant")
        await logger.info(f"AI writing request: {style} style, {max_tokens} tokens")

        try:
            # Use sampling helper
            system_prompt = f"You are a {style} writing assistant. Help the user write content in a {style} tone."

            results = await SamplingHelper.sample_with_system_prompt(
                ctx,
                system_prompt=system_prompt,
                user_prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )

            if results:
                generated_content = results[0]
                await logger.info("AI generation completed successfully")

                # Notify about completion
                await NotificationHelper.notify_resource_changed(ctx, "ai://generated_content")

                return f"Generated Content ({style} style):\n\n{generated_content}"
            else:
                await logger.warning("No AI results received")
                return "AI generation failed - no results received"

        except Exception as e:
            await logger.error(f"AI generation failed: {str(e)}")
            return f"AI generation failed: {str(e)}"

    # === 4. SESSION AND AUTHENTICATION ===

    @mcp.tool()
    async def secure_data_access(
        resource_id: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate authentication and session management."""
        if not ctx:
            return "Error: Context required"

        logger = create_mcp_logger(ctx, "secure_access")

        # Check authentication
        authenticated = await AuthenticationHelper.require_authentication(ctx)
        if not authenticated:
            await logger.warning("Unauthorized access attempt")
            return AuthenticationHelper.create_auth_error_response()

        # Get session information
        session_info = SessionHelper.get_session_info(ctx)
        context_info = SessionHelper.get_request_context_info(ctx)
        capabilities = await SessionHelper.check_client_capabilities(ctx)

        await logger.info(f"Authorized access to resource: {resource_id}")

        # Simulate secure data access
        secure_data = {
            "resource_id": resource_id,
            "access_time": datetime.now().isoformat(),
            "session_info": session_info,
            "client_capabilities": capabilities,
            "context_info": context_info,
            "data": f"Secure data for {resource_id}",
        }

        return json.dumps(secure_data, indent=2)

    # === 5. COMPREHENSIVE WORKFLOW EXAMPLE ===

    @mcp.tool()
    async def complete_workflow_demo(
        task_description: str,
        ctx: Context[ServerSession, Any] = None
    ) -> str:
        """Demonstrate a complete workflow using all MCP features."""
        if not ctx:
            return "Error: Context required"

        logger = create_mcp_logger(ctx, "workflow")
        await logger.info("Starting complete workflow demonstration")

        workflow_results = []

        # Step 1: Get user preferences
        await logger.info("Step 1: Gathering user preferences")

        class WorkflowPreferences(BaseModel):
            priority: str = Field(
                description="Task priority: high, medium, low")
            notify_completion: bool = Field(
                description="Send notification when complete")
            ai_assistance: bool = Field(description="Use AI assistance")
            detailed_logging: bool = Field(
                description="Enable detailed logging")

        prefs_result = await ElicitationHelper.elicit_user_input(
            ctx,
            f"Please provide preferences for task: '{task_description}'",
            WorkflowPreferences
        )

        if prefs_result.action.value != "accept" or not prefs_result.data:
            return "Workflow cancelled - no preferences provided"

        preferences = prefs_result.data
        workflow_results.append(
            f"✓ Preferences gathered: {preferences.dict()}")

        # Step 2: AI Analysis (if requested)
        if preferences.ai_assistance:
            await logger.info("Step 2: AI analysis requested")

            try:
                analysis = await SamplingHelper.sample_text(
                    ctx,
                    f"Analyze this task and provide recommendations: {task_description}",
                    max_tokens=150,
                    temperature=0.5
                )

                if analysis:
                    workflow_results.append(
                        f"✓ AI Analysis: {analysis[0][:100]}...")
                else:
                    workflow_results.append(
                        "⚠ AI Analysis: Failed to get results")

            except Exception as e:
                workflow_results.append(f"⚠ AI Analysis: Error - {str(e)}")

        # Step 3: Process with progress notifications
        await logger.info("Step 3: Processing with progress updates")

        for i in range(0, 101, 25):
            await NotificationHelper.send_progress_notification(ctx, i, 100)
            workflow_results.append(f"✓ Progress: {i}%")
            await asyncio.sleep(0.1)

        # Step 4: Detailed logging (if requested)
        if preferences.detailed_logging:
            await logger.debug("Detailed logging enabled")
            await logger.info("Processing completed successfully")
            await logger.notice("Workflow executed with all features")

        # Step 5: Final notifications
        if preferences.notify_completion:
            await NotificationHelper.notify_resource_list_changed(ctx)
            await NotificationHelper.notify_tool_list_changed(ctx)
            workflow_results.append("✓ Completion notifications sent")

        # Final result
        final_result = {
            "task": task_description,
            "preferences": preferences.dict(),
            "workflow_steps": workflow_results,
            "completion_time": datetime.now().isoformat(),
            "status": "completed"
        }

        await logger.info("Complete workflow demonstration finished")

        return json.dumps(final_result, indent=2)

    # === 6. CONTEXT AND PROPERTIES DEMONSTRATION ===

    @mcp.tool()
    async def context_properties_demo(ctx: Context[ServerSession, Any] = None) -> str:
        """Demonstrate accessing all context properties and methods."""
        if not ctx:
            return "Error: Context required"

        logger = create_mcp_logger(ctx, "context_demo")
        await logger.info("Demonstrating context properties and methods")

        # Session properties
        session_info = SessionHelper.get_session_info(ctx)

        # Request context properties
        context_info = SessionHelper.get_request_context_info(ctx)

        # Client capabilities
        capabilities = await SessionHelper.check_client_capabilities(ctx)

        # FastMCP properties (simulate)
        fastmcp_properties = {
            "server_name": "mcp-advanced-demo",
            "supports_lifespan": True,
            "supports_context": True,
            "supports_elicitation": True,
            "supports_completions": True,
        }

        demo_result = {
            "session_properties": {
                "session_info": session_info,
                "available_methods": [
                    "send_resource_updated",
                    "send_resource_list_changed",
                    "send_tool_list_changed",
                    "send_prompt_list_changed",
                    "send_progress_notification",
                    "request_completion"
                ]
            },
            "request_context_properties": context_info,
            "client_capabilities": capabilities,
            "fastmcp_properties": fastmcp_properties,
            "mcp_logging_levels": ["debug", "info", "warning", "error", "notice"],
            "available_helpers": [
                "ElicitationHelper",
                "SamplingHelper",
                "NotificationHelper",
                "SessionHelper",
                "AuthenticationHelper",
                # "LoggingPatterns" - removed, use create_mcp_logger directly
            ]
        }

        await logger.notice("Context properties demonstration completed")

        return json.dumps(demo_result, indent=2)

    return mcp


def main():
    """Run the advanced features demonstration."""
    server = create_example_server()

    print("🚀 MCP Advanced Features Demo Server Created!")
    print("\nAvailable advanced tools:")
    print("- process_data_with_logging: Logging and notifications")
    print("- interactive_file_processor: Elicitation examples")
    print("- ai_writing_assistant: AI completions and sampling")
    print("- secure_data_access: Authentication and session")
    print("- complete_workflow_demo: Full workflow with all features")
    print("- context_properties_demo: Context and properties exploration")
    print("\nRun with: server.run()")


if __name__ == "__main__":
    main()
