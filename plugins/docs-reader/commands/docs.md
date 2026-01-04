---
name: jcmrs:docs
argument-hint: "[search query]"
description: Search official Claude collaboration platform documentation
allowed-tools:
  - WebFetch
  - Read
  - Skill
---

# Documentation Search

Search and retrieve content from official collaboration platform documentation.

## Reference Documentation

Before starting, load the documentation-query skill:

1. **Load the documentation-query skill** which provides the methodology
2. The skill guides you through Understand → Locate → Present workflow

## Establish Query

If `$ARGUMENTS` is provided, use that as the search query. Otherwise, ask:

"What would you like to search in the documentation?"

Wait for the user's response before continuing.

## Query Workflow

Follow the documentation-query skill methodology:

1. **Understand** - Clarify what information is needed
2. **Locate** - Identify which documentation source has the answer (Components, Protocols, or Competencies)
3. **Present** - Fetch and present the relevant content with architectural context

## Documentation Architecture

**Wiki** (Platform architecture and reference):
- Base: `https://raw.githubusercontent.com/axivo/website/main/claude/content/wiki/`
- **Components**: Plugins, Documentation, Instructions, Memory
- **Protocols**: Equilibrium, Initialization, Response
- **Getting Started**: Configuration and setup

**Tutorials** (Practical competency development):
- Base: `https://raw.githubusercontent.com/axivo/website/main/claude/content/tutorials/`
- **Core Competencies**: Session structuring, Communication, Continuity, Customization, Measurement

## Query Type Mapping

Map user questions to documentation structure:

- "Can Claude Code do X?" → Wiki → Components
- "How does the framework work?" → Wiki → Protocols
- "How do I configure X?" → Wiki → Getting Started
- "Show me how to do X" → Tutorials → Competencies

Begin by understanding what the user wants to find in the documentation.
