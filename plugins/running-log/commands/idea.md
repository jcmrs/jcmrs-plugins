---
name: idea
description: Quick idea capture with AI-filled defaults (description only, zero friction)
argument-hint: "[DESCRIPTION]"
---


Ultra-minimal idea capture while working. AI fills all defaults.

## Usage

```
/idea Local copies of Anthropic docs in AI-optimized format
```

## Execution

### Step 1: Parse Description

Extract description from `$ARGUMENTS`:
- If empty or no arguments: Display usage and exit
- Otherwise: Description = `$ARGUMENTS`

### Step 2: Generate Entry ID

1. Read `.claude/RUNNING_LOG.md` to find highest entry number for today
2. Generate ID: `#ID-YYYYMMDD-NNN` where:
   - YYYY = current year (2025)
   - MM = current month (zero-padded)
   - DD = current day (zero-padded)
   - NNN = next sequence number (001, 002, etc.)

Example: `#ID-20251222-003`

### Step 3: Generate AI Tags

Analyze description and generate 2-4 relevant tags based on:
- Existing tags in RUNNING_LOG.md (for consistency)
- Domain keywords (documentation, api, framework, tooling, etc.)
- Technology mentions (anthropic, claude, python, etc.)

**Tag Guidelines**:
- Lowercase, hyphenated (e.g., `api-design`, `local-tooling`)
- Prefer existing tags over creating new ones
- Max 4 tags per entry

### Step 4: Create Entry

Format entry with AI-filled defaults:

```markdown
## Idea/Note | [Entry ID] | [ISO 8601 Timestamp]

**Description**: [User-provided description from $ARGUMENTS]
**Confidence/Priority**: TBD
**Status**: Backlog
**Type**: Idea/Note
**Profile**: DEVELOPER
**Tags**: [AI-generated tags]

---
```

**ISO 8601 Timestamp Format**: `YYYY-MM-DDTHH:MM:SS+TZ`
Example: `2025-12-22T15:30:00+01:00`

### Step 5: Append to RUNNING_LOG.md

1. Read `.claude/RUNNING_LOG.md`
2. Find the `## Entry Backlog` section
3. Insert new entry at the TOP of the backlog (reverse chronological order)
4. Update `**Last Updated**` timestamp in header
5. Write file using Edit tool

### Step 6: Update LAST_ENTRIES.md

1. Read `.claude/LAST_ENTRIES.md`
2. Add new entry to top of table:
   ```
   | [Entry ID] | Idea/Note | [Description (truncated to 60 chars)] | TBD | Backlog | [Tags] |
   ```
3. Keep only last 20 entries (remove oldest if > 20)
4. Update `**Last Updated**` timestamp
5. Increment `**Total Entries**` count
6. Write file using Edit tool

### Step 7: Confirm

Display:
```
✅ Idea logged: [Entry ID]
📝 [First 60 chars of description...]
🏷️  Tags: [tag1, tag2, tag3]
```

## File Initialization

If `.claude/RUNNING_LOG.md` doesn't exist, create it:

```markdown
# Running Log - DEVELOPER Profile

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

[Entries will appear here in reverse chronological order]

---
```

If `.claude/LAST_ENTRIES.md` doesn't exist, create it:

```markdown
# Last Entries - Quick Access Cache

**Last Updated**: [ISO 8601 timestamp]
**Profile**: DEVELOPER@75%

---

## Recent Entries (Last 20)

| ID | Type | Description | Confidence | Status | Tags |
|----|------|-------------|------------|--------|------|

---

**Total Entries**: 0
**Session**: [Current date]
```

## Important Notes

- Use Read tool to read files
- Use Edit tool to update existing files
- Use Write tool only if file doesn't exist
- Entry IDs must be unique and sequential per day
- Always update both RUNNING_LOG.md and LAST_ENTRIES.md
- Keep LAST_ENTRIES.md at max 20 entries
- Tags should be consistent with existing tags in the log

## Examples

### Example 1: First Idea of Day

```
User: /idea Add plugin permission system for marketplace

AI generates:
- Entry ID: #ID-20251222-001
- Tags: plugin-system, marketplace, permissions, security
- Timestamp: 2025-12-22T10:15:00+01:00

Output:
✅ Idea logged: #ID-20251222-001
📝 Add plugin permission system for marketplace
🏷️  Tags: plugin-system, marketplace, permissions, security
```

### Example 2: Second Idea (Same Day)

```
User: /idea Local AI-optimized Anthropic docs

AI generates:
- Entry ID: #ID-20251222-002 (incremented)
- Tags: documentation, anthropic, ai-optimization, local-tooling
- Timestamp: 2025-12-22T15:30:00+01:00

Output:
✅ Idea logged: #ID-20251222-002
📝 Local AI-optimized Anthropic docs
🏷️  Tags: documentation, anthropic, ai-optimization, local-tooling
```

## Error Handling

**No description provided:**
```
Usage: /idea [DESCRIPTION]

Example: /idea Add dark mode toggle to settings
```

**File errors:**
- If RUNNING_LOG.md unreadable → Initialize new file
- If LAST_ENTRIES.md unreadable → Initialize new file
- If Edit fails → Show error, ask user to check file permissions

---

Execute the command based on `$ARGUMENTS`.
