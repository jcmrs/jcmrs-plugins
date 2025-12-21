# /running-log - Running Log Command

You are executing the `/running-log` command to manage persistent process memory entries.

## Parse Arguments

Check `$ARGUMENTS` for flags:
- No arguments or empty: **Manual entry mode**
- `--show` or `--show N`: **Display mode** (show last N entries, default 10)
- `--debug`: **Debug mode** (show last 5 entries with regex details)

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

## Mode 3: Manual Entry (no arguments)

### Step 1: Gather Entry Details

Prompt user for each field:

```
**Entry Type?** [Idea/Note | Consultation | Process Memory]
```

Wait for response. Then:

```
**Description** (1-2 sentences):
```

Wait for response. Then:

```
**Confidence/Priority** (% or High/Med/Low):
```

Wait for response. Then:

```
**Status** [Assumed/Validated/Rejected/Todo/In Progress/Done/Blocked]:
```

Wait for response. Then:

```
**Tags** (comma-separated):
```

Wait for response. Then (optional):

```
**Linked To** (entry IDs like #ID-20251221-001, or press Enter to skip):
```

Wait for response.

### Step 2: Generate Entry ID

1. Check existing entries in RUNNING_LOG.md to find highest entry number for today
2. Generate ID: `#ID-YYYYMMDD-NNN` where:
   - YYYY = current year
   - MM = current month (zero-padded)
   - DD = current day (zero-padded)
   - NNN = next sequence number (001, 002, etc.)

Example: `#ID-20251221-006`

### Step 3: Create Entry

Format entry using schema:

```markdown
## [Entry Type] | [Entry ID] | [ISO 8601 Timestamp]

**Description**: [user input]
**Confidence/Priority**: [user input]
**Status**: [user input]
**Type**: [Entry Type from step 1]
**Profile**: DEVELOPER
**Linked To**: [user input if provided]
**Tags**: [user input]

[If user wants to add extended context, prompt: "Extended context (optional, press Enter to skip):"]

---
```

### Step 4: Append to RUNNING_LOG.md

1. Read `.claude/RUNNING_LOG.md`
2. Find the `## Entry Backlog` section
3. Insert new entry at the TOP of the backlog (reverse chronological)
4. Update `**Last Updated**` timestamp in header
5. Write file

### Step 5: Update LAST_ENTRIES.md

1. Read `.claude/LAST_ENTRIES.md`
2. Add new entry to top of table
3. Keep only last 20 entries
4. Update `**Last Updated**` timestamp
5. Increment `**Total Entries**` count
6. Write file

### Step 6: Confirm

Display:
```
✅ Logged entry [Entry ID] to .claude/RUNNING_LOG.md
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
