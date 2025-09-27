"""
Prompts implementation for MCP template.

This is where you define your prompts. Users mainly need to modify this file.
"""

from mcp.server.fastmcp import FastMCP

from .helpers.logging import get_logger
from .helpers.validation import sanitize_string

logger = get_logger(__name__)


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

    @mcp.prompt()
    def explain_concept(concept: str, audience: str = "intermediate", include_examples: str = "true") -> str:
        """Generate a prompt to explain a technical concept."""
        concept = sanitize_string(concept, max_length=200)
        audience = sanitize_string(audience, max_length=50)
        
        include_examples_bool = include_examples.lower() == "true"
        examples_instruction = "Include practical examples to illustrate the concept." if include_examples_bool else "Focus on clear explanations without examples."
        
        return f"""Explain the technical concept of "{concept}" to a {audience} level audience.

Requirements:
- Use clear, accessible language appropriate for {audience} level
- Structure your explanation logically
- {examples_instruction}
- Cover the key aspects and why it matters
- Address common misconceptions if relevant

Concept to explain: {concept}
Target audience: {audience}"""

    @mcp.prompt()
    def debug_help(error_message: str, context: str = "", language: str = "") -> str:
        """Generate a debugging assistance prompt."""
        error_message = sanitize_string(error_message, max_length=1000)
        context = sanitize_string(context, max_length=1000)
        language = sanitize_string(language, max_length=50)
        
        context_section = f"\nAdditional context: {context}" if context else ""
        language_section = f"\nProgramming language/technology: {language}" if language else ""
        
        return f"""Help debug the following error:

Error message: {error_message}{context_section}{language_section}

Please provide:
1. Explanation of what this error means
2. Common causes of this error
3. Step-by-step troubleshooting approach
4. Specific solutions or fixes to try
5. Prevention strategies for the future

Focus on practical, actionable advice."""

    @mcp.prompt()
    def write_documentation(feature: str, target_audience: str = "developers") -> str:
        """Generate a prompt for writing technical documentation."""
        feature = sanitize_string(feature, max_length=200)
        target_audience = sanitize_string(target_audience, max_length=100)
        
        return f"""Write comprehensive documentation for the following feature: {feature}

Target audience: {target_audience}

Please include:
1. Overview and purpose
2. Key features and benefits
3. Getting started guide
4. Step-by-step usage instructions
5. Code examples (if applicable)
6. Common issues and troubleshooting
7. Best practices and tips

Make the documentation clear, well-structured, and easy to follow for {target_audience}."""


# Example of how to add your own prompt:
"""
To add a new prompt, just add a function with the @mcp.prompt() decorator:

@mcp.prompt()
def my_custom_prompt(topic: str, style: str = "professional") -> str:
    '''Description of what your prompt generates.'''
    # Your prompt logic here
    return f"Write about {topic} in a {style} style..."

The function signature automatically defines the prompt's arguments.
The docstring becomes the prompt's description.
"""
