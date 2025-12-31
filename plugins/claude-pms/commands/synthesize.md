---
name: pms:synthesize
description: Generate procedural rules from existing semantic patterns
---

# Procedural Rule Synthesis

Convert confirmed semantic patterns into actionable Claude Code rules.

## What This Does

1. Load semantic knowledge from `.claude/pms/semantic/patterns.json`
2. Filter strong patterns (strength = "strong" or "critical")
3. Generate markdown rule files
4. User approval workflow (unless `auto_synthesize: true`)
5. Save to `.claude/rules/pms/`

**Requires semantic extraction first** - run `/pms:extract` if needed.

## Prerequisites

- Semantic patterns exist (`.claude/pms/semantic/patterns.json`)
- At least one strong pattern (≥3 occurrences)

## Usage

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/synthesize.py" \
  --project-path "$CLAUDE_PROJECT_DIR"
```

## User Approval Workflow

**Unless `auto_synthesize: true` in config:**

1. **Review proposed rules**:
   ```
   === Proposed Rules ===

   user-preferences.md:
   # User Preferences

   **Always run tests before committing code**
   - Observed 8 times (critical pattern)
   - Evidence: session-1, session-2, session-3...
   ```

2. **Approve or reject**:
   - Approve all → Rules generated
   - Reject all → Stored in metadata (won't re-propose)
   - Select specific rules → Only approved ones saved

3. **Rules saved to `.claude/rules/pms/`**

## Expected Output

```
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

## Rule File Categories

**user-preferences.md**:
- Testing requirements
- Commit practices
- Code review expectations
- Documentation standards

**code-patterns.md**:
- Language/framework conventions
- Testing strategies
- Error handling patterns
- Architectural patterns

**anti-patterns.md**:
- Common mistakes to avoid
- Discouraged practices
- Known bug sources

## Activate New Rules

**After synthesis succeeds:**

1. Exit Claude Code: `exit` or Ctrl+D
2. Restart: `claude` or `cc`
3. Rules load automatically from `.claude/rules/pms/`

## Troubleshooting

**"No semantic knowledge found"**: Run `/pms:extract` first.

**"No strong patterns found"**: All patterns are emerging (< 3 occurrences). Continue working.

**"Permission denied"**: Check write permissions on `.claude/rules/pms/`

**"Auto-synthesize enabled but still prompted"**: Command overrides config - use hook triggers for auto mode.

## Auto-Approve Mode

Skip approval prompts (use cautiously):

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/synthesize.py" \
  --project-path "$CLAUDE_PROJECT_DIR" \
  --auto-approve
```

Or enable in config:
```yaml
processing:
  auto_synthesize: true
```

## Review Generated Rules

```bash
# View user preferences
cat "$CLAUDE_PROJECT_DIR/.claude/rules/pms/user-preferences.md"

# View all rule files
ls -la "$CLAUDE_PROJECT_DIR/.claude/rules/pms/"
```
