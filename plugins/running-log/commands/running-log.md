---
name: running-log
description: Display running log entries - show recent entries or debug details
argument-hint: "[--show N|--debug]"
---


Display running log entries. For adding ideas, use `/idea`. For post-processing, use `/review-backlog`.

## Usage

```
/running-log --show [N]    # Show last N entries (default: 10)
/running-log --debug       # Show last 5 entries with full details
```

## Parse Arguments

Check `$ARGUMENTS` for flags:
- `--show` or `--show N`: **Display mode** (show last N entries, default 10)
- `--debug`: **Debug mode** (show last 5 entries with regex details)
- No arguments or empty: Display usage help

## File Paths

- **Main log**: `.claude/RUNNING_LOG.md`
- **Cache**: `.claude/LAST_ENTRIES.md`

Check if files exist. If not, initialize them.

---

## Mode 1: Display (`--show [N]`)

1. Read `.claude/LAST_ENTRIES.md`
2. Parse the entry table
3. Extract last N entries (default: 10, or use number from `$ARGUMENTS`)
4. Display in compact format:
   ```
   Last N entries:

   #ID-YYYYMMDD-NNN | Type | Description | Status
   #ID-YYYYMMDD-NNN | Type | Description | Status
   ```

---

## Mode 2: Debug (`--debug`)

1. Read `.claude/RUNNING_LOG.md`
2. Extract last 5 entries from Entry Backlog section
3. Display full entry content including:
   - All fields (Description, Confidence, Status, Type, Profile, Tags)
   - Extended Context
   - Pattern Detected (if present)
   - Raw Output (if present)
   - Detection Method

Format each entry with full markdown, separated by `---`

---

## Mode 3: Usage Help (no arguments)

Display usage information:

```
Running Log v2.0 - Display & Quick-Capture

Display Modes:
  /running-log --show [N]    Show last N entries (default: 10)
  /running-log --debug       Show last 5 entries with full details

Quick-Capture:
  /idea [DESCRIPTION]        Add idea to backlog (one-line, AI fills defaults)

Post-Processing:
  /review-backlog            Prioritize, link, organize entries

Examples:
  /running-log --show 5              Show last 5 entries
  /running-log --debug               Show debugging details
  /idea Local AI-optimized docs      Add quick idea
  /review-backlog                    Review and organize backlog
```

---

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

---

## Important Notes

- Use Read tool to read files
- Use Edit tool to update existing files
- Use Write tool only if file doesn't exist
- Generate ISO 8601 timestamps: `YYYY-MM-DDTHH:MM:SS+TZ`
- Entry IDs must be unique and sequential per day
- Always update both RUNNING_LOG.md and LAST_ENTRIES.md
- Keep LAST_ENTRIES.md at max 20 entries

Execute the appropriate mode based on `$ARGUMENTS`.
