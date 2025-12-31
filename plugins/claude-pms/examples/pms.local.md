---
# Claude PMS Configuration
#
# This file configures the Procedural Memory System behavior for this project.
# All settings are optional - defaults will be used if not specified.

# === Trigger Configuration ===
# Control when PMS automatically encodes sessions
triggers:
  # Encode before context compaction (recommended: true)
  precompact: true

  # Encode at session end (recommended: true)
  session_end: true

  # Encode when Claude stops (optional, default: false)
  # May capture incomplete sessions
  stop: false

# === Processing Modes ===
# Control automatic vs manual processing
processing:
  # Auto-extract patterns after encoding (recommended: true)
  # Enables continuous learning without manual /pms:extract
  continuous_mode: true

  # Auto-synthesize rules after extraction (recommended: false)
  # Requires user approval if false, automatic if true
  auto_synthesize: false

# === Pattern Detection Thresholds ===
# Control when patterns are detected and rules generated
thresholds:
  # Minimum sessions before attempting extraction (default: 10)
  min_sessions: 10

  # Occurrence counts for pattern strength
  emerging_pattern: 2   # 2+ occurrences = emerging pattern
  strong_pattern: 3     # 3+ occurrences = worthy of procedural rule
  critical_pattern: 5   # 5+ occurrences = high priority

# === Encoding Behavior ===
# Control how session experiences are captured
encoding:
  # Prefer conversation context over JSONL transcript (recommended: true)
  # More accurate but requires intact context
  prefer_context: true

  # Use JSONL transcript as fallback if context unavailable
  fallback_jsonl: true

# === Privacy Configuration ===
# Control sensitive data redaction
privacy:
  # Auto-redact sensitive patterns (recommended: true)
  redact_sensitive: true

  # Additional regex patterns to redact (beyond defaults)
  # Defaults already include: API keys, passwords, tokens, credentials
  custom_redaction_patterns:
    - "secret[_-]?key"
    - "auth[_-]?token"
    # Add project-specific patterns here

# === Performance ===
# Timeouts for long-running operations
timeouts:
  # Episodic encoding timeout (seconds)
  encode: 30

  # Semantic extraction timeout (seconds)
  extract: 60

  # Procedural synthesis timeout (seconds)
  synthesize: 45
---

# Claude PMS - Procedural Memory System

This project uses Claude PMS to learn from your coding sessions and generate project-scoped rules.

## Quick Start

1. **Automatic Learning:** PMS will automatically capture session experiences on PreCompact and SessionEnd events
2. **Manual Reflection:** Run `/pms:reflect` to analyze patterns and generate rules
3. **Check Status:** Run `/pms:status` to see memory state

## Configuration

Edit the YAML frontmatter above to customize:
- **Triggers:** When to capture sessions
- **Continuous Mode:** Auto-extract patterns vs manual
- **Thresholds:** How many occurrences = pattern
- **Privacy:** What data to redact

## Commands

- `/pms:encode` - Manually capture current session
- `/pms:reflect` - Full pipeline: extract patterns + generate rules
- `/pms:extract` - Extract patterns only (no rule generation)
- `/pms:synthesize` - Generate rules from detected patterns
- `/pms:status` - Show current memory state
- `/pms:config` - Open this configuration file

## Memory Structure

```
.claude/
├── pms/                          # PMS memory storage
│   ├── episodic/                 # Session experiences
│   ├── semantic/                 # Detected patterns
│   ├── procedural/               # Rule metadata
│   └── metadata/                 # System state
└── rules/pms/                    # Generated rules (loaded automatically)
```

## Privacy

All sensitive data (API keys, passwords, tokens, credentials) is automatically redacted before storage.

## Restart Required

After rules are generated, restart your Claude Code session to load the new rules.
