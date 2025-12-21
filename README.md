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

## License

BSD-3-Clause

## Contributing

Contributions welcome!
