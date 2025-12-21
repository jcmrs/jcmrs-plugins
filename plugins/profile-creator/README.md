# Profile Creator

**Status:** Early Development (v0.1.0)

## What It Does

The Profile Creator transforms messy human intent and repository analysis into operational domain profiles with behavioral programming. It bridges the gap between what non-technical users envision and what AI assistants need for effective collaboration.

## The Problem It Solves

Creating effective domain profiles is nearly impossible for humans because:
- We lack access to role taxonomies and domain knowledge graphs
- We don't understand ontological structures that AI needs
- We can't systematically generate behavioral constraints
- Manual creation takes months (see: the Domain Linguist profile took 2 months)

But humans ARE good at:
- Vision and high-level concepts
- User stories and domain intuition
- Understanding "why" and "what"

The Profile Creator operationalizes the collaboration: humans provide vision, AI provides ontological validation and systematic behavioral synthesis.

## How It Works

**6-Phase Knowledge Engineering Pipeline:**

1. **Intent Structuring** - Conversational discovery produces structured intent object
2. **Repository Analysis** - Extracts technical patterns using Glob/Read/Grep (no MCP)
3. **Ontology Mapping** - Maps to domain knowledge graphs (CrewAI, LangChain, etc.)
4. **Behavioral Synthesis** - Generates 50+ observations with behavioral programming
5. **Profile Validation** - Automated quality gate (THE KILLER - catches 95% of issues)
6. **Profile Generation** - Outputs living operational profile(s)

## Output

**Singular Profile:** `CLAUDE.md` - Single operational profile

**Composite Profile (HMAS):**
- `CLAUDE.md` - System Owner orchestrating
- `Researcher.md` - Primary role
- `Domain_Linguist.md` - Backroom specialist
- `Codebase_Analyst.md` - Backroom specialist

Profiles are LIVING behavioral systems with:
- Activation triggers (auto-activate on conditions)
- Self-monitoring (detects bias/drift)
- Rejection protocols (blocks invalid requests)
- Transformation logic (adapts behavior)
- Behavioral observations (4-5 per methodology category)

NOT just documentation that describes behavior.

## Usage

```bash
# Start conversational profile creation
/create-profile

# Validate existing profile
/validate-profile path/to/profile.md

# With direct input (advanced)
/create-profile "research team" "https://github.com/joaomdmoura/crewai"
```

## Requirements

- Repository URL (mandatory) - "what exists"
- Structured Intent (mandatory) - "what to build"
- Study Links (optional) - Additional framework docs, domain resources

## Current Status

**Implemented:**
- ✓ Plugin structure
- ✓ Design documentation

**In Progress:**
- Phase 1: Intent Structuring (conversational flow)

**Not Yet Implemented:**
- Phases 2-6 of the pipeline
- Workflow commands
- Error handling
- Testing suite

## Design Documentation

Complete architectural design captured in:
- Conversation Log: `.claude/conversations/2024/12/21-profile-creator-skill-design.md`
- Diary Entry: `.claude/diary/2024/12/21.md`

## License

Same as parent project (Axivo Claude Collaboration Platform)
