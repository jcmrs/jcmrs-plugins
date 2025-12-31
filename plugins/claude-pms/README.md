# Claude PMS - Procedural Memory System

> **"Shame on you."** - Because Claude learns from your corrections.

## Overview

Claude PMS (Procedural Memory System) is a cognitive learning plugin that enables Claude Code to learn from session experiences, extract behavioral patterns, and generate project-scoped rules for consistent behavior.

**Three-Tier Memory Architecture:**
- **Episodic Memory:** Captures specific session experiences (what happened, when, where)
- **Semantic Memory:** Extracts patterns, preferences, and anti-patterns from episodes
- **Procedural Memory:** Generates actionable rules for Claude Code's Rules system

## Quick Start

### Installation

The plugin is automatically available through the jcmrs-plugins marketplace.

### First Use

1. **Work on your project** - PMS automatically captures sessions on PreCompact and SessionEnd events
2. **After 10+ sessions, run:** `/pms:reflect`
3. **Review proposed rules** - Approve or reject patterns
4. **Restart session** - New rules load automatically

That's it! Claude now learns your preferences and coding patterns.

## How It Works

```
Session Activity → Episodic Encoding → Semantic Extraction → Procedural Synthesis
                         ↓                    ↓                      ↓
                   episodic/*.json    semantic/*.json    rules/pms/*.md
                                                              ↓
                                                    Claude Code Rules System
```

### 1. Episodic Encoding (Automatic)

Captures each session's experience:
- Task summary and work performed
- Design decisions made
- Challenges encountered and solutions applied
- User preferences observed (from corrections/feedback)
- Code patterns and anti-patterns
- Context and technologies used

**Privacy:** All sensitive data (API keys, passwords, tokens) is automatically redacted.

### 2. Semantic Extraction (Automatic or Manual)

Analyzes episodic records to detect patterns:
- **Emerging patterns:** 2+ occurrences
- **Strong patterns:** 3+ occurrences (worthy of rules)
- **Critical patterns:** 5+ occurrences (high priority)

Categorizes patterns as:
- User preferences (commit style, testing approach, code review)
- Code patterns (language/framework preferences)
- Anti-patterns (mistakes to avoid)

### 3. Procedural Synthesis (Manual)

Converts confirmed patterns into project-scoped rules:
- Generates markdown rule files in `.claude/rules/pms/`
- Groups related rules (preferences, testing, code-patterns, anti-patterns)
- Requires user approval before creating rules
- Rules load automatically in new sessions

## Commands

| Command | Description |
|---------|-------------|
| `/pms:encode` | Manually capture current session experience |
| `/pms:reflect` | Full pipeline: extract patterns + generate rules |
| `/pms:extract` | Extract patterns only (no rule generation) |
| `/pms:synthesize` | Generate rules from detected patterns |
| `/pms:status` | Show current memory state and statistics |
| `/pms:config` | Open configuration file for editing |

## Configuration

Edit `.claude/pms.local.md` in your project to customize:

```yaml
triggers:
  precompact: true      # Capture before compaction
  session_end: true     # Capture at session end
  stop: false           # Capture when Claude stops

processing:
  continuous_mode: true      # Auto-extract after encoding
  auto_synthesize: false     # Require approval for rules

thresholds:
  min_sessions: 10           # Minimum before extraction
  emerging_pattern: 2        # 2+ = emerging
  strong_pattern: 3          # 3+ = rule-worthy
  critical_pattern: 5        # 5+ = high priority
```

**See template at:** `examples/pms.local.md`

## Memory Structure

```
{project}/.claude/
├── pms/                          # PMS memory storage (project-scoped)
│   ├── episodic/
│   │   ├── sessions-2025-01.json # Monthly session logs
│   │   └── index.json            # Session ID → file mapping
│   ├── semantic/
│   │   ├── patterns.json         # Detected patterns
│   │   ├── preferences.json      # User preferences
│   │   └── anti-patterns.json    # Mistakes to avoid
│   ├── procedural/
│   │   └── rules-metadata.json   # Rule file tracking
│   └── metadata/
│       └── processed.json        # Processing state
├── rules/pms/                    # Generated rules (Claude Code native)
│   ├── user-preferences.md
│   ├── testing-patterns.md
│   ├── code-patterns.md
│   └── anti-patterns.md
└── pms.local.md                  # Configuration (YAML frontmatter)
```

## Privacy

**All sensitive data is automatically redacted before storage:**
- API keys and tokens
- Passwords and credentials
- Secret keys and certificates
- Custom patterns (configurable)

**Project-Scoped Isolation:**
- All memory stored per-project (no global learning)
- No cross-project contamination
- Each project learns independently

## Architecture

**Tech Stack:**
- Bash hooks for event triggers
- Python 3.8+ for processing
- Prompt-based analysis for intelligent pattern detection
- JSON for structured storage
- Markdown for rules (Claude Code Rules system)

**Design Principles:**
- Context-first encoding (uses conversation history)
- JSONL fallback (when context unavailable)
- Non-fatal errors (session continues normally)
- Windows 11 compatible (no Cipher dependency)

## Examples

### Example: User Preference Detection

**Session 1:** User corrects: "Don't add Claude Code attribution to commits"
**Session 2:** User corrects: "Remove the attribution comment"
**Session 3:** User corrects again

**After 3+ occurrences → Extracted Pattern:**
```json
{
  "pattern": "No Claude Code attribution in commits",
  "strength": "strong",
  "occurrences": 3,
  "evidence": ["session-001", "session-002", "session-003"]
}
```

**Generated Rule (in `.claude/rules/pms/user-preferences.md`):**
```markdown
## Commit Style
- Never add "Generated with Claude Code" or similar attribution
- Keep commit messages focused on changes, not tools
```

### Example: Testing Pattern Detection

**Sessions 5, 7, 9, 12:** User runs tests before committing
**Session 11:** User blocks commit when tests fail

**After 5+ occurrences → Extracted Pattern:**
```json
{
  "pattern": "Always run tests before commits",
  "strength": "critical",
  "occurrences": 5
}
```

**Generated Rule (in `.claude/rules/pms/testing-patterns.md`):**
```markdown
## Pre-Commit Testing
- Always run test suite before creating commits
- Ensure all tests pass before committing
- If tests fail, fix them or update them as needed
- Never commit code with failing tests
```

## Troubleshooting

### "Insufficient sessions" when running /pms:extract

**Cause:** Fewer than 10 episodic records captured
**Solution:** Work through more sessions, then run `/pms:reflect` again

### "No strong patterns detected"

**Cause:** Patterns haven't occurred 3+ times yet
**Solution:** Continue working, patterns emerge over time

### Rules not loading in new session

**Cause:** Rules cached from previous session
**Solution:** Completely restart Claude Code (not just new conversation)

### Privacy redaction too aggressive

**Cause:** Custom patterns matching normal code
**Solution:** Edit `.claude/pms.local.md` → remove overly broad patterns

## Future Enhancements (v2)

- **Import/Export Skill:** Selectively share rules between projects
- **Pattern Confidence Scores:** Machine learning-based pattern validation
- **Visual Pattern Dashboard:** Web UI for memory exploration
- **Cross-Session Context:** Link related sessions by topic

## Contributing

This plugin is part of the jcmrs-plugins collection. See main repository for contribution guidelines.

## License

MIT License - See LICENSE file in repository root

---

**Claude PMS - Because your preferences matter. Shame on you.**
