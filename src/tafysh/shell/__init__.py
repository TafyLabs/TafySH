"""Shell wrapper and user I/O handling."""

from tafysh.shell.completer import (
    CompletionResult,
    CompletionType,
    ShellCompleter,
    get_completer,
    setup_completion,
)
from tafysh.shell.help import (
    HelpCategory,
    HelpSystem,
    HelpTopic,
    get_help_system,
    show_help,
)
from tafysh.shell.history import HistoryEntry, HistoryManager, ReadlineHistory
from tafysh.shell.memory import (
    MemoryEntry,
    MemoryStore,
    format_memory_list,
    forget,
    get_memory_store,
    recall,
    remember,
)
from tafysh.shell.input_classifier import (
    ClassifiedInput,
    InputClassifier,
    InputType,
    SPECIAL_COMMANDS,
    parse_special_command,
)
from tafysh.shell.prompt import (
    AgentStatus,
    Colors,
    PromptContext,
    PromptRenderer,
    PromptStyle,
    strip_ansi,
)
from tafysh.shell.pty_manager import PTYManager
from tafysh.shell.wrapper import ShellWrapper

__all__ = [
    # Wrapper
    "ShellWrapper",
    # PTY Manager
    "PTYManager",
    # Completer
    "CompletionResult",
    "CompletionType",
    "ShellCompleter",
    "get_completer",
    "setup_completion",
    # Input Classifier
    "ClassifiedInput",
    "InputClassifier",
    "InputType",
    "SPECIAL_COMMANDS",
    "parse_special_command",
    # Prompt
    "AgentStatus",
    "Colors",
    "PromptContext",
    "PromptRenderer",
    "PromptStyle",
    "strip_ansi",
    # History
    "HistoryEntry",
    "HistoryManager",
    "ReadlineHistory",
    # Memory
    "MemoryEntry",
    "MemoryStore",
    "format_memory_list",
    "forget",
    "get_memory_store",
    "recall",
    "remember",
    # Help
    "HelpCategory",
    "HelpSystem",
    "HelpTopic",
    "get_help_system",
    "show_help",
]
