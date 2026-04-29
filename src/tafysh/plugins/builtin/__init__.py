"""Built-in plugins for TafySH."""

from tafysh.plugins.builtin.code import CodeToolset
from tafysh.plugins.builtin.filesystem import FilesystemToolset
from tafysh.plugins.builtin.process import ProcessToolset
from tafysh.plugins.builtin.shell import ShellToolset

__all__ = [
    "CodeToolset",
    "FilesystemToolset",
    "ProcessToolset",
    "ShellToolset",
]
