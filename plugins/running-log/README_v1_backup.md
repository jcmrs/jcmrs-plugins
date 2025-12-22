# Running Log Skill

**Version**: 1.0.0
**Domain**: Process Memory, Decision Tracking, Cross-Session Learning
**Status**: Phase 1 Complete — Ready for Phase 2 Prototype Testing

---

## Overview

The Running Log skill maintains a persistent, schema-driven running log that captures:
- **Ideas and observations** (human and AI)
- **External consultations** (Perplexity, research, documentation)
- **Claude's reasoning patterns** (assumptions, decisions, uncertainties, learnings)

Unlike conversation logs (narrative) or diary entries (reflective), the running log is **schema-driven and actionable**—enabling future queries like "What assumptions did I make?" or "Which ideas are blocked?"

---

## Installation

This plugin is part of the jcmrs-plugins marketplace. To install:

```bash
# Ensure jcmrs-plugins marketplace is configured
# The running-log plugin will be available for installation
```

---

## Quick Start

### 1. Activate the Skill

```
/activate running-log
```

**Expected output**: "Running log activated | Profile: DEVELOPER | Threshold: 75%"

This creates:
- `.claude/RUNNING_LOG.md` — Main log (chronological + auto-sections)
- `.claude/LAST_ENTRIES.md` — Dedup tracking (10 most recent)

### 2. Manual Logging

```
/log idea "Feature request: plugin permission system | Priority: High"
/log consultation "Perplexity AI: marketplace architecture | Confidence: High | Source: Dec 21"
/log process "Assumption: API returns paginated results | Confidence: 72% | Status: Assumed"
```

### 3. Review Entries

```
/review                              # Dashboard: auto-sections + recent 10
/review high-priority                # All High-Priority Ideas
/review open-risks                   # Open Risks / Low-Confidence Items
/review --debug                      # Diagnostics (thresholds, suppressed, dedup)
/review --linked #ID-001             # All entries linked to #ID-001
/review --since 2025-12-20           # Entries since date
```

---

## How It Works

### Automatic Entry Detection

The skill monitors Profile output for signal phrases at 3 cadence points per session:

**1. Session Start** (on activation)
- Query: "What context from previous sessions matters?"
- Capture: Key assumptions carried forward, open questions

**2. Mid-Toolchain** (formula: `min(2, floor(tool_count / 3))`)
- 3 tools → 1 check | 6 tools → 2 checks | 9+ → 2 (capped)
- Query: "What observations did that tool expose?"
- Capture: Post-observation insights, decision points, uncertainties

**3. Session End** (before context clear)
- Query: "What did I learn? What assumptions held/failed?"
- Capture: Key learnings, validated/rejected assumptions

### Profile Signal Phrases

**DEVELOPER Profile** (75% confidence threshold):
- "uncertainty on [X]" / "uncertainty about [X]"
- "assumption that [X]"
- "confidence < [threshold]%"
- "fork in reasoning" / "decision point"
- "might be wrong about [X]"

**RESEARCHER Profile** (60% confidence threshold):
- "hypothesis: [X]"
- "source: [citation]" / "citation: [X]"
- "need to verify [X]"
- "limitation: [X]"

**ENGINEER Profile** (70% confidence threshold):
- "risk: [X]"
- "dependency: [X]"
- "assumes [X]"
- "bottleneck: [X]"
- "failure mode: [X]"

### 3-Layer Noise Filtering

1. **Confidence Threshold**: Only log entries ≥ Profile threshold
2. **Entry Cap**: DEVELOPER: 8/session, RESEARCHER: 12/session, ENGINEER: 10/session
3. **Cross-Session Deduplication**: Levenshtein 85% similarity → suppress

---

## Entry Schema

### Entry Types

**1. Idea/Note**
- Track proposals, observations, feature requests
- Fields: Description, Priority (High/Med/Low), Status, Tags, Linked To

**2. Consultation**
- Document external knowledge (research, docs, user feedback)
- Fields: Description, Source/Citation, Confidence, Status (Reviewed/Pending/Disputed), Linked To

**3. Process Memory**
- Claude's reasoning traces (assumptions, decisions, uncertainties, learnings)
- Fields: Description, Category (Decision/Assumption/Uncertainty/Learning), Confidence (0-100%), Status (Assumed/Validated/Rejected), Outcome, Learning, Linked To

---

## Auto-Generated Sections

Regenerated on-demand (`/review`) or after 5+ new entries:

**📊 High-Priority Ideas**
- Type = Idea/Note + Priority = High + Status ≠ Done
- Sorted: Newest first

**⚠️ Open Risks / Low-Confidence Items**
- Type = Process Memory + (Status = Assumed OR Confidence < 60%)
- Sorted: Lowest confidence first

**🔗 Linked Process Insights**
- Type = Process Memory with "Linked To" populated
- Grouped by: Idea/Consultation referenced

---

## Examples

### Example 1: Idea → Consultation → Process Memory Link

```
/log idea "Design plugin permission system | Priority: High"
→ Creates #ID-001

/log consultation "Anthropic docs | Confidence: High"
→ Creates #ID-002, auto-linked to #ID-001

DEVELOPER flags "uncertainty on plugin directory access"
→ Creates #ID-003 (Process Memory, Confidence 60%), auto-linked to #ID-001, #ID-002

/review --linked #ID-001
→ Shows all three connected
```

### Example 2: Assumption Failure Tracking

```
Entry Created: #ID-004 | "Assumed `.jcmrs-plugins/` is valid | Confidence: 5% | Status: Assumed"

Later Updated: #ID-004 → Status: Rejected | Outcome: Spec requires `.claude-plugin/` | Learning: Consult spec first

Value: Future queries show pattern of assumption-failures
```

---

## Variants

### research-running-log
**Additional Fields**: CitationStrength, Sources, Hypothesis, ExperimentDesign
**Threshold**: 55% (tolerates exploratory thinking)
**Use Case**: Research projects, hypothesis testing, literature review

### architecture-running-log
**Additional Fields**: RiskScore (1-10), AffectedComponents, DependencyGraph, MitigationStrategy
**Threshold**: 70% (architectural precision)
**Use Case**: System design, infrastructure planning, technical debt tracking

---

## Configuration

Default thresholds per Profile:
- **DEVELOPER**: 75% (demands precision)
- **RESEARCHER**: 60% (tolerates hypotheses)
- **ENGINEER**: 70% (balanced)
- **DEFAULT**: 70% (fallback if no Profile active)

---

## Phase Status

**Current**: Phase 1 Complete (Specification)
**Next**: Phase 2 Prototype Testing (5+ sessions, signal validation, noise data)
**Timeline**: Version 1.1 after Phase 2 empirical tuning

See `RUNNING_LOG_IMPLEMENTATION_PLAN.md` for complete 6-phase roadmap.

---

## Documentation

- **Complete Specification**: `SKILL_RUNNING_LOG_SPECIFICATION.md`
- **Implementation Plan**: `RUNNING_LOG_IMPLEMENTATION_PLAN.md`
- **Skill Methodology**: `skills/running-log/SKILL.md`

---

## Support

For questions, feedback, or issues, please refer to the jcmrs-plugins repository.
