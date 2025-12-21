# /running-log - Running Log Command (Phase 2 Stub)

## Purpose
Manually log entries and display running log contents for Phase 2 validation testing.

## Usage

```bash
/running-log                    # Manual entry (prompts for details)
/running-log --show [N]         # Display last N entries (default: 10)
/running-log --debug            # Show last 5 with regex match details
```

## Implementation

### Initialization

On first invocation, create files in `.claude/` directory:

1. **RUNNING_LOG.md** - Main log file with all entries
2. **LAST_ENTRIES.md** - Quick-access cache of last 20 entries

File template for RUNNING_LOG.md:
```markdown
# Running Log - [Profile Name] Profile

**Created**: [ISO 8601 timestamp]
**Last Updated**: [ISO 8601 timestamp]

---

## Auto-Generated Sections

### 🔥 High-Priority Ideas
[Auto-populated from entries tagged High/Critical]

### ⚠️ Open Risks / Low-Confidence Items
[Auto-populated from entries with confidence < 60%]

### 🔗 Linked Process Insights
[Auto-populated from Process Memory entries with Linked To]

---

## Entry Backlog

[Entries appear here in reverse chronological order]
```

### Command Behavior

**`/running-log` (no arguments)**:
1. Prompt user for entry details:
   - Entry type: Idea/Note, Consultation, or Process Memory
   - Description (1-2 sentences)
   - Confidence/Priority
   - Status
   - Tags
2. Generate entry ID (format: #ID-YYYYMMDD-NNN)
3. Append to RUNNING_LOG.md
4. Update LAST_ENTRIES.md
5. Confirm: "✅ Logged entry #ID-YYYYMMDD-NNN"

**`/running-log --show [N]`**:
1. Read LAST_ENTRIES.md
2. Display last N entries (default: 10)
3. Format: ID | Type | Description | Status

**`/running-log --debug`**:
1. Read last 5 entries from RUNNING_LOG.md
2. For each entry, show:
   - Full entry content
   - Regex pattern that triggered it (if auto-generated)
   - Raw Profile output that matched pattern
   - Confidence calculation

### Phase 2 Stub Limitations

This is a **manual stub** for Phase 2 validation testing:
- ❌ No automatic signal detection (Phase 3+)
- ❌ No regex pattern matching (Phase 3+)
- ❌ No auto-generation from Profile responses (Phase 3+)
- ✅ Manual entry logging works
- ✅ Entry display works
- ✅ File creation works

**Phase 2 Testing Workflow**:
1. Trigger signal phrases manually in responses
2. Use `/running-log` to manually log what SHOULD have been detected
3. Document in Phase 2 report: "Signal triggered → Manual entry logged → Expected: Auto-detection"
4. This validates the SCHEMA and WORKFLOW, deferring actual regex implementation

## File Locations

- `.claude/RUNNING_LOG.md` - Main log (jcmrs-plugins repository)
- `.claude/LAST_ENTRIES.md` - Recent entries cache

## Examples

**Manual entry**:
```
User: /running-log
Claude:
Entry type? [Idea/Note | Consultation | Process Memory]
> Process Memory

Description (1-2 sentences):
> Uncertainty on API rate limit scope - per-user vs per-application

Confidence (%):
> 80

Status: [Assumed/Validated/Rejected/Todo/In Progress/Done/Blocked]
> Assumed

Tags (comma-separated):
> api, rate-limiting, uncertainty

✅ Logged entry #ID-20251221-001 to .claude/RUNNING_LOG.md
```

**Display entries**:
```
User: /running-log --show 3
Claude:
Last 3 entries:

#ID-20251221-003 | Process Memory | Critical blocker on skill activation | Blocked
#ID-20251221-002 | Process Memory | Assumption about marketplace auto-loading | Assumed
#ID-20251221-001 | Process Memory | Uncertainty on API rate limit scope | Assumed
```

**Debug view**:
```
User: /running-log --debug
Claude:
Last 5 entries with detection details:

## Process Memory | #ID-20251221-001 | 2025-12-21T18:15:00+01:00
**Description**: Uncertainty on API rate limit scope
**Confidence**: 80%
**Status**: Assumed
**Pattern Matched**: Uncertainty (/uncertainty\s+(on|about)/)
**Raw Output**: "I have uncertainty on whether the API rate limit applies per-user or per-application"
**Detection**: Manual (stub) - Would auto-detect in Phase 3+

---
```

## Next Steps After Phase 2

- Phase 3: Implement actual regex pattern matching
- Phase 3: Add auto-detection from Profile responses
- Phase 3: Add confidence threshold filtering
- Phase 4: Add deduplication (Levenshtein 85%)
- Phase 4: Add session entry caps
