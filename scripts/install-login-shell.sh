#!/usr/bin/env bash
#
# TafySH Login Shell Installer
#
# This script configures TafySH as a valid login shell:
# 1. Adds TafySH to /etc/shells
# 2. Optionally sets it as the default shell for the current user
# 3. Creates initial ~/.tafyshrc configuration
#
# Usage:
#   ./install-login-shell.sh              # Just add to /etc/shells
#   ./install-login-shell.sh --set-default # Also set as default shell
#   ./install-login-shell.sh --uninstall   # Remove from /etc/shells
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info() {
    echo -e "${BLUE}==>${NC} ${BOLD}$1${NC}"
}

success() {
    echo -e "${GREEN}==>${NC} ${BOLD}$1${NC}"
}

warn() {
    echo -e "${YELLOW}Warning:${NC} $1"
}

error() {
    echo -e "${RED}Error:${NC} $1" >&2
}

die() {
    error "$1"
    exit 1
}

# Find TafySH binary
find_tafysh() {
    local tafysh_path=""

    # Check common locations
    if command -v tafysh >/dev/null 2>&1; then
        tafysh_path=$(command -v tafysh)
    elif [[ -x "$HOME/.local/bin/tafysh" ]]; then
        tafysh_path="$HOME/.local/bin/tafysh"
    elif [[ -x "/usr/local/bin/tafysh" ]]; then
        tafysh_path="/usr/local/bin/tafysh"
    elif [[ -x "/usr/bin/tafysh" ]]; then
        tafysh_path="/usr/bin/tafysh"
    fi

    # Resolve symlinks to get absolute path
    if [[ -n "$tafysh_path" ]]; then
        # Use readlink if available, otherwise realpath
        if command -v readlink >/dev/null 2>&1; then
            tafysh_path=$(readlink -f "$tafysh_path" 2>/dev/null || echo "$tafysh_path")
        elif command -v realpath >/dev/null 2>&1; then
            tafysh_path=$(realpath "$tafysh_path" 2>/dev/null || echo "$tafysh_path")
        fi
    fi

    echo "$tafysh_path"
}

# Check if TafySH is in /etc/shells
is_in_shells() {
    local tafysh_path="$1"
    grep -q "^${tafysh_path}$" /etc/shells 2>/dev/null
}

# Add TafySH to /etc/shells
add_to_shells() {
    local tafysh_path="$1"

    if is_in_shells "$tafysh_path"; then
        info "TafySH already in /etc/shells"
        return 0
    fi

    info "Adding TafySH to /etc/shells..."
    echo "$tafysh_path" | sudo tee -a /etc/shells >/dev/null
    success "Added to /etc/shells"
}

# Remove TafySH from /etc/shells
remove_from_shells() {
    local tafysh_path="$1"

    if ! is_in_shells "$tafysh_path"; then
        info "TafySH not in /etc/shells"
        return 0
    fi

    info "Removing TafySH from /etc/shells..."
    sudo sed -i.bak "\|^${tafysh_path}$|d" /etc/shells
    success "Removed from /etc/shells"
}

# Set TafySH as default shell
set_default_shell() {
    local tafysh_path="$1"

    if ! is_in_shells "$tafysh_path"; then
        die "TafySH must be in /etc/shells before setting as default"
    fi

    info "Setting TafySH as default shell..."
    chsh -s "$tafysh_path"
    success "Default shell changed to TafySH"
}

# Restore original shell
restore_shell() {
    local original_shell="${SHELL:-/bin/bash}"

    # Common shells to try
    local shells=("$original_shell" "/bin/bash" "/bin/zsh" "/bin/sh")

    for shell in "${shells[@]}"; do
        if [[ -x "$shell" ]] && grep -q "^${shell}$" /etc/shells 2>/dev/null; then
            info "Restoring shell to $shell..."
            chsh -s "$shell"
            success "Shell restored to $shell"
            return 0
        fi
    done

    warn "Could not restore shell. Please run: chsh -s /bin/bash"
}

# Create default ~/.tafyshrc
create_tafyshrc() {
    local rc_file="$HOME/.tafyshrc"

    if [[ -f "$rc_file" ]]; then
        info "~/.tafyshrc already exists"
        return 0
    fi

    info "Creating ~/.tafyshrc..."
    cat > "$rc_file" << 'EOF'
# TafySH Configuration File
# This file is sourced when TafySH starts in interactive mode.

# Aliases
# alias ll='ls -la'
# alias gs='git status'

# Environment variables for TafySH
# export TAFYSH_LOG_LEVEL=INFO

# Custom prompt (optional)
# export TAFYSH_PROMPT_PREFIX="my-shell"

# Tool registration (advanced)
# :tool register my-tool "Description" "command"

# Welcome message (optional)
# echo "Welcome to TafySH!"
EOF
    success "Created ~/.tafyshrc"
}

# Check system requirements
check_requirements() {
    # Check /etc/shells exists
    if [[ ! -f /etc/shells ]]; then
        die "/etc/shells not found. This system may not support login shells."
    fi

    # Check if we can use sudo
    if ! command -v sudo >/dev/null 2>&1; then
        warn "sudo not available. You may need to run this as root."
    fi

    # Check chsh
    if ! command -v chsh >/dev/null 2>&1; then
        warn "chsh not found. You won't be able to set TafySH as default shell."
    fi
}

# Print usage
usage() {
    cat << EOF
TafySH Login Shell Installer

Usage:
    $0 [options]

Options:
    --set-default    Set TafySH as default shell
    --uninstall      Remove TafySH from /etc/shells
    --restore        Restore original shell
    --help           Show this help message

Examples:
    $0                    # Add to /etc/shells only
    $0 --set-default      # Add and set as default
    $0 --uninstall        # Remove from /etc/shells
EOF
}

# Main
main() {
    local set_default=false
    local uninstall=false
    local restore=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --set-default)
                set_default=true
                shift
                ;;
            --uninstall)
                uninstall=true
                shift
                ;;
            --restore)
                restore=true
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                die "Unknown option: $1"
                ;;
        esac
    done

    echo ""
    echo -e "${BOLD}TafySH Login Shell Installer${NC}"
    echo ""

    check_requirements

    # Find TafySH
    local tafysh_path
    tafysh_path=$(find_tafysh)

    if [[ -z "$tafysh_path" ]]; then
        die "TafySH not found. Please install it first: pip install tafysh"
    fi

    info "Found TafySH: $tafysh_path"

    # Verify it works
    if ! "$tafysh_path" --version >/dev/null 2>&1; then
        die "TafySH binary not working properly"
    fi

    local version
    version=$("$tafysh_path" --version 2>/dev/null || echo "unknown")
    info "Version: $version"
    echo ""

    # Handle uninstall
    if $uninstall; then
        remove_from_shells "$tafysh_path"
        echo ""
        success "TafySH removed from login shells"
        echo ""
        echo "Note: If TafySH was your default shell, run:"
        echo "  chsh -s /bin/bash"
        exit 0
    fi

    # Handle restore
    if $restore; then
        restore_shell
        exit 0
    fi

    # Install
    add_to_shells "$tafysh_path"
    create_tafyshrc

    # Set as default if requested
    if $set_default; then
        echo ""
        set_default_shell "$tafysh_path"
    fi

    echo ""
    success "Installation complete!"
    echo ""
    echo "TafySH is now a valid login shell."
    echo ""
    echo "Next steps:"
    if ! $set_default; then
        echo "  - Set as default shell: chsh -s $tafysh_path"
    fi
    echo "  - Customize: vim ~/.tafyshrc"
    echo "  - Start now: tafysh"
    echo ""

    # PAM notes
    echo -e "${BOLD}PAM Integration Notes:${NC}"
    echo "  - TafySH uses standard exit codes for PAM compatibility"
    echo "  - Environment from /etc/environment and pam_env is loaded"
    echo "  - Resource limits from /etc/security/limits.conf are respected"
    echo ""

    # Sudo notes
    echo -e "${BOLD}Sudo Notes:${NC}"
    echo "  - 'sudo -s' will spawn TafySH"
    echo "  - 'sudo -i' will run TafySH as login shell"
    echo "  - Add TAFYSH env vars to /etc/sudoers Defaults env_keep if needed"
    echo ""
}

main "$@"
