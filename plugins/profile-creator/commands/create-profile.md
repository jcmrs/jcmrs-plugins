---
name: create-profile
description: Create operational domain profile through 6-phase knowledge engineering pipeline
argument-hint: "[intent] [repository_url]"
---


Create a living operational domain profile through conversational knowledge engineering pipeline.

## Usage

```bash
/create-profile [intent] [repository_url]
```

## Arguments

- `intent` (optional): Quick description like "research team" or "system architect"
- `repository_url` (optional): GitHub/GitLab repository URL to analyze

## Behavior

Launches the **6-Phase Knowledge Engineering Pipeline**:

### Phase 1: Intent Structuring (Conversational)

If no arguments provided, begins guided conversation with educational context:

1. "What's the primary role or archetype for this profile?"
   - Context: Examples like 'Researcher', 'System Architect', 'Domain Linguist'

2. "What's the domain focus?"
   - Context: Specific area like 'CrewAI codebase', 'API documentation'

3. "Single profile or multi-role structure?"
   - Context: Single = one profile, Multi-role = System Owner + backroom specialists

4. "Any critical behavioral constraints?"
   - Context: Must-haves like 'hallucination prevention', 'peer review'

5. "Repository URL?" (if analyzing codebase)

6. "Additional study links?" (optional framework docs)

Produces **Structured Intent Object** for validation.

If arguments provided, constructs structured intent automatically and confirms with user.

### Phase 2: Repository Analysis (Automated)

- Uses Glob/Read/Grep to extract technical patterns (no MCP - preserves session time)
- Identifies frameworks, architecture, tools
- Analyzes package manifests, documentation, configuration

### Phase 3: Ontology Mapping (Validated)

- Maps to Domain Knowledge Graphs (CrewAI, LangChain, Autogen, Semantic Kernel)
- Validates against actual frameworks (prevents hallucinations)
- **User validation checkpoint** - confirms mappings are accurate

### Phase 4: Behavioral Synthesis (Automated)

- Generates 50+ observations from 8 universal categories
- Creates execution_protocol with autonomy/monitoring constraints
- Injects inheritance from COLLABORATION base
- Produces methodology_techniques (4+ per domain)

### Phase 5: Profile Validation (AUTOMATED QUALITY GATE)

**The Killer Phase** - catches 95% of issues before user sees them.

Checklist enforcement:
- ✅ 8+ execution_protocol.autonomy observations
- ✅ Inheritance relations exist (COLLABORATION base)
- ✅ 4+ methodology_techniques per domain
- ✅ Hallucination prevention constraints present
- ✅ Reporting hierarchy complete (for HMAS)

IF FAIL → Auto-regenerate Phase 4 (max 3 attempts with diagnostic feedback)
IF PASS → Continue to Phase 6

### Phase 6: Profile Generation (Output)

Writes operational profile file(s):

**Singular:** `CLAUDE.md`

**Composite (HMAS):**
- `CLAUDE.md` (System Owner)
- `{PrimaryRole}.md` (e.g., Researcher.md)
- `{Specialist}.md` (backroom profiles)

User reviews final output with option to iterate.

## Examples

```bash
# Guided conversation (recommended for first use)
/create-profile

# Quick creation with defaults
/create-profile "research team" "https://github.com/joaomdmoura/crewai"

# Documentation project
/create-profile "documentation architect" "https://github.com/facebook/docusaurus"
```

## Iteration Support

At validation checkpoints:
- **Phase 1:** Review structured intent → [Confirm / Adjust]
- **Phase 3:** Review ontology mappings → [Confirm / Adjust / Add Links]
- **Phase 6:** Review generated profile → [Accept / Refine Sections / Regenerate]

## Error Handling

- Invalid repo URL → Validate and retry with suggestion
- Inaccessible repo → Fallback to study_links only
- Unknown framework → Graceful degradation with warning
- Phase 5 validation failure (3x) → Surface diagnostic with suggestions

## Output Format

Living operational profiles with 6 layers:
1. Constitutional (Identity, Prime Directive, Focus Areas)
2. Knowledge (Domain Graphs, Blind Spots)
3. Activation (Triggers, Prerequisites)
4. Operational (Methodology, Tools, Artifacts)
5. Social (Reporting Lines for HMAS)
6. Behavioral (Execution Protocol, Observations, Inheritance)

Profiles have agency: activation triggers, self-monitoring, rejection protocols, transformation logic.

## Current Implementation Status

**Phase 1:** In Development - Basic conversational flow
**Phases 2-6:** Not Yet Implemented - See design in conversation log

## Related Commands

- `/validate-profile [path]` - Run Phase 5 validation on existing profile
- `/adjust-phase [N]` - (Future) Backward iteration to specific phase
- `/regenerate-phase [N]` - (Future) Manual retry of phase

## Design Reference

Complete architecture in: `.claude/conversations/2024/12/21-profile-creator-skill-design.md`
