---
name: pms:reflect
description: Run full PMS pipeline - extract patterns and generate rules from episodic memory
---

# PMS Reflection - Full Pipeline

Analyze accumulated episodic records, extract patterns, and generate procedural rules.

## What This Does

**Full pipeline execution:**

1. **Semantic Extraction** (`scripts/extract.py`):
   - Load all episodic records from `.claude/pms/episodic/`
   - Detect recurring patterns (preferences, code patterns, anti-patterns)
   - Categorize by strength (emerging/strong/critical)
   - Save to `.claude/pms/semantic/`

2. **Procedural Synthesis** (`scripts/synthesize.py`):
   - Filter strong patterns (≥3 occurrences)
   - Generate actionable rules
   - User approval workflow
   - Save to `.claude/rules/pms/`

## Prerequisites

- At least 10 episodic records (default threshold)
- Check with `/pms:status` first

## Usage

Run the full reflection pipeline:

```bash
# Step 1: Semantic Extraction
echo "Running semantic extraction..."
python "$CLAUDE_PLUGIN_ROOT/scripts/extract.py" \
  --project-path "$CLAUDE_PROJECT_DIR"

# Step 2: Procedural Synthesis (if patterns detected)
if [ $? -eq 0 ]; then
  echo ""
  echo "Running procedural synthesis..."
  python "$CLAUDE_PLUGIN_ROOT/scripts/synthesize.py" \
    --project-path "$CLAUDE_PROJECT_DIR"

  echo ""
  echo "✓ PMS reflection complete!"
  echo "✓ Restart Claude Code session to load new rules"
else
  echo "Semantic extraction completed with no actionable patterns."
  echo "Continue working to accumulate more data."
fi
```

## Expected Output

```
Running semantic extraction...
Analyzing 25 episodic records...
Detected 12 patterns
  - 4 preferences
  - 6 code patterns
  - 2 anti-patterns
Semantic knowledge saved to .claude/pms/semantic/

Running procedural synthesis...
Found 8 strong patterns for rule generation
  - 4 user preferences
  - 3 code patterns
  - 1 anti-patterns
Generated: user-preferences.md
Generated: code-patterns.md
Generated: anti-patterns.md

✓ Generated 3 rule files in .claude/rules/pms/
✓ Restart Claude Code session to load new rules
```

## User Approval

The synthesis step includes approval workflow (unless `auto_synthesize: true`):

1. Proposed rules displayed
2. Review patterns and evidence
3. Approve all / approve selected / reject all
4. Only approved rules are saved

## What Happens Next

**After successful reflection:**
1. Rule files generated in `.claude/rules/pms/`
2. Restart Claude Code: `exit` then `claude` (or `cc`)
3. New rules activate automatically

**If insufficient data:**
- Continue working to accumulate more sessions
- Check thresholds in `.claude/pms.local.md`

## Troubleshooting

**"Insufficient sessions (X/10)"**: Need more episodic records. Use `/pms:encode` or wait for auto-triggers.

**"No strong patterns found"**: Patterns exist but none meet threshold (≥3 occurrences). Continue working.

**"Permission denied"**: Check file permissions on `.claude/rules/pms/` directory.

Run `/pms:status` to check current memory state.
