# Fish completion for TafySH
# Install: cp tafysh.fish ~/.config/fish/completions/
# Or: cp tafysh.fish /usr/share/fish/vendor_completions.d/

# Disable file completions by default
complete -c tafysh -f

# Global options
complete -c tafysh -s h -l help -d 'Show help message'
complete -c tafysh -l version -d 'Show version'
complete -c tafysh -l debug -d 'Enable debug mode'
complete -c tafysh -s q -l quiet -d 'Suppress output'
complete -c tafysh -l no-color -d 'Disable color output'
complete -c tafysh -s c -l config -d 'Configuration file' -r -F
complete -c tafysh -s m -l model -d 'Model to use' -xa 'claude-3-5-sonnet-latest claude-sonnet-4-20250514 gpt-4o gpt-4-turbo llama3.2 mistral'
complete -c tafysh -s p -l provider -d 'LLM provider' -xa 'anthropic openai ollama openrouter litellm'

# Commands
complete -c tafysh -n __fish_use_subcommand -a config -d 'Manage configuration'
complete -c tafysh -n __fish_use_subcommand -a status -d 'Show status'
complete -c tafysh -n __fish_use_subcommand -a version -d 'Show version'
complete -c tafysh -n __fish_use_subcommand -a help -d 'Show help'

# Config subcommands
complete -c tafysh -n '__fish_seen_subcommand_from config' -a init -d 'Initialize configuration'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a show -d 'Show current configuration'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a edit -d 'Edit configuration file'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a reset -d 'Reset to defaults'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a import -d 'Import configuration'
complete -c tafysh -n '__fish_seen_subcommand_from config' -a export -d 'Export configuration'

# Enable file completion for import/export
complete -c tafysh -n '__fish_seen_subcommand_from import export' -F
