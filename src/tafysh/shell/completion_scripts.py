"""Shell completion script generation for TafySH.

Generates completion scripts for bash, zsh, and fish that can be
installed for use when TafySH is invoked as a command (not as a shell).
"""

import os
from pathlib import Path
from typing import Tuple

from tafysh import __version__


def get_bash_completion() -> str:
    """Generate bash completion script.

    Returns:
        Bash completion script content
    """
    return f'''# Bash completion for TafySH v{__version__}
# Install: tafysh completions bash > /etc/bash_completion.d/tafysh
# Or: tafysh completions bash >> ~/.bashrc

_tafysh_completions() {{
    local cur prev words cword
    _init_completion || return

    local commands="config status completions devices help"
    local config_commands="init show edit reset"
    local devices_commands="list add remove status"
    local completions_shells="bash zsh fish"
    local global_opts="--help --version --config --log-level --login --norc --noprofile --rcfile --mcp-server --profile-startup"

    case "${{prev}}" in
        tafysh)
            COMPREPLY=($(compgen -W "${{commands}} ${{global_opts}}" -- "${{cur}}"))
            return
            ;;
        config)
            COMPREPLY=($(compgen -W "${{config_commands}}" -- "${{cur}}"))
            return
            ;;
        completions)
            COMPREPLY=($(compgen -W "${{completions_shells}}" -- "${{cur}}"))
            return
            ;;
        devices)
            COMPREPLY=($(compgen -W "${{devices_commands}}" -- "${{cur}}"))
            return
            ;;
        --config|--rcfile)
            _filedir
            return
            ;;
        --log-level)
            COMPREPLY=($(compgen -W "DEBUG INFO WARNING ERROR" -- "${{cur}}"))
            return
            ;;
        bash|zsh|fish)
            COMPREPLY=($(compgen -W "--install" -- "${{cur}}"))
            return
            ;;
    esac

    case "${{cur}}" in
        -*)
            COMPREPLY=($(compgen -W "${{global_opts}}" -- "${{cur}}"))
            return
            ;;
    esac

    # Default to file completion
    _filedir
}}

complete -F _tafysh_completions tafysh
'''


def get_zsh_completion() -> str:
    """Generate zsh completion script.

    Returns:
        Zsh completion script content
    """
    return f'''#compdef tafysh

# Zsh completion for TafySH v{__version__}
# Install: tafysh completions zsh > /usr/share/zsh/site-functions/_tafysh
# Or: Place in a directory in your $fpath

_tafysh() {{
    local context state state_descr line
    typeset -A opt_args

    local -a commands
    commands=(
        'config:Manage configuration'
        'status:Show status'
        'completions:Generate shell completions'
        'devices:Device management'
        'help:Show help'
    )

    local -a config_commands
    config_commands=(
        'init:Initialize configuration'
        'show:Show current configuration'
        'edit:Edit configuration file'
        'reset:Reset to defaults'
    )

    local -a devices_commands
    devices_commands=(
        'list:List all devices'
        'add:Add a device'
        'remove:Remove a device'
        'status:Check device status'
    )

    local -a global_opts
    global_opts=(
        '--help[Show help message]'
        '--version[Show version]'
        '--config[Configuration file]:file:_files -g "*.yaml"'
        '--log-level[Log level]:level:(DEBUG INFO WARNING ERROR)'
        '(-l --login)'{{'{{-l,--login}}'}}'[Run as login shell]'
        '--norc[Skip rc files]'
        '--noprofile[Skip profile files]'
        '--rcfile[Custom RC file]:file:_files'
        '--mcp-server[Run as MCP server]'
        '--profile-startup[Profile startup time]'
    )

    _arguments -C \\
        "${{global_opts[@]}}" \\
        '1: :->command' \\
        '*:: :->args'

    case $state in
        command)
            _describe -t commands 'tafysh command' commands
            ;;
        args)
            case $words[1] in
                config)
                    if (( CURRENT == 2 )); then
                        _describe -t commands 'config command' config_commands
                    fi
                    ;;
                completions)
                    if (( CURRENT == 2 )); then
                        _values 'shell' bash zsh fish
                    elif (( CURRENT == 3 )); then
                        _values 'options' '--install[Install to system]'
                    fi
                    ;;
                devices)
                    if (( CURRENT == 2 )); then
                        _describe -t commands 'devices command' devices_commands
                    elif [[ $words[2] == "add" ]]; then
                        _hosts
                    fi
                    ;;
            esac
            ;;
    esac
}}

_tafysh "$@"
'''


def get_fish_completion() -> str:
    """Generate fish completion script.

    Returns:
        Fish completion script content
    """
    return f'''# Fish completion for TafySH v{__version__}
# Install: tafysh completions fish > ~/.config/fish/completions/tafysh.fish

# Disable file completions by default
complete -c tafysh -f

# Global options
complete -c tafysh -s h -l help -d 'Show help message'
complete -c tafysh -l version -d 'Show version'
complete -c tafysh -l config -d 'Configuration file' -r -F
complete -c tafysh -l log-level -d 'Log level' -xa 'DEBUG INFO WARNING ERROR'
complete -c tafysh -s l -l login -d 'Run as login shell'
complete -c tafysh -l norc -d 'Skip rc files'
complete -c tafysh -l noprofile -d 'Skip profile files'
complete -c tafysh -l rcfile -d 'Custom RC file' -r -F
complete -c tafysh -l mcp-server -d 'Run as MCP server'
complete -c tafysh -l profile-startup -d 'Profile startup time'

# Commands
complete -c tafysh -n __fish_use_subcommand -a config -d 'Manage configuration'
complete -c tafysh -n __fish_use_subcommand -a status -d 'Show status'
complete -c tafysh -n __fish_use_subcommand -a completions -d 'Generate shell completions'
complete -c tafysh -n __fish_use_subcommand -a devices -d 'Device management'
complete -c tafysh -n __fish_use_subcommand -a help -d 'Show help'

# Config subcommands
complete -c tafysh -n '__fish_seen_subcommand_from config' -a init -d 'Initialize configuration'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a show -d 'Show current configuration'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a edit -d 'Edit configuration file'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a reset -d 'Reset to defaults'

# Completions subcommands
complete -c tafysh -n '__fish_seen_subcommand_from completions' -a bash -d 'Generate bash completions'
complete -c tafysh -n '__fish_seen_subcommand_from completions' -a zsh -d 'Generate zsh completions'
complete -c tafysh -n '__fish_seen_subcommand_from completions' -a fish -d 'Generate fish completions'
complete -c tafysh -n '__fish_seen_subcommand_from completions; and __fish_seen_subcommand_from bash zsh fish' -l install -d 'Install completions'

# Devices subcommands
complete -c tafysh -n '__fish_seen_subcommand_from devices' -a list -d 'List all devices'
complete -c tafysh -n '__fish_seen_subcommand_from devices' -a add -d 'Add a device'
complete -c tafysh -n '__fish_seen_subcommand_from devices' -a remove -d 'Remove a device'
complete -c tafysh -n '__fish_seen_subcommand_from devices' -a status -d 'Check device status'
'''


def install_completion(shell: str, script: str) -> Tuple[bool, str]:
    """Install completion script to appropriate location.

    Args:
        shell: Shell type (bash, zsh, fish)
        script: Completion script content

    Returns:
        Tuple of (success, path_or_error)
    """
    home = Path.home()

    # Determine installation path
    if shell == "bash":
        # Try system-wide first, then user
        paths = [
            Path("/etc/bash_completion.d/tafysh"),
            Path("/usr/share/bash-completion/completions/tafysh"),
            home / ".local" / "share" / "bash-completion" / "completions" / "tafysh",
        ]
    elif shell == "zsh":
        paths = [
            Path("/usr/share/zsh/site-functions/_tafysh"),
            Path("/usr/local/share/zsh/site-functions/_tafysh"),
            home / ".zsh" / "completions" / "_tafysh",
        ]
    elif shell == "fish":
        paths = [
            Path("/usr/share/fish/vendor_completions.d/tafysh.fish"),
            home / ".config" / "fish" / "completions" / "tafysh.fish",
        ]
    else:
        return False, f"Unknown shell: {shell}"

    # Try each path
    for path in paths:
        try:
            # Try to create parent directory
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write the script
            path.write_text(script)
            return True, str(path)
        except PermissionError:
            continue
        except Exception as e:
            continue

    # All paths failed
    return False, f"Could not write to any of: {', '.join(str(p) for p in paths)}"


def get_completion_script(shell: str) -> str:
    """Get completion script for specified shell.

    Args:
        shell: Shell type (bash, zsh, fish)

    Returns:
        Completion script content

    Raises:
        ValueError: If shell is not supported
    """
    if shell == "bash":
        return get_bash_completion()
    elif shell == "zsh":
        return get_zsh_completion()
    elif shell == "fish":
        return get_fish_completion()
    else:
        raise ValueError(f"Unsupported shell: {shell}")
