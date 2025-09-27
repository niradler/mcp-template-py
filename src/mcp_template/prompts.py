"""
Prompts implementation for MCP server.

This is where you define your prompts. Users mainly need to modify this file.
"""

from mcp.server.fastmcp import FastMCP

from .helpers import sanitize_string


def register_prompts(mcp: FastMCP) -> None:
    """Register all prompts with the FastMCP server."""

    @mcp.prompt()
    def hello_world(name: str = "World") -> str:
        """A simple hello world prompt."""
        name = sanitize_string(name, max_length=100)
        return f"Say hello to {name} in a friendly and welcoming way. Be warm and engaging in your response."

    @mcp.prompt()
    def code_review(code: str, language: str = "unknown", focus: str = "general quality") -> str:
        """Generate a code review prompt for the given code."""
        code = sanitize_string(code, max_length=10000)
        language = sanitize_string(language, max_length=50)
        focus = sanitize_string(focus, max_length=200)

        return f"""Please review the following {language} code and provide feedback focusing on {focus}.

Code to review:
```{language}
{code}
```

Please provide:
1. Overall assessment
2. Specific issues or concerns
3. Suggestions for improvement
4. Best practices recommendations

Focus your review on: {focus}"""
