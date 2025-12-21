# Running Log Skill - Implementation Plan

**Created**: December 21, 2025
**Status**: Planning → Implementation (Phases 1-6 ahead)
**Testbed**: jcmrs-plugins marketplace repository
**Design Reference**: See `.claude/conversations/2025-12-21-running-log-skill-brainstorm.md`

---

## Executive Summary

This plan operationalizes a process memory skill for Claude Code without requiring architectural redesign. The skill maintains a persistent `RUNNING_LOG.md` in each project, capturing ideas, consultations, and Claude's own reasoning patterns via Profile-driven automation.

**Implementation approach**: Phased, with empirical validation at each step. **No dependencies on the skill itself being operational**—plan is standalone.

**Timeline philosophy**: Structure matters (phases, gates, unknowns). Calendar time is arbitrary; focus on phase completion and gate decisions.

---

## Phase 1: Core SKILL.md Specification ⏳

**Objective**: Write complete, unambiguous SKILL.md blueprint that Claude can execute perfectly on first try.

**Deliverables**:
- [ ] SKILL.md v1.0 with schema, behavioral rules, commands, Profile signal definitions
- [ ] RUNNING_LOG.md template (header + auto-sections structure)
- [ ] LAST_ENTRIES.md template (for cross-session deduplication)
- [ ] Configuration section (thresholds by Profile) with YAML + table
- [ ] Signal Parsing regex patterns (5 signal types, prescriptive)
- [ ] Signal Parsing Test Cases (5 documented test scenarios for Phase 2 validation)

**Scope**:
- Complete SKILL.md specification (spec-only, no implementation code)
- Regex patterns explicit and testable (not "see implementation later")
- Test cases documented as validation expectations (Phase 2 will execute)
- File templates (RUNNING_LOG.md, LAST_ENTRIES.md) ready to initialize
- All variant hooks documented (research-, architecture- extensions)

**Acceptance Criteria**:
- [ ] SKILL.md is self-contained and unambiguous
- [ ] Schema complete (all mandatory/optional fields documented)
- [ ] Behavioral rules unambiguous (3-cadence checks, thresholds, noise filters)
- [ ] Commands fully specified with examples (`/log`, `/review`, `/activate`, `/review --debug`)
- [ ] Profile signal regex patterns explicit (5 patterns, testable against real Profile output)
- [ ] Thresholds documented per Profile (YAML + comparison table)
- [ ] Noise filters specified (Levenshtein 85%, entry caps, confidence thresholds)
- [ ] Signal test cases documented (Phase 2 validation expectations)
- [ ] No "TBD" or "see implementation" placeholders

**Unknowns at Start**:
- Real Profile signal output format (Phase 2 will inspect raw Profile signals)
- Actual cadence trigger frequency in practice (Phase 2 will measure)
- Noise ratio at 75% DEVELOPER threshold (Phase 2 will collect empirical data)
- Levenshtein 85% false positive/negative rate (Phase 2 will validate)

**Definition of Done**:
- SKILL.md ready to copy into `.claude/skills/running-log/` without revision
- All spec sections complete and internally consistent
- Signal parsing test cases documented as validation expectations
- Phase 2 has clear, unambiguous validation criteria

**Effort**: ~5-7 hours
- SKILL.md structure & schema: 2-3 hrs
- Profile signals & regex patterns: 1-2 hrs
- Test case documentation: 0.5-1 hr
- Review & polish for spec completeness: 1 hr

---

## Phase 2: Prototype in jcmrs-plugins + Signal Validation 🧪

**Objective**: Deploy core skill; run 5+ real sessions; collect noise/signal data; validate signal parsing works.

**Deliverables**:
- [ ] `.claude/skills/running-log/` folder created in jcmrs-plugins
- [ ] SKILL.md copied; RUNNING_LOG.md initialized
- [ ] 5+ sessions run with DEVELOPER profile active
- [ ] Prototype log with real entries (ideas, consultations, process memories)
- [ ] Signal Parsing Validation Report:
  - [ ] Execute 5 signal parsing test cases against real DEVELOPER Profile output
  - [ ] Log raw Profile signal strings (first 3 sessions for transparency)
  - [ ] Verify regex patterns match actual Profile signals
  - [ ] Document any signal format mismatches or unexpected emissions
- [ ] Noise analysis: categorize entries as High/Medium/Low signal
- [ ] Cadence frequency report: actual mid-toolchain triggers vs. expected
- [ ] Cross-session dedup validation: false positive/negative rate
- [ ] Phase 2 Data Collection Report (see template below)

**Scope**:
- Deploy only Phase 1 spec (core only; no variants yet)
- Use only DEVELOPER profile (75% confidence threshold)
- Run 5+ sessions of real work (not contrived scenarios)
- Log everything exactly as spec dictates (no manual filtering)
- **Validate signal parsing**: Raw Profile output captured and analyzed
- Collect all data using Phase 2 Data Collection Template

**Acceptance Criteria**:
- [ ] Running-log skill deploys without errors
- [ ] `/log` and `/review` commands work as specified
- [ ] RUNNING_LOG.md grows with real entries (not dummy data)
- [ ] Cross-session dedup (LAST_ENTRIES.md) prevents obvious duplicates
- [ ] **Signal parsing validation: 4-5/5 test cases pass OR signal format documented**
- [ ] Noise ratio quantified (target: 70%+ high-signal entries)
- [ ] Cadence data collected (actual trigger frequency documented)
- [ ] Profile signal parsing understood (or raw output captured for Phase 3)
- [ ] No crashes or silent failures

**Unknowns Being Resolved**:
- [ ] Real Profile signal output format (inspect raw signals, document format)
- [ ] Actual noise ratio at 75% DEVELOPER threshold (measure, compare to target 70%+)
- [ ] Mid-cadence frequency (1-3x per session? Verify formula)
- [ ] Levenshtein 85% dedup accuracy (track false positives/negatives)
- [ ] User experience: Is 3-5 entries/session manageable?

**Definition of Done**:
- Running-log fully functional in jcmrs-plugins
- 5+ real sessions completed with data logged
- Signal parsing validation report completed (test results + raw signal samples)
- Noise analysis completed (High/Medium/Low categorization with rationales)
- All unknowns resolved or clearly documented for Phase 3

**Effort**: ~5-7 hours
- Session execution & logging: 3+ hrs (5+ real sessions)
- Data analysis (noise, cadence, dedup): 2-3 hrs
- Signal parsing validation & report: 1-2 hrs

**Risk Mitigations**:
- If signal parsing fails: Log raw Profile output (first 3 sessions), Phase 3 refines regex
- If noise ratio >8 entries: Increase confidence threshold from 75% → 78%
- If noise ratio <2 entries: Decrease confidence threshold from 75% → 72%
- If mid-toolchain triggers >3x/session: Cap using `min(2, floor(tool_count / 3))`
- If Levenshtein 85% too aggressive: Loosen to 82%
- If dedup misses duplicates: Tighten to 88%

---

## Phase 2 Data Collection Template

**Use this template after each session to standardize data capture:**

```
# Phase 2 Session Report

**Session #**: [1-5]
**Date**: [YYYY-MM-DD]
**Time**: [HH:MM - HH:MM]
**Profile**: DEVELOPER@75%
**Project Context**: [Brief description of work]
**Tools Executed**: [Approximate count: file reads, API calls, analysis, etc.]
**Duration**: [Minutes]

---

## Entry Metrics

**Total Candidates Generated**: [N]
**Total Logged**: [N]
**Total Suppressed**: [N]

**Breakdown by Type**:
- Process Memory: [N logged] / [N candidates]
- Idea: [N logged] / [N candidates]
- Consultation: [N logged] / [N candidates]

---

## Cadence Execution

**Start Check**: ✓ Triggered [time]
**Mid-Toolchain Checks**: [N] triggered
  - Tools executed: [N]
  - Formula calculation: min(2, floor([N]/3)) = [expected] ✓
**End Check**: ✓ Triggered [time]

---

## Signal Parsing Validation (Test 5 Cases)

| Test # | Input | Expected Pattern | Result | Raw Profile Output |
|--------|-------|------------------|--------|-------------------|
| 1 | "uncertainty on API limits" | `uncertainty (on\|about)` | ✓ PASS | [raw text] |
| 2 | "assuming cache valid" | `assum(e\|ing\|ption)` | ✓ PASS | [raw text] |
| 3 | "confidence below 60%" | `confidence (below\|<)` | ✓ PASS | [raw text] |
| 4 | "fork in reasoning" | `(fork\|branch\|decision)` | ✓ PASS | [raw text] |
| 5 | "need to clarify" | `need to clarify\|ambiguous` | ✓ PASS | [raw text] |

**Pass Rate**: 5/5 ✓
**Notes**: [Any signal format surprises? Unexpected emissions? Parsing delays?]

---

## Noise Analysis

### High-Signal Entries (Quality ⭐⭐⭐⭐⭐)

- #ID-XXX: "Decision between sync and async APIs" → Useful for future reference
- #ID-XXX: "Assumption: database is normalized" → Flags knowledge gap to validate

[List all high-signal entries with rationale]

**High-Signal Count**: [N]
**High-Signal Ratio**: [N]/[Total Logged] = [X%] (Target: 70%+)

### Medium-Signal Entries (Quality ⭐⭐⭐⭐)

[Entries with useful insights but less critical]

**Medium-Signal Count**: [N]
**Medium-Signal Ratio**: [X%]

### Low-Signal Entries (Quality ⭐⭐)

[Entries that are noise; candidates for threshold increase]

**Low-Signal Count**: [N]
**Low-Signal Ratio**: [X%]

---

## Deduplication Effectiveness

**LAST_ENTRIES.md Dedup Hits**: [N] entries prevented
**False Positives** (suppressed incorrectly): [List with similarity %, explain]
**False Negatives** (should have been suppressed): [List, explain]
**Levenshtein 85% Assessment**: Accurate | Too aggressive | Too permissive

---

## Threshold Assessment

**Applied Threshold**: DEVELOPER @ 75%
**Candidates Below Threshold**: [N] suppressed
**Assessment**: Below-threshold entries were [useful/noise/mix]
**Phase 3 Recommendation**: Keep at 75% | Increase to 78% | Decrease to 72%

---

## User Experience

**Perceived Value**: Entries felt [essential/useful/somewhat useful/noisy]
**Most Valuable Type**: [Process Memory | Idea | Consultation]
**Pain Points**: [Too many entries? Not capturing key moments? Triggers at wrong times?]
**Manual Overrides**: [Did you use `/log` to capture something auto-logging missed?]

---

## Unknowns Resolved

- [ ] Profile signal format verified: [describe format]
- [ ] Cadence frequency confirmed: [X triggers/session vs. expected Y]
- [ ] Noise ratio measured: [X% high-signal]
- [ ] Dedup accuracy confirmed: [X% correct, Y% false positive]

---
```

---

## Phase 3: Threshold Tuning & Core Refinement 🔧

**Objective**: Use Phase 2 noise data to tune thresholds; refine core spec based on empirical results.

**Deliverables**:
- [ ] Noise analysis: categorize Phase 2 entries as "High-Signal", "Medium-Signal", "Low-Signal"
- [ ] Threshold recommendation: adjust DEVELOPER from 75% based on noise ratio data
- [ ] Cadence refinement: if mid-cadence triggered >3x, document rate limit adjustment
- [ ] SKILL.md v1.1: updated thresholds, refined rules, documented Phase 2 discoveries
- [ ] Prototype log archived (preserved for reference in Phase 6)

**Scope**:
- Analyze Phase 2 noise data from all 5+ sessions
- Identify which entries were "actually useful" vs. "noise" (quantify)
- Correlate entry type (Idea vs. Consultation vs. Process Memory) with signal quality
- Test threshold adjustment on Phase 2 data retroactively (what if we'd used 78%?)
- Refine cadence rules if needed

**Acceptance Criteria**:
- [ ] Noise analysis quantified (e.g., "78% High-Signal, 15% Medium, 7% Low")
- [ ] Threshold adjustment documented (why move from 75% to X%, supported by data)
- [ ] Cadence refinement documented (actual frequency, recommended limits)
- [ ] SKILL.md v1.1 incorporates all findings
- [ ] No "we'll figure this out later" placeholders

**Unknowns Being Resolved**:
- [ ] What confidence threshold actually separates signal from noise?
- [ ] Is cadence rule (3 checks/session) sufficient or too aggressive?
- [ ] Do different entry types have different noise profiles?

**Definition of Done**:
- Threshold tuned based on empirical Phase 2 data
- Core SKILL.md refined and versioned v1.1
- Prototype data archived for Phase 6 reference

**Effort**: ~3-4 hours (data analysis + refinement)

**No Go-Backward Risk**: If tuning doesn't converge, revert to Phase 2 spec and re-prototype with adjusted hypothesis.

---

## Phase 4: Variant Templates 📊

**Objective**: Create domain-specific variants based on Phase 3 core spec.

**Deliverables**:
- [ ] research-running-log/SKILL.md: extends core with citation_strength, sources, hypothesis fields
- [ ] architecture-running-log/SKILL.md: extends core with risk_score, dependency_graph, affected_components fields
- [ ] Variant RUNNING_LOG.md templates (domain-specific auto-sections)
- [ ] Variant documentation (when to use which, customization guide)

**Scope**:
- Start from Phase 3 core spec (v1.1)
- Add domain-specific optional fields without breaking core schema
- Define variant-specific thresholds if needed (e.g., RESEARCHER@60% for research-running-log)
- Document field meanings and how they're populated

**Acceptance Criteria**:
- [ ] Variants extend core schema (no conflicts, backward compatible)
- [ ] Each variant has example entries (concrete usage)
- [ ] Variant auto-sections make sense (e.g., "High-Risk Ideas" for architecture variant)
- [ ] Documentation clear on when to use each variant

**Unknowns Being Resolved**:
- [ ] What other domains need variants? (Now: research, architecture; future: data science, DevOps, etc.)
- [ ] Do variants need different threshold tuning?

**Definition of Done**:
- 2 variants complete and documented
- Each has example RUNNING_LOG entries
- Ready for Phase 5 packaging

**Effort**: ~3-4 hours (extension design + documentation)

**Dependency**: Phase 3 (core spec v1.1) must be complete first.

---

## Phase 5: Marketplace Distribution 📦

**Objective**: Package core + variants for jcmrs-plugins marketplace; create INSTALL.md and discovery docs.

**Deliverables**:
- [ ] `.claude-plugin/` structure for running-log marketplace entry
- [ ] INSTALL.md: copy-paste instructions, activation guide
- [ ] README.md: skill overview, entry types, commands, Profile integration
- [ ] Variants listed in marketplace.json (core, research-running-log, architecture-running-log)
- [ ] Quick-start guide (new user, first session)

**Scope**:
- Package Phase 3 core spec + Phase 4 variants
- Create installation instructions (how to copy into .claude/skills/)
- Document activation ("activate running-log")
- List marketplace entry (jcmrs-plugins/marketplace.json updated)
- Create variant selection guide

**Acceptance Criteria**:
- [ ] New user can install in <5 minutes (timed)
- [ ] README clear on what running-log does
- [ ] All entry types documented with examples
- [ ] Commands documented with examples
- [ ] Profile integration explained
- [ ] Variants listed with "when to use" guidance
- [ ] INSTALL.md works for fresh projects (not just jcmrs-plugins)

**Definition of Done**:
- Running-log skill discoverable and installable via marketplace
- Documentation complete and user-tested

**Effort**: ~2-3 hours (packaging + documentation)

**Dependency**: Phase 4 (variants) must be complete.

---

## Phase 6: Multi-Profile Validation 🎯

**Objective**: Test running-log with multiple Profiles; validate cross-Profile behavior.

**Deliverables**:
- [ ] Test runs with RESEARCHER profile (60% threshold)
- [ ] Test runs with other Profiles (ENGINEER, etc. if defined)
- [ ] Cross-Profile interaction validation (switching profiles mid-session, etc.)
- [ ] Multi-variant validation (research-running-log with RESEARCHER, architecture-running-log with ENGINEER)
- [ ] Final SKILL.md v2.0 incorporating all multi-Profile findings

**Scope**:
- Deploy marketplace package (Phase 5)
- Run 5+ sessions with RESEARCHER profile
- Test threshold differences (60% vs 75%)
- Test with multiple variants
- Validate marketplace discovery and installation

**Acceptance Criteria**:
- [ ] RESEARCHER profile logs entries appropriately at 60% threshold
- [ ] Cross-Profile switching doesn't break running-log
- [ ] Variants work with appropriate Profiles (research variant + RESEARCHER, etc.)
- [ ] Marketplace distribution works for fresh projects
- [ ] No regressions from Phase 3-5

**Unknowns Being Resolved**:
- [ ] Do different Profiles have different noise profiles? (RESEARCHER vs DEVELOPER)
- [ ] Is 60% right for RESEARCHER? (May need tuning)
- [ ] Are there other Profiles that should support running-log?

**Definition of Done**:
- Running-log validated across multiple Profiles
- Variants tested in appropriate contexts
- Ready for production use in jcmrs-plugins + marketplace distribution

**Effort**: ~4-5 hours (testing + validation)

**Dependency**: Phase 5 (marketplace packaging) complete.

---

## Checkpoint Summary

| Phase | Checkpoint | Gate Decision |
|-------|-----------|----------------|
| 1 → 2 | SKILL.md complete, test cases documented, no placeholders | Proceed if spec is unambiguous |
| 2 → 3 | Prototype log with 5+ sessions, signal parsing validated, noise data collected | Proceed if thresholds converge (no thrashing) |
| 3 → 4 | Core spec v1.1 stable, threshold tuned empirically | Proceed if variants don't require core redesign |
| 4 → 5 | Variants complete, examples documented | Proceed if variants extend cleanly (no conflicts) |
| 5 → 6 | Marketplace packaged, installation tested | Proceed if installation works first-time |
| 6 → Done | Multi-Profile validated, no regressions | Skill production-ready |

---

## Risk Management

### Risk: Noise Creep
**Mitigation**: Crisp Profile definitions, empirical tuning in Phase 3, entry caps, `/review --debug` audit trail

### Risk: Profile Dependency
**Mitigation**: Fallback threshold (70% default), clear activation guidance

### Risk: Signal Parsing Breaks
**Mitigation**: Phase 2 validates 5 test cases, logs raw Profile output, Phase 3 refines regex

### Risk: Variants Introduce Conflicts
**Mitigation**: Strict backward compatibility, independent testing

### Risk: Marketplace Installation Fails
**Mitigation**: Timed installation test, fresh project validation

---

## Resisting Predispositions (Trap Avoidance)

| Predisposition | Trap | Avoidance |
|---|---|---|
| "Let's add features" | Scope creep; variants without core validation | Phase 1-3 core only; Phase 4 for variants |
| "Ship it after one test" | Insufficient data | Phase 2: 5+ sessions required |
| "We'll fix it in v2" | Deferred design debt | Every phase has DoD; no placeholders |
| "PoC looks good enough" | Rework risk | Phase 1-3 trap-proofed |
| "Skip validation, move on" | Silent failures | Each phase has acceptance criteria |
| "One profile is enough" | Missing requirements | Phase 6: multi-Profile validation |
| "Inflate Phase 1 with testing" | Scope creep blocks prototype | Phase 1 = spec only; Phase 2 = execution |

---

## Timeline & Effort

| Phase | Effort | Structure | Dependencies |
|-------|--------|-----------|--------------|
| 1: Core SKILL.md | 5-7 hrs | Spec-only | None |
| 2: Prototype + Validation | 5-7 hrs | Execution + data | Phase 1 |
| 3: Tuning | 3-4 hrs | Analysis | Phase 2 |
| 4: Variants | 3-4 hrs | Extension | Phase 3 |
| 5: Packaging | 2-3 hrs | Distribution | Phase 4 |
| 6: Multi-Profile | 4-5 hrs | Validation | Phase 5 |
| **Total** | **22-30 hrs** | Sequential phases | Clear gates |

**Note**: Calendar time is arbitrary. Focus on phase completion and gate decisions.

---

## Success Criteria

✅ **Production-ready when**:
- [ ] Core spec validated (Phase 1-3)
- [ ] Prototype tested in real sessions (Phase 2)
- [ ] Thresholds empirically tuned (Phase 3)
- [ ] Variants extend cleanly (Phase 4)
- [ ] Marketplace packaged (Phase 5)
- [ ] Multi-Profile validated (Phase 6)
- [ ] Zero "we'll figure this out later" items
- [ ] Installation works first-time
- [ ] Noise ratio 70%+ high-signal
- [ ] Profiles integrate cleanly

---

## Document Control

**Version**: 1.1 (Phase 1/2 Scope Clarified)
**Last Updated**: December 21, 2025
**Status**: Ready for Phase 1 Implementation

