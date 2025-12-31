# Claude PMS - Technical Architecture

## System Overview

Claude PMS implements a three-tier cognitive memory architecture inspired by human memory systems:
- **Episodic Memory** (Hippocampus) - Specific event recall
- **Semantic Memory** (Neocortex) - Pattern abstraction and knowledge
- **Procedural Memory** (Basal Ganglia) - Automated behaviors and skills

## Three-Tier Memory Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SESSION ACTIVITY                              │
│                                                                      │
│  User corrections, code reviews, preferences expressed, patterns    │
└───────────────┬──────────────────────────────────────────────────────┘
                │
                ├──▶ Hook: PreCompact (before context compaction)
                ├──▶ Hook: SessionEnd (at session termination)
                └──▶ Hook: Stop (when Claude stops)
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EPISODIC ENCODING ENGINE                          │
│                                                                      │
│  Strategy: Context-first → JSONL fallback                           │
│  Privacy: Automatic redaction (API keys, passwords, tokens)         │
│  Storage: Monthly JSON files (.claude/pms/episodic/)                │
│  Timeout: 30s (with partial record on timeout)                      │
└───────────────┬──────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   SEMANTIC EXTRACTION ENGINE                         │
│                                                                      │
│  Frequency Analysis:                                                │
│    - Emerging: 2+ occurrences                                       │
│    - Strong: 3+ occurrences (rule-worthy)                           │
│    - Critical: 5+ occurrences (high priority)                       │
│                                                                      │
│  Pattern Categories:                                                │
│    - User preferences (commit style, testing approach)              │
│    - Code patterns (framework preferences, design patterns)         │
│    - Anti-patterns (mistakes to avoid)                              │
│                                                                      │
│  Storage: Semantic JSON files (.claude/pms/semantic/)               │
│  Timeout: 60s (with error recovery)                                 │
└───────────────┬──────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  PROCEDURAL SYNTHESIS ENGINE                         │
│                                                                      │
│  Input: Strong patterns (strength >= "strong")                      │
│  Process:                                                            │
│    1. Filter patterns by minimum strength threshold                 │
│    2. Group by category (preferences, code, anti-patterns)          │
│    3. Generate markdown rules per category                          │
│    4. Save to .claude/rules/pms/ (Claude Code native)               │
│                                                                      │
│  Output: Markdown rule files with YAML frontmatter                  │
│  Approval: User confirmation required (unless auto_synthesize)      │
└───────────────┬──────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CLAUDE CODE RULES SYSTEM                           │
│                                                                      │
│  Rules load automatically on session start                          │
│  Project-scoped isolation (no cross-project contamination)          │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Episodic Encoding Engine (`scripts/encode.py`)

**Purpose:** Capture session experiences with privacy protection and fallback resilience

**Strategy Pattern:**
1. **Context-First Encoding** (Preferred)
   - Uses conversation history directly
   - Prompt-based analysis (future: uses `prompts/analyze-session.txt`)
   - Rich structured data extraction
   - Fallback on failure

2. **JSONL Fallback Encoding**
   - Reads session transcript from `~/.claude/projects/{project}/transcripts/`
   - Extracts metadata: tool usage, file operations, error messages
   - Best-effort approach when context unavailable
   - Handles malformed JSONL gracefully (skips up to N bad lines)

**Privacy Redaction:**
- **Default Patterns:** API keys, passwords, tokens, Bearer tokens, secret keys
- **Custom Patterns:** User-configurable via `custom_redaction_patterns`
- **Redaction Markers:** `[REDACTED]`, `[REDACTED_TOKEN]`, `api_key=[REDACTED]`
- **Over-Redaction on Failure:** If redaction fails, conservatively redacts entire fields

**Error Handling:**
- **Timeout:** 30s limit (configurable)
  - Partial record saved with `[TIMEOUT]` marker if exceeded
  - Includes limitations array documenting timeout
- **Encoding Failures:** Falls back through context → JSONL → minimal record
- **Non-Fatal:** Session continues normally even if encoding fails

**Storage Schema:**
```json
{
  "session_id": "uuid-v4",
  "timestamp": "ISO-8601 UTC",
  "project_path": "absolute/path",
  "git_branch": "branch-name",
  "trigger": "precompact|session-end|stop|manual",
  "encoding_mode": "context|jsonl_fallback|partial_timeout",

  "task_summary": "One-line session summary",
  "work_summary": "Detailed work performed",
  "design_decisions": ["Decision 1", "Decision 2"],
  "challenges": ["Challenge 1"],
  "solutions": ["Solution 1"],

  "user_preferences": ["Preference 1", "Preference 2"],
  "code_patterns": ["Pattern 1"],
  "anti_patterns": ["Anti-pattern 1"],

  "context": {
    "technologies": ["Python", "FastAPI"],
    "files_modified": ["path/to/file.py"],
    "tools_used": ["Read", "Write", "Edit"]
  },

  "limitations": ["Optional: encoding issues encountered"]
}
```

**Monthly File Merging:**
- Sessions stored in `sessions-YYYY-MM.json`
- Atomic write with temp file + rename (corruption protection)
- Index file (`index.json`) maps session ID → filename for fast lookup

### 2. Semantic Extraction Engine (`scripts/extract.py`)

**Purpose:** Analyze episodic records to detect behavioral patterns

**Pattern Detection Algorithm:**
1. Load all episodic records from monthly files
2. Extract preferences, code patterns, anti-patterns from each session
3. Count occurrences across sessions (session ID = evidence)
4. Filter by threshold (minimum 2 occurrences = emerging)
5. Categorize strength (2=emerging, 3=strong, 5=critical)
6. Generate pattern records with evidence and metadata

**Extraction Functions:**
- `extract_user_preferences(sessions)`: Extracts `user_preferences` field
- `extract_code_patterns(sessions)`: Extracts `code_patterns` field
- `extract_anti_patterns(sessions)`: Extracts `anti_patterns` field
- Returns: `Dict[pattern_description, List[session_ids]]`

**Frequency Analysis:**
```python
def detect_frequency_patterns(sessions, emerging, strong, critical):
    # Count occurrences per pattern
    pattern_counts = count_pattern_occurrences(sessions)

    # Filter by threshold
    qualified = filter(lambda p: p.count >= emerging, pattern_counts)

    # Categorize strength
    for pattern in qualified:
        if pattern.count >= critical:
            pattern.strength = "critical"
        elif pattern.count >= strong:
            pattern.strength = "strong"
        else:
            pattern.strength = "emerging"

    return qualified
```

**Error Handling:**
- **Corrupted Files:** Skips invalid JSON, continues with valid files
  - Reports corrupted filenames to stderr
  - Returns tuple: (sessions, corrupted_files)
- **Timeout:** 60s limit (Unix-like systems only)
  - Uses signal.alarm() for timeout enforcement
  - Returns False if extraction exceeds limit
- **Insufficient Sessions:** Returns early if below min_sessions threshold

**Storage Schema:**
```json
{
  "patterns": [
    {
      "pattern_id": "pref_123456",
      "description": "Pattern description",
      "category": "preference|code_pattern|anti_pattern",
      "strength": "emerging|strong|critical",
      "occurrences": 5,
      "evidence": ["session-1", "session-2"],
      "detected_at": "ISO-8601 UTC"
    }
  ],
  "count": 10,
  "last_updated": "ISO-8601 UTC"
}
```

**Output Files:**
- `semantic/patterns.json` - All detected patterns
- `semantic/preferences.json` - User preferences only
- `semantic/code-patterns.json` - Code patterns only
- `semantic/anti-patterns.json` - Anti-patterns only

### 3. Procedural Synthesis Engine (`scripts/synthesize.py`)

**Purpose:** Convert semantic patterns into actionable Claude Code rules

**Rule Generation Pipeline:**
1. **Load Patterns:** Read from `semantic/patterns.json`
2. **Filter by Strength:** Only patterns with `strength >= "strong"`
3. **Group by Category:** Separate preferences, code patterns, anti-patterns
4. **Generate Markdown:** Create rule files per category
5. **Save Rules:** Write to `.claude/rules/pms/`
6. **Update Metadata:** Track generated rules in `procedural/rules-metadata.json`

**Rule File Format:**
```markdown
---
title: User Preferences
version: 1
pattern_count: 5
generated_at: 2025-12-31T12:00:00Z
strength: strong
---

# User Preferences

These patterns reflect preferences you've expressed 3+ times.

## Commit Style

- No Claude Code attribution in commits
- Keep commit messages focused on changes

**Evidence:** Detected across 3 sessions

## Testing Approach

- Always run tests before committing
- Ensure all tests pass

**Evidence:** Detected across 5 sessions (critical pattern)
```

**Approval Workflow:**
- **Default:** Requires user approval before generating rules
- **Auto-Synthesize Mode:** Generates rules automatically (configurable)
- **User Interaction:** Presents patterns for review before synthesis

**Metadata Tracking:**
```json
{
  "rules": [
    {
      "filename": "user-preferences.md",
      "category": "preference",
      "pattern_count": 5,
      "generated_at": "ISO-8601 UTC",
      "source_patterns": ["pref_123", "pref_456"]
    }
  ],
  "last_synthesis": "ISO-8601 UTC"
}
```

## Hook Integration

### PreCompact Hook

**Trigger:** Before Claude Code compacts conversation context

**Purpose:** Capture session experience before context is lost

**Implementation:**
```json
{
  "PreCompact": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/encode.py --trigger precompact",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Behavior:**
- Non-blocking (session continues if encoding fails)
- Saves episodic record before context compaction
- Uses context-first encoding (conversation history available)

### SessionEnd Hook

**Trigger:** When Claude Code session terminates

**Purpose:** Final capture of session experience

**Implementation:**
```json
{
  "SessionEnd": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/encode.py --trigger session-end",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Behavior:**
- Non-blocking (session ends normally if encoding fails)
- Captures any work done after last PreCompact
- May use JSONL fallback if context already compacted

### Stop Hook

**Trigger:** When Claude stops working (optional, disabled by default)

**Purpose:** Capture intermediate session points

**Configuration:**
```yaml
triggers:
  stop: false  # Disabled by default (too frequent)
```

**Note:** Not recommended for general use - creates too many episodic records

### SessionStart Hook

**Trigger:** When Claude Code session starts

**Purpose:** Check memory statistics and suggest actions

**Implementation:**
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/status.py --silent",
          "timeout": 5
        }
      ]
    }
  ]
}
```

**Behavior:**
- Reports session count to user
- Suggests `/pms:reflect` if 10+ sessions accumulated
- Silent mode: Only shows if actionable

## Data Flow

### Encoding Flow

```
Session Activity
      ↓
Hook Trigger (PreCompact/SessionEnd/Stop)
      ↓
encode.py --trigger={event}
      ↓
Try: encode_from_context()
      ↓ (on failure)
Try: encode_from_jsonl()
      ↓
Apply Privacy Redaction
      ↓
Save to Monthly File (.claude/pms/episodic/sessions-YYYY-MM.json)
      ↓
Update Index (.claude/pms/episodic/index.json)
      ↓
[Optional] Trigger Extraction (if continuous_mode)
```

### Extraction Flow

```
User: /pms:extract
  OR
Automatic (if continuous_mode)
      ↓
extract.py --min-sessions=10
      ↓
Load All Episodic Records
      ↓
Check Session Count >= min_sessions
      ↓
Extract User Preferences (count occurrences)
      ↓
Extract Code Patterns (count occurrences)
      ↓
Extract Anti-Patterns (count occurrences)
      ↓
Filter by Threshold (emerging >= 2)
      ↓
Categorize Strength (2=emerging, 3=strong, 5=critical)
      ↓
Save to Semantic Files (.claude/pms/semantic/)
      ↓
Report: X patterns detected (Y strong, Z critical)
```

### Synthesis Flow

```
User: /pms:synthesize
  OR
User: /pms:reflect (extract + synthesize)
      ↓
synthesize.py [--auto-approve]
      ↓
Load Semantic Patterns
      ↓
Filter: strength >= "strong"
      ↓
Group by Category (preferences, code, anti-patterns)
      ↓
Generate Markdown Rules
      ↓
Save to .claude/rules/pms/{category}.md
      ↓
Update Metadata (.claude/pms/procedural/rules-metadata.json)
      ↓
Report: X rule files generated
      ↓
User: Restart Claude Code session to load new rules
```

## Configuration System

**Configuration File:** `.claude/pms.local.md`

**Format:** YAML frontmatter + markdown documentation

**Schema:**
```yaml
triggers:
  precompact: boolean       # Encode before compaction
  session_end: boolean      # Encode at session end
  stop: boolean             # Encode when Claude stops
  session_start: boolean    # Show status at session start

thresholds:
  min_sessions: integer     # Minimum episodic records before extraction
  emerging_pattern: integer # Minimum occurrences for emerging
  strong_pattern: integer   # Minimum occurrences for strong (rule-worthy)
  critical_pattern: integer # Minimum occurrences for critical

privacy:
  redact_sensitive: boolean           # Enable automatic redaction
  custom_redaction_patterns: string[] # Additional regex patterns

encoding:
  prefer_context: boolean   # Prefer context-first over JSONL
  fallback_jsonl: boolean   # Use JSONL if context fails

extraction:
  auto_extract: boolean     # Auto-extract after encoding
  continuous_mode: boolean  # Synonym for auto_extract

synthesis:
  auto_synthesize: boolean  # Generate rules without approval
  require_approval: boolean # Require user approval (inverse of auto)
```

**Defaults:**
```python
PMSConfig(
    precompact=True,
    session_end=True,
    stop=False,
    session_start=False,
    min_sessions=10,
    emerging_pattern=2,
    strong_pattern=3,
    critical_pattern=5,
    redact_sensitive=True,
    custom_redaction_patterns=[],
    prefer_context=True,
    fallback_jsonl=True,
    auto_extract=False,
    continuous_mode=False,
    auto_synthesize=False,
    require_approval=True
)
```

## Privacy and Security

### Automatic Redaction

**Default Patterns:**
```python
DEFAULT_PATTERNS = [
    # API keys and tokens
    (r'\b[A-Za-z0-9_-]{20,}\b', '[REDACTED_TOKEN]'),
    (r'api[_-]?key[\'"\s:=]+[\w-]+', 'api_key=[REDACTED]'),
    (r'access[_-]?token[\'"\s:=]+[\w-]+', 'access_token=[REDACTED]'),
    (r'secret[_-]?key[\'"\s:=]+[\w-]+', 'secret_key=[REDACTED]'),

    # Passwords
    (r'password[\'"\s:=]+[^\s\'",}]+', 'password=[REDACTED]'),

    # Bearer tokens
    (r'Bearer\s+[\w-]+', 'Bearer [REDACTED]'),
]
```

**Custom Patterns:**
Users can add project-specific patterns via configuration:
```yaml
privacy:
  custom_redaction_patterns:
    - "internal[_-]?token"
    - "company_secret"
```

**Recursive Redaction:**
- Applies to strings, dictionaries, lists, nested structures
- Preserves data structure, only redacts values
- Returns: `(redacted_data, redaction_count)`

**Over-Redaction Strategy:**
If redaction fails (exception during processing):
1. Log error to stderr
2. Conservatively redact entire sensitive fields
3. Mark fields with `[REDACTED - redaction error]`
4. Continue encoding with over-redacted data

### Project-Scoped Isolation

**Memory Storage:** All memory files stored in `{project}/.claude/pms/`

**Benefits:**
- No cross-project contamination
- Each project learns independently
- Privacy by design (no global memory)
- Easy cleanup (delete `.claude/pms/` to reset)

**Sharing:** Future feature - selective export/import of specific patterns

## Error Handling and Recovery

### Corruption Recovery

**JSON Corruption:**
- **Detection:** Safe load with default fallback
- **Handling:** Skip corrupted files, continue with valid files
- **Reporting:** Log corrupted filenames to stderr
- **Backup:** Corrupted files moved to `.backup/` directory

**Recovery Utilities (`scripts/recovery.py`):**

1. **rebuild_semantic(project_path)**
   - Rebuilds semantic knowledge from episodic records
   - Use when `semantic/` corrupted or deleted
   - Re-runs pattern detection on all episodic records

2. **backup_corrupted(filepath)**
   - Moves corrupted file to `.backup/` with timestamp
   - Removes original corrupted file
   - Allows cleanup without data loss

3. **validate_memory_structure(project_path)**
   - Validates all PMS JSON files
   - Checks: structure, required fields, JSON validity
   - Returns: `(is_valid, error_messages)`

4. **reset_pms(project_path, keep_episodic=True)**
   - Resets PMS to clean state
   - Optional: preserve episodic records
   - Removes: semantic, procedural, rule files

### Timeout Handling

**Encoding Timeout (30s):**
- Saves partial record with `[TIMEOUT]` marker
- Includes limitations array
- Session continues normally

**Extraction Timeout (60s):**
- Raises `ExtractionTimeoutError`
- Cancels alarm (Unix-like systems)
- Returns False to caller

**Synthesis:** No timeout (user-initiated, fast operation)

### Malformed JSONL Handling

**Strategy:** Best-effort parsing
- Skip malformed lines (JSON decode errors)
- Log first 5 errors to stderr
- Continue processing valid lines
- Limit: 1000 records per file (performance)

**Reporting:**
```
Skipped 3 malformed JSONL lines, processed 127 valid lines
```

## Testing Architecture

### Unit Tests (`tests/`)

**Coverage:** 79 tests, ~85% code coverage

**Test Categories:**
- `test_config.py` - Configuration loading and validation
- `test_json_handler.py` - JSON corruption recovery, atomic writes
- `test_redaction.py` - Privacy redaction (all patterns and structures)
- `test_encode.py` - Episodic encoding logic
- `test_extract.py` - Semantic pattern detection
- `test_synthesize.py` - Procedural rule generation
- `test_recovery.py` - Recovery utilities

**Testing Patterns:**
- Pytest framework
- Temp directories for isolation
- Mock complex dependencies (filesystem, git)
- Test both success and failure paths

### Integration Tests (`tests/integration/`)

**Full Pipeline Test (`test_full_pipeline.sh`):**

**Steps:**
1. Create test project structure
2. Create test configuration
3. Create mock session transcripts (JSONL)
4. Run episodic encoding (4 sessions)
5. Populate pattern data (manual for testing)
6. Run semantic extraction
7. Run procedural synthesis
8. Validate JSON schemas
9. Test recovery utilities

**Verification:**
- All files created correctly
- Pattern detection works
- Rule generation succeeds
- JSON schemas valid
- Memory structure valid

**Environment:** Windows 11 compatible (uses bash from Git Bash)

## Performance Considerations

### Encoding Performance

**Context-First:** Fast (< 1s typical)
- Direct access to conversation history
- No file I/O
- Minimal processing

**JSONL Fallback:** Moderate (1-5s typical)
- File search: `~/.claude/projects/**/transcripts/*.jsonl`
- Parse up to 1000 lines per file
- Skip malformed lines

**Timeout:** 30s limit prevents runaway encoding

### Extraction Performance

**Session Count Impact:**
- 10 sessions: < 1s
- 50 sessions: < 5s
- 100 sessions: < 10s

**Optimization:**
- Single pass through all sessions
- In-memory processing (no repeated file reads)
- Early exit if insufficient sessions

**Timeout:** 60s limit for large projects

### Synthesis Performance

**Fast Operation:** < 1s typical
- Reads one semantic file
- Filters patterns (in-memory)
- Generates markdown (simple templates)
- Writes few output files

**No Timeout:** User-initiated, blocking operation

### Memory Footprint

**Encoding:** Low (< 10 MB)
- Single session data
- Minimal context
- Immediate file write

**Extraction:** Moderate (< 50 MB for 100 sessions)
- All episodic records in memory
- Pattern dictionaries
- Transient data structures

**Synthesis:** Minimal (< 5 MB)
- Few patterns
- Small rule files

## Future Architecture Considerations

### Version 2.0 Enhancements

**Import/Export System:**
- Selective pattern sharing between projects
- Export: Generate portable pattern bundles
- Import: Merge external patterns with local knowledge
- Conflict resolution for duplicate patterns

**Pattern Confidence Scoring:**
- Machine learning-based pattern validation
- Confidence score per pattern (0.0 - 1.0)
- Threshold: Only synthesize patterns with confidence > 0.7
- Features: recency, consistency, user explicit feedback

**Visual Pattern Dashboard:**
- Web UI for memory exploration
- Timeline view of episodic records
- Pattern evolution graphs
- Rule management interface

**Cross-Session Context:**
- Link related sessions by topic/feature
- Session chains (series of related work)
- Context inheritance (session N builds on session N-1)
- Enhanced pattern detection across chains

## Dependencies

**Runtime:**
- Python 3.8+ (scripts)
- Bash 4.0+ (hooks)
- Claude Code 1.0+ (plugin system)

**Python Packages:**
- Standard library only (no external dependencies)
- `json`, `pathlib`, `re`, `datetime`, `collections`

**Platform:**
- Windows 11 (primary target)
- macOS / Linux (Unix-like systems with SIGALRM support)

**No External Services:**
- No Cipher dependency (project-scoped only)
- No internet connectivity required
- Fully offline operation

## Deployment

**Distribution:** jcmrs-plugins marketplace

**Installation:** Automatic via plugin system

**Activation:**
- Plugin enabled by default
- Hooks register on plugin load
- No additional setup required

**Configuration:**
- Optional: Create `.claude/pms.local.md` for customization
- Defaults work for most users

**Upgrade Path:**
- Plugin updates via marketplace
- Memory format versioned (forward compatibility)
- Automatic migration for schema changes

---

**Document Version:** 1.0
**Last Updated:** 2025-12-31
**Maintained By:** jcmrs-plugins team
