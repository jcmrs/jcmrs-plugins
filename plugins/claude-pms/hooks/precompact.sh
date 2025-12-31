#!/bin/bash
# PreCompact hook for Claude PMS
# Captures session experience before context compaction
# Only runs if enabled in configuration

set -euo pipefail

# Load configuration (sets PMS_TRIGGER_PRECOMPACT environment variable)
source "$CLAUDE_PLUGIN_ROOT/scripts/load-config.sh"

# Check if PreCompact trigger is enabled
if [ "$PMS_TRIGGER_PRECOMPACT" != "true" ]; then
    # Disabled - exit silently
    echo '{
      "continue": true,
      "suppressOutput": true
    }'
    exit 0
fi

# Get project path
PROJECT_PATH="${PMS_PROJECT_PATH:-${CLAUDE_PROJECT_DIR:-$(pwd)}}"

# Call Python encode script
# This will capture the current session experience
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" \
    --project-path "$PROJECT_PATH" \
    --trigger "precompact" \
    || {
        # Non-fatal error - log and continue
        echo '{
          "continue": true,
          "suppressOutput": true,
          "systemMessage": "PMS encoding skipped (error occurred)"
        }'
        exit 0
    }

# Success
echo '{
  "continue": true,
  "suppressOutput": true,
  "systemMessage": "Session experience captured by PMS"
}'
