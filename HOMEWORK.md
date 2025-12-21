# HOMEWORK: Multi-Disciplinary Curriculum & Reference
## Claude Code, Agent Skills, MCP, Domain Profiles, Ontologies, MMAS & Governance

**Document Purpose**: Comprehensive, structured reference material for understanding and building with Anthropic's Claude Code ecosystem. Serves as foundational curriculum for:
- Creating reusable skills (Agent Skills standard)
- Building plugins and marketplaces
- Designing Domain Profiles and ontologies
- Architecting Multi-Agent Systems (MMAS)
- Understanding Model Context Protocol (MCP)
- Implementing governance and versioning

**Scope**: Anthropic official documentation + third-party implementations + research papers + standards specifications

**Status**: Foundation curriculum - evolves with Anthropic releases and community contributions

---

## TABLE OF CONTENTS

1. [Foundational Concepts](#foundational-concepts)
2. [Curriculum Structure](#curriculum-structure)
3. [Claude Code: Official Ecosystem](#claude-code-official-ecosystem)
4. [Agent Skills Standard](#agent-skills-standard)
5. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
6. [Domain Profiles & Ontologies](#domain-profiles--ontologies)
7. [Multi-Agent Systems (MMAS)](#multi-agent-systems-mmas)
8. [Governance, Versioning, & Standards](#governance-versioning--standards)
9. [Research & Advanced Topics](#research--advanced-topics)
10. [Reference Materials & Repositories](#reference-materials--repositories)
11. [Learning Pathways](#learning-pathways)
12. [Unresolved Questions](#unresolved-questions-for-research)

---

## FOUNDATIONAL CONCEPTS

### Core Entities & Relationships

**Plugin**: Extensible module in Claude Code containing skills, commands, agents, hooks, and/or MCP integrations.

**Skill**: Reusable, portable instruction set (SKILL.md format) extending Claude capabilities. Adopts Agent Skills standard (YAML frontmatter + Markdown instructions + resources). Distributed via marketplaces.

**Marketplace**: Git-backed repository with `.claude-plugin/marketplace.json` listing plugins and skills. Discovered and installed via Claude Code.

**Agent Skills Standard**: Open standard announced Dec 18, 2025. Portable format for domain-specific instructions, scripts, and resources. Adopted by Microsoft (VS Code), OpenAI (ChatGPT/Codex), Cursor, Atlassian, Figma, Notion, etc.

**Model Context Protocol (MCP)**: Open standard for AI connections to external tools/data. Secure, standardized way to expose APIs, databases, tools to Claude.

**Domain Profile**: Ontology-backed profile combining skills, roles, MCP resources, and hierarchical structures for specialized domains (Finance, DevOps, Healthcare, etc.). Enables domain-specific behavior.

**Ontology**: Formal knowledge representation (YAML/OWL/RDF) defining:
- Concepts (Agent, Skill, Role, Domain)
- Relationships (hasSkill, composedOf, delegatesTo)
- Constraints (disjointWith, requiresSkill)
- Inference rules for automated discovery

**Multi-Agent System (MMAS)**: Hierarchical coordination of multiple specialized agents (System Owner orchestrator + Backroom specialists) for complex task decomposition. Uses Domain Profiles and skills.

**AGENTS.md**: Universal "README for agents" (adopted 60k+ repos). Defines project context, commands, architecture, and testing for compatible AI tools.

**CLAUDE.md**: Anthropic-specific agent configuration (auto-loaded in Claude Code). Falls back to AGENTS.md for interoperability.

### Architectural Stack

```
User Request
    ↓
AGENTS.md / CLAUDE.md (execution directives)
    ↓
Domain Profile (Ontology + role definitions)
    ↓
Skills (SKILL.md) + MCP (Tool/Data access)
    ↓
Claude Code / Claude.ai / Claude API
    ↓
Result
```

---

## CURRICULUM STRUCTURE

### Multi-Disciplinary Areas

This curriculum spans:

1. **Platform Engineering**: Claude Code plugins, marketplaces, architecture
2. **Knowledge Engineering**: Skills design, progressive disclosure, reusability
3. **Semantic Web**: Ontologies, YAML/OWL schemas, FAIR principles
4. **Systems Design**: MMAS hierarchies, delegation, composition
5. **Governance**: Versioning, standards compliance, approval workflows
6. **Integration**: MCP for tools, APIs, databases
7. **Research**: Multi-agent coordination, agent capabilities, evaluation

### Learning Pathways

See [Learning Pathways](#learning-pathways) section for recommended progression.

---

## CLAUDE CODE: OFFICIAL ECOSYSTEM

### Core Documentation (Primary References)

All official docs hosted at **https://code.claude.com/docs/en/**

| Component | URL | Covers |
|-----------|-----|--------|
| **Plugins** | `/plugins` | Plugin structure, `.claude-plugin/plugin.json`, commands, agents, skills, hooks, MCP |
| **Plugin Marketplaces** | `/plugin-marketplaces` | Creating/managing marketplaces; `.claude-plugin/marketplace.json` schema |
| **Plugins Reference** | `/plugins-reference` | Technical specifications, JSON schemas, component reference |
| **Skills** | `/skills` | Agent Skills standard, SKILL.md format, creating reusable skills |
| **MCP** | `/mcp` | Model Context Protocol integration in Claude Code |
| **Slash Commands** | `/slash-commands` | Plugin command structure, invocation patterns |
| **Hooks** | `/hooks` | Event handling, automation triggers |
| **Subagents** | `/sub-agents` | Agent configuration, capabilities |
| **Settings** | `/settings` | Plugin configuration, marketplace management |

### Plugin Directory Structure (Official Spec)

```
marketplace-repo/
│
├── .claude-plugin/
│   └── marketplace.json                    # Marketplace manifest (REQUIRED)
│       └── Schema:
│           - name: marketplace identifier (kebab-case)
│           - owner: { name, url }
│           - plugins: [
│               {
│                 name: plugin-id (kebab-case),
│                 source: "./plugins/plugin-id",
│                 description: brief text
│               }
│             ]
│
├── plugins/
│   │
│   └── plugin-id/
│       │
│       ├── .claude-plugin/
│       │   └── plugin.json               # Plugin manifest
│       │       └── Schema:
│       │           - name: plugin-id
│       │           - version: semantic (1.0.0)
│       │           - description: purpose
│       │
│       ├── skills/
│       │   └── skill-id/
│       │       └── SKILL.md              # Reusable instruction set
│       │           └── Format: YAML frontmatter + Markdown
│       │
│       ├── commands/
│       │   ├── command-1.md              # User-invocable slash commands
│       │   └── command-2.md
│       │
│       ├── .mcp.json                     # MCP server configuration (optional)
│       │   └── Defines external tool/data access
│       │
│       ├── hooks/
│       │   └── hooks.json                # Event handlers (optional)
│       │
│       └── README.md                     # Plugin documentation
│
└── README.md                              # Marketplace documentation
```

### Naming Conventions

- **Marketplace**: `.claude-plugin/` (dot-prefix, standard for all plugin systems)
- **Plugin IDs**: `kebab-case` (lowercase, hyphens, no spaces)
- **Versions**: `MAJOR.MINOR.PATCH` (semantic versioning)
- **Skills**: `skill-id/SKILL.md` inside `skills/` directory
- **Commands**: `command-name.md` inside `commands/` directory

### Key Distinction: marketplace.json vs plugin.json

| Aspect | marketplace.json | plugin.json |
|--------|------------------|------------|
| **Purpose** | Lists available plugins for installation | Describes individual plugin metadata |
| **Location** | Root: `.claude-plugin/marketplace.json` | Per-plugin: `plugins/[name]/.claude-plugin/plugin.json` |
| **Scope** | Marketplace-level | Plugin-level |
| **Required Fields** | `name`, `owner`, `plugins` | `name`, `version`, `description` |
| **Plugin Entries** | `name`, `source`, `description` only | Full metadata |
| **Auto-Discovery** | Skills/commands auto-discovered from directories | N/A |

**Critical Rule**: Do NOT duplicate plugin metadata in marketplace.json. Keep it lightweight. Plugin.json holds the detail.

---

## AGENT SKILLS STANDARD

### Official Announcement & Adoption

- **Announcement Date**: December 18, 2025
- **Announcement**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Specification**: https://agentskills.io
- **Reference Organization**: https://github.com/agentskills
- **Anthropic Examples**: https://github.com/anthropics/skills (14.3k stars)

### Adoption (Cross-Platform)

**Native Support**:
- Claude Code, Claude.ai, Claude API
- Installation: `/plugin marketplace add anthropics/skills`

**Third-Party**:
- Microsoft: VS Code, GitHub Copilot CLI
- OpenAI: ChatGPT, Codex
- Others: Cursor, Atlassian, Figma, Notion, Canva, Stripe, Zapier

**Governance**: Open standard; contributions via GitHub; support from Agentic AI Foundation.

### SKILL.md: Canonical Format

Every skill follows this structure:

```markdown
---
name: skill-id                              # Unique ID (lowercase-hyphen)
description: |                              # 1-2 sentence purpose
  What this skill does and when/why to use it.
version: 1.0.0                              # MAJOR.MINOR.PATCH
domain: domain-name                         # skos:Concept (finance, healthcare, dev, etc.)
requires: [dependency-1, dependency-2]      # Prerequisite skills
composableIn: [CompositeProfile]            # Which profiles/systems use this skill
sha256: abc123...                           # Content hash (immutable reference)
fair: doi:10.123/skills.v1.0.0              # PURL/DOI for FAIR compliance
replaces: 0.9.0                             # Previous version (if applicable)
replacedBy: 1.1.0                           # Next version (post-merge)
migration: auto-script.js                   # Handles breaking changes
governance: AgenticAIFoundation/PR-123      # Approval trail
---

## Summary
[Metadata-only overview for quick scanning]
- Core workflow: [3-step outline]
- When to use: [Scenario]
- When NOT to use: [Limitations]

[TOTAL: 50-100 tokens]

## Detailed Instructions
1. [First step with context]
   - Sub-step 1a
   - Sub-step 1b
2. [Second step]
3. [Third step]

[Comprehensive guidance; loaded on-demand]

## Examples
- **Input**: User request or scenario
- **Output**: Expected result or behavior

## Resources
- `reference.md`: Domain knowledge, ontology, external links
- `mcp-server/endpoint.json`: MCP endpoint definitions
- `templates/`: Reusable templates
- `scripts/`: Utility scripts

```

### Progressive Disclosure Pattern (Token Efficiency)

Skills implement intelligent context loading:

```
Phase 1: Metadata (YAML frontmatter)
├── Loaded automatically
├── Content: name, description, version, domain, requires
└── Cost: ~50 tokens

    ↓ (If user needs quick overview)

Phase 2: Summary Section
├── High-level outline, key workflows
├── Scenarios (when/why to use)
└── Cost: ~100 tokens

    ↓ (If user needs detailed guidance)

Phase 3: Detailed Instructions
├── Full methodology, step-by-step
├── Examples, edge cases
└── Cost: ~500+ tokens

    ↓ (If user needs tools/resources)

Phase 4: Resources
├── MCP endpoints, reference docs, templates
├── Loaded as needed for actual execution
└── Cost: ~200+ tokens
```

**Benefit**: Matches human reading patterns (skim → dive deep) and avoids context bloat.

### Creating & Distributing Skills

**Starting Point**: Fork or use template from https://github.com/anthropics/skills/tree/main/template-skill

**Workflow**:
1. Create folder: `skills/[skill-id]/`
2. Write `SKILL.md` following canonical format
3. Add resources: `reference.md`, `mcp-server/`, `templates/`, `scripts/`
4. Test in Claude Code or Claude.ai
5. Push to GitHub
6. Register in marketplace `.claude-plugin/marketplace.json`
7. Install: `/plugin marketplace add [repo-url]`

**GitHub Structure for Skill Marketplace**:
```
your-skills-marketplace/
├── .claude-plugin/marketplace.json
├── skills/
│   ├── skill-1/
│   │   ├── SKILL.md
│   │   ├── reference.md
│   │   ├── mcp-server/ (optional)
│   │   └── resources/
│   └── skill-2/SKILL.md
└── README.md
```

---

## MODEL CONTEXT PROTOCOL (MCP)

### What & Why

**MCP**: Open standard enabling secure AI connections to external systems (tools, APIs, databases, services).

**Vision**: Make tools accessible to Claude as first-class citizens (like we treat skills).

**Current Integration**: Claude Desktop, Claude Code, Claude API, and expanding to other platforms.

### Primary Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| **Announcement** | https://www.anthropic.com/news/model-context-protocol | Overview, vision, adoption |
| **Build with Claude** | https://www.anthropic.com/learn/build-with-claude | Guides: setup, ready-made servers, remote servers |
| **Code Execution with MCP** | https://www.anthropic.com/engineering/code-execution-with-mcp | Advanced pattern: sandboxed code as tool API |
| **Specification** | https://modelcontextprotocol.io | Full spec, server templates, examples |
| **Example Server** | https://github.com/anthropics/skills/tree/main/mcp-server | Reference Python/Node implementation |

### Core Use Cases

1. **Tool Integration**: Expose CLIs/APIs as MCP servers
   - Google Drive, Git, Slack, Jira
   - Custom internal tools
   - Public APIs

2. **Data Access**: Connect to systems
   - Databases (PostgreSQL, MongoDB)
   - File systems (S3, local)
   - Data warehouses (Snowflake, BigQuery)

3. **Code Execution**: Sandboxed computation
   - Keep PII private (stays in sandbox)
   - Control flow (loops, state, polling)
   - Efficient multi-tool orchestration

4. **Plugin Integration**: MCP servers within Claude Code plugins
   - Tools as first-class in `.mcp.json`
   - Progressive disclosure (query → execute → results)

### Code Execution with MCP (Advanced Pattern)

**Concept**: Treat MCP tools as TypeScript/Python APIs, not direct function calls.

```
1. Model generates code (JavaScript/Python)
   └── Code calls MCP endpoints as library functions
       └── e.g., `servers/google-drive/getDocument.ts`

2. Code executes in sandbox
   └── Filters/transforms data locally
   └── Handles loops, state, conditional logic

3. Results returned to model
   └── PII stays in sandbox (not returned unless used)
   └── Efficient multi-tool composition
```

**Benefits**:
- Privacy: PII filtered before return
- Scalability: Loops/polling in code, not via API
- Control: Data transformation in code

### MCP Configuration in Plugins

**File**: `.mcp.json` in plugin root

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {
        "API_KEY": "${env:API_KEY}",
        "BASE_URL": "https://api.example.com"
      }
    },
    "another-server": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {}
    }
  }
}
```

### Building MCP Servers

**Reference**: https://github.com/anthropics/skills/tree/main/mcp-server

**Languages**: Python, Node.js, Rust, Go, etc.

**Server Exposes**:
- `list_resources()`: Available data/tools
- `read_resource(uri)`: Fetch specific resource
- `call_tool(name, args)`: Execute tool
- Streaming support for large responses

---

## DOMAIN PROFILES & ONTOLOGIES

### What are Domain Profiles?

Profiles extending skills into structured, role-based hierarchies for specialized domains.

**Components**:
- **Ontology**: Formal knowledge structure (YAML/OWL)
- **Skills**: Mapped to domain via `hasSkill`, `composableIn`
- **Roles**: System Owner (orchestrator), Backroom specialists (experts)
- **MCP Resources**: Tool/data access for domain
- **AGENTS.md / CLAUDE.md**: Execution directives

**Purpose**: Enable domain-specific behavior, delegation, and composable agent systems.

### Ontology Design (BFO-Compliant Architecture)

**Three-Tier Modular Approach**:

#### Upper Ontology (BFO/OWL Primitives)

```
Continuant (static, unchanging across time)
├── AgentProfile rdf:type Continuant
├── DomainProfile rdf:type Continuant
└── Role (SystemOwner, FinanceSpecialist, DevSpecialist)

Occurrent (dynamic, changes over time)
├── SkillExecution rdf:type Occurrent
├── WorkflowExecution rdf:type Occurrent
└── DataTransformation rdf:type Occurrent

Quality (properties)
├── hasCompetenceLevel (integer, 0-100)
├── hasAvailability (boolean)
└── hasLatency (milliseconds)
```

#### Middle Ontology (Domain-Level Profiles)

```
SystemOwnerProfile
├── rdf:type Agent
├── hasRole "Orchestrator"
├── hasSubProfile [BackroomProfile]
├── delegatesTo [TaskAgent]
└── orchestratesVia "AGENTS.md"

BackroomProfile (e.g., FinanceProfile)
├── rdf:type Agent
├── hasDomain "finance"
├── requiresSkill [brand-guidelines, xlsx-processor, mcp-accounting]
├── composedOf [FinanceComposite]
└── supportsRole [FinanceSpecialist, AuditSpecialist]

TaskAgent
├── rdf:type Agent
├── executesSkill [mcp-accounting]
└── reportsTo [BackroomProfile]
```

#### Lower Ontology (Skills & Resources)

```
Skill (rdf:type skos:Concept)
├── name "xlsx-processor"
├── inDomain "finance"
├── reusableIn [FinanceProfile, DevProfile]
├── hasResource [template.xlsx, reference.md]
└── composableWith [brand-guidelines, mcp-server]

MCP Server (rdf:type Tool)
├── endpoint "servers/accounting/getTransactions"
├── consumesFrom [Database]
├── producesFormat "JSON"
└── requires [OAuth]
```

### DOMAIN.md Template

```yaml
---
name: FinanceDomainProfile
version: 1.0.0
description: Finance domain with accounting and reporting skills
domain: finance                    # skos:Concept
systemOwner: true                  # Can orchestrate sub-profiles
subProfiles: []                    # Backroom specialists (if composite)
hasSkill:
  - brand-guidelines              # Shared across all domains
  - xlsx-processor                # Excel automation
  - mcp-accounting                # Real-time GL, AP/AR access
composableWith:
  - DevDomainProfile              # Can work with DevOps domain
  - ReportingDomainProfile        # Can work with analytics
mcpServers:
  - accounting: servers/accounting/config.json
ontologyIRI: https://example.com/finance-domain/v1.0.0
ontologyFormat: owl               # OWL or YAML-LD
---

## Domain Definition
This profile specializes Finance operations: accounting, reporting, reconciliation.

## Role Hierarchy
- **System Owner**: Orchestrates finance requests
- **Accounting Specialist**: GL, AP/AR, bank reconciliation
- **Reporting Specialist**: Financial statements, dashboards
- **Audit Specialist**: Compliance, variance analysis

## Skills Composition
### brand-guidelines
Applied across all domains; ensures consistent voice/style.

### xlsx-processor
Transforms raw accounting data into reports. Handles:
- GL export → statement preparation
- AP aging → payment prioritization
- Variance → root cause analysis

### mcp-accounting
Real-time access to accounting system:
- `getGLAccounts()`: Chart of accounts
- `getTransactions(dateRange)`: GL transactions
- `getAPAgingReport()`: Payable agings
- `reconcile(account, statement)`: Bank reconciliation

## Execution Flow (AGENTS.md Directives)
1. Owner receives finance request: "Reconcile checking account, QA variance"
2. Route to FinanceComposite (orchestrator delegates)
3. Parallel execution:
   - Accounting Specialist: xlsx-processor + mcp-accounting → reconciliation
   - Reporting Specialist: xlsx-processor + templates → variance analysis
4. Results aggregate: reconciliation status + variance explanation
5. Owner validates and returns response

## Interdomain Interactions
- **Finance ↔ Dev**: Share brand-guidelines; DevOps can access cost reports
- **Finance ↔ HR**: Share employee data via mcp-employee server
- **Finance ↔ Sales**: Share revenue data via mcp-crm server

## Semantic Tagging (For Ontology Linking)
```
<span property="rdfs:domain" resource="https://example.com/finance">Finance</span>
<span property="skos:relatedMatch" resource="https://dbpedia.org/page/Finance">Finance</span>
```

---

## MULTI-AGENT SYSTEMS (MMAS)

### What & Why MMAS

**MMAS**: Hierarchical coordination of multiple specialized agents for complex task decomposition.

**Motivation**:
- Single agent limited by context window and generality
- Specialized agents excel in narrow domains
- Orchestration needed for multi-step workflows
- Delegation reduces model calls per agent

### MMAS Hierarchy Patterns

#### Control Structures

**Centralized**
```
SystemOwner
├── All goals flow through Owner
├── Owner decomposes → Backroom agents
└── Resilience: single point of failure
```

**Decentralized**
```
Agent A ←→ Agent B
Agent C ←→ Agent D
└── Peer negotiation, consensus
```

**Hybrid** (recommended)
```
SystemOwner (strategic decisions)
├── FinanceComposite (tactic level)
│   ├── Parallel leaf agents
│   └── Results aggregate back
├── DevComposite (tactic level)
│   └── Similar structure
└── Reactive layer (operational, real-time)
```

#### Information Flows

**Top-Down** (goal decomposition)
```
Owner: "Analyze Q4 financials"
  ↓ Delegates to FinanceComposite
    ↓ Decomposes to:
      - Accounting agent: GL analysis
      - Reporting agent: dashboard creation
      - Audit agent: variance investigation
```

**Bottom-Up** (aggregation)
```
Leaf agents report ← Composite aggregates ← Owner validates
```

**Bidirectional** (adaptive)
```
Owner ↔ Composite ↔ Leaf agents
└── Feedback loops; agents adjust strategy based on partial results
```

#### Temporal Layers

**Strategic** (hours/days)
- Mission planning, resource allocation
- Handled by System Owner profile

**Tactical** (minutes)
- Skill orchestration, composite coordination
- Handled by Backroom profiles/composites

**Operational** (ms/sec)
- Real-time execution, MCP calls
- Handled by leaf agents

### Composite Types

| Type | Structure | Use Case | Example |
|------|-----------|----------|---------|
| **Sequential** | A→B→C | Pipelines | docx → pdf → xlsx export |
| **Parallel** | A∥B∥C | Concurrent tasks | Multi-domain analysis (finance∥dev∥hr) |
| **Hierarchical** | Owner → [Composite1, Composite2] | Backroom coordination | SystemOwner delegates multiple composites |
| **Holonic** | Composite contains sub-composites | Recursive structure | EnterpriseWorkflow → [BrandGuidelines + [MCP + Reporting]] |
| **Market** | Bid/auction skills | Dynamic allocation | Agents bid on tasks; best-fit executes |

### Canonical MMAS Structure (Von Neumann Architecture per Agent)

```
Agent State (storage)
├── Profile: CLAUDE.md / AGENTS.md (beliefs)
├── Goals: Current objectives (desires)
├── Skills: Available reusable actions (intentions)
└── History: Past executions (memory)

Control (decision logic)
├── BDI reasoning: Beliefs + Desires + Intentions
├── Delegation: Route to subagent if specialized
└── Adaptation: Adjust strategy based on feedback

Logic (skill execution)
├── Select appropriate skill
├── Compose with other skills if needed
├── Execute via MCP or in-process
└── Handle errors/fallbacks

I/O (communication)
├── In: Goals from parent agent
├── Out: Results to parent agent
└── Inter-agent: Communicate with siblings
```

### State Persistence & Self-Adaptation (BDI-O)

Agents adapt behavior based on:
- **Beliefs**: Current profile state, learned facts
- **Desires**: Goals, preferences, constraints
- **Intentions**: Active plans, committed skills
- **Monitoring**: Detect drift, failures, opportunities

Example adaptation:
```
Belief: "Standard xlsx skill failing on large files"
  ↓
Desire: "Complete financial report"
  ↓
Revise Intention: "Switch to streaming xlsx processor" (BDI-O)
  ↓
Replan: Use mcp-server instead of local xlsx
  ↓
Execute revised plan
```

---

## GOVERNANCE, VERSIONING, & STANDARDS

### Semantic Versioning Strategy

**Format**: `MAJOR.MINOR.PATCH`

| Component | Meaning | When to Increment |
|-----------|---------|------------------|
| **MAJOR** | Breaking changes | Remove skill, change interface, incompatible ontology |
| **MINOR** | New features, backward-compatible | Add skill, new resources, enhancement |
| **PATCH** | Bug fixes, documentation | Fix behavior, clarify examples, typos |

### Metadata Fields for Versioning

Every SKILL.md, DOMAIN.md should include:

```yaml
version: 1.2.3
changelog: https://github.com/org/repo/blob/main/CHANGELOG.md
sha256: def456...                      # Content integrity
fair: doi:10.123/skills.finance.v1.2.3 # PURL/DOI registry
replaces: 1.1.0                         # Previous stable
replacedBy: 1.3.0                       # Next (after merge)
migration: auto-migrate-v1.2.3.js       # Breaking change script
governance: AgenticAIFoundation/PR-456  # Approval trail
created: 2025-12-21T10:00:00Z
author: [email/github handle]
license: Apache-2.0
```

### Governance Workflow

```
Propose
│ ├─ Fork repo
│ ├─ Create skill/profile with metadata
│ └─ Open PR
     ↓
Review
│ ├─ Domain experts validate
│ ├─ AI auditors (Claude Code) check consistency
│ ├─ SHACL validation for ontologies
│ └─ Backwards compatibility check
     ↓
Stage
│ ├─ Merge to `staging/` branch
│ ├─ Automated tests
│ │  ├─ Load in VS Code/Claude Code/OpenAI
│ │  ├─ Check interoperability
│ │  └─ Verify MCP endpoints
│ └─ Integration testing
     ↓
Release
│ ├─ Tag semver: `v1.2.3-finance-skill`
│ ├─ Publish PURL/DOI
│ ├─ Update registry
│ └─ Notify subscribers
     ↓
Deprecate (Optional)
│ ├─ Mark `replacedBy` in metadata
│ ├─ Provide auto-migration script
│ └─ Set deprecation timeline (e.g., 6 months)
```

### FAIR Compliance (Findable, Accessible, Interoperable, Reusable)

**Findable**: Assign persistent identifier (PURL, DOI)
```yaml
fair: doi:10.123/skills.finance.v1.2.3
```

**Accessible**: Public GitHub repo, documented setup
```yaml
homepage: https://github.com/org/skills/tree/main/finance
documentation: https://org.github.io/skills/finance
```

**Interoperable**: Follow standards (SKILL.md, AGENTS.md, Agent Skills)
```yaml
standards: [agent-skills, agents-md, owl]
```

**Reusable**: Clear license, comprehensive metadata
```yaml
license: Apache-2.0
requires: [mcp-accounting-v1.0+]
composableIn: [FinanceProfile, EnterpriseWorkflow]
```

---

## RESEARCH & ADVANCED TOPICS

### Key Research Areas (From Provided Papers)

#### Multi-Agent Coordination
- MMAS hierarchies, control flows
- Consensus mechanisms
- Load balancing across agents

#### Agent Capabilities & Evaluation
- OpenHands: Generalist agent platform, benchmarks
- xLAM: Large action models for agents
- AgentStudio: Virtual agent toolkits, GroundUI dataset

#### Domain Knowledge & Ontologies
- BFO (Basic Formal Ontology) for upper-level design
- NeOn methodology for ontology engineering
- FAIR principles for data/knowledge management

#### Standards & Interoperability
- Agent Skills ecosystem adoption
- MCP integration across platforms
- Security, governance, trust in agentic systems

### Papers & Resources to Study

| Topic | Resource | URL |
|-------|----------|-----|
| **MMAS Hierarchies** | arxiv.org | https://arxiv.org/html/2508.12683v1 |
| **Ontology Design** | Dario Gariglio (FAIR) | https://dgarijo.com/papers/best_practices2020.pdf |
| **OpenHands** | All-Hands-AI | http://arxiv.org/pdf/2407.16741.pdf |
| **xLAM (Action Models)** | Research paper | https://arxiv.org/pdf/2409.03215.pdf |
| **AgentStudio** | Virtual agents | https://arxiv.org/pdf/2403.17918.pdf |
| **BDI Ontology** | Beliefs-Desires-Intentions | https://www.emergentmind.com/topics/bdi-ontology-bdi-o |

---

## REFERENCE MATERIALS & REPOSITORIES

### Official Anthropic

| Repo | Purpose | URL |
|------|---------|-----|
| **anthropics/skills** | Reference Agent Skills (14.3k stars) | https://github.com/anthropics/skills |
| **anthropics/anthropic-cookbook** | Code snippets, patterns, prompts | https://github.com/anthropics/anthropic-cookbook |
| **anthropics/claude-cookbooks** | API usage cookbooks | https://github.com/anthropics/claude-cookbooks |
| **anthropic-sdk-python** | Python SDK (MCP/plugin support) | https://github.com/anthropics/anthropic-sdk-python |

### Standards & Specifications

| Standard | Purpose | URL |
|----------|---------|-----|
| **Agent Skills** | Open standard specification | https://agentskills.io |
| **agents.md** | Universal agent README (60k+ repos) | https://agents.md |
| **Model Context Protocol** | MCP specification & servers | https://modelcontextprotocol.io |
| **agentskills GitHub Org** | Reference implementations | https://github.com/agentskills |

### Third-Party Implementations

| Tool | Implementation | URL |
|------|----------------|-----|
| **VS Code / GitHub Copilot** | Skills integration | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| **OpenAI Codex** | Agent Skills support | https://developers.openai.com/codex/skills/ |
| **Cursor** | Early adopter | Community docs |
| **OpenHands** | Open agent platform | https://github.com/All-Hands-AI/OpenHands |

---

## LEARNING PATHWAYS

### Recommended Progression

#### Week 1: Foundations
- [ ] Read Claude Code official docs (plugins, skills)
- [ ] Understand marketplace.json vs plugin.json distinction
- [ ] Grasp Agent Skills standard (SKILL.md format)
- [ ] Study progressive disclosure pattern
- [ ] **Deliverable**: Create first SKILL.md using template

#### Week 2: Integration
- [ ] Understand MCP: what, why, how
- [ ] Code execution with MCP pattern
- [ ] Study AGENTS.md / CLAUDE.md
- [ ] Read third-party implementations (VS Code, OpenAI)
- [ ] **Deliverable**: Create plugin with SKILL.md + MCP integration

#### Week 3: Ontologies & Domains
- [ ] BFO basics for upper ontology
- [ ] NeOn methodology for ontology engineering
- [ ] Design Domain Profile structure (YAML schema)
- [ ] Semantic tagging (RDFa) for ontology linking
- [ ] **Deliverable**: Design DOMAIN.md for specific domain (Finance, DevOps, etc.)

#### Week 4: Multi-Agent Systems
- [ ] MMAS hierarchy patterns (centralized/decentralized/hybrid)
- [ ] Von Neumann architecture for agent state
- [ ] BDI-O (Beliefs-Desires-Intentions-Ontology)
- [ ] Composite skill orchestration
- [ ] **Deliverable**: Design System Owner + 2 Backroom profiles for composite system

#### Week 5: Governance & Standards
- [ ] Semantic versioning strategy
- [ ] FAIR principles for reusability
- [ ] Governance workflows (PR review, staging, release)
- [ ] Migration scripts for breaking changes
- [ ] **Deliverable**: Document versioning/governance for marketplace

#### Week 6: Research & Advanced
- [ ] Read research papers on MMAS, agent capabilities
- [ ] Study OpenHands, xLAM, AgentStudio
- [ ] Understand agent evaluation metrics
- [ ] Plan next research direction
- [ ] **Deliverable**: Proposal for advanced feature (e.g., auto-ontology generation, agent evaluation)

### Self-Paced Study Questions

**Week 1**:
- What's the difference between marketplace.json and plugin.json?
- How does progressive disclosure save tokens?
- What makes a skill "portable" across platforms?

**Week 2**:
- How does MCP enable code execution safety?
- What does AGENTS.md specify that plugin.json doesn't?
- How would you add tool access to a skill?

**Week 3**:
- What's the benefit of formal ontologies over just documentation?
- How does RDFa embedding help discovery?
- Design a Domain Profile for your expertise area.

**Week 4**:
- How would you model delegation in a System Owner → Backroom hierarchy?
- What's the difference between sequential and parallel composites?
- How does BDI-O enable agent adaptation?

**Week 5**:
- Why is semantic versioning critical for MMAS?
- What should happen when a skill you depend on breaks?
- How do you ensure backwards compatibility?

**Week 6**:
- How would you evaluate if an agent system is "good"?
- What gaps exist in current standards?
- How would you design the next evolution?

---

## UNRESOLVED QUESTIONS (FOR RESEARCH)

### Architecture & Standards

- [ ] Should Domain Profiles be separate marketplace or included in plugins?
- [ ] How to auto-discover compatible Domain Profiles in marketplace?
- [ ] Optimal granularity for ontologies (when to split domains)?
- [ ] How to version ontologies independently from skills?

### Governance & Tooling

- [ ] SHACL validation for ontology consistency?
- [ ] Automated compatibility checking between skills?
- [ ] How to handle dependency resolution in MMAS (skill X requires MCP server Y v1.2+)?
- [ ] Who maintains the "standards registry"?

### MMAS & Coordination

- [ ] Best practices for load balancing in hierarchical systems?
- [ ] How to handle agent failures/retry strategies?
- [ ] Optimal delegation depth (how many levels)?
- [ ] Communication overhead: when does overhead exceed benefit?

### Security & Privacy

- [ ] How to audit agent skill execution?
- [ ] Permissions model: which agents can call which MCP endpoints?
- [ ] How to prevent skill sandboxing escapes?
- [ ] How to handle sensitive data across multiple agents?

### Evaluation & Metrics

- [ ] How to measure "goodness" of Domain Profiles?
- [ ] Benchmarks for MMAS performance?
- [ ] User satisfaction metrics for agent systems?
- [ ] Cost metrics (tokens, latency, tool calls)?

---

## DOCUMENT METADATA

**Created**: 2025-12-21
**Author**: Anthropic Documentation + Research synthesis
**Source Material**:
- Official Anthropic docs (code.claude.com, anthropic.com)
- Perplexity AI research compilation
- Third-party implementations (VS Code, OpenAI, Cursor)
- Academic papers (MMAS, ontologies, agents)

**References**: 100+ URLs, 50+ research papers, GitHub repositories

**Status**: Foundation curriculum
- Requires quarterly updates as Anthropic releases new standards
- Community contributions welcome
- Questions/gaps tracked in [Unresolved Questions](#unresolved-questions-for-research)

### How to Use This Document

**As Reference**:
- Ctrl+F search by concept (e.g., "progressive disclosure", "ontology", "BDI")
- Link to sections when designing skills/profiles
- Share with team for shared understanding

**As Curriculum**:
- Follow [Learning Pathways](#learning-pathways) week-by-week
- Complete deliverables each week
- Self-assess with study questions
- Plan research directions

**As Living Document**:
- Update as standards evolve
- Add new research findings
- Document decisions made (cross-reference with actual implementations)
- Track answers to unresolved questions

---

**END OF HOMEWORK.md**
