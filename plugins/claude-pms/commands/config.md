---
name: pms:config
description: Open or view PMS configuration file
---

# PMS Configuration Management

Manage Claude PMS configuration settings.

## Configuration Location

```
$CLAUDE_PROJECT_DIR/.claude/pms.local.md
```

YAML frontmatter format with markdown documentation.

## Usage

### Open in Editor (if available)

```bash
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/pms.local.md"

# Try common editors
if command -v code >/dev/null 2>&1; then
  code "$CONFIG_FILE"
elif command -v nano >/dev/null 2>&1; then
  nano "$CONFIG_FILE"
elif command -v vim >/dev/null 2>&1; then
  vim "$CONFIG_FILE"
else
  echo "No editor found. View config manually:"
  echo "$CONFIG_FILE"
fi
```

### View Current Configuration

```bash
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/pms.local.md"

if [ -f "$CONFIG_FILE" ]; then
  echo "=== Current Configuration ==="
  echo ""
  cat "$CONFIG_FILE"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "To edit: Open $CONFIG_FILE in your editor"
  echo "After changes: Restart Claude Code session"
else
  echo "Config not found. Creating default..."
  mkdir -p "$(dirname "$CONFIG_FILE")"
  cp "$CLAUDE_PLUGIN_ROOT/examples/pms.local.md" "$CONFIG_FILE"
  echo "✓ Created default config at:"
  echo "  $CONFIG_FILE"
  echo ""
  echo "Edit this file to customize PMS behavior"
fi
```

## Configuration Options

### Triggers (When to capture sessions)
```yaml
triggers:
  precompact: true      # Before context compaction
  session_end: true     # When session ends
  stop: false           # When Claude stops (optional)
```

### Processing Modes
```yaml
processing:
  continuous_mode: true      # Auto-extract after encoding
  auto_synthesize: false     # Require approval for rules
```

**continuous_mode:**
- `true`: Automatically run extraction after each encoding
- `false`: Manual control with `/pms:extract`

**auto_synthesize:**
- `true`: Automatically generate rules without approval
- `false`: User approval required (recommended)

### Thresholds
```yaml
thresholds:
  min_sessions: 10           # Minimum before extraction
  emerging_pattern: 2        # 2+ occurrences
  strong_pattern: 3          # 3+ occurrences (rule-worthy)
  critical_pattern: 5        # 5+ occurrences (high priority)
```

### Privacy Settings
```yaml
privacy:
  redact_sensitive: true     # Auto-redact API keys, passwords
  custom_redaction_patterns:
    - "custom_secret_pattern"
```

### Encoding Preferences
```yaml
encoding:
  prefer_context: true       # Use conversation history first
  fallback_jsonl: true       # Fall back to JSONL if needed
```

### Timeouts (seconds)
```yaml
timeouts:
  encode: 30                 # Max encoding time
  extract: 60                # Max extraction time
  synthesize: 45             # Max synthesis time
```

## Applying Changes

**After editing configuration:**

1. Save the file
2. Exit Claude Code: `exit` or Ctrl+D
3. Restart: `claude` or `cc`
4. Changes take effect

**Configuration is loaded at session start** - changes mid-session won't apply.

## Example Configurations

### Minimal (Auto-everything)
```yaml
---
triggers:
  precompact: true
processing:
  continuous_mode: true
  auto_synthesize: true
---
```

**Use when:** Trust the system, want hands-off operation

### Conservative (Manual control)
```yaml
---
triggers:
  precompact: false
  session_end: false
processing:
  continuous_mode: false
  auto_synthesize: false
---
```

**Use when:** Want explicit control over all operations

### Recommended (Balanced)
```yaml
---
triggers:
  precompact: true
  session_end: true
processing:
  continuous_mode: true
  auto_synthesize: false      # Manual approval for rules
thresholds:
  min_sessions: 10
  strong_pattern: 3
---
```

**Use when:** Want automatic capture but manual rule approval

## Troubleshooting

**"Config not loading"**: Check YAML syntax with online validator.

**"Thresholds ignored"**: Values clamped to valid ranges:
- `min_sessions`: 5-50
- `emerging_pattern`: 2-10
- `strong_pattern` ≥ `emerging_pattern`
- `critical_pattern` ≥ `strong_pattern`

**"Changes not applying"**: Restart Claude Code session.

**"Default config restored"**: Invalid YAML causes fallback to defaults. Check syntax.

## Configuration File Location

```bash
echo "$CLAUDE_PROJECT_DIR/.claude/pms.local.md"
```

## Verify Configuration Loaded

Check with `/pms:status` - shows current thresholds and triggers.
