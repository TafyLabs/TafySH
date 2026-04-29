"""Agent Factory - Creates and configures agent instances."""

import asyncio
from typing import Any, Callable, Optional

from tafysh.agent.agent_loop import AgentConfig, AgentContext, AgentLoop
from tafysh.agent.llm_client import LLMClient
from tafysh.agent.providers.anthropic import AnthropicClient
from tafysh.agent.providers.openai import OpenAIClient
from tafysh.config.schemas import TafySHConfig, LLMProvider
from tafysh.memory.manager import MemoryManager
from tafysh.security.controller import SecurityController
from tafysh.telemetry.logger import get_logger
from tafysh.tools.registry import ToolRegistry
from tafysh.workflows.executor import WorkflowExecutor

logger = get_logger(__name__)


def create_llm_client(config: TafySHConfig) -> LLMClient:
    """Create an LLM client based on configuration.

    Args:
        config: TafySH configuration

    Returns:
        Configured LLM client

    Raises:
        ValueError: If provider is not supported
    """
    if config.llm.provider == LLMProvider.ANTHROPIC:
        return AnthropicClient(
            api_key=config.llm.api_key,
            model=config.llm.model,
            timeout=config.llm.timeout_seconds,
        )
    elif config.llm.provider == LLMProvider.OPENAI:
        return OpenAIClient(
            api_key=config.llm.api_key,
            model=config.llm.model,
            timeout=config.llm.timeout_seconds,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.llm.provider}")


def create_agent_loop(
    config: TafySHConfig,
    tool_registry: Optional[ToolRegistry] = None,
) -> AgentLoop:
    """Create a fully configured agent loop.

    Args:
        config: TafySH configuration
        tool_registry: Optional pre-configured tool registry

    Returns:
        Configured AgentLoop
    """
    llm_client = create_llm_client(config)

    if tool_registry is None:
        tool_registry = ToolRegistry()
        # Register default tools (Phase 4)
        # For now, create empty registry

    agent_config = AgentConfig(
        max_steps=10,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
        timeout=30.0,
    )

    return AgentLoop(
        llm_client=llm_client,
        tool_registry=tool_registry,
        config=agent_config,
    )


def create_ai_handler(config: TafySHConfig) -> callable:
    """Create an AI handler function for the shell wrapper.

    This creates a synchronous handler that can be used with ShellWrapper.

    Args:
        config: TafySH configuration

    Returns:
        Handler function that takes request string and returns response
    """
    agent = create_agent_loop(config)

    def handler(request: str) -> str:
        """Handle an AI request synchronously."""
        # Run the async agent in a new event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                context = AgentContext(
                    cwd=str(config.shell.cwd) if hasattr(config.shell, 'cwd') else "",
                )
                result = loop.run_until_complete(agent.invoke(request, context))

                if result.success:
                    return result.response
                else:
                    return f"Error: {result.error}\n\n{result.response}"
            finally:
                loop.close()
        except Exception as e:
            logger.error("AI handler error", error=str(e))
            return f"AI Error: {str(e)}"

    return handler


async def create_async_ai_handler(config: TafySHConfig) -> Callable:
    """Create an async AI handler function.

    Args:
        config: TafySH configuration

    Returns:
        Async handler function
    """
    agent = create_agent_loop(config)

    async def handler(request: str) -> str:
        """Handle an AI request asynchronously."""
        context = AgentContext()
        result = await agent.invoke(request, context)

        if result.success:
            return result.response
        else:
            return f"Error: {result.error}\n\n{result.response}"

    return handler


def create_memory_manager(
    config: TafySHConfig,
    db_path: Optional[str] = None,
) -> MemoryManager:
    """Create a memory manager instance.

    Args:
        config: TafySH configuration
        db_path: Optional custom database path

    Returns:
        Configured MemoryManager
    """
    # Use config memory path or default
    memory_db_path = db_path or "~/.tafysh/memory.db"

    return MemoryManager(db_path=memory_db_path)


def create_workflow_executor(
    config: TafySHConfig,
    tool_registry: Optional[ToolRegistry] = None,
    security_controller: Optional[SecurityController] = None,
    memory_manager: Optional[MemoryManager] = None,
) -> WorkflowExecutor:
    """Create a workflow executor with LangGraph support.

    Args:
        config: TafySH configuration
        tool_registry: Optional pre-configured tool registry
        security_controller: Optional security controller
        memory_manager: Optional memory manager for context

    Returns:
        Configured WorkflowExecutor
    """
    llm_client = create_llm_client(config)

    if tool_registry is None:
        tool_registry = ToolRegistry()

    return WorkflowExecutor(
        llm_client=llm_client,
        tool_registry=tool_registry,
        security_controller=security_controller,
        memory_manager=memory_manager,
        max_steps=10,
        tool_timeout=30.0,
    )


def create_workflow_handler(
    config: TafySHConfig,
    tool_registry: Optional[ToolRegistry] = None,
    security_controller: Optional[SecurityController] = None,
    memory_manager: Optional[MemoryManager] = None,
) -> Callable[[str], str]:
    """Create a workflow-based AI handler for the shell.

    Uses LangGraph workflows instead of simple agent loop.

    Args:
        config: TafySH configuration
        tool_registry: Optional tool registry
        security_controller: Optional security controller
        memory_manager: Optional memory manager

    Returns:
        Handler function that takes request and returns response
    """
    executor = create_workflow_executor(
        config, tool_registry, security_controller, memory_manager
    )

    def handler(request: str) -> str:
        """Handle an AI request using workflows."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                context = {
                    "cwd": str(config.shell.cwd) if hasattr(config.shell, 'cwd') else "",
                }
                result = loop.run_until_complete(executor.execute(request, context))

                if result.success:
                    return result.response
                else:
                    return f"Error: {result.error}\n\n{result.response}"
            finally:
                loop.close()
        except Exception as e:
            logger.error("Workflow handler error", error=str(e))
            return f"Workflow Error: {str(e)}"

    return handler


async def create_async_workflow_handler(
    config: TafySHConfig,
    tool_registry: Optional[ToolRegistry] = None,
    security_controller: Optional[SecurityController] = None,
    memory_manager: Optional[MemoryManager] = None,
) -> Callable[[str], Any]:
    """Create an async workflow handler.

    Args:
        config: TafySH configuration
        tool_registry: Optional tool registry
        security_controller: Optional security controller
        memory_manager: Optional memory manager

    Returns:
        Async handler function
    """
    executor = create_workflow_executor(
        config, tool_registry, security_controller, memory_manager
    )

    async def handler(request: str) -> str:
        """Handle an AI request asynchronously using workflows."""
        result = await executor.execute(request)

        if result.success:
            return result.response
        else:
            return f"Error: {result.error}\n\n{result.response}"

    return handler
