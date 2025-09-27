#!/usr/bin/env python3
"""Main entry point for the MCP template server."""

import sys
import click

from .helpers.logging import setup_logging, setup_file_logging, get_default_log_file
from .server import create_server


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio"]),
    default="stdio",
    help="Transport type to use (default: stdio)",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Logging level (default: INFO)",
)
@click.option(
    "--log-file",
    type=click.Path(),
    help="Log file path (default: logs/mcp-template.log for stdio, stderr otherwise)",
)
@click.option(
    "--enable-file-logging",
    is_flag=True,
    default=False,
    help="Enable file logging (recommended for stdio transport to avoid conflicts)",
)
def main(
    transport: str,
    log_level: str,
    log_file: str | None,
    enable_file_logging: bool,
) -> None:
    """Run the MCP template server with advanced MCP features."""
    
    # For stdio transport, use file logging by default to avoid conflicts
    if transport == "stdio":
        if enable_file_logging or log_file:
            log_file_path = log_file or get_default_log_file()
            setup_file_logging(log_file_path, log_level)
            click.echo(f"📝 File logging enabled: {log_file_path}", err=True)
        else:
            # Warn about stdio conflicts but don't force file logging
            setup_logging(level=log_level)
            click.echo("⚠️  Warning: Console logging with stdio transport may cause conflicts.", err=True)
            click.echo("💡 Use --enable-file-logging to avoid issues.", err=True)
    else:
        setup_logging(level=log_level, log_file=log_file)
    
    # Create the server
    server = create_server()
    
    try:
        click.echo("🚀 Starting MCP template server with advanced features...", err=True)
        click.echo("📋 Available features:", err=True)
        click.echo("   • MCP Context Logging", err=True)
        click.echo("   • Elicitation (user input)", err=True)
        click.echo("   • AI Completions & Sampling", err=True)
        click.echo("   • Notifications", err=True)
        click.echo("   • Session Management", err=True)
        click.echo("   • Authentication Helpers", err=True)
        click.echo("", err=True)
        
        # FastMCP handles the transport automatically
        server.run()
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped by user", err=True)
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
