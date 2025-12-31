#!/bin/bash
# SessionStart hook for Claude PMS
# Initializes PMS directory structure and loads configuration
# Runs at the start of every Claude Code session

set -euo pipefail

# Get project path
PROJECT_PATH="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PMS_DIR="$PROJECT_PATH/.claude/pms"
CONFIG_FILE="$PROJECT_PATH/.claude/pms.local.md"

# Create PMS directory structure if it doesn't exist
if [ ! -d "$PMS_DIR" ]; then
    mkdir -p "$PMS_DIR/episodic"
    mkdir -p "$PMS_DIR/semantic"
    mkdir -p "$PMS_DIR/procedural"
    mkdir -p "$PMS_DIR/metadata"

    # Create empty index files
    echo '{}' > "$PMS_DIR/episodic/index.json"
    echo '{}' > "$PMS_DIR/metadata/processed.json"
fi

# Create rules directory if it doesn't exist
RULES_DIR="$PROJECT_PATH/.claude/rules/pms"
if [ ! -d "$RULES_DIR" ]; then
    mkdir -p "$RULES_DIR"
fi

# Copy default configuration if it doesn't exist
if [ ! -f "$CONFIG_FILE" ]; then
    # Copy from plugin examples
    if [ -f "$CLAUDE_PLUGIN_ROOT/examples/pms.local.md" ]; then
        cp "$CLAUDE_PLUGIN_ROOT/examples/pms.local.md" "$CONFIG_FILE"
    fi
fi

# Load configuration and export environment variables
source "$CLAUDE_PLUGIN_ROOT/scripts/load-config.sh"

# Output success message (visible in transcript if not suppressed)
echo '{
  "continue": true,
  "suppressOutput": true,
  "systemMessage": "Claude PMS initialized - Learning from this session"
}'
