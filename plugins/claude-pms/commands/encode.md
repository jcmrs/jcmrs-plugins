---
name: pms:encode
description: Manually encode current session as episodic memory record
---

# Manual Episodic Encoding

Capture the current session's work as an episodic memory record.

## What This Does

1. Analyzes the current conversation history
2. Extracts structured information (tasks, decisions, patterns, preferences)
3. Applies privacy redaction (API keys, passwords, etc.)
4. Saves episodic record to `.claude/pms/episodic/sessions-YYYY-MM.json`

## Usage

Simply invoke this command at any point during a session to manually capture the session state.

**When to use:**
- After completing significant work
- Before taking a break
- When you want to preserve learning without waiting for auto-triggers

## Execution

Execute the episodic encoding script:

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" \
  --project-path "$CLAUDE_PROJECT_DIR" \
  --trigger manual
```

## Expected Output

```
Episodic record saved: sessions-2025-12.json
Session ID: abc-123-def-456
Timestamp: 2025-12-31T02:30:00Z
```

## What Happens Next

- **Continuous mode enabled**: Semantic extraction runs automatically if threshold met
- **Continuous mode disabled**: Run `/pms:reflect` or `/pms:extract` when ready

## Troubleshooting

**"Context unavailable"**: Falls back to JSONL transcript parsing (best effort).

**"Privacy redaction failed"**: Over-redacts suspicious patterns for safety.

**"Encoding timeout"**: Saves partial record. Run again if needed.

Check `.claude/pms/episodic/` for saved records.
