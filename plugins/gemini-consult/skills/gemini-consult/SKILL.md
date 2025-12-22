# Gemini Consult: Large Codebase Analysis Assistant

Intelligent consultation orchestrator that leverages Google Gemini's CLI for analyzing codebases exceeding typical context limitations.

## Core Purpose

Bridge the gap between context-constrained AI assistants and comprehensive codebase understanding by orchestrating strategic use of Google Gemini's expanded context window.

**Problem it solves:**
- Claude Code's context limits prevent full codebase analysis
- Large file comparisons exceed token budgets
- Project-wide pattern detection requires more context than available
- Architectural decisions need holistic codebase visibility

**Solution approach:**
- Intelligently route appropriate queries to Gemini CLI
- Construct optimal @ syntax queries for maximum insight
- Synthesize Gemini's analysis back into Claude Code workflow
- Preserve session efficiency by avoiding unnecessary context consumption

## When to Use Gemini Consult

**Trigger Conditions (Auto-recommend):**

The skill should activate when:
- User asks about "entire codebase", "whole project", "all files"
- Analysis scope > 5 files or > 100KB combined content
- Comparative analysis needed across distant modules
- Architecture or pattern questions requiring project-wide view
- Security audit or compliance verification across codebase
- Feature implementation verification in large projects

**User Explicit Triggers:**
- "Use Gemini to analyze..."
- "Consult Gemini about..."
- "@gemini check if..."

**When NOT to use:**
- Single file analysis (< 50KB) → Use Claude Code Read tool
- Already have sufficient context loaded
- Real-time debugging or rapid iteration
- Questions answerable from loaded files

## The 3-Phase Consultation Workflow

### Phase 1: Query Assessment & Planning

**Objective:** Determine if Gemini consultation is appropriate and construct optimal query strategy.

**Assessment Checklist:**
```javascript
assessment = {
  scope_size: estimate_file_count_and_size(),
  analysis_type: identify_analysis_category(),
  context_available: check_current_session_context(),
  query_complexity: evaluate_question_depth()
}

recommendation = {
  use_gemini: scope_size > threshold || analysis_type in ['architecture', 'security_audit', 'cross_project'],
  query_strategy: construct_query_plan(),
  expected_value: estimate_insight_gain()
}
```

**User Interaction:**

Present recommendation clearly:

"This analysis requires examining **[N files / X MB]** across **[scope]**. I recommend using Gemini CLI because [reason].

I'll construct a query that:
- Includes: [file patterns]
- Focuses on: [specific analysis aspects]
- Returns: [expected insights]

Proceed with Gemini consultation? [Yes / Adjust scope / Use Claude Code only]"

**Query Construction Strategy:**

Based on analysis type, determine optimal @ syntax pattern:

1. **Full Project Analysis:**
   ```bash
   gemini --all_files -p "Analyze complete project architecture"
   ```

2. **Directory-Scoped Analysis:**
   ```bash
   gemini -p "@src/ @tests/ Compare implementation vs test coverage"
   ```

3. **Multi-File Comparison:**
   ```bash
   gemini -p "@src/auth/login.js @src/auth/register.js @src/middleware/auth.js Analyze authentication flow consistency"
   ```

4. **Targeted Pattern Search:**
   ```bash
   gemini -p "@src/**/*.js Find all error handling patterns and identify inconsistencies"
   ```

### Phase 2: Query Execution & Monitoring

**Objective:** Execute Gemini CLI query and capture comprehensive output.

**Execution Protocol:**

1. **Construct Command:**
   ```bash
   gemini_command = build_query(
     scope: assessment.scope,
     prompt: refined_user_question,
     flags: determine_flags()
   )
   ```

2. **Execute with Monitoring:**
   ```bash
   # Execute via Bash tool
   result = bash_execute(gemini_command, timeout=120)

   # Monitor for:
   # - CLI availability (is gemini installed?)
   # - Authentication status (logged in?)
   # - Rate limiting (hit quota?)
   # - Error messages
   ```

3. **Capture Output:**
   - Full response text
   - Any warnings or errors
   - File inclusion confirmations
   - Token usage statistics (if available)

**Error Handling:**

```javascript
if (error.type === 'CLI_NOT_FOUND') {
  return {
    status: 'blocked',
    message: "Gemini CLI not installed. Install: npm install -g @google/generative-ai",
    fallback: "Use Claude Code tools for subset analysis?"
  }
}

if (error.type === 'AUTH_REQUIRED') {
  return {
    status: 'blocked',
    message: "Gemini CLI requires authentication. Run: gemini auth login",
    fallback: null
  }
}

if (error.type === 'RATE_LIMIT') {
  return {
    status: 'retry',
    message: "Gemini API rate limit reached. Retry in [time] or reduce scope?",
    fallback: "Split analysis into smaller chunks?"
  }
}

if (error.type === 'CONTEXT_OVERFLOW') {
  return {
    status: 'adjust',
    message: "Even Gemini's context exceeded. Analysis scope too large.",
    strategy: "Split into multiple focused queries with specific file patterns"
  }
}
```

### Phase 3: Synthesis & Integration

**Objective:** Transform Gemini's output into actionable insights for Claude Code workflow.

**Synthesis Process:**

1. **Parse Gemini Response:**
   - Extract key findings
   - Identify file-specific insights (with line references)
   - Categorize recommendations
   - Note confidence levels or uncertainties

2. **Contextualize for Current Session:**
   ```markdown
   ## Gemini Consultation Results

   **Query:** [original question]
   **Scope:** [files/directories analyzed]
   **Key Findings:**

   1. [Finding with file:line references]
   2. [Finding with architectural implications]
   3. [Finding with security considerations]

   **Recommendations:**
   - [Actionable item 1]
   - [Actionable item 2]

   **Follow-up Actions:**
   - [ ] Review identified files in Claude Code
   - [ ] Implement suggested changes
   - [ ] Verify with local testing
   ```

3. **Store in Cipher (Memory):**
   ```
   cipher_store("Gemini Consultation - [Topic]

   Analysis Type: [architecture/security/feature/pattern]
   Scope: [file patterns]
   Date: [timestamp]

   Key Insights:
   - [Insight 1 with file references]
   - [Insight 2 with implications]

   Recommended Actions:
   - [Action 1]
   - [Action 2]

   Query Pattern Used:
   ```bash
   [gemini command]
   ```

   Results archived for future reference.")
   ```

4. **Present to User:**

   Clear, structured output:

   "✅ Gemini Analysis Complete

   **Analyzed:** [N files across M directories]

   **Critical Findings:**

   1. **[Category]:** [Finding]
      - Files: `src/file1.js:45`, `src/file2.js:89`
      - Impact: [High/Medium/Low]
      - Action: [Specific recommendation]

   2. **[Category]:** [Finding]
      ...

   **Next Steps:**

   I've stored these insights in Cipher for future reference. Would you like me to:

   A) Deep dive into specific finding [#1, #2, etc.]
   B) Implement recommended changes
   C) Run focused analysis on subset
   D) Continue with different question"

## Analysis Type Patterns

### Architecture Analysis

**Trigger Patterns:**
- "How is [system] architected?"
- "What's the overall structure?"
- "Explain the codebase organization"

**Query Construction:**
```bash
gemini --all_files -p "Analyze the complete architecture:
1. Identify main components and their responsibilities
2. Map data flow between modules
3. Describe architectural patterns used
4. Note any architectural inconsistencies
5. Highlight coupling and dependency issues"
```

**Synthesis Focus:**
- Component diagram (textual representation)
- Dependency graph insights
- Pattern identification
- Architectural recommendations

### Security Audit

**Trigger Patterns:**
- "Security vulnerabilities?"
- "Check for [security issue]"
- "Audit authentication/authorization"

**Query Construction:**
```bash
gemini -p "@src/ @lib/ Perform security audit:
1. Identify potential SQL injection points
2. Check for XSS vulnerabilities
3. Verify authentication implementation
4. Review authorization logic
5. Check for exposed secrets or credentials
6. Assess input validation coverage"
```

**Synthesis Focus:**
- Vulnerability severity ranking
- Specific file:line locations
- Proof of concept (if safe to demonstrate)
- Remediation steps with code examples

### Feature Implementation Verification

**Trigger Patterns:**
- "Is [feature] implemented?"
- "How does [feature] work?"
- "Find all places where [feature] is used"

**Query Construction:**
```bash
gemini -p "@src/ Verify [feature] implementation:
1. Locate all files implementing this feature
2. Trace the complete execution flow
3. Identify edge cases handled
4. Check for test coverage
5. Note any incomplete or inconsistent implementations"
```

**Synthesis Focus:**
- Implementation completeness (%)
- File locations with code snippets
- Flow diagram (textual)
- Gaps or inconsistencies

### Pattern Detection

**Trigger Patterns:**
- "Find all [pattern] usage"
- "Identify inconsistent [pattern]"
- "How is [pattern] implemented across codebase?"

**Query Construction:**
```bash
gemini -p "@src/**/*.js Analyze [pattern] usage:
1. Find all instances of this pattern
2. Compare implementations for consistency
3. Identify outliers or anti-patterns
4. Suggest standardization approach"
```

**Synthesis Focus:**
- Pattern instances grouped by consistency
- Deviation analysis
- Refactoring recommendations

### Cross-Project Comparison

**Trigger Patterns:**
- "Compare [repo1] and [repo2]"
- "How does this differ from [other implementation]?"

**Query Construction:**
```bash
# Note: Requires sequential queries or multi-repo setup
gemini -p "@project1/src/ Analyze [aspect] implementation"
gemini -p "@project2/src/ Analyze same [aspect] implementation"
# Then ask Gemini to compare the two analyses
```

**Synthesis Focus:**
- Side-by-side comparison table
- Unique approaches in each
- Strengths/weaknesses
- Recommendation for current project

## Best Practices

### Query Construction Principles

1. **Be Specific:**
   - ❌ "Analyze the code"
   - ✅ "Analyze authentication flow in @src/auth/, focusing on session management and token validation"

2. **Scope Appropriately:**
   - ❌ `gemini --all_files -p "Fix bug"` (too broad)
   - ✅ `gemini -p "@src/auth/ @tests/auth/ Identify why session timeout isn't working"`

3. **Use Numbered Questions:**
   - Helps Gemini structure response
   - Makes synthesis easier
   - Ensures comprehensive coverage

4. **Include Expected Deliverables:**
   ```bash
   gemini -p "@src/ Analyze error handling. Provide:
   1. List of all error types caught
   2. Consistency analysis across modules
   3. Gaps in error coverage
   4. Recommendation for standardization"
   ```

### Context Management

**When to Chain Queries:**

Instead of one massive query, use sequential focused queries:

```bash
# Query 1: Discovery
gemini -p "@src/ Identify all database access patterns"

# Query 2: Deep Dive (based on Query 1 findings)
gemini -p "@src/models/ @src/repositories/ Analyze ORM usage consistency"

# Query 3: Verification
gemini -p "@tests/ Verify test coverage for identified DB patterns"
```

**Benefits:**
- More focused responses
- Better error recovery
- Progressive refinement
- Lower cost per query

### Integration with Claude Code Workflow

**Workflow Pattern:**

```
1. User asks broad question in Claude Code
2. Claude recognizes scope exceeds context
3. Gemini Consult skill activates
4. Execute Gemini query
5. Synthesize findings
6. Store in Cipher
7. Continue in Claude Code with specific file work
```

**Example:**

```
User: "I want to refactor our authentication system for better security"

Claude (recognizes large scope):
  → Activates Gemini Consult
  → Runs: gemini -p "@src/auth/ @middleware/ Analyze authentication architecture..."
  → Receives comprehensive analysis
  → Stores in Cipher
  → Responds: "Based on Gemini analysis, here are 5 critical areas..."

User: "Start with #1 - JWT token handling"

Claude (now focused):
  → Uses Read tool for specific files identified by Gemini
  → Implements changes using normal Claude Code workflow
  → References Gemini insights from Cipher as needed
```

## Error Handling

### CLI Availability Check

**Before any query:**
```bash
# Check if gemini CLI is available
which gemini || echo "NOT_FOUND"
```

**If not found:**
1. Inform user about installation
2. Provide installation command
3. Offer fallback (Claude Code subset analysis)
4. Store user preference (install later / use fallback)

### Authentication Management

**Check auth status:**
```bash
gemini auth status
```

**If not authenticated:**
1. Explain auth requirement
2. Provide auth command
3. Pause consultation until resolved
4. Resume when authenticated

### Scope Overflow Handling

**If Gemini returns context overflow:**

```javascript
overflow_strategy = {
  approach: "Divide and Conquer",

  steps: [
    "Split scope into logical chunks (by directory, feature, module)",
    "Run multiple focused queries",
    "Synthesize results client-side",
    "Present unified findings"
  ],

  example: {
    original: "gemini --all_files -p 'Analyze everything'",
    split: [
      "gemini -p '@src/frontend/ Analyze frontend architecture'",
      "gemini -p '@src/backend/ Analyze backend architecture'",
      "gemini -p '@src/shared/ Analyze shared utilities'",
      // Then synthesize findings
    ]
  }
}
```

### Result Quality Validation

**Validate Gemini output before presenting:**

```javascript
validation_checks = {
  // Gemini hallucination check
  file_references_exist: verify_files_exist(gemini_response.mentioned_files),

  // Response completeness
  addresses_all_query_points: check_numbered_questions_answered(),

  // Actionability
  has_specific_recommendations: !is_vague(gemini_response.recommendations),

  // Confidence indicators
  notes_uncertainties: gemini_response.includes("not sure", "possibly", "might")
}

if (!validation_checks.all_pass) {
  refine_query_and_retry_OR_flag_to_user();
}
```

## State Management

### Session State

```javascript
gemini_consult_state = {
  active_consultation: boolean,
  current_phase: 1 | 2 | 3,

  assessment: {
    scope: {...},
    strategy: {...},
    user_approved: boolean
  },

  execution: {
    command: string,
    status: 'pending' | 'running' | 'complete' | 'error',
    output: string,
    errors: []
  },

  synthesis: {
    findings: [],
    recommendations: [],
    follow_up_actions: [],
    stored_in_cipher: boolean
  }
}
```

### Persistence Strategy

**Store in Cipher after every successful consultation:**
- Query pattern used
- Scope analyzed
- Key findings
- Timestamp for future reference

**Retrieve from Cipher when:**
- Similar query detected
- User asks "what did Gemini say about X?"
- Building on previous analysis

## Key Principles

1. **Gemini for Breadth, Claude for Depth:** Use Gemini to understand the forest, Claude Code to work on specific trees

2. **Always Validate Scope:** Don't waste Gemini queries on small scopes Claude Code handles efficiently

3. **Synthesize, Don't Dump:** Transform Gemini's output into actionable Claude Code workflow steps

4. **Store Knowledge:** Gemini insights go into Cipher for long-term memory

5. **Progressive Refinement:** Start broad, narrow down based on findings

6. **User in Control:** Always ask permission before executing Gemini queries (they may have quota concerns)

7. **Graceful Fallback:** If Gemini unavailable, offer Claude Code alternatives (subset analysis, iterative exploration)

## Future Enhancements

**Planned Features:**
- Auto-detection of optimal query patterns based on question analysis
- Cost estimation before query execution
- Multi-stage query orchestration (discovery → deep-dive → verification)
- Integration with MCP servers for expanded analysis capabilities
- Query result caching to avoid redundant API calls

## Implementation Status

**Current:** Specification complete
**Next:** Implement Phase 1 (Query Assessment)
**Future:** Full 3-phase workflow, error handling, Cipher integration
