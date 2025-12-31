# JCMRS Marketplace for Claude Code Plugins

A curated marketplace of Claude Code plugins.

## Available Plugins

### Profile Creator

**Status:** 🧪 Testing Phase

Plugin extending the Axivo Claude Collaboration Platform, providing functionality to create Domain Profiles - rooted in behavioral programming, SRE, Domain Knowledge Graphs Ontology (langroid, crewai, langraph, semantic kernel et alii) - and comprehensive guided templates and validation.

**Features:**
- 6-phase guided creation methodology
- Extensive inline guidance for non-technical users
- Templates for singular and composite (HMAS) profiles
- Reference examples across multiple domains
- Complete validation and testing framework

**Location:** `./plugins/profile-creator`

---

### Running Log

**Status:** 🧪 Testing Phase (Phase 1 Complete, Phase 2 Prototype Testing In Progress)

Persistent schema-driven running log that captures ideas, consultations, and Claude's reasoning patterns for cross-session learning and process memory. Addresses context window dependency by maintaining structured decision trails, assumptions, and learnings across sessions.

**Features:**
- Automatic signal detection (5 regex patterns for uncertainty, assumptions, decisions, critical issues)
- Profile-driven automation (DEVELOPER, RESEARCHER, ENGINEER thresholds)
- 3-cadence monitoring (session start, mid-toolchain, session end)
- 3-layer noise filtering (confidence threshold, entry cap, deduplication)
- Auto-generated sections (High-Priority Ideas, Open Risks, Linked Process Insights)
- Variant support (research-running-log, architecture-running-log)

**Commands:**
- `/activate running-log` — Initialize skill
- `/log [type] [content]` — Manual entry creation
- `/review [filter]` — Query and display log

**Location:** `./plugins/running-log`

---

### Procedural Memory System (PMS)

**Status:** ✅ Production Ready (v1.0.0)

> **"Shame on you."** - Because Claude learns from your corrections.

Long-term learning system that transforms conversational history into actionable procedural knowledge through a three-tier memory architecture. Captures both rigid procedures (technical patterns, coding practices) and flexible processes (workflows, decision patterns), extracting recurring behaviors and synthesizing context-aware rules that persist across sessions.

**Features:**
- **Three-tier memory architecture**: Episodic → Semantic → Procedural transformation pipeline
- **Dual encoding strategies**: Context-first encoding + JSONL fallback for comprehensive session capture
- **Intelligent pattern detection**: Frequency-based analysis with configurable thresholds (emerging, strong, critical)
- **Automatic rule synthesis**: Generates markdown rules from strong patterns, injected into `.claude/rules/pms/`
- **Privacy-first design**: Automatic redaction of API keys, passwords, tokens, and custom sensitive patterns
- **Hook integration**: Auto-encoding at PreCompact, SessionEnd, Stop, and SessionStart events
- **Error recovery**: Corruption detection, backup system, and rebuild from episodic records
- **Comprehensive testing**: 80 tests with 100% critical path coverage

**Commands:**
- `/pms:encode` — Manual episodic encoding trigger
- `/pms:extract` — Semantic pattern extraction from sessions
- `/pms:synthesize` — Procedural rule generation from patterns
- `/pms:reflect` — Complete workflow (encode → extract → synthesize)
- `/pms:status` — Display memory system state
- `/pms:validate` — Validate JSON schema integrity
- `/pms:reset` — Clear semantic/procedural memory
- `/pms:rebuild` — Regenerate semantic knowledge from episodic records

**Documentation:**
- `ARCHITECTURE.md` - Technical deep dive into component design
- `SKILL.md` - Plugin-dev integration guide
- `examples/USAGE_EXAMPLES.md` - 7 workflow scenarios + troubleshooting
- `VALIDATION_GUIDE.md` - End-to-end testing instructions
- `CHANGELOG.md` - v1.0.0 release notes

**Location:** `./plugins/claude-pms`

## Installation

### Local Development

```bash
/plugin marketplace add ~/path/to/jcmrs-plugins
```

### From Remote

```bash
/plugin marketplace add https://github.com/jcmrs/jcmrs-plugins
```

## Documentation

See individual plugin directories for complete documentation:

### Profile Creator
- `plugins/profile-creator/` - Profile Creator plugin
- `plugins/profile-creator/EXAMPLES_README.md` - Comprehensive guide with examples

### Running Log
- `plugins/running-log/` - Running Log plugin
- `plugins/running-log/README.md` - Quick start guide and command reference
- `RUNNING_LOG_IMPLEMENTATION_PLAN.md` - 6-phase implementation roadmap
- `SKILL_RUNNING_LOG_SPECIFICATION.md` - Complete technical specification

### Procedural Memory System
- `plugins/claude-pms/` - Procedural Memory System plugin
- `plugins/claude-pms/README.md` - Quick start guide and user documentation
- `plugins/claude-pms/ARCHITECTURE.md` - Technical architecture and component design
- `plugins/claude-pms/SKILL.md` - Plugin-dev integration and trigger phrases
- `plugins/claude-pms/examples/USAGE_EXAMPLES.md` - 7 workflow examples and troubleshooting
- `plugins/claude-pms/VALIDATION_GUIDE.md` - End-to-end testing instructions
- `plugins/claude-pms/CHANGELOG.md` - Version history and release notes

## License

BSD-3-Clause

## Contributing

Contributions welcome!
