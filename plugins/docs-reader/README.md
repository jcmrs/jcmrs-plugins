# Documentation Reader Plugin

Official collaboration platform documentation access through components, protocols, and competencies.

## Overview

This plugin provides systematic access to the Claude Collaboration Platform documentation, enabling both users and Claude Code to query and reference official documentation organized by platform architecture.

## Features

- **Architecture-Aware Documentation Access**: Understands platform structure (Components, Protocols, Competencies)
- **Dual Use Cases**: Supports both user-initiated queries and agent self-reference
- **Progressive Disclosure**: Lean core skill with focused resource files
- **On-Demand Fetching**: Retrieves documentation from GitHub as needed

## Documentation Structure

### Wiki (Platform Architecture & Reference)
- **Base URL**: `https://raw.githubusercontent.com/axivo/website/main/claude/content/wiki/`
- **Components** (4 subsystems): Plugins, Documentation, Instructions, Memory
- **Protocols** (3 operational sequences): Equilibrium, Initialization, Response
- **Getting Started**: Configuration and setup

### Tutorials (Practical Competency Development)
- **Base URL**: `https://raw.githubusercontent.com/axivo/website/main/claude/content/tutorials/`
- **Core Competencies** (5 skills): Session structuring, Communication, Continuity, Customization, Measurement

## Usage

### Command Interface

```
/jcmrs:docs [search query]
```

**Example queries:**
- `/jcmrs:docs How does the memory system work?` → Wiki → Components → Memory System
- `/jcmrs:docs What is the response protocol?` → Wiki → Protocols → Response Protocol
- `/jcmrs:docs How do I structure sessions?` → Tutorials → Competency 1

### Skill Trigger

The documentation-query skill activates when:
- User asks about platform capabilities ("Can Claude Code do X?")
- User asks how the framework works ("How does initialization work?")
- User asks for configuration guidance ("How do I configure X?")
- Claude Code needs to reference architecture or implementation patterns

## Structure

```
docs-reader/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   └── docs.md              # /docs slash command
├── skills/
│   └── documentation-query/
│       ├── SKILL.md         # Core skill methodology
│       ├── LICENSE          # BSD 3-Clause (AXIVO)
│       └── resources/
│           ├── wiki-index.md      # Wiki structure reference
│           └── tutorials-index.md # Tutorials structure reference
├── LICENSE                  # BSD 3-Clause (jcmrs)
└── README.md               # This file
```

## Query Type Mapping

### User-Initiated Queries
| Question Pattern | Documentation Source | Specific Section |
|-----------------|---------------------|------------------|
| "Can Claude Code do X?" | Wiki → Components | Plugins, Documentation, Instructions, or Memory |
| "How does the framework work?" | Wiki → Protocols | Equilibrium, Initialization, or Response |
| "How do I configure X?" | Wiki → Getting Started | Configuration section |
| "Show me how to do X" | Tutorials → Competencies | Relevant competency (1-5) |

### Agent-Initiated Queries
| Claude Code Need | Documentation Source | Purpose |
|------------------|---------------------|---------|
| Explaining platform capabilities | Wiki → Components | Accurate capability description |
| Understanding framework behavior | Wiki → Protocols | Correct protocol application |
| Implementing plugin features | Wiki → Components → Plugins | Pattern reference |
| Teaching collaboration techniques | Tutorials → Competencies | Best practices |

## Methodology

The skill follows a three-stage approach:

1. **Understand**: Clarify what type of understanding is needed (capabilities, mechanisms, or techniques)
2. **Locate**: Map query to Components, Protocols, or Competencies
3. **Present**: Fetch and present documentation with architectural context

## Development

This plugin is part of the jcmrs-plugins marketplace for Claude Code. It provides access to the Claude Collaboration Platform documentation and follows the platform's skill patterns:
- Natural conversational flow
- Progressive disclosure
- YAML frontmatter metadata
- Imperative/infinitive language
- Understanding-focused architecture

Original platform repository: https://github.com/jcmrs/claude

## License

Plugin: BSD 3-Clause License (jcmrs)
Skill: BSD 3-Clause License (AXIVO)

See LICENSE files for details.

## Repository

https://github.com/jcmrs/jcmrs-plugins
