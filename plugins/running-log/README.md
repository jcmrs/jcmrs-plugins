# Running Log Skill v2.0

**Version**: 2.0.0
**Domain**: Process Memory, Decision Tracking, Cross-Session Learning
**Status**: Redesigned based on Phase 2 validation findings

---

## Overview

The Running Log skill maintains a persistent, schema-driven running log through **three distinct workflows**:

1. **Quick-Capture** (`/idea`) - Human adds ideas while working (zero friction)
2. **Auto-Detection** (AI) - Claude monitors its own reasoning patterns
3. **Post-Processing** (`/review-backlog`) - AI organizes, prioritizes, links entries

**Critical Design Insight**: Human entry workflows differ fundamentally from AI auto-detection workflows. v2.0 separates these cleanly.

---

## Installation

This plugin is part of the jcmrs-plugins marketplace. The plugin installs automatically when the marketplace is configured.

---

## Quick Start

### 1. Adding Ideas (Quick-Capture)

```bash
/idea Local copies of Anthropic docs in AI-optimized format
```

**What happens**:
- Entry created immediately with auto-generated ID
- AI fills defaults: Priority = TBD, Status = Backlog
- AI generates relevant tags from description
- You continue working (zero friction)

**Why this works**: Ideas are captured for later evaluation, not evaluated at capture time.

### 2. Viewing Entries

```bash
/running-log --show 10      # Show last 10 entries
/running-log --debug        # Show full details for debugging
```

### 3. Organizing Backlog

```bash
/review-backlog             # Full review: prioritize, link, harmonize tags
/review-backlog --ideas     # Review only ideas (prioritize TBD items)
/review-backlog --risks     # Review low-confidence Process Memory
/review-backlog --tags      # Harmonize tags only
```

**What it does**:
- Analyzes all entries
- Suggests priorities for TBD ideas (High/Med/Low with rationale)
- Identifies relationships between entries
- Harmonizes inconsistent tags
- Regenerates auto-sections

---

## Architecture: Three-Component System

### Component 1: `/idea` (Human Quick-Capture)

**Purpose**: Ultra-minimal idea capture while working

**Usage**:
```bash
/idea Add plugin permission system for marketplace
/idea Local AI-optimized Anthropic docs
/idea WebSocket support for real-time updates
```

**AI automatically fills**:
- Entry ID: `#ID-20251222-001` (auto-incremented)
- Timestamp: ISO 8601
- Confidence/Priority: `TBD` (evaluated during backlog review)
- Status: `Backlog`
- Tags: AI-generated from description + existing taxonomy
- Type: `Idea/Note`
- Profile: Active profile (DEVELOPER)

**Why separate from Process Memory**:
- Humans capture ideas mid-work (no time for metadata)
- Evaluation happens later during `/review-backlog`
- Zero friction = more ideas captured

---

### Component 2: AI Auto-Detection (Background Process)

**Purpose**: Monitor Claude's responses for reasoning patterns

**Entry Types**:

#### Consultation (External Sources)
AI auto-detects when referencing:
- Documentation lookups
- Research queries
- User-provided references
- Framework/library citations

**Creates**: Consultation entry with source, confidence in quality

#### Process Memory (AI Reasoning Patterns)
AI auto-detects loggable patterns in its own responses:

**Pattern 1: Uncertainty**
```
Matches: "uncertainty on [X]", "uncertainty about [Y]"
Creates: Process Memory entry with 80% confidence
```

**Pattern 2: Assumption**
```
Matches: "assume that [X]", "assuming the [Y]"
Creates: Process Memory entry with 75% confidence, Status: Assumed
```

**Pattern 3: Confidence Threshold**
```
Matches: "confidence below 60%", "less than 70% confidence"
Creates: Consultation entry for validation
```

**Pattern 4: Decision/Fork**
```
Matches: "fork in reasoning", "decided on [X] over [Y]"
Creates: Process Memory entry with alternatives + rationale
```

**Pattern 5: Critical Signal**
```
Matches: "critical issue", "blocker on [X]", "must clarify [Y]"
Creates: Process Memory entry with 95% confidence, flagged as critical
```

**Cadence**: 3 automatic checks per session
1. Session Start (continuity)
2. Mid-Toolchain (after `floor(tool_count / 3)` tools)
3. Session End (archive learnings)

**Confidence Thresholds** (auto-log only if >=):
- DEVELOPER: 75%
- RESEARCHER: 60%
- ENGINEER: 70%

**Noise Filtering**:
1. Confidence threshold
2. Entry cap per session (DEVELOPER: 8, RESEARCHER: 12, ENGINEER: 10)
3. Deduplication (Levenshtein 85% similarity suppresses duplicates)

---

### Component 3: `/review-backlog` (Librarian Function)

**Purpose**: Post-process entries to organize, prioritize, and link

**Full Review**:
```bash
/review-backlog
```

**Output**:
```
🔍 Backlog Review Results

💡 Ideas Requiring Prioritization (5):
- #ID-20251222-001: Local AI-optimized docs
  → Suggested: High
  → Rationale: Aligns with knowledge-base work

🔗 Suggested Links (3):
- #ID-20251222-001 ← #ID-20251221-008
  Reason: Both reference documentation workflows

🏷️  Tag Harmonization (2 groups):
- Rename "docs" → "documentation" (4 entries)

⚠️  Open Risks (2):
- #ID-20251221-004: Confidence 65%
  → Low confidence on validation approach

Apply changes? [Y/n]
```

**Focused Reviews**:
```bash
/review-backlog --ideas         # Only prioritize TBD ideas
/review-backlog --risks         # Only review low-confidence items
/review-backlog --tags          # Only harmonize tags
/review-backlog --link #ID-001  # Find entries related to #ID-001
```

**Why separate from capture**:
- Humans can't know relationships while mid-work
- Requires full-backlog context to identify patterns
- Deliberate activity, not real-time capture
- AI analyzes relationships humans can't see

---

## Entry Schema

### Idea/Note Entries

```markdown
## Idea/Note | #ID-20251222-001 | 2025-12-22T15:30:00+01:00

**Description**: Local copies of Anthropic docs in AI-optimized format
**Confidence/Priority**: TBD
**Status**: Backlog
**Type**: Idea/Note
**Profile**: DEVELOPER
**Tags**: documentation, anthropic, ai-optimization, local-tooling

---
```

### Process Memory Entries

```markdown
## Process Memory | #ID-20251222-002 | 2025-12-22T16:45:00+01:00

**Description**: Critical blocker - running-log command not loading despite plugin installation
**Confidence**: 95%
**Status**: Blocked
**Type**: Process Memory
**Profile**: DEVELOPER
**Tags**: critical, blocker, activation, phase-2
**Pattern Detected**: Critical signal - /critical|blocker|blocking|must\s+(clarify|understand|verify)/i
**Raw Output**: "This is a critical blocker - must clarify activation mechanism"

**Extended Context**:
Discovered plugin installed in cache but commands directory missing.
Requires marketplace update to sync latest commit with command files.

---
```

---

## Auto-Generated Sections

Located at top of `RUNNING_LOG.md`, regenerated by `/review-backlog`:

### 🔥 High-Priority Ideas
- Type = Idea/Note + Priority = High + Status ≠ Done
- Sorted: Newest first

### ⚠️ Open Risks / Low-Confidence Items
- Type = Process Memory + Confidence < 60%
- Sorted: Lowest confidence first

### 🔗 Linked Process Insights
- Entries with "Linked To" field populated
- Shows how learnings connect

---

## Migration from v1.0

**Key Changes**:
1. **`/log` command removed** → Use `/idea [description]` instead
2. **Interactive prompting removed** → `/idea` is one-line only
3. **Confidence/Status for ideas** → Now defaults (TBD/Backlog)
4. **Tags** → AI-generated, not human-entered
5. **Linked To** → Post-processing via `/review-backlog`, not capture-time

**Existing logs compatible**: v1.0 entries remain valid, new entries use v2.0 schema

---

## Design Rationale (Phase 2 Learnings)

### Problem 1: Nonsensical Fields for Ideas
**v1.0**: Asked humans for confidence/priority when capturing ideas
**Issue**: Ideas are captured for later evaluation, not evaluated at capture time
**v2.0 Fix**: Defaults to TBD/Backlog, evaluation happens during `/review-backlog`

### Problem 2: Inconsistent Human Tags
**v1.0**: Asked humans to enter free-form tags
**Issue**: Million inconsistent tags, none relevant
**v2.0 Fix**: AI auto-generates tags from description + existing taxonomy

### Problem 3: Impossible "Linked To" Field
**v1.0**: Asked humans to provide entry IDs while capturing
**Issue**: Humans don't memorize IDs mid-work
**v2.0 Fix**: AI identifies relationships during `/review-backlog` post-processing

### Problem 4: Monolithic Command
**v1.0**: Single `/log` command tried to handle all entry types
**Issue**: Human quick-capture ≠ AI auto-detection workflows
**v2.0 Fix**: Split into `/idea` (human), auto-detection (AI), `/review-backlog` (librarian)

---

## Examples

### Example 1: Quick Idea Capture

```bash
# User is working, has an idea
/idea Add plugin permission system for marketplace

# AI creates entry immediately
✅ Idea logged: #ID-20251222-001
📝 Add plugin permission system for marketplace
🏷️  Tags: plugin-system, marketplace, permissions, security

# User continues working (zero friction)
```

### Example 2: AI Auto-Detection

```
# During session, Claude says:
"I'm uncertain about the best approach for handling plugin dependencies..."

# AI auto-detects "uncertain about" pattern
# Creates Process Memory entry:
## Process Memory | #ID-20251222-002 | 2025-12-22T16:30:00+01:00
**Description**: Uncertainty about plugin dependency handling approach
**Confidence**: 80%
**Status**: Assumed
**Pattern Detected**: Uncertainty signal
```

### Example 3: Backlog Review

```bash
/review-backlog

# AI analyzes all entries, outputs:
💡 Ideas Requiring Prioritization (2):
- #ID-20251222-001: Plugin permission system → Suggested: High
  Rationale: Critical for marketplace security, blocks other features

🔗 Suggested Links:
- #ID-20251222-002 → #ID-20251222-001
  Reason: Uncertainty in 002 relates to implementation of idea in 001

Apply changes? [Y/n]
> Y

✅ Applied 3 changes
```

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/idea [DESCRIPTION]` | Quick-capture idea | `/idea Add dark mode toggle` |
| `/running-log --show [N]` | Show last N entries | `/running-log --show 5` |
| `/running-log --debug` | Show full entry details | `/running-log --debug` |
| `/review-backlog` | Full backlog review | `/review-backlog` |
| `/review-backlog --ideas` | Prioritize ideas only | `/review-backlog --ideas` |
| `/review-backlog --risks` | Review low-confidence items | `/review-backlog --risks` |
| `/review-backlog --tags` | Harmonize tags | `/review-backlog --tags` |

---

## File Structure

```
project/
├── .claude/
│   ├── RUNNING_LOG.md              # Main log
│   ├── LAST_ENTRIES.md             # Quick-access cache (20 recent)
│   └── skills/
│       └── running-log/
│           └── SKILL.md            # Skill specification
└── plugins/
    └── running-log/
        ├── commands/
        │   ├── idea.md                # Quick-capture command
        │   ├── review-backlog.md      # Librarian command
        │   └── running-log.md         # Display command
        ├── skills/
        │   └── running-log/
        │       └── SKILL.md           # Full specification
        └── .claude-plugin/
            └── plugin.json            # Plugin metadata
```

---

## Version History

**v2.0.0** (Current)
- Redesigned architecture: three-component system
- Separated human quick-capture from AI auto-detection
- Added `/review-backlog` librarian function
- Removed nonsensical fields from idea capture
- AI-generated tags for consistency

**v1.0.0** (Previous)
- Initial specification
- Monolithic `/log` command
- Interactive prompting for all entry types

---

## Support

For questions, feedback, or issues, please refer to the jcmrs-plugins repository.
