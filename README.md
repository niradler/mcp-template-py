# MCP Template Python

A comprehensive template for creating MCP (Model Context Protocol) servers in Python using FastMCP with **all advanced features**.

## 🚀 Features

- ✅ **FastMCP Framework** - Simple decorator-based API
- ✅ **Complete MCP Support** - Prompts, Tools, and Resources
- ✅ **Advanced MCP Features** - Completions, Elicitation, Sampling, Logging, Notifications
- ✅ **Context & Session Management** - Full MCP context integration
- ✅ **Authentication Helpers** - Built-in auth patterns
- ✅ **Comprehensive Testing** - Unit and E2E tests
- ✅ **MCP Inspector Ready** - Works with the official inspector
- ✅ **Production Ready** - Logging, error handling, best practices

## 🎯 Advanced MCP Features Covered

| Feature                 | Description                                             | Example Tool                                   |
| ----------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| **MCP Context Logging** | Proper logging through MCP context (no stdio conflicts) | `logging_demo`                                 |
| **Elicitation**         | Ask users for input with schema validation              | `interactive_processor`, `preferences_manager` |
| **AI Completions**      | Request AI completions from the client                  | `ai_analyzer`                                  |
| **Sampling**            | Sample text from AI models                              | `ai_writing_assistant`                         |
| **Notifications**       | Send various MCP notifications                          | `notification_demo`                            |
| **Session Properties**  | Access session info and capabilities                    | `session_inspector`                            |
| **Request Context**     | Access request context and lifespan                     | `context_properties_demo`                      |
| **Authentication**      | Auth patterns and helpers                               | `secure_data_access`                           |

## 🚀 Quick Start

1. **Install dependencies:**

   ```bash
   uv sync --all-extras
   ```

2. **Run with file logging (recommended for stdio):**

   ```bash
   uv run mcp-template --enable-file-logging
   ```

3. **Test with MCP Inspector:**

   ```bash
   npx @modelcontextprotocol/inspector uv run mcp-template --enable-file-logging
   ```

4. **Try advanced features:**

   ```bash
   # Test elicitation (user input)
   # Call tool: interactive_processor with data: "test data"

   # Test AI completions (if client supports)
   # Call tool: ai_analyzer with text: "analyze this"

   # Test notifications
   # Call tool: notification_demo with notification_type: "progress"

   # Test logging levels
   # Call tool: logging_demo with log_level: "info", message: "test"
   ```

## 📁 Core Files (What You Need to Know)

### **Main Files (Edit These):**

- **`src/mcp_template/prompts.py`** - Define your prompts here
- **`src/mcp_template/tools.py`** - Define your tools here
- **`src/mcp_template/resources.py`** - Define your resources here

### **Helper Files (Use These):**

- **`src/mcp_template/helpers/mcp_features.py`** - All advanced MCP helpers
- **`src/mcp_template/helpers/logging.py`** - MCP-compatible logging
- **`src/mcp_template/helpers/validation.py`** - Input validation
- **`src/mcp_template/helpers/headers.py`** - Header parsing utilities

Everything else is infrastructure - you don't need to modify it unless you want advanced customization.

## 🛠 Development

### Quick Tasks (using tasks.py)

```bash
# Setup development environment
python tasks.py dev-setup

# Run all tests
python tasks.py test

# Format and lint code
python tasks.py format
python tasks.py lint

# Run the server with file logging
uv run mcp-template --enable-file-logging

# Test with MCP Inspector
python tasks.py inspector

# See all available tasks
python tasks.py help
```

## 💡 Adding Advanced Features to Your Tools

### 1. Basic Tool with MCP Context Logging

```python
@mcp.tool()
async def my_tool(data: str, ctx: Context[ServerSession, Any] = None) -> str:
    """My tool with proper MCP logging."""
    if not ctx:
        return "Error: Context required"

    # Use MCP context logging (won't interfere with stdio)
    logger = create_mcp_logger(ctx, "my_tool")
    await logger.info(f"Processing data: {data}")

    result = f"Processed: {data}"

    # Send notification
    await NotificationHelper.notify_resource_changed(ctx, "my://resource")

    return result
```

### 2. Interactive Tool with Elicitation

```python
@mcp.tool()
async def interactive_tool(task: str, ctx: Context[ServerSession, Any] = None) -> str:
    """Tool that asks user for input."""
    if not ctx:
        return "Error: Context required"

    # Ask for confirmation
    confirmed = await ElicitationHelper.elicit_simple_confirmation(
        ctx, f"Are you sure you want to {task}?"
    )

    if not confirmed:
        return "Operation cancelled by user"

    # Ask for options
    class TaskOptions(BaseModel):
        priority: str = Field(description="Priority: high, medium, low")
        notify_when_done: bool = Field(description="Send notification when complete")

    options_result = await ElicitationHelper.elicit_user_input(
        ctx, "Please provide task options:", TaskOptions
    )

    if options_result.action.value == "accept" and options_result.data:
        return f"Task '{task}' started with options: {options_result.data.dict()}"

    return "Task cancelled - no options provided"
```

### 3. AI-Powered Tool

```python
@mcp.tool()
async def ai_assistant(prompt: str, ctx: Context[ServerSession, Any] = None) -> str:
    """Tool that uses AI completions."""
    if not ctx:
        return "Error: Context required"

    try:
        # Use AI to process the prompt
        results = await SamplingHelper.sample_text(
            ctx,
            prompt,
            max_tokens=200,
            temperature=0.7
        )

        if results:
            return f"AI Response: {results[0]}"
        else:
            return "AI processing failed - no results"

    except Exception as e:
        return f"AI processing error: {str(e)}"
```

### 4. Tool with Notifications and Progress

```python
@mcp.tool()
async def long_running_task(duration: int, ctx: Context[ServerSession, Any] = None) -> str:
    """Tool that shows progress and sends notifications."""
    if not ctx:
        return "Error: Context required"

    logger = create_mcp_logger(ctx, "long_task")
    await logger.info(f"Starting task with duration: {duration}")

    # Send progress updates
    for i in range(0, 101, 20):
        await NotificationHelper.send_progress_notification(ctx, i, 100)
        await asyncio.sleep(duration / 5)  # Simulate work

    # Send completion notification
    await NotificationHelper.notify_tool_list_changed(ctx)
    await logger.info("Task completed successfully")

    return f"Task completed in {duration} seconds"
```

## 📚 Advanced Examples

The template includes comprehensive examples:

- **`examples/advanced_features_demo.py`** - Complete showcase of all features
- **`examples/usage_examples.py`** - Basic usage patterns
- **`src/mcp_template/tools.py`** - Real implementations you can learn from

## 🎨 MCP Logging Best Practices

### ❌ Don't Use Regular Logging (Conflicts with stdio):

```python
import logging
logger = logging.getLogger(__name__)
logger.info("This can break stdio transport!")
```

### ✅ Use MCP Context Logging:

```python
# In your tool function
if ctx:
    logger = create_mcp_logger(ctx, "my_component")
    await logger.info("This works perfectly with MCP!")
    await logger.error("Error messages too!")
    await logger.debug("Debug info goes through MCP")
```

### ✅ File Logging for Infrastructure:

```bash
# Run server with file logging
uv run mcp-template --enable-file-logging

# Or specify custom log file
uv run mcp-template --log-file custom.log
```

## 🔧 Key Helpers Available

- **`ElicitationHelper`** - Ask users for input with schema validation
- **`SamplingHelper`** - Request AI completions and sampling
- **`NotificationHelper`** - Send various MCP notifications
- **`SessionHelper`** - Access session properties and capabilities
- **`AuthenticationHelper`** - Handle authentication patterns
- **`create_mcp_logger`** - Create MCP context loggers
- **`MCPPatterns`** - Complete workflow patterns

## 🏗 Project Structure

```
mcp-template-py/
├── src/mcp_template/
│   ├── __init__.py
│   ├── main.py              # Entry point with advanced CLI
│   ├── server.py            # FastMCP server with lifespan
│   ├── helpers/             # 🎯 Advanced MCP helpers
│   │   ├── __init__.py
│   │   ├── mcp_features.py  # ⭐ All advanced MCP features
│   │   ├── logging.py       # 🔊 MCP context logging
│   │   ├── headers.py       # 🔒 Auth and header utilities
│   │   └── validation.py    # ✅ Input validation
│   ├── prompts.py           # ⭐ Your prompts
│   ├── tools.py             # ⭐ Your tools (with advanced examples)
│   └── resources.py         # ⭐ Your resources
├── tests/
│   ├── unit/                # Unit tests
│   ├── e2e/                 # End-to-end tests
│   └── fixtures/            # Test fixtures
├── examples/
│   ├── usage_examples.py         # Basic usage
│   └── advanced_features_demo.py # 🚀 Full feature showcase
└── scripts/
    └── test_client.py       # Test client for manual testing
```

## 🎪 What Makes This Template Special

1. **All MCP Features**: Complete coverage of every MCP capability
2. **Production Ready**: Proper logging, error handling, testing
3. **Easy to Use**: Simple decorators, comprehensive helpers
4. **Best Practices**: Follows official SDK patterns exactly
5. **Comprehensive Examples**: Learn from real implementations
6. **Zero Configuration**: Works out of the box with MCP Inspector

## 🚀 Ready to Build?

1. **Clone/copy this template**
2. **Edit the 3 main files**: `prompts.py`, `tools.py`, `resources.py`
3. **Use the helpers** for advanced features
4. **Test with MCP Inspector**
5. **Deploy your MCP server!**

The template handles all the complex MCP infrastructure so you can focus on building amazing tools! 🎯

## 📖 License

MIT License
