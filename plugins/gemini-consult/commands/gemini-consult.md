---
name: jcmrs:gemini-consult
description: Execute Google Gemini CLI for large codebase analysis using @ syntax
argument-hint: "[scope-pattern] [query]"
allowed-tools:
  - Bash
  - mcp__cipher__ask_cipher
---

# Gemini Consult Command

Execute Google Gemini CLI for analyzing large codebases that exceed Claude Code's context limits.

## Command Format

The command accepts free-form arguments combining scope patterns and queries:

```bash
/jcmrs:gemini-consult @src/main.py Explain this file's purpose and structure
/jcmrs:gemini-consult @package.json @src/index.js Analyze dependencies
/jcmrs:gemini-consult @src/ Summarize the architecture
/jcmrs:gemini-consult @src/ @tests/ Analyze test coverage
/jcmrs:gemini-consult @./ Give me an overview of this project
/jcmrs:gemini-consult --all_files Analyze project structure and dependencies
```

## Execution Protocol

### 1. Parse Arguments

Extract the complete query from user input:
- Everything after `/jcmrs:gemini-consult` is the query
- Query includes both scope patterns (@...) and question text
- Preserve exact formatting and spacing

### 2. Construct Gemini Command

Build the Gemini CLI command:

```bash
gemini -p "[complete user query]"
```

**Important**:
- Use double quotes around the entire prompt
- Escape any internal quotes if present
- Preserve @ syntax exactly as provided
- Include --all_files flag if present

### 3. Execute Query

Run the Gemini command via Bash tool:

```bash
gemini -p "[query]"
```

**Timeout**: Set to 120 seconds (Gemini queries can take time for large scopes)

**Error handling**:
- If gemini command not found: Direct user to run `/jcmrs:gemini-check`
- If timeout: Suggest reducing scope or splitting into multiple queries
- If other errors: Display error message and suggest diagnostics

### 4. Process Results

When Gemini returns output:

**A. Synthesize Summary**

Extract key insights:
- Main findings (3-5 bullet points)
- File references mentioned (with paths)
- Critical recommendations
- Confidence level or uncertainties noted

**B. Validate Output**

Quick validation checks:
- File paths mentioned: Note if they exist in current repo
- Specific claims: Flag any that seem uncertain
- Completeness: Check if query was fully addressed

**C. Format Response**

Present in this structure:

```markdown
## Gemini Analysis Results

**Query**: [original query]
**Scope**: [scope patterns used]

### Key Findings

1. [Finding 1 with file references]
2. [Finding 2 with implications]
3. [Finding 3 with recommendations]

### Recommendations

- [Actionable item 1]
- [Actionable item 2]

### Full Gemini Output

<details>
<summary>Click to expand complete response</summary>

[Complete Gemini output here]

</details>

---

*Analysis stored in Cipher for future reference*
```

### 5. Store in Cipher

Automatically store the consultation in Cipher:

```
mcp__cipher__ask_cipher("Store: Gemini Consultation - [Topic from query]

Query: [original query]
Scope: [scope patterns]
Date: [timestamp]

Key Findings:
- [Finding 1]
- [Finding 2]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]

Complete output archived for reference.")
```

**Storage benefits**:
- Future queries can reference past analyses
- User can ask "What did Gemini say about X?"
- Builds knowledge base over time

## Usage Tips

**Single file analysis**:
```bash
/jcmrs:gemini-consult @src/auth/login.js Explain authentication flow
```

**Comparative analysis**:
```bash
/jcmrs:gemini-consult @src/api/v1/ @src/api/v2/ Compare API versions
```

**Security audit**:
```bash
/jcmrs:gemini-consult @src/ Find SQL injection vulnerabilities
```

**Architecture review**:
```bash
/jcmrs:gemini-consult --all_files Analyze project architecture and dependencies
```

**Feature verification**:
```bash
/jcmrs:gemini-consult @src/ @tests/ Verify dark mode implementation
```

## Important Notes

- **Paths are relative**: @ patterns are relative to current working directory
- **Large scopes take time**: --all_files can take 30-60 seconds
- **Gemini required**: User must have `gemini` CLI installed and in PATH
- **No API key needed**: Assumes gemini is already authenticated
- **Results cached**: Gemini may cache results for identical queries

## Error Recovery

**Command not found**:
```
Error: 'gemini' command not found
→ Run /jcmrs:gemini-check to diagnose
→ Install: npm install -g @google/generative-ai
```

**Timeout**:
```
Error: Query timeout (>120s)
→ Reduce scope: Use specific directories instead of --all_files
→ Split query: Analyze frontend and backend separately
```

**Empty response**:
```
Error: Gemini returned no output
→ Check query syntax (@ patterns correct?)
→ Verify files exist at specified paths
→ Try simpler query first
```

## Integration with Skill

This command complements the gemini-consult skill:
- **Skill**: Provides knowledge about when/how to use Gemini
- **Command**: Executes the actual Gemini query
- **Both**: Store results in Cipher for continuity

Users can invoke this command directly or let the skill suggest it when appropriate.
