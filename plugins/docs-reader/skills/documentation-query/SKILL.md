---
name: documentation-query
description: Access official collaboration platform documentation organized by platform components, protocols, and core competencies. Use when user asks about platform capabilities, how the framework works, or when Claude Code needs to reference architecture, implementation patterns, or best practices to answer questions accurately.
license: LICENSE
metadata:
  documentation: https://axivo.com/claude/
  profile: DEVELOPER, ENGINEER, RESEARCHER
  project: Claude Collaboration Platform
  repository: https://github.com/axivo/claude
---

# Documentation Query

Systematic access to official platform documentation through understanding-focused architecture.

## Skill Methodology

Documentation access through platform architecture understanding. Extends all profiles with structured reference to components, protocols, and competencies.

> [!IMPORTANT]
> The skill embodies Understand Architecture → Locate Precisely → Present Systematically
>
> - Understand platform architecture (Components, Protocols, Competencies)
> - Locate documentation based on query type
> - Present information that builds understanding

### Documentation Architecture

The platform documentation is organized for systematic understanding:

**Wiki** - Platform architecture and reference:
- **Components** (4 subsystems): Plugins, Documentation, Instructions, Memory
- **Protocols** (3 operational sequences): Equilibrium, Initialization, Response

**Tutorials** - Practical competency development:
- **Core Competencies** (5 skills): Session structuring, Communication, Continuity, Customization, Measurement

> [!IMPORTANT]
> Documentation structure reflects platform architecture - understanding the structure reveals how the platform works.

## Query Type Mapping

### User-Initiated Queries

When users ask questions, map to documentation structure:

| User Question | Documentation Source | Specific Section |
|---------------|---------------------|------------------|
| "Can Claude Code do X?" | Wiki → Components | Plugins, Documentation, Instructions, or Memory |
| "How does the framework work?" | Wiki → Protocols | Equilibrium, Initialization, or Response |
| "How do I configure X?" | Wiki → Getting Started | Configuration section |
| "Show me how to do X" | Tutorials → Competencies | Relevant competency (1-5) |
| "What are profiles?" | Wiki → Components | Memory System |
| "How do skills work?" | Wiki → Components | Plugins System |
| "What is the response protocol?" | Wiki → Protocols | Response Protocol |

### Agent-Initiated Queries

When Claude Code needs reference documentation:

| Claude Code Need | Documentation Source | Purpose |
|------------------|---------------------|---------|
| Explaining platform capabilities | Wiki → Components | Accurate capability description |
| Understanding framework behavior | Wiki → Protocols | Correct protocol application |
| Implementing plugin features | Wiki → Components → Plugins | Pattern reference |
| Teaching collaboration techniques | Tutorials → Competencies | Best practices |
| Troubleshooting framework issues | Wiki → Protocols | Diagnostic understanding |
| Profile customization guidance | Wiki → Components → Memory | Profile system reference |

> [!IMPORTANT]
> Agent queries are proactive - Claude Code should reference documentation to provide accurate, platform-aligned guidance.

## Understanding Stage

Clarify what type of understanding is needed.

### For User Queries

Ask focused questions to map to architecture:

- "Are you asking what the platform can do?" → Components
- "Are you asking how something works?" → Protocols
- "Are you asking how to do something?" → Competencies (Tutorials)

### For Agent Queries

Determine information need:

- Answering "Can it...?" → Components (verify capability)
- Explaining "How does...?" → Protocols (explain mechanism)
- Guiding "How to...?" → Competencies (teach technique)

## Location Stage

Use architecture understanding to locate documentation.

### Wiki Structure

Consult [wiki-index.md](./resources/wiki-index.md) for:

**Components Section:**
- Plugins System
- Documentation System
- Instructions System
- Memory System

**Protocols Section:**
- Equilibrium Protocol
- Initialization Protocol
- Response Protocol

**Getting Started:**
- Configuration and setup

### Tutorials Structure

Consult [tutorials-index.md](./resources/tutorials-index.md) for:

**Core Competencies:**
1. Session structuring
2. Effective communication
3. Cross-session continuity
4. Profile customization
5. Effectiveness measurement

## Presentation Stage

Fetch and present with architectural context.

### Building Understanding

When presenting documentation:
1. **Provide architectural context** - "This is in the Memory System component because..."
2. **Show relationships** - "This protocol uses these components..."
3. **Connect to use cases** - "This helps you accomplish X by..."

### For Agent Reference

When Claude Code queries internally:
1. **Quick reference** - Extract specific pattern or capability
2. **Verify accuracy** - Confirm platform behavior before stating it
3. **Update understanding** - Learn from official docs, not assumptions

## Session Guidelines

### User Documentation Queries

- Ask clarifying questions to understand the need
- Map to Components, Protocols, or Competencies
- Present with architectural context
- Offer related documentation if relevant

### Agent Self-Reference

- Query proactively when uncertain about platform behavior
- Verify capabilities before claiming them
- Reference protocols when explaining framework operations
- Use components documentation for implementation patterns

### DON'T

- Guess at platform capabilities - check Components
- Explain protocols from memory - fetch actual documentation
- Assume competency patterns - reference tutorials
- Mix up component responsibilities
