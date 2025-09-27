#!/usr/bin/env python3
"""Test client for manual testing of the MCP server."""

import asyncio
import json
import sys
from typing import Any, Dict, List

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import (
    CallToolRequest,
    GetPromptRequest, 
    ListPromptsRequest,
    ListResourcesRequest,
    ListToolsRequest,
    ReadResourceRequest,
)


class MCPTestClient:
    """Test client for interacting with the MCP server."""
    
    def __init__(self):
        self.client: Client = Client()
        self.connected = False
    
    async def connect(self) -> None:
        """Connect to the MCP server."""
        try:
            # Start the server as a subprocess
            server_params = StdioServerParameters(
                command="uv",
                args=["run", "mcp-template"],
            )
            
            # Connect via stdio
            read_stream, write_stream = await stdio_client(server_params)
            await self.client.connect(read_stream, write_stream)
            
            self.connected = True
            print("✅ Connected to MCP server")
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            sys.exit(1)
    
    async def disconnect(self) -> None:
        """Disconnect from the server."""
        if self.connected:
            await self.client.disconnect()
            self.connected = False
            print("✅ Disconnected from server")
    
    async def test_list_prompts(self) -> None:
        """Test listing prompts."""
        print("\n📝 Testing list_prompts...")
        try:
            response = await self.client.list_prompts()
            print(f"Found {len(response.prompts)} prompts:")
            for prompt in response.prompts:
                args_desc = ", ".join([f"{arg.name}{'*' if arg.required else ''}" 
                                     for arg in prompt.arguments])
                print(f"  • {prompt.name}: {prompt.description}")
                print(f"    Arguments: {args_desc}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_get_prompt(self, name: str, arguments: Dict[str, Any]) -> None:
        """Test getting a specific prompt."""
        print(f"\n📝 Testing get_prompt: {name}")
        try:
            request = GetPromptRequest(name=name, arguments=arguments)
            response = await self.client.get_prompt(request)
            print(f"Description: {response.description}")
            print(f"Messages ({len(response.messages)}):")
            for i, message in enumerate(response.messages):
                print(f"  {i+1}. [{message.role}]: {message.content.text[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_list_tools(self) -> None:
        """Test listing tools."""
        print("\n🔧 Testing list_tools...")
        try:
            response = await self.client.list_tools()
            print(f"Found {len(response.tools)} tools:")
            for tool in response.tools:
                required_args = []
                optional_args = []
                
                if "properties" in tool.inputSchema:
                    required = tool.inputSchema.get("required", [])
                    for prop_name in tool.inputSchema["properties"]:
                        if prop_name in required:
                            required_args.append(prop_name)
                        else:
                            optional_args.append(prop_name)
                
                args_desc = ""
                if required_args:
                    args_desc += "Required: " + ", ".join(required_args)
                if optional_args:
                    if args_desc:
                        args_desc += "; "
                    args_desc += "Optional: " + ", ".join(optional_args)
                
                print(f"  • {tool.name}: {tool.description}")
                if args_desc:
                    print(f"    Arguments: {args_desc}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_call_tool(self, name: str, arguments: Dict[str, Any]) -> None:
        """Test calling a specific tool."""
        print(f"\n🔧 Testing call_tool: {name}")
        try:
            request = CallToolRequest(name=name, arguments=arguments)
            response = await self.client.call_tool(request)
            
            if response.isError:
                print(f"❌ Tool error:")
            else:
                print(f"✅ Tool result:")
            
            for i, content in enumerate(response.content):
                if content.type == "text":
                    print(f"  {i+1}. {content.text}")
                else:
                    print(f"  {i+1}. [{content.type}] (binary content)")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_list_resources(self) -> None:
        """Test listing resources."""
        print("\n📚 Testing list_resources...")
        try:
            response = await self.client.list_resources()
            print(f"Found {len(response.resources)} resources:")
            for resource in response.resources:
                print(f"  • {resource.uri}: {resource.name}")
                print(f"    {resource.description} ({resource.mimeType})")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_read_resource(self, uri: str) -> None:
        """Test reading a specific resource."""
        print(f"\n📚 Testing read_resource: {uri}")
        try:
            request = ReadResourceRequest(uri=uri)
            response = await self.client.read_resource(request)
            
            print(f"Resource contents ({len(response.contents)} items):")
            for i, content in enumerate(response.contents):
                if content.type == "text":
                    text = content.text
                    if len(text) > 200:
                        text = text[:200] + "..."
                    print(f"  {i+1}. [text]: {text}")
                else:
                    print(f"  {i+1}. [{content.type}] (binary content)")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def run_comprehensive_tests(self) -> None:
        """Run a comprehensive test suite."""
        print("🚀 Starting comprehensive MCP server tests...\n")
        
        # Test prompts
        await self.test_list_prompts()
        await self.test_get_prompt("hello_world", {"name": "Test Client"})
        await self.test_get_prompt("code_review", {
            "code": "def hello():\n    return 'Hello World'",
            "language": "python",
            "focus": "style"
        })
        
        # Test tools
        await self.test_list_tools()
        await self.test_call_tool("echo", {"text": "Hello from test client!", "repeat": 2})
        await self.test_call_tool("calculate", {"expression": "15 + 27"})
        await self.test_call_tool("timestamp", {"format": "human"})
        await self.test_call_tool("text_stats", {
            "text": "This is a test text for analysis. This text contains repeated words.",
            "include_words": True
        })
        await self.test_call_tool("json_format", {
            "json_data": '{"name":"test","data":[1,2,3],"nested":{"key":"value"}}',
            "indent": 4
        })
        await self.test_call_tool("server_status", {"include_cache": True})
        
        # Test resources
        await self.test_list_resources()
        await self.test_read_resource("template://info")
        await self.test_read_resource("template://status")
        await self.test_read_resource("template://help")
        await self.test_read_resource("file://example.txt")
        
        # Test error handling
        print("\n🧪 Testing error handling...")
        await self.test_call_tool("unknown_tool", {})
        await self.test_call_tool("echo", {})  # Missing required argument
        await self.test_read_resource("unknown://resource")
        
        print("\n✅ Comprehensive tests completed!")


async def main():
    """Main test function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
MCP Test Client

Usage:
  python test_client.py              # Run comprehensive tests
  python test_client.py prompts      # Test prompts only
  python test_client.py tools        # Test tools only
  python test_client.py resources    # Test resources only
  python test_client.py --help       # Show this help
        """)
        return
    
    client = MCPTestClient()
    
    try:
        await client.connect()
        
        if len(sys.argv) == 1:
            # Run all tests
            await client.run_comprehensive_tests()
        else:
            test_type = sys.argv[1].lower()
            
            if test_type == "prompts":
                await client.test_list_prompts()
                await client.test_get_prompt("hello_world", {"name": "Test"})
                await client.test_get_prompt("code_review", {
                    "code": "print('hello')", 
                    "language": "python"
                })
            
            elif test_type == "tools":
                await client.test_list_tools()
                await client.test_call_tool("echo", {"text": "Test"})
                await client.test_call_tool("calculate", {"expression": "5 * 7"})
                await client.test_call_tool("server_status", {})
            
            elif test_type == "resources":
                await client.test_list_resources()
                await client.test_read_resource("template://info")
                await client.test_read_resource("template://status")
            
            else:
                print(f"Unknown test type: {test_type}")
                print("Available types: prompts, tools, resources")
    
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
