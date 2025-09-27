"""Logging utilities for MCP server."""

import logging
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration for the MCP server.

    NOTE: When using stdio transport, console logging can interfere with MCP protocol.
    Use file logging or MCP context logging instead.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid conflicts
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add file handler if specified (recommended for stdio transport)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    else:
        # Only add console handler if no file logging and not using stdio
        # This should be avoided when using stdio transport
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # Set specific logger levels
    logging.getLogger("mcp").setLevel(log_level)
    logging.getLogger("mcp_template").setLevel(log_level)

    # Suppress noisy third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def setup_file_logging(log_file: str = "mcp-template.log", level: str = "INFO") -> None:
    """Setup file-only logging (recommended for stdio transport)."""
    setup_logging(level=level, log_file=log_file)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)


class MCPContextLogger:
    """Helper for logging through MCP context to avoid stdio conflicts."""

    def __init__(self, ctx: Context[ServerSession, any], component: str = "server"):
        self.ctx = ctx
        self.component = component

    async def debug(self, message: str) -> None:
        """Log debug message through MCP context."""
        await self.ctx.debug(f"[{self.component}] {message}")

    async def info(self, message: str) -> None:
        """Log info message through MCP context."""
        await self.ctx.info(f"[{self.component}] {message}")

    async def warning(self, message: str) -> None:
        """Log warning message through MCP context."""
        await self.ctx.warning(f"[{self.component}] {message}")

    async def error(self, message: str) -> None:
        """Log error message through MCP context."""
        await self.ctx.error(f"[{self.component}] {message}")

    async def notice(self, message: str) -> None:
        """Log notice message through MCP context."""
        await self.ctx.notice(f"[{self.component}] {message}")


def create_mcp_logger(ctx: Context[ServerSession, any], component: str = "server") -> MCPContextLogger:
    """Create an MCP context logger."""
    return MCPContextLogger(ctx, component)


# File logging helpers
def ensure_log_directory(log_file: str) -> str:
    """Ensure log directory exists and return full path."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return str(log_path.absolute())


def get_default_log_file() -> str:
    """Get default log file path."""
    return ensure_log_directory("logs/mcp-template.log")
