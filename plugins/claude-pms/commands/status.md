---
name: pms:status
description: Display current PMS memory state and configuration
---

# PMS Memory Status

View the current state of procedural memory across all tiers.

## What This Shows

1. **Episodic Memory**: Session records captured
2. **Semantic Memory**: Patterns detected and categorized
3. **Procedural Memory**: Rules generated and active
4. **Configuration**: Current thresholds and triggers
5. **Timeline**: Last encoding, extraction, synthesis timestamps

## Usage

```bash
#!/bin/bash

# Configuration
PROJECT_DIR="${CLAUDE_PROJECT_DIR}"
PMS_DIR="$PROJECT_DIR/.claude/pms"

echo "=== Claude PMS - Procedural Memory System ==="
echo ""

# 1. Episodic Memory Status
echo "📝 Episodic Memory (Sessions Recorded)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

EPISODIC_DIR="$PMS_DIR/episodic"
if [ -d "$EPISODIC_DIR" ]; then
  SESSION_COUNT=$(find "$EPISODIC_DIR" -name "sessions-*.json" -exec jq '.sessions | length' {} + | awk '{s+=$1} END {print s}')
  MONTHLY_FILES=$(find "$EPISODIC_DIR" -name "sessions-*.json" | wc -l)

  echo "Total Sessions: ${SESSION_COUNT:-0}"
  echo "Monthly Files: ${MONTHLY_FILES:-0}"

  # Last encoded
  if [ -f "$EPISODIC_DIR/index.json" ]; then
    LAST_SESSION=$(jq -r 'to_entries | max_by(.key) | .key' "$EPISODIC_DIR/index.json" 2>/dev/null || echo "Unknown")
    echo "Last Encoded: $LAST_SESSION"
  fi
else
  echo "Status: Not initialized"
fi

echo ""

# 2. Semantic Memory Status
echo "🧠 Semantic Memory (Patterns Detected)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SEMANTIC_DIR="$PMS_DIR/semantic"
if [ -f "$SEMANTIC_DIR/patterns.json" ]; then
  TOTAL_PATTERNS=$(jq -r '.count // 0' "$SEMANTIC_DIR/patterns.json")
  EMERGING=$(jq '[.patterns[] | select(.strength == "emerging")] | length' "$SEMANTIC_DIR/patterns.json")
  STRONG=$(jq '[.patterns[] | select(.strength == "strong")] | length' "$SEMANTIC_DIR/patterns.json")
  CRITICAL=$(jq '[.patterns[] | select(.strength == "critical")] | length' "$SEMANTIC_DIR/patterns.json")

  echo "Total Patterns: $TOTAL_PATTERNS"
  echo "  • Emerging (2+ occurrences): $EMERGING"
  echo "  • Strong (3+ occurrences): $STRONG"
  echo "  • Critical (5+ occurrences): $CRITICAL"

  # Breakdown by category
  PREFERENCES=$(jq -r '.count // 0' "$SEMANTIC_DIR/preferences.json" 2>/dev/null || echo "0")
  CODE_PATTERNS=$(jq -r '.count // 0' "$SEMANTIC_DIR/code-patterns.json" 2>/dev/null || echo "0")
  ANTI_PATTERNS=$(jq -r '.count // 0' "$SEMANTIC_DIR/anti-patterns.json" 2>/dev/null || echo "0")

  echo ""
  echo "By Category:"
  echo "  • User Preferences: $PREFERENCES"
  echo "  • Code Patterns: $CODE_PATTERNS"
  echo "  • Anti-Patterns: $ANTI_PATTERNS"

  LAST_EXTRACTION=$(jq -r '.last_updated // "Unknown"' "$SEMANTIC_DIR/patterns.json")
  echo ""
  echo "Last Extraction: $LAST_EXTRACTION"
else
  echo "Status: Not extracted"
  echo "Run: /pms:extract"
fi

echo ""

# 3. Procedural Memory Status
echo "⚙️  Procedural Memory (Active Rules)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RULES_DIR="$PROJECT_DIR/.claude/rules/pms"
PROCEDURAL_METADATA="$PMS_DIR/procedural/rules-metadata.json"

if [ -d "$RULES_DIR" ] && [ "$(ls -A "$RULES_DIR" 2>/dev/null)" ]; then
  RULE_FILES=$(ls "$RULES_DIR"/*.md 2>/dev/null | wc -l)
  echo "Rule Files: $RULE_FILES"

  # List files
  if [ $RULE_FILES -gt 0 ]; then
    echo "Files:"
    ls "$RULES_DIR"/*.md 2>/dev/null | while read file; do
      basename "$file"
    done | sed 's/^/  • /'
  fi

  # Last synthesis
  if [ -f "$PROCEDURAL_METADATA" ]; then
    LAST_SYNTHESIS=$(jq -r '.last_synthesis // "Unknown"' "$PROCEDURAL_METADATA")
    PATTERN_COUNT=$(jq -r '.pattern_count // 0' "$PROCEDURAL_METADATA")
    echo ""
    echo "Last Synthesis: $LAST_SYNTHESIS"
    echo "Patterns Converted: $PATTERN_COUNT"
  fi
else
  echo "Status: No rules generated"
  echo "Run: /pms:synthesize"
fi

echo ""

# 4. Configuration Summary
echo "⚙️  Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CONFIG_FILE="$PROJECT_DIR/.claude/pms.local.md"
if [ -f "$CONFIG_FILE" ]; then
  # Parse YAML frontmatter (basic extraction)
  TRIGGER_PRECOMPACT=$(grep -A 20 "^triggers:" "$CONFIG_FILE" | grep "precompact:" | awk '{print $2}' || echo "true")
  CONTINUOUS_MODE=$(grep -A 20 "^processing:" "$CONFIG_FILE" | grep "continuous_mode:" | awk '{print $2}' || echo "true")
  MIN_SESSIONS=$(grep -A 20 "^thresholds:" "$CONFIG_FILE" | grep "min_sessions:" | awk '{print $2}' || echo "10")
  STRONG_THRESHOLD=$(grep -A 20 "^thresholds:" "$CONFIG_FILE" | grep "strong_pattern:" | awk '{print $2}' || echo "3")

  echo "Triggers:"
  echo "  • PreCompact: $TRIGGER_PRECOMPACT"
  echo ""
  echo "Processing:"
  echo "  • Continuous Mode: $CONTINUOUS_MODE"
  echo ""
  echo "Thresholds:"
  echo "  • Min Sessions: $MIN_SESSIONS"
  echo "  • Strong Pattern: $STRONG_THRESHOLD occurrences"
else
  echo "Status: Using defaults"
  echo "Create: .claude/pms.local.md"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Readiness check
if [ "${SESSION_COUNT:-0}" -ge "${MIN_SESSIONS:-10}" ]; then
  if [ "$STRONG" -gt 0 ] 2>/dev/null; then
    echo "✓ Ready for rule generation!"
    echo "  Run: /pms:synthesize"
  else
    echo "⚠ Data sufficient but no strong patterns yet"
    echo "  Continue working to strengthen patterns"
  fi
elif [ "${SESSION_COUNT:-0}" -gt 0 ]; then
  NEEDED=$((${MIN_SESSIONS:-10} - ${SESSION_COUNT:-0}))
  echo "⏳ Need $NEEDED more sessions before extraction"
  echo "  Current: ${SESSION_COUNT:-0} / ${MIN_SESSIONS:-10}"
else
  echo "👋 No data yet - system will capture sessions automatically"
  echo "  Or run: /pms:encode"
fi

echo ""
```

## Example Output

```
=== Claude PMS - Procedural Memory System ===

📝 Episodic Memory (Sessions Recorded)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Sessions: 25
Monthly Files: 2
Last Encoded: session-abc-123-def-456

🧠 Semantic Memory (Patterns Detected)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Patterns: 12
  • Emerging (2+ occurrences): 4
  • Strong (3+ occurrences): 6
  • Critical (5+ occurrences): 2

By Category:
  • User Preferences: 4
  • Code Patterns: 6
  • Anti-Patterns: 2

Last Extraction: 2025-12-31T01:30:00Z

⚙️  Procedural Memory (Active Rules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rule Files: 3
Files:
  • user-preferences.md
  • code-patterns.md
  • anti-patterns.md

Last Synthesis: 2025-12-31T02:00:00Z
Patterns Converted: 8

⚙️  Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Triggers:
  • PreCompact: true

Processing:
  • Continuous Mode: true

Thresholds:
  • Min Sessions: 10
  • Strong Pattern: 3 occurrences

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Ready for rule generation!
  Run: /pms:synthesize
```

## Troubleshooting

**"Not initialized"**: No `.claude/pms/` directory. Run `/pms:encode` to initialize.

**"jq: command not found"**: Install jq for JSON parsing: `brew install jq` (macOS) or equivalent.

**Inaccurate counts**: Check for corrupted JSON files in `.claude/pms/`.
