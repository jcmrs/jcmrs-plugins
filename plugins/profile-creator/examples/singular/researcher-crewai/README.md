# Researcher - CrewAI Framework Expert

## Overview

This is a complete, production-quality singular operational profile demonstrating all Profile Creator design principles. It provides deep expertise in the CrewAI multi-agent framework through systematic source validation.

## Profile Characteristics

**Type**: Singular Operational Profile
**Domain**: CrewAI Multi-Agent Framework
**Archetype**: Researcher
**Observation Count**: 70+ across 10 categories
**Profile Length**: ~450 lines

## What Makes This Profile "Alive"

This profile demonstrates the distinction between **living operational profiles** and **dead documentation**:

### Living Characteristics Present

1. **Activation Triggers** (Section 3)
   - Auto-activates when CrewAI topics detected
   - Condition-specific patterns for engagement
   - No explicit user invocation required

2. **Self-Monitoring** (Section 7 - Monitoring)
   - Detects confirmation bias, anchoring bias, availability bias
   - Monitors for drift from validated patterns to speculation
   - Catches language degradation (tentative vs authoritative)
   - Tracks citation quality degradation

3. **Rejection Protocols** (Throughout behavioral constraints)
   - Refuses to speculate about undocumented features
   - Rejects vague requirements preventing proper research
   - Challenges flawed assumptions rather than accommodating

4. **Transformation Logic** (Decision Heuristics + Observations)
   - Adapts technical depth based on user's demonstrated understanding
   - Escalates from docs → source code → community based on ambiguity
   - Adjusts validation rigor based on claim criticality

## Key Design Decisions

### 1. Narrow Domain Focus

**Decision**: Specialize in CrewAI only, not general multi-agent frameworks

**Rationale**: Deep expertise in one framework beats shallow coverage of many. Explicit blind spots (AutoGPT, LangGraph) maintain boundaries.

**Implementation**: Focus areas are CrewAI-specific (Agent Architecture, Task Design, Crew Orchestration), not generic (AI systems, Agent frameworks).

### 2. Systematic Validation Methodology

**Decision**: Always validate claims against sources before confirming

**Rationale**: Prevents hallucination of non-existent CrewAI features, which is the profile's prime directive.

**Implementation**: 8-step process with source prioritization hierarchy (docs → code → examples → community).

### 3. Three-Tier Confidence Levels

**Decision**: Label all findings as "validated", "inferred", or "uncertain"

**Rationale**: Transparency about confidence prevents users from treating speculation as fact.

**Implementation**: Built into process (step 8) and observations category (Communication of Findings).

### 4. Version-Aware Recommendations

**Decision**: Track CrewAI versions and note breaking changes

**Rationale**: CrewAI evolves rapidly; version-agnostic advice causes implementation failures.

**Implementation**: Dedicated observation category (Version & Compatibility Management) with 7 observations.

### 5. Anti-Pattern Detection

**Decision**: Identify problematic patterns proactively, not just answer questions

**Rationale**: Users often don't know they're implementing anti-patterns. Expert profiles should catch these.

**Implementation**: Full observation category (Anti-Pattern Detection) with 8 specific patterns.

### 6. Performance as Distinct Expertise

**Decision**: Separate observation category for performance & optimization

**Rationale**: Performance is often overlooked in framework learning; making it explicit ensures consideration.

**Implementation**: 7 observations covering parallelization, tool optimization, LLM usage, memory, timeouts.

## Behavioral Programming Highlights

### Observation Organization (10 Categories)

1. **CrewAI Framework Patterns** (7 obs) - Core framework usage
2. **Research & Validation Methodology** (8 obs) - How research is conducted
3. **Source Validation Hierarchy** (7 obs) - Prioritization of sources
4. **Pattern Analysis & Recommendation** (8 obs) - How to recommend approaches
5. **Anti-Pattern Detection** (8 obs) - Identifying problematic patterns
6. **Integration Patterns** (7 obs) - Connecting CrewAI to other systems
7. **Performance & Optimization** (7 obs) - Making crews efficient
8. **Error Handling & Robustness** (7 obs) - Building reliable systems
9. **Communication of Findings** (7 obs) - How to explain research
10. **Version & Compatibility Management** (7 obs) - Tracking changes
11. **Edge Case & Limitation Awareness** (7 obs) - Knowing boundaries

**Total**: 70+ observations encoding deep CrewAI expertise

### Autonomy Observations (12 total)

These prevent the profile from defaulting to generic assistant mode:

- "As a CrewAI Researcher, I need to validate that" not "Let me try to help"
- "The docs don't show that feature" not "Maybe that exists"
- Challenges flawed assumptions rather than accommodating them
- Insists on source verification even under pressure for quick answers

### Monitoring Observations (8 total)

These enable self-correction:

- Detects when drifting from validated patterns to speculation
- Catches language becoming tentative instead of authoritative
- Monitors for citation quality degradation
- Notices when providing outdated info without version check

## Usage Scenarios

### Scenario 1: Capability Validation

**User**: "Can CrewAI agents delegate tasks to each other dynamically?"

**Profile Response**:
1. Activates (trigger: CrewAI capability question)
2. Searches official docs for "delegation"
3. Finds delegation feature in hierarchical process
4. Validates against source code
5. Cites docs.crewai.com/core-concepts/processes#hierarchical-process
6. Explains how delegation works with manager agent
7. Notes version requirement if applicable
8. Provides example from crewai-examples

**Confidence**: "Validated" (found in official docs + examples)

### Scenario 2: Pattern Recommendation

**User**: "I have 5 tasks that need to run in a specific order. How should I structure my crew?"

**Profile Response**:
1. Analyzes use case (sequential dependency)
2. Recommends sequential process over hierarchical
3. Explains why (no dynamic coordination needed)
4. Provides task dependency configuration pattern
5. Cites official sequential process documentation
6. Warns about common anti-patterns (over-engineering with hierarchical)
7. Suggests when to reconsider (if requirements change)

**Trade-off Presented**: Sequential (simpler) vs Hierarchical (more flexible but overkill for this)

### Scenario 3: Anti-Pattern Detection

**User**: "I'm creating 10 agents, each handling one small step"

**Profile Response**:
1. Detects over-engineering anti-pattern
2. Challenges approach: "10 agents for small steps suggests over-engineering"
3. Analyzes task breakdown for genuine parallelism needs
4. Likely recommends: single agent with 10 sequential tasks
5. Explains coordination overhead of many agents
6. Cites best practices from docs on crew sizing
7. Provides simpler alternative with trade-offs

**Rejection**: Polite but firm challenge to problematic pattern

## Learning from This Example

### For Profile Creators

**What to replicate:**
- Narrow domain focus (depth over breadth)
- Systematic methodology (repeatable process)
- Explicit confidence levels (transparency)
- Anti-pattern detection (proactive expertise)
- Version awareness (evolving domains)

**What to adapt:**
- Observation categories should match your domain's structure
- Validation hierarchy specific to your knowledge sources
- Autonomy patterns match your archetype (Researcher asserts research, Architect asserts design, etc.)

### For Profile Users

**How to evaluate if this profile worked:**
- Claims are always cited with specific sources
- Multiple approaches presented when options exist
- Uncertainty is flagged explicitly, never masked
- Version requirements noted when relevant
- Anti-patterns caught proactively

**Red flags indicating profile isn't active:**
- Generic multi-agent advice not specific to CrewAI
- Claims without citations
- Speculation about capabilities
- No version considerations
- Single "best practice" without trade-offs

## Technical Notes

### Tool Integration

The profile uses:
- `WebFetch` for documentation retrieval
- `mcp__context7__get-library-docs` for API reference
- `Read` and `Grep` for source code analysis
- `mcp__cipher__ask_cipher` for historical knowledge
- `LSP` for deep codebase navigation

This tool selection enables the validation methodology.

### Process Rigor

The 8-step process ensures:
1. Claims are identified
2. Sources are prioritized
3. Documentation is searched
4. Code is cross-referenced if needed
5. Validation is completed
6. Recommendations are synthesized
7. Citations are documented
8. Confidence is assessed

Every response should trace to this process.

### Observation Density

70+ observations across 10 categories might seem like overkill. It's not. This density:
- Covers the breadth of CrewAI domain
- Encodes expert judgment patterns
- Prevents gaps in expertise
- Enables fine-grained behavior control

Profiles with <40 observations are likely too shallow for complex domains.

## Validation Checklist

This profile passes all Profile Creator validation requirements:

- [x] 8+ autonomy observations (has 12)
- [x] 5+ monitoring observations (has 8)
- [x] Inheritance from COLLABORATION base
- [x] 4+ methodology techniques per domain (has 7+ per category)
- [x] Hallucination prevention constraints present
- [x] Identity, Prime Directive, Focus Areas defined
- [x] 5+ domain knowledge graphs (has 7)
- [x] Operational methodology defined (8-step process)
- [x] Activation triggers present (living profile)
- [x] Self-monitoring mechanisms (8 monitoring observations)
- [x] Rejection protocols (behavioral constraints)
- [x] Transformation logic (decision heuristics)

## Relationship to Templates

This example was built from `templates/singular/profile-template.md` with:
- All inline guidance removed (production-ready)
- Template placeholders replaced with real CrewAI content
- Observation categories customized to CrewAI domain structure
- Real sources, real patterns, real anti-patterns
- Validation against actual CrewAI framework

Use this as reference for what a completed profile should look like.

## Maintenance Notes

**When to update this profile:**
- CrewAI releases breaking changes
- New CrewAI features added (new process types, memory improvements)
- Official documentation structure changes significantly
- Anti-patterns become canonical (rare but possible)

**Version compatibility**: This profile was created for CrewAI 0.30.0+ patterns. Some observations may need updates for future major versions.
