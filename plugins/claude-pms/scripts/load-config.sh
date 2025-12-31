#!/bin/bash
# Load PMS configuration from project-level pms.local.md
# Parses YAML frontmatter and exports as environment variables
# Falls back to defaults if config missing or invalid

set -euo pipefail

# Get project path (current working directory)
PROJECT_PATH="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_PATH/.claude/pms.local.md"

# Default configuration values
DEFAULT_TRIGGER_PRECOMPACT="true"
DEFAULT_TRIGGER_SESSION_END="true"
DEFAULT_TRIGGER_STOP="false"
DEFAULT_CONTINUOUS_MODE="true"
DEFAULT_AUTO_SYNTHESIZE="false"
DEFAULT_MIN_SESSIONS="10"
DEFAULT_EMERGING_PATTERN="2"
DEFAULT_STRONG_PATTERN="3"
DEFAULT_CRITICAL_PATTERN="5"
DEFAULT_PREFER_CONTEXT="true"
DEFAULT_FALLBACK_JSONL="true"
DEFAULT_REDACT_SENSITIVE="true"
DEFAULT_TIMEOUT_ENCODE="30"
DEFAULT_TIMEOUT_EXTRACT="60"
DEFAULT_TIMEOUT_SYNTHESIZE="45"

# Function to parse YAML value from frontmatter
parse_yaml_value() {
    local key="$1"
    local default="$2"
    local value

    # Extract value from YAML frontmatter (between --- markers)
    value=$(sed -n '/^---$/,/^---$/p' "$CONFIG_FILE" 2>/dev/null | \
            grep -E "^[[:space:]]*${key}:" | \
            sed "s/^[[:space:]]*${key}:[[:space:]]*//" | \
            tr -d '\r\n' || echo "$default")

    # If empty or invalid, use default
    if [ -z "$value" ]; then
        echo "$default"
    else
        echo "$value"
    fi
}

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    # Config doesn't exist - use all defaults
    export PMS_TRIGGER_PRECOMPACT="$DEFAULT_TRIGGER_PRECOMPACT"
    export PMS_TRIGGER_SESSION_END="$DEFAULT_TRIGGER_SESSION_END"
    export PMS_TRIGGER_STOP="$DEFAULT_TRIGGER_STOP"
    export PMS_CONTINUOUS_MODE="$DEFAULT_CONTINUOUS_MODE"
    export PMS_AUTO_SYNTHESIZE="$DEFAULT_AUTO_SYNTHESIZE"
    export PMS_MIN_SESSIONS="$DEFAULT_MIN_SESSIONS"
    export PMS_EMERGING_PATTERN="$DEFAULT_EMERGING_PATTERN"
    export PMS_STRONG_PATTERN="$DEFAULT_STRONG_PATTERN"
    export PMS_CRITICAL_PATTERN="$DEFAULT_CRITICAL_PATTERN"
    export PMS_PREFER_CONTEXT="$DEFAULT_PREFER_CONTEXT"
    export PMS_FALLBACK_JSONL="$DEFAULT_FALLBACK_JSONL"
    export PMS_REDACT_SENSITIVE="$DEFAULT_REDACT_SENSITIVE"
    export PMS_TIMEOUT_ENCODE="$DEFAULT_TIMEOUT_ENCODE"
    export PMS_TIMEOUT_EXTRACT="$DEFAULT_TIMEOUT_EXTRACT"
    export PMS_TIMEOUT_SYNTHESIZE="$DEFAULT_TIMEOUT_SYNTHESIZE"
    export PMS_CONFIG_LOADED="defaults"
else
    # Parse configuration from YAML frontmatter
    export PMS_TRIGGER_PRECOMPACT=$(parse_yaml_value "precompact" "$DEFAULT_TRIGGER_PRECOMPACT")
    export PMS_TRIGGER_SESSION_END=$(parse_yaml_value "session_end" "$DEFAULT_TRIGGER_SESSION_END")
    export PMS_TRIGGER_STOP=$(parse_yaml_value "stop" "$DEFAULT_TRIGGER_STOP")
    export PMS_CONTINUOUS_MODE=$(parse_yaml_value "continuous_mode" "$DEFAULT_CONTINUOUS_MODE")
    export PMS_AUTO_SYNTHESIZE=$(parse_yaml_value "auto_synthesize" "$DEFAULT_AUTO_SYNTHESIZE")
    export PMS_MIN_SESSIONS=$(parse_yaml_value "min_sessions" "$DEFAULT_MIN_SESSIONS")
    export PMS_EMERGING_PATTERN=$(parse_yaml_value "emerging_pattern" "$DEFAULT_EMERGING_PATTERN")
    export PMS_STRONG_PATTERN=$(parse_yaml_value "strong_pattern" "$DEFAULT_STRONG_PATTERN")
    export PMS_CRITICAL_PATTERN=$(parse_yaml_value "critical_pattern" "$DEFAULT_CRITICAL_PATTERN")
    export PMS_PREFER_CONTEXT=$(parse_yaml_value "prefer_context" "$DEFAULT_PREFER_CONTEXT")
    export PMS_FALLBACK_JSONL=$(parse_yaml_value "fallback_jsonl" "$DEFAULT_FALLBACK_JSONL")
    export PMS_REDACT_SENSITIVE=$(parse_yaml_value "redact_sensitive" "$DEFAULT_REDACT_SENSITIVE")
    export PMS_TIMEOUT_ENCODE=$(parse_yaml_value "encode" "$DEFAULT_TIMEOUT_ENCODE")
    export PMS_TIMEOUT_EXTRACT=$(parse_yaml_value "extract" "$DEFAULT_TIMEOUT_EXTRACT")
    export PMS_TIMEOUT_SYNTHESIZE=$(parse_yaml_value "synthesize" "$DEFAULT_TIMEOUT_SYNTHESIZE")
    export PMS_CONFIG_LOADED="file"
fi

# Export project path for use by Python scripts
export PMS_PROJECT_PATH="$PROJECT_PATH"

# Success indicator
export PMS_CONFIG_STATUS="loaded"
