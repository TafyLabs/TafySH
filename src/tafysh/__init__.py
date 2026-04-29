"""
TafySH - AI-enhanced terminal shell with LLM-powered capabilities.

TafySH wraps traditional shells (Bash/Zsh/Fish) with intelligent features:
- Natural language to command translation
- Multi-step autonomous task execution
- Multi-device orchestration
- Strong security with human-in-the-loop
- Memory and context management
"""

__version__ = "0.2.3"
__author__ = "Bobby Larson"

from tafysh.config.schemas import TafySHConfig

__all__ = [
    "__version__",
    "TafySHConfig",
]
