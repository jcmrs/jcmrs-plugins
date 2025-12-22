# Gemini Consult Skill

> **Analyze large codebases beyond Claude Code's context limits using Google Gemini's CLI**

## Overview

Gemini Consult is a Claude Code skill that intelligently routes large-scale codebase analysis to Google Gemini's CLI, leveraging its expanded context window for project-wide insights. It seamlessly integrates Gemini's analysis back into your Claude Code workflow.

### What It Does

- **Analyzes entire codebases** that exceed Claude Code's context limits
- **Compares multiple large files** for consistency and patterns
- **Performs project-wide audits** (architecture, security, features)
- **Detects patterns** across distributed codebase locations
- **Synthesizes findings** into actionable Claude Code workflow steps

### When to Use It

✅ **Use Gemini Consult when:**
- Analyzing 5+ files or > 100KB of code
- Need project-wide architectural understanding
- Performing security audits across codebase
- Verifying feature implementations in large projects
- Comparing implementations across modules

❌ **Use Claude Code directly when:**
- Working with single files (< 50KB)
- Already have sufficient context loaded
- Rapid iteration on known files
- Real-time debugging

## Prerequisites

### Install Google Gemini CLI

```bash
# Install via npm
npm install -g @google/generative-ai

# Authenticate
gemini auth login

# Verify installation
gemini --version
```

### API Key Setup

You'll need a Google AI API key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Configure during `gemini auth login`

## Quick Start

### Example 1: Analyze Complete Architecture

```
You: "Analyze the overall architecture of this project"

Claude (via Gemini Consult):
  → Detects large scope
  → Constructs query: gemini --all_files -p "Analyze architecture..."
  → Returns synthesized findings with file references
  → Stores insights in Cipher for future reference
```

### Example 2: Security Audit

```
You: "Check for security vulnerabilities across the codebase"

Claude (via Gemini Consult):
  → Scopes to @src/ @lib/ directories
  → Runs focused security audit query
  → Returns ranked findings with file:line references
  → Provides remediation steps
```

### Example 3: Feature Implementation Verification

```
You: "Is dark mode fully implemented across the app?"

Claude (via Gemini Consult):
  → Analyzes @src/ @components/ @styles/
  → Traces feature implementation
  → Reports completeness and gaps
  → Suggests next steps
```

## How It Works

### The @ Syntax

Gemini CLI uses `@` to reference files and directories:

```bash
# Single file
gemini -p "@src/main.py Explain this file"

# Multiple files
gemini -p "@package.json @src/index.js Analyze dependencies"

# Entire directory
gemini -p "@src/ Summarize architecture"

# All files in project
gemini --all_files -p "Find security issues"
```

### 3-Phase Consultation Workflow

**Phase 1: Query Assessment**
- Claude analyzes your question
- Determines if Gemini consultation is appropriate
- Constructs optimal query strategy
- Asks for your approval

**Phase 2: Execution**
- Executes Gemini CLI query
- Monitors for errors (auth, rate limits, etc.)
- Captures comprehensive output

**Phase 3: Synthesis**
- Transforms Gemini's output into actionable insights
- Provides file:line references
- Stores findings in Cipher (Claude's memory)
- Presents structured recommendations

## Usage Patterns

### Architecture Analysis

**Your question:**
```
"How is the authentication system architected?"
```

**What happens:**
```bash
# Gemini Consult constructs:
gemini -p "@src/auth/ @middleware/auth/ Analyze authentication architecture:
1. Identify main components
2. Map data flow
3. Describe patterns used
4. Note security measures"
```

**You receive:**
- Component breakdown with file locations
- Data flow description
- Pattern identification
- Security assessment
- Recommendations for improvements

### Cross-Module Comparison

**Your question:**
```
"Compare error handling across backend and frontend"
```

**What happens:**
```bash
# Gemini Consult runs:
gemini -p "@src/backend/ @src/frontend/ Compare error handling:
1. Backend error patterns
2. Frontend error patterns
3. Consistency analysis
4. Standardization recommendations"
```

**You receive:**
- Side-by-side comparison
- Inconsistencies highlighted
- Refactoring suggestions

### Pattern Detection

**Your question:**
```
"Find all database query patterns and identify inefficiencies"
```

**What happens:**
```bash
gemini -p "@src/**/*.js Find database query patterns:
1. List all query types
2. Identify N+1 queries
3. Note missing indexes
4. Suggest optimizations"
```

**You receive:**
- Query pattern inventory
- Performance issues with file:line references
- Optimization recommendations

## Integration with Claude Code

Gemini Consult seamlessly integrates into your Claude Code workflow:

```
┌─────────────────────────────────────────────────┐
│ You ask broad question in Claude Code           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Claude detects scope > context limits           │
│ → Activates Gemini Consult skill                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Presents query plan for your approval           │
│ "Analyzing [N files] with Gemini. Proceed?"     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Executes Gemini CLI query                       │
│ → Captures output                               │
│ → Validates results                             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Synthesizes findings                            │
│ → Extracts file:line references                 │
│ → Ranks by importance                           │
│ → Stores in Cipher                              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Presents structured results                     │
│ "Here are 5 critical findings..."               │
│ "Would you like me to deep dive into #1?"       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Continue in Claude Code with specific files     │
│ → Uses Read tool for targeted work              │
│ → References Gemini insights from Cipher        │
│ → Implements changes                            │
└─────────────────────────────────────────────────┘
```

## Best Practices

### 1. Be Specific in Your Questions

❌ **Vague:** "Analyze the code"

✅ **Specific:** "Analyze authentication flow focusing on session management and token validation"

### 2. Start Broad, Then Narrow

```
Step 1: "What's the overall architecture?" (Gemini)
Step 2: "Deep dive into auth module" (Claude Code + Gemini insights)
Step 3: "Implement specific fix in auth/login.js" (Claude Code)
```

### 3. Use for Analysis, Not Implementation

Gemini Consult is for **understanding and planning**, not writing code:
- ✅ "Identify all API endpoints"
- ✅ "Find security vulnerabilities"
- ✅ "Analyze test coverage gaps"
- ❌ "Write new authentication module" (use Claude Code)

### 4. Leverage Stored Insights

Gemini findings are stored in Cipher. Reference them later:
```
You: "Based on the Gemini analysis from earlier, implement fix #2"

Claude: → Retrieves insight from Cipher
        → Uses specific file references
        → Implements in Claude Code
```

## Common Use Cases

### 🏗️ Architecture Review

"Analyze the complete project architecture and identify coupling issues"

**Returns:** Component map, dependency graph, architectural patterns, recommendations

### 🔒 Security Audit

"Perform comprehensive security audit for SQL injection and XSS"

**Returns:** Vulnerability list (ranked), file:line locations, remediation steps

### ✅ Feature Verification

"Verify that pagination is consistently implemented across all list views"

**Returns:** Implementation locations, consistency analysis, gaps identified

### 📊 Code Quality Analysis

"Find all code smells and anti-patterns"

**Returns:** Issue categorization, examples with locations, refactoring suggestions

### 🔄 Migration Planning

"Analyze codebase for migration from React Class components to Hooks"

**Returns:** Component inventory, complexity assessment, migration order recommendations

## Troubleshooting

### "Gemini CLI not found"

```bash
# Install Gemini CLI
npm install -g @google/generative-ai

# Verify
gemini --version
```

### "Authentication required"

```bash
# Login to Gemini
gemini auth login

# Follow prompts to authenticate
```

### "Rate limit exceeded"

**Option 1:** Wait for quota reset (shown in error message)

**Option 2:** Reduce scope:
```
Instead of: gemini --all_files
Use: gemini -p "@src/specific-module/"
```

**Option 3:** Split into multiple focused queries

### "Context overflow even with Gemini"

Your project is extremely large. Use progressive analysis:

```
Query 1: gemini -p "@src/frontend/ Analyze frontend"
Query 2: gemini -p "@src/backend/ Analyze backend"
Query 3: gemini -p "@src/shared/ Analyze shared"

Then synthesize findings client-side
```

## Limitations

- **Not for real-time debugging:** Gemini queries take time; use Claude Code for rapid iteration
- **API costs:** Gemini API has usage costs; queries are metered
- **Internet required:** Gemini CLI needs internet connection
- **Not for code generation:** Use for analysis, not writing large code blocks

## Advanced Features

### Query Chaining

For complex analyses, chain multiple queries:

```
1. Discovery: gemini --all_files -p "Identify all state management approaches"
2. Deep Dive: gemini -p "@src/stores/ Analyze Redux usage patterns"
3. Verification: gemini -p "@tests/ Check test coverage for identified stores"
```

### Custom Scope Patterns

Target specific file types or patterns:

```bash
# All TypeScript files
gemini -p "@src/**/*.ts ..."

# Specific pattern
gemini -p "@src/**/auth*.js ..."

# Multiple directories
gemini -p "@src/components/ @src/hooks/ @src/utils/ ..."
```

## FAQ

**Q: When should I use Gemini vs Claude Code?**

A: Use Gemini for breadth (project-wide understanding), Claude Code for depth (specific implementation work).

**Q: Are Gemini queries free?**

A: Gemini API has usage-based pricing. Check [Google AI pricing](https://ai.google.dev/pricing) for details.

**Q: Can I use this offline?**

A: No, Gemini CLI requires internet connection and API access.

**Q: Will this slow down my Claude Code session?**

A: No - Gemini queries run externally. Your Claude session continues after receiving results.

**Q: What if Gemini gives wrong information?**

A: Gemini Consult validates file references and flags uncertainties. Always verify critical findings in Claude Code.

## Future Enhancements

**Planned improvements** (contributions welcome):

### Commands
- [ ] `/jcmrs:gemini-history` - View and re-run past Gemini consultations from Cipher
- [ ] Query templates for common analysis patterns (security audit, architecture review, etc.)
- [ ] Interactive query builder with scope pattern suggestions

### Agents
- [ ] **Query Constructor Agent** - Automatically builds optimal Gemini queries based on user questions
- [ ] **Result Validator Agent** - Deep validation of Gemini output before presenting to user

### Integrations
- [ ] **Serena (MCP) Integration** - Leverage Serena MCP server for enhanced analysis capabilities
  - Combine Gemini's breadth with Serena's specialized tools
  - Cross-reference findings between systems
  - Unified analysis workflow

### Settings
- [ ] User-configurable thresholds for auto-suggest (files count, size limits)
- [ ] Custom query templates in `.claude/gemini-consult.local.md`
- [ ] Saved query patterns for frequent analysis types

### Documentation
- [ ] Examples directory with common query patterns
- [ ] Video tutorials for different analysis scenarios
- [ ] Case studies: architecture reviews, security audits, migration planning

**Want to contribute?** See Contributing section below for how to get started.

## Contributing

Found a useful query pattern? Encountered an edge case? Contributions welcome:

1. Fork the repository
2. Add your pattern to SKILL.md
3. Test with real codebases
4. Submit pull request

## Support

- **Issues:** [GitHub Issues](https://github.com/jcmrs/jcmrs-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jcmrs/jcmrs-plugins/discussions)

## License

MIT License - see LICENSE file for details

---

**Built for Claude Code** | Powered by Google Gemini | Part of jcmrs-plugins marketplace
