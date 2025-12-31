# Procedural Memory System - Usage Examples

> **"Shame on you."** - Because Claude learns from your corrections.

This guide provides practical examples of using PMS in real-world workflows. PMS learns both **rigid procedures** (technical patterns, coding practices) and **flexible processes** (workflows, decision-making patterns), ensuring comprehensive behavioral learning across sessions.

## Example 1: Basic Workflow - First-Time Setup

### Scenario
You've just installed claude-pms and want to start building long-term memory for your project.

### Steps

**1. Configure PMS (Optional - defaults work well)**
```bash
# Create configuration file
cat > .claude/pms.local.md << 'EOF'
---
triggers:
  precompact: true      # Auto-encode before context compaction
  session_end: true     # Auto-encode when session ends
  stop: false           # Don't auto-encode on every stop

thresholds:
  min_sessions: 10      # Need 10 sessions before extraction
  emerging_pattern: 2   # 2+ occurrences = emerging
  strong_pattern: 3     # 3+ occurrences = strong
  critical_pattern: 5   # 5+ occurrences = critical

privacy:
  redact_sensitive: true
  custom_redaction_patterns: []

processing:
  continuous_mode: false
  auto_extract: false
  auto_synthesize: false
---

# PMS Configuration

Default configuration works well for most projects. Automatic encoding happens at natural session boundaries (context compaction, session end).
EOF
```

**2. Work on your project normally**
```
# Example: Implement authentication feature
Claude Code → Implement JWT authentication
Claude Code → Add refresh token endpoint
Claude Code → Create middleware for auth validation
[Work continues...]
```

**3. Encoding happens automatically**

When you reach context limit or end session, PMS automatically encodes:
```
[PreCompact hook triggers]
✓ Encoded session to .claude/pms/episodic/sessions-2025-12.json
  Session ID: session-20251231-103045
  Transcript: .claude/projects/myproject/transcripts/session-20251231-103045.jsonl
  Tool calls: 15
  Files modified: 8
```

**4. Continue working for 9 more sessions**

PMS encodes each session automatically. No manual intervention needed.

**5. After 10 sessions, check status**
```
/pms:status
```

Output:
```
Procedural Memory System Status
=============================

Episodic Memory:
  Sessions: 10
  Latest: session-20251231-153022 (2025-12-31 15:30:22)
  Storage: .claude/pms/episodic/

Semantic Memory:
  Status: Ready for extraction (10+ sessions)
  Last extraction: Never

Procedural Memory:
  Rules: 0
  Last synthesis: Never

Next Steps:
  Run /pms:extract to analyze patterns
```

**6. Extract patterns**
```
/pms:extract
```

Output:
```
Analyzing 10 episodic records...
Detected 4 patterns:
  - 3 user preferences (1 strong, 2 emerging)
  - 2 code patterns (1 strong, 1 emerging)
  - 1 anti-pattern (emerging)

Strong patterns:
  ✓ "Use HTTPOnly cookies for auth" (5 occurrences)
  ✓ "Repository pattern for data access" (3 occurrences)

Saved to .claude/pms/semantic/
```

**7. Review patterns**
```bash
cat .claude/pms/semantic/patterns.json | jq '.patterns[] | select(.strength == "strong")'
```

Output:
```json
{
  "pattern_id": "pref_1735649422",
  "description": "Use HTTPOnly cookies for auth",
  "category": "preference",
  "strength": "strong",
  "occurrences": 5,
  "evidence": [
    "session-20251231-103045",
    "session-20251231-113012",
    "session-20251231-123401",
    "session-20251231-133022",
    "session-20251231-143015"
  ],
  "detected_at": "2025-12-31T15:45:22Z"
}
```

**8. Generate rules**
```
/pms:synthesize
```

Output:
```
Synthesizing rules from semantic patterns...

Strong patterns eligible for rule generation:
  1. "Use HTTPOnly cookies for auth" (preference, 5 occurrences)
  2. "Repository pattern for data access" (code_pattern, 3 occurrences)

Generate rules for these patterns? (y/n): y

✓ Generated .claude/rules/pms/preference_use-httponly-cookies.md
✓ Generated .claude/rules/pms/code-pattern_repository-pattern.md

Rules will apply to all future sessions.
```

**9. Verify rules are loaded**
```bash
cat .claude/rules/pms/preference_use-httponly-cookies.md
```

Output:
```markdown
---
pattern_id: pref_1735649422
category: preference
strength: strong
occurrences: 5
---

# User Preference: HTTPOnly Cookie Authentication

**Detected Pattern**: User consistently prefers using HTTPOnly cookies for authentication tokens across 5 sessions.

**Apply this guidance**: When implementing authentication:
- Store JWT tokens in HTTPOnly cookies
- Avoid localStorage for sensitive tokens
- Set Secure flag in production
- Implement CSRF protection

**Evidence**:
- session-20251231-103045: JWT authentication implementation
- session-20251231-113012: Refresh token endpoint
- session-20251231-123401: Auth middleware
- session-20251231-133022: User service integration
- session-20251231-143015: Security review
```

**10. Test rules in new session**

Start new session and ask Claude to implement authentication:
```
Claude Code → Add logout endpoint with token invalidation
```

Claude will automatically apply the rule and use HTTPOnly cookies without being told.

---

## Example 2: Advanced Workflow - Manual Control

### Scenario
You want fine-grained control over pattern detection and rule generation.

### Configuration
```yaml
---
triggers:
  precompact: false     # Manual encoding only
  session_end: false
  stop: false

thresholds:
  min_sessions: 5       # Lower threshold for faster feedback
  emerging_pattern: 2
  strong_pattern: 4     # Higher threshold for quality
  critical_pattern: 7

processing:
  continuous_mode: false
  auto_extract: false
  auto_synthesize: false
---
```

### Workflow

**1. Selective encoding**

Only encode sessions with significant learnings:
```
# After implementing complex feature
/pms:encode

# Skip encoding routine bug fixes
[No encoding]

# After architectural decisions
/pms:encode
```

**2. Early extraction**

Check patterns after 5 sessions instead of 10:
```
/pms:extract
```

**3. Review before synthesis**

Examine patterns carefully:
```bash
# Review all patterns
cat .claude/pms/semantic/patterns.json | jq '.patterns[]'

# Check pattern quality
cat .claude/pms/semantic/patterns.json | jq '.patterns[] | select(.occurrences >= 4)'

# Review specific category
cat .claude/pms/semantic/code-patterns.json
```

**4. Selective synthesis**

Generate rules only for verified patterns:
```
# Edit patterns.json to mark patterns for synthesis
# Then run synthesis with approval
/pms:synthesize
```

**5. Custom pattern filtering**

Create filtered pattern file:
```bash
cat .claude/pms/semantic/patterns.json | \
  jq '.patterns |= map(select(.strength == "strong" or .strength == "critical"))' \
  > .claude/pms/semantic/patterns-filtered.json
```

---

## Example 3: Privacy-Conscious Workflow

### Scenario
Working on project with sensitive data. Need strict privacy controls.

### Configuration
```yaml
---
privacy:
  redact_sensitive: true
  custom_redaction_patterns:
    - 'internal[_-]?api[_-]?key'
    - 'database[_-]?connection[_-]?string'
    - 'customer[_-]?id:\s*\d+'
    - 'email:\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
---
```

### Workflow

**1. Verify redaction**

After encoding, check episodic records:
```bash
# Check for sensitive data
grep -r "api_key" .claude/pms/episodic/
grep -r "password" .claude/pms/episodic/
grep -r "@" .claude/pms/episodic/

# Should only find [REDACTED] markers
```

**2. Test custom patterns**

Verify custom redaction works:
```bash
cat .claude/pms/episodic/sessions-2025-12.json | \
  grep -E "internal_api_key|database_connection|customer_id|email"
```

Expected: All matches show `[REDACTED]`

**3. Review before synthesis**

Check semantic patterns don't contain sensitive data:
```bash
cat .claude/pms/semantic/patterns.json | \
  grep -iE "password|secret|key|token|credential"
```

**4. Audit generated rules**

Before applying, verify rules don't leak sensitive information:
```bash
for rule in .claude/rules/pms/*.md; do
  echo "Checking $rule..."
  grep -iE "password|api_key|secret|token" "$rule"
done
```

---

## Example 4: Team Collaboration

### Scenario
Multiple developers using PMS on shared codebase.

### Setup

**1. Shared configuration**

Commit `.claude/pms.local.md` to repository:
```bash
git add .claude/pms.local.md
git commit -m "Add PMS configuration for team"
```

**2. Personal episodic records**

Add to `.gitignore`:
```
.claude/pms/episodic/
.claude/pms/semantic/
```

**3. Shared procedural rules**

Commit generated rules:
```bash
git add .claude/rules/pms/
git commit -m "Add team coding patterns from PMS"
```

### Workflow

**Developer A:**
```
# Work on feature
[10 sessions]
/pms:extract
/pms:synthesize
git add .claude/rules/pms/
git commit -m "Add repository pattern rule"
git push
```

**Developer B:**
```
git pull
# New rules automatically apply
[Rules from Developer A now active]
```

**Team lead:**
```
# Review rules before merging PR
cat .claude/rules/pms/*.md
# Approve or request changes
```

---

## Example 5: Continuous Mode (Advanced)

### Scenario
Research project with rapid iteration. Want automatic pattern detection.

### Configuration
```yaml
---
processing:
  continuous_mode: true
  auto_extract: true
  auto_synthesize: false  # Manual approval for rule generation

thresholds:
  min_sessions: 3  # Lower threshold for rapid feedback
---
```

### Workflow

**1. Work normally**
```
[Implement feature 1]
[Implement feature 2]
[Implement feature 3]
```

**2. Automatic processing**

After 3rd session:
```
[SessionEnd hook triggers]
✓ Encoded session
✓ Extracted patterns (3 sessions)
  - 2 emerging patterns detected
```

**3. Review and approve**
```
/pms:status
# Shows 2 emerging patterns ready for review

# Review patterns
cat .claude/pms/semantic/patterns.json

# Approve synthesis when patterns are strong
/pms:synthesize
```

---

## Example 6: Recovery from Corruption

### Scenario
Episodic JSON file corrupted. Need to recover.

### Workflow

**1. Detect corruption**
```
/pms:validate
```

Output:
```
Validating memory structure...

✗ Corrupted file detected:
  .claude/pms/episodic/sessions-2025-12.json
  Error: JSONDecodeError - Expecting ',' delimiter: line 45 column 5

Backing up corrupted file to:
  .claude/pms/.backup/sessions-2025-12_20251231-160322.json

Recommendations:
  1. Review backup file
  2. Attempt manual JSON repair
  3. Or remove file and lose this month's sessions
```

**2. Attempt repair**
```bash
# Edit backup file to fix JSON syntax
vim .claude/pms/.backup/sessions-2025-12_20251231-160322.json

# Copy repaired file back
cp .claude/pms/.backup/sessions-2025-12_20251231-160322.json \
   .claude/pms/episodic/sessions-2025-12.json
```

**3. Validate repair**
```
/pms:validate
```

**4. Rebuild semantic knowledge**
```
/pms:rebuild
```

Output:
```
Rebuilding semantic knowledge from episodic records...
Found 10 episodic records across 1 file
Extracting patterns...
✓ Detected 4 patterns
✓ Saved to .claude/pms/semantic/
```

---

## Example 7: Migration Between Projects

### Scenario
Want to apply patterns learned in Project A to Project B.

### Workflow

**1. Export patterns from Project A**
```bash
cd /path/to/project-a
cp -r .claude/rules/pms /tmp/pms-patterns-export
```

**2. Review and filter**
```bash
# Review all patterns
cat /tmp/pms-patterns-export/*.md

# Remove project-specific patterns
rm /tmp/pms-patterns-export/code-pattern_projecta-specific.md
```

**3. Import to Project B**
```bash
cd /path/to/project-b
mkdir -p .claude/rules/pms
cp /tmp/pms-patterns-export/* .claude/rules/pms/
```

**4. Verify rules apply**
```bash
# Check rules are loaded
ls -la .claude/rules/pms/

# Start new session - rules automatically active
```

---

## Troubleshooting Examples

### Problem: No patterns detected after 10 sessions

**Diagnosis:**
```
/pms:status
# Shows 10 sessions but 0 patterns

# Check episodic records
cat .claude/pms/episodic/sessions-2025-12.json | jq '.sessions[0]'
```

**Possible causes:**
1. Episodic records have empty pattern arrays (encoding doesn't populate them)
2. Threshold too high
3. Work too diverse (no recurring patterns)

**Solution:**
```
# Lower thresholds temporarily
# Edit .claude/pms.local.md:
thresholds:
  emerging_pattern: 1

# Re-extract
/pms:extract
```

### Problem: Too many noisy patterns

**Diagnosis:**
```
/pms:extract
# Shows 50+ patterns, mostly irrelevant

cat .claude/pms/semantic/patterns.json | jq '.count'
# Output: 53
```

**Solution:**
```
# Raise thresholds
# Edit .claude/pms.local.md:
thresholds:
  emerging_pattern: 3
  strong_pattern: 5
  critical_pattern: 8

# Re-extract with higher bar
/pms:extract
```

### Problem: Rules not applying in new sessions

**Diagnosis:**
```bash
# Check rules exist
ls -la .claude/rules/pms/

# Check rules are valid markdown
cat .claude/rules/pms/*.md
```

**Solutions:**
1. Restart Claude Code session to reload rules
2. Check rule file names don't have special characters
3. Verify rule frontmatter is valid YAML

---

## Best Practices Summary

1. **Start with defaults** - They work well for most projects
2. **Review before synthesizing** - Don't generate rules from low-quality patterns
3. **Use privacy redaction** - Always enable for production projects
4. **Regular reflection** - Run `/pms:reflect` at natural boundaries
5. **Validate periodically** - Run `/pms:validate` monthly
6. **Archive old sessions** - Keep episodic records manageable
7. **Version control rules** - Commit `.claude/rules/pms/` for team sharing
8. **Test recovery** - Verify backup/recovery before disaster strikes

