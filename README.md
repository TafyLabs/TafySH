# TafySH

**AI-Enhanced Terminal Shell with LLM-Powered Capabilities**

TafySH wraps traditional shells (Bash/Zsh/Fish) with intelligent features:

- Natural language to command translation
- Multi-step autonomous task execution
- Multi-device orchestration (servers, robots, IoT)
- Strong security with human-in-the-loop
- Memory and context management

## Installation

Requires [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# From PyPI (when released)
uv pip install tafysh

# From source
git clone https://github.com/TafyLabs/TafySH.git
cd TafySH
uv sync
uv pip install -e ".[dev]"
```

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Start TafySH
uv run tafysh

# Or with custom config
uv run tafysh --config ~/.tafysh/config.yaml
```

## Usage

Inside the TafySH shell:

```bash
# Regular shell commands work normally
ls -la
git status

# AI-powered requests (prefix with 'ai ')
ai list all python files modified today
ai explain what this git command does: git rebase -i HEAD~3
ai help me set up a Python virtual environment

# Force shell execution (prefix with !)
!echo "force shell mode"
```

## Configuration

Create `~/.tafysh/config.yaml`:

```yaml
llm:
  provider: anthropic
  model: claude-sonnet-4-20250514

shell:
  backend: zsh
  ai_prefix: "ai "

security:
  mode: normal
  require_confirmation: true

log_level: INFO
```

See `examples/config.yaml` for full options.

## Development

```bash
# Install dev dependencies
make dev

# Or manually with uv
uv pip install -e ".[dev,all]"

# Run tests
make test

# Run linters
make lint

# Run type checks
make type-check

# Run all checks
make check

# Sync dependencies
make sync

# Update lock file
make lock
```

## Architecture

TafySH is built with a modular architecture:

```
tafysh/
├── shell/         # User I/O, PTY management
├── agent/         # LLM client, planning, execution
├── tools/         # Tool interface, registry
├── workflows/     # LangGraph orchestration
├── memory/        # Session & persistent storage
├── security/      # Risk classification, RBAC
├── telemetry/     # Logging, metrics, health
├── orchestrator/  # Multi-device, SSH, MCP
├── plugins/       # Extensible toolsets
└── config/        # Configuration management
```

See [docs/ARCHITECTURE_SUMMARY.md](docs/ARCHITECTURE_SUMMARY.md) for details.

## Implementation Status

| Phase | Component | Status |
|-------|-----------|--------|
| 0 | Foundation | ✅ Complete |
| 1 | Shell Wrapper | ✅ Complete |
| 2 | LLM Integration | ✅ Complete |
| 3 | Security | ✅ Complete |
| 4 | Tool Interface | ✅ Complete |
| 5 | Workflows | ✅ Complete |
| 6 | Memory | ✅ Complete |
| 7 | Telemetry | ✅ Complete |
| 8 | Orchestration | ✅ Complete |
| 9 | Robotics | ✅ Complete |
| 10 | Polish | ✅ Complete |
| 11 | Testing & Coverage | ✅ Complete |
| 12 | Release & Distribution | ✅ Complete |

See [docs/IMPLEMENTATION_CHECKLIST.md](docs/IMPLEMENTATION_CHECKLIST.md) for details.

## Security

TafySH includes multiple security layers:

- **Risk Classification**: Commands classified as SAFE, MEDIUM, HIGH, CRITICAL
- **RBAC**: Role-based access control (VIEWER, OPERATOR, ADMIN)
- **Human-in-the-Loop**: Approval required for dangerous operations
- **Audit Logging**: All actions logged for compliance

## Contributing

Contributions are welcome! Please read the documentation and submit PRs.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
