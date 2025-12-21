# Running Log Skill Specification v1.0

**Name**: running-log
**Version**: 1.0
**Domain**: Process Memory, Decision Tracking, Cross-Session Learning
**Status**: Spec-only (Phase 1), ready for deployment

---

## Purpose

Maintain a persistent, schema-driven running log that captures:
- Ideas and observations (human and AI)
- External consultations (Perplexity, research, documentation)
- Claude's own reasoning patterns (assumptions, decisions, uncertainties, learnings)

Creates searchable, auto-organized entry backlog across sessions without waiting for architectural redesign.

Unlike conversation logs (narrative) or diary entries (reflective), the running log is **schema-driven and actionable**—enabling future queries like "What assumptions did I make?" or "Which ideas are blocked?"

---

## Entry Schema

All entries follow this structure:

```
## [Entry Type] | #ID-[AUTO] | [Timestamp ISO 8601]

**Description**: [1-2 sentence summary]
**Confidence/Priority**: [%] or [High/Med/Low]
**Status**: [Assumed/Validated/Rejected/Todo/In Progress/Done/Blocked]
**Type**: [Idea/Note | Consultation | Process Memory]
**Profile**: [DEVELOPER | RESEARCHER | ENGINEER | ...]
**Linked To**: [#ID-XXX, #ID-YYY] (optional)
**Tags**: [comma-separated labels]

[Extended description, context, rationale, next steps]

---
```

### Entry Types

**1. Idea/Note**
- Human-provided or AI-generated ideas, observations, feature requests
- Fields: Description, Priority (High/Med/Low), Status, Tags, Linked To
- Purpose: Track proposals and observations

**2. Consultation**
- External input (Perplexity, Anthropic docs, research, user feedback)
- Fields: Description, Source/Citation, Confidence (High/Med/Low), Status (Reviewed/Pending/Disputed), Linked To
- Purpose: Document external knowledge sources

**3. Process Memory**
- Claude's reasoning traces: assumptions made, uncertainties flagged, decisions evaluated, learnings captured
- Fields: Description, Category (Decision/Assumption/Uncertainty/Learning), Confidence (0-100%), Status (Assumed/Validated/Rejected), Outcome (optional), Learning (optional), Linked To
- Purpose: Track AI decision-making and cross-session patterns

---

## Behavioral Rules

### Automatic Entry Triggers (Profile-Driven)

Profiles embed "observation patterns" that signal loggable content. The skill monitors for these signals at 3 cadence points per session.

**Profile Signal Phrases** (Exact matching patterns):

**DEVELOPER Profile**:
- "uncertainty on [X]" / "uncertainty about [X]"
- "assumption that [X]"
- "confidence < [threshold]%"
- "fork in reasoning" / "decision point"
- "might be wrong about [X]"

→ When detected: Auto-log as Process Memory | Confidence: [Profile-assessed]

**RESEARCHER Profile**:
- "hypothesis: [X]"
- "source: [citation]" / "citation: [X]"
- "confidence [threshold]%"
- "need to verify [X]"
- "limitation: [X]"

→ When detected: Auto-log as Process Memory OR Consultation (if external source)

**ENGINEER Profile**:
- "risk: [X]"
- "dependency: [X]"
- "assumes [X]"
- "bottleneck: [X]"
- "failure mode: [X]"

→ When detected: Auto-log as Process Memory | Status: Potential Risk

### Profile Signal Patterns (Detection Regex)

These regex patterns detect the signal phrases above in actual Profile output:

**Pattern 1: Uncertainty Detection**
```regex
/uncertainty\s+(on|about|regarding|around)\s+([^.!?]+)/i
```
Matches: "uncertainty on X", "I have uncertainty about Y", "uncertainty regarding Z"
Confidence: 80% (clear signal of explicit uncertainty)

**Pattern 2: Assumption Detection**
```regex
/assum(e|ing|ption)\s+(that|about|the)\s+([^.!?]+)/i
```
Matches: "assume that X", "assuming the Y", "assumption about Z"
Confidence: 75% (explicit assumption flagged)

**Pattern 3: Confidence Threshold**
```regex
/confidence\s+(less\s+than|below|<)\s*(\d+)%?/i
```
Matches: "confidence below 60%", "less than 70% confidence", "confidence < 50"
Confidence: Extracted value (user-stated confidence level)

**Pattern 4: Decision/Fork**
```regex
/(fork|branch|decision\s+point|chose|decided|rejected)\s+(in|on)?\s*([^.!?]+)/i
```
Matches: "fork in reasoning", "decided on approach X", "chose Y over Z", "decision point: A vs B"
Confidence: 85% (explicit decision documented)

**Pattern 5: Critical Signal**
```regex
/critical|blocker|blocking|must\s+(clarify|understand|verify)/i
```
Matches: "critical issue", "blocker on X", "must clarify Y", "blocking investigation"
Confidence: 95% (escalated importance flagged)

**Implementation Notes**:
- All patterns use case-insensitive flag (`/i`)
- Patterns capture the signal phrase and context (groups 2+)
- Apply patterns sequentially; first match wins (order: Critical > Decision > Assumption > Confidence > Uncertainty)
- If multiple patterns match, use highest confidence pattern
- Suppress pattern if no capture group (empty match) to avoid false positives

### Cadence: 3 Checks Per Session

**1. Session Start** (On activation)
- Query: "What context from previous sessions matters?"
- Capture: Key assumptions carried forward, open questions from last session
- Purpose: Continuity; prevent assumption blindness

**2. Mid-Toolchain** (After tool operations)
- Trigger: Formula `min(2, floor(tool_count / 3))`
  - Example: 3 tools → 1 check | 6 tools → 2 checks | 9 tools → 2 checks (capped at 2)
- Query: "What observations did that tool expose?"
- Capture: Post-observation insights, decision points, uncertainties
- Purpose: Capture decision-critical moments

**3. Session End** (Before context clear)
- Query: "What did I learn? What assumptions held/failed?"
- Capture: Key learnings, validated/rejected assumptions, unresolved items
- Purpose: Archive session reasoning for future reference

**Total**: ~3 automatic checks + manual `/log` entries = 3-8 entries/session for DEVELOPER profile

### Confidence Thresholds

Auto-log only if confidence >= Profile threshold:

```
DEVELOPER:  75% (demands precision)
RESEARCHER: 60% (tolerates hypotheses)
ENGINEER:   70% (balanced)
DEFAULT:    70% (fallback if no Profile active)
```

Manual `/log` commands bypass thresholds (humans decide what matters).

### Noise Filtering (3 Layers)

**1. Confidence Threshold**
- Only log entries >= Profile threshold
- Suppressed entries queryable via `/review --debug`

**2. Entry Cap Per Session**
- DEVELOPER: 8 entries/session max
- RESEARCHER: 12 entries/session max
- ENGINEER: 10 entries/session max
- Excess: Logged as `| Status: Suppressed (cap exceeded)`, queryable

**3. Deduplication (Cross-Session)**
- Maintain LAST_ENTRIES.md with 10 most recent entry summaries
- If new entry > 85% similar (Levenshtein distance) → Suppress + log to audit trail
- Purpose: Prevent "I assumed X" accumulation across sessions

### Auto-Generated Sections

Regenerated on-demand (`/review`) or after 5+ new entries:

**#High-Priority Ideas**
- Type = Idea/Note + Priority = High + Status ≠ Done
- Sorted: Newest first
- Purpose: Quick reference for active work

**#Open Risks / Low-Confidence Items**
- Type = Process Memory + (Status = Assumed OR Confidence < 60%)
- Sorted: Lowest confidence first
- Purpose: Spotlight items needing validation

**#Linked Process Insights**
- Type = Process Memory with "Linked To" populated
- Grouped by: Idea/Consultation referenced
- Purpose: Show how learnings connect to external input

---

## Commands

### /log [TYPE] [CONTENT]

Manually create entry.

```
/log idea "Feature request: plugin permission system | Priority: High"
/log consultation "Perplexity AI: marketplace architecture | Confidence: High | Source: Dec 21"
/log process "Assumption: API returns paginated results | Confidence: 72% | Status: Assumed"
```

**Behavior**:
- Auto-increments #ID
- Adds timestamp
- Tags active Profile
- Appends to chronological section
- Regenerates auto-sections
- Bypasses confidence threshold (human decision)

---

### /review [FILTER]

Query and display running log.

```
/review                              # Show dashboard: auto-sections + recent 10
/review high-priority                # Show all High-Priority Ideas
/review open-risks                   # Show Open Risks
/review [idea|consultation|process]  # Show all entries of type
/review --debug                      # Show diagnostics (thresholds, suppressed, dedup)
/review --linked #ID-001             # Show all entries linked to #ID-001
/review --since 2025-12-20           # Show entries since date
```

**Behavior**:
- Returns formatted sections
- `--debug` shows:
  - Applied Profile threshold
  - Suppressed entries (why: threshold, cap, or dedup)
  - Dedup audit trail
- Auto-sections regenerated before display

---

### /activate running-log

Initialize skill for project.

```
/activate running-log
```

**Behavior**:
- Creates `.claude/RUNNING_LOG.md` with header + template
- Creates `.claude/LAST_ENTRIES.md` for dedup tracking
- Registers active Profile with skill
- Returns: "Running log activated | Profile: DEVELOPER | Threshold: 75%"

**Idempotent**: Safe to run multiple times.

---

## Configuration

```yaml
running_log:
  enabled: true
  file_path: ".claude/RUNNING_LOG.md"
  state_file: ".claude/LAST_ENTRIES.md"

  profiles:
    DEVELOPER:
      threshold: 75
      entry_cap: 8
    RESEARCHER:
      threshold: 60
      entry_cap: 12
    ENGINEER:
      threshold: 70
      entry_cap: 10
    DEFAULT:
      threshold: 70
      entry_cap: 8

  deduplication:
    enabled: true
    levenshtein_threshold: 0.85
    cross_session: true
```

---

## File Structure

```
project/
├── .claude/
│   ├── RUNNING_LOG.md              # Main log (chronological + auto-sections)
│   ├── LAST_ENTRIES.md             # Dedup tracking (10 most recent)
│   └── skills/
│       └── running-log/
│           └── SKILL.md            # This specification
├── RUNNING_LOG_IMPLEMENTATION_PLAN.md  # (project root, not .claude/)
└── [project files]
```

### RUNNING_LOG.md Structure

```markdown
# RUNNING_LOG v1.0 | DEVELOPER@75%

## 📊 High-Priority Ideas
[Auto-generated, newest first]

## ⚠️ Open Risks / Low-Confidence Items
[Auto-generated, sorted by confidence ascending]

## 🔗 Linked Process Insights
[Auto-generated, grouped by related consultations/ideas]

---

## Chronological Entries

## Idea/Note | #ID-001 | 2025-12-21T15:00Z
[Entry content]

---

## Consultation | #ID-002 | 2025-12-21T14:30Z
[Entry content]

---

[Additional entries...]
```

---

## Signal Parsing Test Cases (Phase 2 Executes These)

**5 Test Cases for Regex Pattern Validation**

### Test Case 1: Uncertainty Phrase
**Input**: "I have significant uncertainty regarding the transaction isolation level needed"
**Expected**: Uncertainty signal detected
**Confidence Assignment**: 80%
**Phase 2 Procedure**: Execute regex, verify match, confirm entry created with 80%

### Test Case 2: Assumption
**Input**: "I'm assuming that the message queue has at-least-once delivery semantics"
**Expected**: Assumption signal detected
**Confidence Assignment**: 75%
**Phase 2 Procedure**: Verify assumption captured, check cross-session tracking

### Test Case 3: Confidence Threshold
**Input**: "My confidence below 65% on whether this caching layer will reduce latency enough"
**Expected**: Confidence threshold signal detected
**Confidence Assignment**: 65% (extracted from input)
**Phase 2 Procedure**: Verify threshold parsing, confirm entry logged at exact threshold

### Test Case 4: Decision Fork
**Input**: "I decided on PostgreSQL over MongoDB because of ACID transaction guarantees"
**Expected**: Decision fork detected
**Confidence Assignment**: 85%
**Phase 2 Procedure**: Verify both options captured (PostgreSQL vs MongoDB), rationale stored

### Test Case 5: Critical Signal
**Input**: "This authentication blocker must be resolved before proceeding with API integration"
**Expected**: Critical signal detected
**Confidence Assignment**: 95%
**Phase 2 Procedure**: Verify blocker flagged, confirm appears in Open Risks section

---

## Variant Hooks

Variants extend core schema without breaking backward compatibility.

### research-running-log
**Additional Fields**:
- CitationStrength: Highly Cited / Cited / Emerging / Anecdotal
- Sources: [URLs, references]
- Hypothesis: Testable claim
- ExperimentDesign: How to test hypothesis

**Threshold**: 55% (tolerates exploratory thinking)

### architecture-running-log
**Additional Fields**:
- RiskScore: 1-10
- AffectedComponents: [system, service, layer]
- DependencyGraph: Text list of dependencies
- MitigationStrategy: How to reduce risk

**Threshold**: 70% (architectural precision)

---

## Examples

### Example 1: Idea → Consultation → Process Memory Link

**Step 1**: `/log idea "Design plugin permission system | Priority: High"` → #ID-001

**Step 2**: `/log consultation "Anthropic docs | Confidence: High"` → #ID-002, auto-linked to #ID-001

**Step 3**: DEVELOPER flags "uncertainty on plugin directory access" → #ID-003 (Process Memory, Confidence 60%), auto-linked to #ID-001, #ID-002

**Result**: `/review --linked #ID-001` shows all three connected.

### Example 2: Assumption Failure

**Entry Created**: #ID-004 | "Assumed `.jcmrs-plugins/` is valid | Confidence: 5% | Status: Assumed"

**Later Updated**: #ID-004 → Status: Rejected | Outcome: Spec requires `.claude-plugin/` | Learning: Consult spec first

**Value**: Future queries show pattern of assumption-failures.

---

## Initialization

**First Run**:
1. `/activate running-log`
2. System creates `.claude/RUNNING_LOG.md` + `.claude/LAST_ENTRIES.md`
3. Skill monitors Profile for signals
4. Confirm: "Running log activated | Profile: DEVELOPER | Threshold: 75%"

**Variant Setup**:
1. Choose variant (research-running-log or architecture-running-log)
2. Copy variant SKILL.md (extends core)
3. `/activate running-log`
4. Confirm: "Running log activated | Variant: research | Profile: RESEARCHER | Threshold: 60%"

---

## Version & Maintenance

**Current**: v1.0 (Phase 1 spec-only)
**Expected Updates**:
- v1.1: Post-prototype tuning (Phase 3)
- v2.0: Multi-Profile refinement (Phase 6)
- v2.1+: Variant-specific updates

**Schema Stability**: Core schema (mandatory fields, entry types) stable. Confidence thresholds may adjust based on Phase 2 empirical data.

---

## Next Phase: Phase 2 Execution

Deploy SKILL.md as working skill, run 5+ sessions, execute 5 signal parsing test cases, collect noise data.

See RUNNING_LOG_IMPLEMENTATION_PLAN.md Phase 2 section for execution details and Phase 2 Data Collection Template.

---

**End of SKILL.md Specification v1.0**

*This specification is copy-paste ready. Place in `.claude/skills/running-log/SKILL.md` and run `/activate running-log` to begin.*
