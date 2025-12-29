# Semantic Linguist Plugin

**Version:** 1.0.0
**Type:** Cognitive Adapter, Semantic Bridge

## Overview

Semantic Linguist is a proactive plugin that bridges the gap between human natural language and AI technical specificity. It provides real-time semantic validation and ontological translation to prevent miscommunication, assumptions, and hallucinations during conversations with Claude Code.

### The Problem

Users frequently encounter the "abyss" between natural language intent and technical precision:
- Vague terminology: "make it talk", "we need an api"
- Ambiguous requests: "can you check for gaps", "make it portable"
- Meta-questions triggering assumptions: "am I making sense?", "does this make sense?"
- Made-up terms that drag conversations into interpretation territory

Without intervention, these ambiguities lead to:
- AI assumptions and hallucinations
- Misaligned implementations
- Wasted development time
- Project failures from misunderstood requirements

### The Solution

Semantic Linguist operates as a **First Line of Defense**, intercepting potentially ambiguous user messages and providing:

1. **Real-time Ambiguity Detection** - Identifies vague, ambiguous, or unclear terminology
2. **Domain Knowledge Validation** - Verifies requests against technical domain knowledge (Autogen, Langroid, etc.)
3. **Ontological Translation** - Maps natural language to precise technical concepts
4. **Conversational Clarification** - Asks clarifying questions before proceeding with assumptions

## Features

### 🔍 Proactive Ambiguity Detection

- **UserPromptSubmit Hook**: Analyzes every user message in real-time
- **Pattern Matching**: Detects vague verbs, unclear references, domain confusion
- **Confidence Scoring**: Only triggers on high-confidence ambiguities (>80%)
- **User Trigger Recognition**: Responds to meta-questions like "am I making sense?"

### 🧠 Semantic Validation Skill

- **Progressive Disclosure**: Lean core skill with detailed references
- **Domain Knowledge Graphs**: Autogen, Langroid, and extensible to custom domains
- **Decision Trees**: Systematic approach to resolving ambiguities
- **Translation Patterns**: Comprehensive mappings from ambiguous → precise terminology

### 📚 Multi-Domain Knowledge

Supports multiple technical domains with full API coverage:
- **Autogen**: Multi-agent frameworks, ConversableAgent, GroupChat, etc.
- **Langroid**: ChatAgent, ToolAgent, multi-agent patterns
- **Extensible**: Add custom domain knowledge for your specific tech stack

### ⚙️ Manual Commands

- **`/validate-terminology`**: Analyze recent conversation (5-10 messages) for ambiguities
- **`/map-domain`**: Explore domain terminology mappings interactively
- **`/semantic-config`**: Configure detection sensitivity and user trigger phrases

### 🎯 Conversational Interaction

Never assumes - always verifies:
- Presents options when ambiguity detected
- Asks clarifying questions before proceeding
- Maintains conversational, non-intrusive tone
- Provides detailed reports on request

## Installation

### From Marketplace

```bash
# (Future: marketplace installation)
```

### Local Installation

1. Clone or copy plugin to your project:
   ```bash
   cp -r plugins/semantic-linguist ~/.claude-plugins/
   ```

2. Enable plugin in Claude Code:
   ```bash
   claude --enable-plugin semantic-linguist
   ```

3. Plugin activates silently - no configuration required (uses defaults)

### Optional Configuration

Create `.claude/semantic-linguist.local.md` to customize:

```yaml
---
# Detection sensitivity: low, medium, high
sensitivity: medium

# Interaction style: explicit, guided, silent
interaction: explicit

# Enabled domains
domains:
  - autogen
  - langroid

# Custom user trigger phrases (in addition to defaults)
user_triggers:
  - "is this right?"
  - "checking in"

# Custom terminology mappings
custom_mappings:
  - from: "chat agent"
    to: "ConversableAgent"
    domain: autogen
---
```

## Usage

### Automatic (Recommended)

Semantic Linguist works automatically in the background:

**User:** "I want to create an agent that can talk to other agents"

**Semantic Linguist detects ambiguities and intervenes:**

```
I notice a few terms that could mean different things:

1. "agent" - In Autogen, this could be:
   - ConversableAgent (chat-based interactions)
   - AssistantAgent (task execution with tools)
   - UserProxyAgent (human-in-the-loop)

2. "talk to other agents" - Could mean:
   - GroupChat (multi-agent conversation)
   - Agent-to-agent messaging (send/receive)
   - Task delegation pattern

Which framework are you using, and what kind of interaction
did you have in mind?
```

### Manual Validation

Use commands for explicit validation:

```bash
# Validate recent conversation for ambiguities
/validate-terminology

# Explore domain mappings
/map-domain

# Configure sensitivity and triggers
/semantic-config
```

## Configuration

### Default Settings

Out-of-the-box experience:
- **Sensitivity**: Medium (balanced false positive/negative rate)
- **Interaction**: Explicit (transparent validation)
- **Domains**: Autogen + Langroid enabled
- **Confidence Threshold**: 80% (high confidence only)

### User Triggers

Default phrases that trigger semantic validation:
- "am I making sense?"
- "does this make sense?"
- "non-technical user"
- "am I doing this right?"

Add custom triggers via `/semantic-config` or settings file.

### Detection Patterns

Ambiguity patterns recognized:
- **Vague action verbs**: "make it work", "do the thing", "fix it"
- **Unclear references**: "that", "the previous thing", "like before"
- **Domain confusion**: Mixing business and technical terminology
- **Invented terms**: User-created words not in domain vocabulary
- **Meta-questions**: Seeking validation or confirmation

## Architecture

### Components

```
semantic-linguist/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/
│   └── semantic-validation/     # Core cognitive framework
│       ├── SKILL.md             # Lean skill (1,500-2,000 words)
│       ├── references/          # Detailed frameworks and decision trees
│       ├── examples/            # Real-world ambiguity examples
│       └── knowledge/           # Domain knowledge (separate JSON files)
├── commands/
│   ├── validate-terminology.md # Explicit validation command
│   ├── map-domain.md            # Domain mapping explorer
│   └── semantic-config.md       # Configuration command
├── hooks/
│   └── hooks.json               # UserPromptSubmit hook config
└── scripts/
    ├── detect-ambiguity.py      # Pattern matching utilities
    ├── domain-mapper.py         # Translation logic
    └── knowledge-query.py       # Unified knowledge interface
```

### Knowledge Sources (Query Order)

1. **Static Knowledge**: Fast, always-available JSON files
   - `ambiguous-terms.json`
   - `technical-mappings.json`
   - `ontology-graph.json`

2. **External Documentation**: Current, authoritative sources
   - Official docs (via WebFetch, context7, etc.)
   - API references
   - Examples and guides

3. **Codebase Validation**: Project-specific usage
   - LSP symbol definitions
   - Grep for actual implementations
   - Context-aware recommendations

## Examples

### Example 1: API Ambiguity

**User:** "we need an api"

**Without Semantic Linguist:**
```
Sure! I'll create a REST API server with Express...
[Proceeds with HTTP server implementation]
```

**With Semantic Linguist:**
```
⚠️ "api" could mean several things:

1. HTTP REST API server (Express, FastAPI, Flask)
2. API client (to consume external APIs)
3. API design/documentation (OpenAPI spec)
4. Internal API/interface (function signatures)

What kind of API are you building?
```

### Example 2: Portability Ambiguity

**User:** "we need this portable"

**Without Semantic Linguist:**
```
I'll containerize it with Docker...
[Assumes Docker is the solution]
```

**With Semantic Linguist:**
```
"Portable" could mean:

1. Cross-platform (Windows/Mac/Linux compatible)
2. Containerized (Docker/Podman)
3. Dependency vendoring (bundled dependencies)
4. Executable binary (standalone distribution)

Which type of portability do you need?
```

### Example 3: User Trigger

**User:** "am I making sense here?"

**Semantic Linguist recognizes meta-question and validates:**
```
Let me verify I understand correctly. You mentioned:
- [Key point 1 from recent messages]
- [Key point 2 from recent messages]

Potential ambiguities I noticed:
- "[Term X]" could mean [Option A] or [Option B]
- "[Term Y]" isn't standard in [Domain] - did you mean [Precise Term]?

Does this match your intent?
```

## Top 5 Ambiguities Handled

Based on real user experiences:

1. **"make it talk"** → ConversableAgent.send() vs speech synthesis vs conversation interface
2. **"we need an api"** → HTTP server vs API client vs API design vs internal interface
3. **"make it portable"** → Docker vs cross-platform vs vendoring vs executable
4. **"check for gaps"** → Code coverage vs documentation vs features vs security analysis
5. **"am I making sense"** → User seeking validation (trigger semantic check)

## Future Enhancements

Documented in [Option C Future Reference](./docs/option-c-agent.md):

- **Autonomous Agent**: Deep semantic analysis with tool use
- **Learning System**: Adapt mappings based on user feedback
- **Multi-domain Expansion**: Add more technical domains
- **Codebase Integration**: LSP-based project-specific validation

## Development

### Requirements

- Python 3.9+ (for scripts)
- UV (for dependency management if needed)
- Claude Code 2.0+

### Testing

```bash
# Validate plugin structure
cc validate-plugin semantic-linguist

# Test hook configuration
./scripts/test-hook.sh

# Test ambiguity detection
python scripts/detect-ambiguity.py --test
```

## Contributing

1. Add domain knowledge to `skills/semantic-validation/knowledge/`
2. Document new ambiguity patterns in `examples/`
3. Extend detection patterns in `scripts/detect-ambiguity.py`
4. Test thoroughly with real-world scenarios

## License

MIT

## Author

jcmrs

---

**Remember:** "Never ASSUME - it makes an ass out of u and me." Always verify, never interpret.
