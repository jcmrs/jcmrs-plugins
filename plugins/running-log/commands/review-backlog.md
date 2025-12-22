---
name: review-backlog
description: Post-process running log entries - prioritize, link, harmonize tags, regenerate auto-sections
argument-hint: "[--ideas|--risks|--link ID|--tags]"
---


Post-process running log entries: prioritize, link, harmonize tags, regenerate auto-sections.

## Usage

```
/review-backlog                 # Full review with all suggestions
/review-backlog --ideas         # Review only ideas (prioritize TBD items)
/review-backlog --risks         # Review low-confidence Process Memory items
/review-backlog --link #ID-XXX  # Find and link entries related to specific ID
/review-backlog --tags          # Harmonize tags only
```

## Execution

### Step 1: Parse Arguments

Check `$ARGUMENTS` for mode:
- No arguments or empty: **Full Review Mode**
- `--ideas`: **Ideas Review Mode**
- `--risks`: **Risks Review Mode**
- `--link #ID-XXX`: **Link Discovery Mode**
- `--tags`: **Tag Harmonization Mode**

### Step 2: Load All Entries

1. Read `.claude/RUNNING_LOG.md`
2. Parse all entries from `## Entry Backlog` section
3. Extract for each entry:
   - Entry ID
   - Type (Idea/Note, Consultation, Process Memory)
   - Description
   - Confidence/Priority
   - Status
   - Tags
   - Linked To (if present)

Store in memory for analysis.

---

## Mode 1: Full Review (No Arguments)

Perform all analyses and present comprehensive review.

### Analysis 1: Prioritization

**Find Ideas with Priority = TBD:**

For each TBD idea:
1. Analyze description keywords
2. Check if related to recent Process Memory entries (decisions, critical items)
3. Look for domain alignment (documentation, api, tooling, etc.)
4. Suggest priority: High/Med/Low with brief rationale

**Output Format:**
```
💡 Ideas Requiring Prioritization (N):

- #ID-20251222-001: Local AI-optimized docs
  → Suggested: High
  → Rationale: Aligns with knowledge-base work, mentioned in #ID-20251221-005

- #ID-20251221-003: Plugin permission system
  → Suggested: Med
  → Rationale: Dependent on architecture decisions, no immediate blockers
```

### Analysis 2: Relationship Discovery

**Find Related Entries:**

For each entry, identify potential links based on:
- Shared keywords in descriptions
- Similar tags
- Temporal proximity (entries from same session)
- Causal relationships (decision → idea, consultation → implementation)

**Output Format:**
```
🔗 Suggested Links (N):

- #ID-20251222-001 ← #ID-20251221-008
  Reason: Both reference documentation workflows

- #ID-20251221-005 → #ID-20251221-003
  Reason: Decision in 005 impacts idea in 003

- #ID-20251220-012 ↔ #ID-20251220-015
  Reason: Both discuss marketplace architecture
```

### Analysis 3: Tag Harmonization

**Find Tag Inconsistencies:**

1. Identify similar tags:
   - `docs` vs `documentation`
   - `api` vs `api-design`
   - `anthropic` vs `anthropic-api`

2. Count usage frequency
3. Suggest consolidation to most common variant

**Output Format:**
```
🏷️  Tag Harmonization Suggestions:

- Rename "docs" → "documentation" (4 entries affected)
- Merge "api" + "api-design" → "api-design" (3 entries)
- Merge "anthropic" + "anthropic-api" → "anthropic" (5 entries)
```

### Analysis 4: Risk Highlighting

**Find Low-Confidence Items:**

- Process Memory entries with Confidence < 70%
- Status = Assumed (not yet validated)
- Critical signals (blocker, must-verify, etc.)

**Output Format:**
```
⚠️  Open Risks / Low-Confidence Items (N):

- #ID-20251221-004: Confidence 65%
  → Low confidence on validation approach
  → Status: Todo
  → Linked to: #ID-20251221-005

- #ID-20251220-010: Confidence 60%
  → Assumption about API behavior not yet validated
  → Status: Assumed
```

### Step 3: Display Summary

```
🔍 Backlog Review Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Analysis 1: Prioritization]
[Analysis 2: Relationship Discovery]
[Analysis 3: Tag Harmonization]
[Analysis 4: Risk Highlighting]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Apply changes? [Y/n]
```

### Step 4: Apply Changes (If User Confirms)

If user types "Y" or "yes":

1. **Update Priorities**: Edit entries to change TBD → High/Med/Low
2. **Add Links**: Add "Linked To" fields to suggested entries
3. **Harmonize Tags**: Rename/merge tags across affected entries
4. **Regenerate Auto-Sections**: Update High-Priority Ideas, Open Risks, Linked Insights sections
5. **Update Last Updated timestamp** in header

Confirm:
```
✅ Applied N changes to running log
   - Updated 5 priorities
   - Added 3 links
   - Harmonized 12 tag occurrences
   - Regenerated auto-sections
```

---

## Mode 2: Ideas Review (`--ideas`)

Focus only on prioritizing TBD ideas.

### Execution

1. Load all entries
2. Filter: Type = Idea/Note AND Priority = TBD
3. For each TBD idea:
   - Analyze description
   - Suggest priority with rationale
   - Identify potential links

**Output:**
```
💡 Ideas Review (N ideas with TBD priority)

#ID-20251222-001: Local AI-optimized docs
→ Suggested: High
→ Rationale: Aligns with knowledge-base goals
→ Potential Links: #ID-20251221-008 (documentation workflow)

#ID-20251221-003: Plugin permission system
→ Suggested: Med
→ Rationale: Dependent on architecture, no immediate need

Apply priority suggestions? [Y/n]
```

---

## Mode 3: Risks Review (`--risks`)

Focus only on low-confidence Process Memory items.

### Execution

1. Load all entries
2. Filter: Type = Process Memory AND (Confidence < 70% OR Status = Assumed)
3. For each risk item:
   - Display confidence level
   - Show status
   - Highlight if linked to ideas or consultations
   - Suggest validation steps

**Output:**
```
⚠️  Open Risks Review (N items)

#ID-20251221-004: Confidence 65%
→ Low confidence on validation approach
→ Status: Todo
→ Linked to: #ID-20251221-005 (decision fork)
→ Suggested Action: Test manual stub approach vs auto-detection

#ID-20251220-010: Confidence 60%
→ Assumption about API pagination
→ Status: Assumed
→ Suggested Action: Verify with actual API test
```

---

## Mode 4: Link Discovery (`--link #ID-XXX`)

Find entries related to a specific entry ID.

### Execution

1. Load all entries
2. Find target entry by ID
3. Analyze target entry:
   - Extract keywords from description
   - Extract tags
   - Note type and timestamp

4. Search all other entries for:
   - Shared keywords (≥ 2 words in common)
   - Shared tags (≥ 1 tag)
   - Temporal proximity (same day or adjacent days)
   - Causal language ("because of", "led to", "resulted in")

5. Rank by relevance score:
   - Shared keywords: +2 per keyword
   - Shared tags: +3 per tag
   - Same type: +1
   - Temporal proximity: +1
   - Causal language: +5

**Output:**
```
🔗 Entries Related to #ID-20251222-001

High Relevance (Score ≥ 7):
- #ID-20251221-008 (Score: 9)
  → Shares 3 keywords, 2 tags
  → Same day, both reference documentation

Medium Relevance (Score 4-6):
- #ID-20251220-015 (Score: 5)
  → Shares 2 tags, temporal proximity

Low Relevance (Score 1-3):
- #ID-20251219-003 (Score: 2)
  → Shares 1 keyword

Add "Linked To" field to #ID-20251222-001 with suggested links? [Y/n]
```

---

## Mode 5: Tag Harmonization (`--tags`)

Focus only on tag consistency.

### Execution

1. Load all entries
2. Extract all unique tags
3. Group similar tags:
   - Levenshtein distance < 3 edits
   - Common prefixes/suffixes
   - Semantic similarity (e.g., "doc" vs "documentation")

4. For each group:
   - Count usage frequency
   - Suggest consolidation to most common variant

**Output:**
```
🏷️  Tag Harmonization Report

Group 1: Documentation Tags
- "documentation" (8 uses) ← KEEP
- "docs" (4 uses) → Rename to "documentation"
- "doc" (1 use) → Rename to "documentation"

Group 2: API Tags
- "api-design" (5 uses) ← KEEP
- "api" (3 uses) → Rename to "api-design"

Group 3: Anthropic Tags
- "anthropic" (6 uses) ← KEEP
- "anthropic-api" (2 uses) → Rename to "anthropic"

Apply harmonization? [Y/n]

Changes: 13 tag occurrences across 10 entries
```

---

## Auto-Section Regeneration

After any changes applied, regenerate auto-sections in RUNNING_LOG.md:

### High-Priority Ideas

```markdown
### 🔥 High-Priority Ideas

- #ID-20251222-001: Local AI-optimized docs (Backlog)
- #ID-20251221-012: Add WebSocket support (In Progress)
```

**Criteria**: Type = Idea/Note + Priority = High + Status ≠ Done

### Open Risks / Low-Confidence Items

```markdown
### ⚠️ Open Risks / Low-Confidence Items

- #ID-20251221-004: Validation approach uncertainty (65%)
- #ID-20251220-010: API pagination assumption (60%)
```

**Criteria**: Type = Process Memory + (Confidence < 60% OR Status = Assumed)

### Linked Process Insights

```markdown
### 🔗 Linked Process Insights

- #ID-20251221-005 → #ID-20251221-003 (Decision impacts plugin idea)
- #ID-20251220-012 ↔ #ID-20251220-015 (Marketplace architecture discussion)
```

**Criteria**: Any entry with "Linked To" field populated

---

## Important Notes

- All analysis is AI-driven (relationship detection, priority suggestion, tag harmonization)
- Changes require user confirmation (Y/n prompt)
- Original entries never deleted, only enhanced
- Backup tip: User can check git diff before confirming changes
- Tag harmonization preserves semantic meaning while improving consistency

---

Execute the appropriate mode based on `$ARGUMENTS`.
