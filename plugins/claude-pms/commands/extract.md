---
name: pms:extract
description: Extract semantic patterns from episodic records (without generating rules)
---

# Semantic Pattern Extraction

Analyze episodic records to detect patterns without generating rules yet.

## What This Does

1. Load all episodic records from `.claude/pms/episodic/`
2. Detect recurring patterns across sessions
3. Categorize patterns (preferences, code patterns, anti-patterns)
4. Assess strength (emerging/strong/critical)
5. Save to `.claude/pms/semantic/`

**Does NOT generate rules** - use `/pms:synthesize` afterward if desired.

## When to Use

- **Preview patterns** before rule generation
- **Verify pattern detection** is working correctly
- **Inspect evidence** for detected patterns
- **Separate extraction from synthesis** (manual control)

## Usage

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/extract.py" \
  --project-path "$CLAUDE_PROJECT_DIR"
```

## Expected Output

```
Analyzing 25 episodic records...
Detected 12 patterns
  - 4 preferences
  - 6 code patterns
  - 2 anti-patterns

Semantic knowledge saved to .claude/pms/semantic/
```

## Review Patterns

After extraction, inspect the detected patterns:

```bash
# View all patterns
cat "$CLAUDE_PROJECT_DIR/.claude/pms/semantic/patterns.json" | jq .

# View just preferences
cat "$CLAUDE_PROJECT_DIR/.claude/pms/semantic/preferences.json" | jq .

# Count strong patterns (candidates for rules)
cat "$CLAUDE_PROJECT_DIR/.claude/pms/semantic/patterns.json" | \
  jq '[.patterns[] | select(.strength == "strong" or .strength == "critical")] | length'
```

## Pattern Structure

Each pattern includes:
```json
{
  "pattern_id": "pref_123456",
  "description": "Always run tests before commits",
  "category": "preference",
  "strength": "critical",
  "occurrences": 8,
  "evidence": ["session-1", "session-2", ...],
  "detected_at": "2025-12-31T02:00:00Z"
}
```

## Next Steps

**If strong patterns detected:**
```
Run /pms:synthesize to generate rules from strong patterns
```

**If only emerging patterns:**
```
Continue working - patterns need 3+ occurrences to become strong
```

## Troubleshooting

**"Insufficient sessions (X/10)"**: Need at least 10 episodic records.

**"No patterns found"**: Sessions lack sufficient recurrence. Continue accumulating data.

**"Pattern detection timeout"**: Falls back to frequency-only detection.

Use `/pms:status` to check episodic record count.
