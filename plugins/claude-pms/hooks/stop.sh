#!/bin/bash
# Stop hook for Claude PMS
# Captures session experience when Claude stops
# Only runs if enabled in configuration (default: disabled)

set -euo pipefail

# Load configuration (sets PMS_TRIGGER_STOP environment variable)
source "$CLAUDE_PLUGIN_ROOT/scripts/load-config.sh"

# Check if Stop trigger is enabled (usually disabled)
if [ "$PMS_TRIGGER_STOP" != "true" ]; then
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
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" \
    --project-path "$PROJECT_PATH" \
    --trigger "stop" \
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
  "systemMessage": "Session experience captured by PMS (Stop trigger)"
}'
