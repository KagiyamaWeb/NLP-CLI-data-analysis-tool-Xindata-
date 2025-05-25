#!/bin/bash
set -eo pipefail

# Help message
show_help() {
    echo "Usage: ${0##*/} [QUERY]"
    echo "Example: ./analyze.sh \"Какой процент экспертов выполнил меньше 100 проектов?\""
}

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Load environment with proper quoting handling
export $(grep -v '^#' .env | xargs)

# Execute with query
python main.py "$@"
