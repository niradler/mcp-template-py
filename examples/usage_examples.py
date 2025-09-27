"""Usage examples for the MCP template."""

import json
from mcp_template import create_server
from mcp_template.prompts import register_prompts
from mcp_template.tools import register_tools
from mcp_template.resources import register_resources
from mcp.server.fastmcp import FastMCP


def example_prompts():
    """Examples of using prompts."""
    print("=== Prompt Examples ===\n")
    
    # Create a test server to get the prompt handlers
    mcp = FastMCP("example")
    register_prompts(mcp)
    
    # Get prompt handlers
    prompt_handlers = {handler.name: handler.handler for handler in mcp._prompt_handlers.values()}
    
    # Hello world prompt
    result = prompt_handlers["hello_world"](name="Developer")
    print("Hello World Prompt:")
    print(f"Result: {result[:100]}...\n")
    
    # Code review prompt
    result = prompt_handlers["code_review"](
        code="""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
        """.strip(),
        language="python",
        focus="performance"
    )
    print("Code Review Prompt:")
    print(f"Result preview: {result[:200]}...\n")
    
    # Explain concept prompt
    result = prompt_handlers["explain_concept"](
        concept="microservices",
        audience="intermediate",
        include_examples="true"
    )
    print("Explain Concept Prompt:")
    print(f"Result preview: {result[:200]}...\n")


def example_tools():
    """Examples of using tools."""
    print("=== Tool Examples ===\n")
    
    # Create a test server to get the tool handlers
    mcp = FastMCP("example")
    register_tools(mcp)
    
    # Get tool handlers
    tool_handlers = {handler.name: handler.handler for handler in mcp._tool_handlers.values()}
    
    # Echo tool
    result = tool_handlers["echo"](text="Hello MCP!", repeat=3)
    print("Echo Tool:")
    print(f"Result: {result}\n")
    
    # Calculate tool
    result = tool_handlers["calculate"](expression="(25 + 15) * 2")
    print("Calculate Tool:")
    print(f"Result: {result}\n")
    
    # Text statistics tool
    text = """
    The Model Context Protocol (MCP) is an open protocol that enables 
    secure connections between host applications and external data sources. 
    This protocol allows AI assistants to access relevant information 
    from various systems in a standardized way.
    """
    result = tool_handlers["text_stats"](
        text=text.strip(),
        include_words=True
    )
    print("Text Stats Tool:")
    print(f"Result: {result}\n")
    
    # JSON format tool
    messy_json = '{"name":"example","data":[1,2,3],"config":{"enabled":true,"timeout":30}}'
    result = tool_handlers["json_format"](
        json_data=messy_json,
        indent=2
    )
    print("JSON Format Tool:")
    print(f"Result: {result}\n")
    
    # Server status tool
    result = tool_handlers["server_status"](include_cache=True)
    print("Server Status Tool:")
    print(f"Result: {result}\n")


def example_resources():
    """Examples of using resources."""
    print("=== Resource Examples ===\n")
    
    # Create a test server to get the resource handlers
    mcp = FastMCP("example")
    register_resources(mcp)
    
    # Get resource handlers
    resource_handlers = {handler.template: handler.handler for handler in mcp._resource_handlers.values()}
    
    # Template info resource
    result = resource_handlers["template://info"]()
    data = json.loads(result)
    print("Template Info Resource:")
    print(f"Name: {data['name']}")
    print(f"Version: {data['version']}")
    print(f"Features: {', '.join(data['features'])}\n")
    
    # Server status resource
    result = resource_handlers["template://status"]()
    data = json.loads(result)
    print("Server Status Resource:")
    print(f"Status: {data['status']}")
    print(f"Framework: {data['server_info']['framework']}\n")
    
    # Help documentation resource
    result = resource_handlers["template://help"]()
    print("Help Documentation Resource:")
    print(f"Content preview: {result[:300]}...\n")
    
    # Example file resource
    result = resource_handlers["file://{filename}"](filename="example.txt")
    print("File Resource:")
    print(f"Content: {result[:100]}...\n")


def example_server_creation():
    """Example of creating and configuring the server."""
    print("=== Server Creation Example ===\n")
    
    # Create the FastMCP server
    server = create_server()
    print("✅ FastMCP server created successfully")
    
    # The server is now ready to handle requests
    print("Server capabilities:")
    print("- Prompts: ✅")
    print("- Tools: ✅") 
    print("- Resources: ✅")
    print("- FastMCP framework: ✅")
    print("- Simple decorators: ✅")
    print("\nServer is ready to run with `server.run()`\n")


def example_fastmcp_patterns():
    """Examples of FastMCP patterns and best practices."""
    print("=== FastMCP Patterns ===\n")
    
    # Show how to add a custom tool
    print("Adding a custom tool:")
    print("""
@mcp.tool()
def custom_calculator(a: int, b: int, operation: str = "add") -> str:
    '''Perform custom calculations.'''
    if operation == "add":
        result = a + b
    elif operation == "multiply":
        result = a * b
    else:
        return f"Unknown operation: {operation}"
    
    return f"Result: {result}"
    """)
    
    # Show how to add a custom prompt
    print("Adding a custom prompt:")
    print("""
@mcp.prompt()
def custom_prompt(topic: str, style: str = "professional") -> str:
    '''Generate custom content prompts.'''
    return f"Write about {topic} in a {style} style with examples and key points."
    """)
    
    # Show how to add a custom resource
    print("Adding a custom resource:")
    print("""
@mcp.resource("custom://data/{data_id}")
def get_custom_data(data_id: str) -> str:
    '''Get custom data by ID.'''
    # Your logic here
    data = {"id": data_id, "content": "Custom data"}
    return json.dumps(data)
    """)
    print()


def main():
    """Run all examples."""
    print("🚀 MCP Template Usage Examples (FastMCP)\n")
    
    example_server_creation()
    example_fastmcp_patterns()
    example_prompts()
    example_tools()
    example_resources()
    
    print("✅ All examples completed!")
    print("\n💡 Key Benefits of FastMCP:")
    print("- Simple decorator-based API")
    print("- Automatic type validation")
    print("- No complex routing logic needed")
    print("- Easy to add new features")
    print("- Built-in error handling")


if __name__ == "__main__":
    main()
