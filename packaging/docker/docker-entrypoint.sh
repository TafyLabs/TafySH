#!/bin/bash
set -e

# Install package in editable mode if pyproject.toml exists
if [ -f /app/pyproject.toml ]; then
    echo "Installing TafySH in editable mode..."
    pip install -e /app[dev] --quiet
fi

# Add to /etc/shells if not present
TAFYSH_PATH="/usr/local/bin/tafysh"
if [ -x "$TAFYSH_PATH" ] && ! grep -q "^${TAFYSH_PATH}$" /etc/shells 2>/dev/null; then
    echo "$TAFYSH_PATH" >> /etc/shells
fi

exec "$@"
