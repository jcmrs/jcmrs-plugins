# Profile Creator Examples and Templates

## Overview

This directory contains comprehensive templates and reference examples for creating operational domain profiles with behavioral programming. All materials meet the collaboration platform's standards for living, operational profiles.

## What's Included

### Templates (3 comprehensive files)

**Location**: `templates/`

1. **`singular/profile-template.md`** (~620 lines)
   - Complete template for singular operational profiles
   - Extensive inline guidance with examples of good vs bad
   - Quality criteria and completion checklists
   - Covers all 6 profile layers with detailed instructions

2. **`composite/system-owner-template.md`** (~550 lines)
   - Template for orchestrator in HMAS architecture
   - Delegation and routing patterns
   - Team structure definition (Section 7)
   - Synthesis and coordination methodology

3. **`composite/specialist-template.md`** (~580 lines)
   - Template for backroom specialists in HMAS
   - Deep domain expertise patterns
   - Reporting relationship to System Owner
   - MORE observations than System Owner (50-70 vs 30-40)

**Total**: ~1750 lines of template guidance

### Examples (3 complete sets)

#### Singular Profiles (2 complete examples)

**1. Researcher - CrewAI Framework Expert**
- Location: `examples/singular/researcher-crewai/`
- Files: CLAUDE.md (450 lines), metadata.json, README.md
- Domain: CrewAI multi-agent framework
- Observations: 70+ across 10 categories
- Demonstrates: Framework validation methodology, source hierarchy, confidence levels

**2. System Architect - Cloud Infrastructure & DevOps**
- Location: `examples/singular/system-architect/`
- Files: CLAUDE.md (480 lines), metadata.json, README.md
- Domain: Cloud infrastructure and DevOps
- Observations: 63 across 11 categories
- Demonstrates: Trade-off analysis, Well-Architected Framework, cost optimization

#### Composite Profile (1 HMAS example)

**3. Research Team - CrewAI Multi-Specialist System**
- Location: `examples/composite/research-team/`
- Files: CLAUDE.md (System Owner, 280 lines), Domain_Linguist.md (320 lines), metadata.json
- Architecture: Hierarchical Multi-Agent System (HMAS)
- Demonstrates: Orchestration, delegation, specialist coordination

**Total**: ~2200 lines of example profiles + documentation

## Quick Navigation

```
plugins/profile-creator/
├── templates/
│   ├── singular/
│   │   └── profile-template.md          # Comprehensive singular template
│   └── composite/
│       ├── system-owner-template.md     # HMAS orchestrator template
│       └── specialist-template.md       # HMAS specialist template
│
├── examples/
│   ├── singular/
│   │   ├── researcher-crewai/
│   │   │   ├── CLAUDE.md                # Complete Researcher profile
│   │   │   ├── metadata.json
│   │   │   └── README.md                # Design rationale and learning guide
│   │   └── system-architect/
│   │       ├── CLAUDE.md                # Complete System Architect profile
│   │       ├── metadata.json
│   │       └── README.md
│   └── composite/
│       └── research-team/
│           ├── CLAUDE.md                # System Owner (orchestrator)
│           ├── Domain_Linguist.md       # Specialist profile
│           ├── metadata.json
│           └── (Note: Researcher specialist references singular example)
│
└── EXAMPLES_README.md                   # This file
```

## How to Use These Materials

### For Profile Creators

**Starting Point**: Choose template based on architecture

| If you need... | Use template... | See example... |
|----------------|----------------|----------------|
| Single expert profile | `singular/profile-template.md` | Researcher or System Architect |
| Multi-role team (2+ specialists) | Both composite templates | Research Team |
| Orchestrator profile | `system-owner-template.md` | Research Team CLAUDE.md |
| Specialist profile | `specialist-template.md` | Domain_Linguist.md |

**Creation Process**:
1. Copy appropriate template
2. Read ALL inline guidance comments
3. Replace placeholders with domain-specific content
4. Remove template comments (production-ready)
5. Validate against checklist at template end
6. Test with actual use cases

**Quality Bar**: Your profile should match example depth and specificity.

### For Profile Validators

**Validation Checklist** (from templates):
- [ ] All 6 layers present and complete
- [ ] 8+ autonomy observations (singular), 6-8 (System Owner)
- [ ] 5+ monitoring observations
- [ ] 40-60+ total observations (singular/specialist), 30-40 (System Owner)
- [ ] Living profile indicators (triggers, monitoring, rejection, transformation)
- [ ] Domain knowledge graphs list real, accessible sources
- [ ] Blind spots explicitly defined
- [ ] Process is actionable sequential workflow
- [ ] Decision heuristics cover common decision points

**Compare against examples**: Production profiles should match examples' depth, not be shallower templates with minimal content.

### For Profile Users

**How to evaluate if profile is working**:
- Claims are cited with specific sources
- Autonomy is visible (profile asserts expertise, doesn't defer)
- Monitoring catches mistakes (self-correction happens)
- Boundaries are maintained (profile says "that's not my domain")
- Observations are reflected in behavior (you can see them guiding responses)

**Red flags** indicating profile isn't active:
- Generic responses not specific to domain
- No source citations
- Tentative language ("maybe", "possibly") on domain expertise
- No boundary maintenance (profile attempts everything)
- Observations don't appear in behavior

## Key Design Patterns Demonstrated

### 1. Living vs Dead Profiles

**All examples demonstrate living profiles**:
- **Activation Triggers**: Auto-activate on conditions (not user invocation)
- **Self-Monitoring**: Detect bias, drift, quality degradation
- **Rejection Protocols**: Refuse invalid requests or approaches
- **Transformation Logic**: Adapt behavior based on context

**See**: Researcher Section 7 (Execution Protocol) for comprehensive demonstration

### 2. Observation Organization

**Domain-specific categories** (not generic):
- **Researcher**: 10 categories aligned with research workflow
- **System Architect**: 11 categories aligned with architectural concerns
- **Domain Linguist**: 6 categories aligned with linguistic analysis

**Observation density**:
- Singular/Specialist: 50-70 observations
- System Owner: 30-40 observations (delegates depth to specialists)

### 3. Autonomy and Authority

**Autonomy patterns shown**:
- Self-assertion over deference
- Expertise claiming over hedging
- Boundary maintenance over scope creep
- Quality standards over accommodation

**See**: Each profile's Autonomy section (Section 8) for 8-12 specific patterns

### 4. Composite Architecture (HMAS)

**Research Team demonstrates**:
- System Owner as first line of defense (always active)
- Specialists activated via delegation (not self-initiated)
- Clear boundaries preventing overlap
- Explicit attribution in synthesis
- Routing logic based on substance not keywords

**When to use composite**:
- Domain large enough for specialization
- Distinct sub-domains with minimal overlap
- Coordination overhead justified by depth gains

**When to use singular**:
- Cohesive domain
- Single expert adequate for breadth and depth
- Simpler deployment priority

### 5. Template Adaptation

**Compare Researcher vs System Architect**:
| Element | Researcher | System Architect |
|---------|------------|------------------|
| Validation | Binary (exists/doesn't) | Spectrum (trade-offs) |
| Certainty | High (validated facts) | Contextual (depends on priorities) |
| Output | Validated claims | Architecture proposals |
| Categories | Research workflow | Architectural concerns |

**Same template, completely different domain application.**

## Learning Path

### Beginner Profile Creators

1. **Start with Researcher README** (`examples/singular/researcher-crewai/README.md`)
   - Understand what makes profiles "alive"
   - See complete worked example

2. **Study template comments** (`templates/singular/profile-template.md`)
   - Read ALL inline guidance
   - Understand quality criteria

3. **Create simple singular profile**
   - Choose narrow domain you know well
   - Follow template systematically
   - Aim for 40+ observations

### Intermediate Profile Creators

1. **Compare Researcher vs System Architect**
   - See how templates adapt to different domains
   - Notice methodology differences
   - Understand observation organization choices

2. **Create singular profile in new domain**
   - Apply template to your expertise area
   - Aim for 50-60+ observations
   - Test with real use cases

3. **Study composite architecture** (Research Team)
   - Understand orchestration patterns
   - Learn delegation and routing logic
   - See specialist collaboration

### Advanced Profile Creators

1. **Create composite HMAS system**
   - Design team with 2-3 specialists
   - Define clear boundaries
   - Implement orchestration logic

2. **Optimize observation density**
   - 60-70+ observations for complex domains
   - 8-12 categories aligned with domain structure
   - Behavioral programming that encodes expert judgment

3. **Validate with real usage**
   - Deploy profiles in actual projects
   - Iterate based on behavioral observations
   - Refine autonomy and monitoring patterns

## Common Pitfalls and Solutions

### Pitfall 1: Shallow Observation Count

**Problem**: Only 20-30 observations, all generic
**Solution**: Study examples (60-70 observations), make domain-specific
**Check**: Can you trace expert judgment patterns in observations?

### Pitfall 2: Dead Documentation

**Problem**: Profile describes behavior but doesn't have operational mechanisms
**Solution**: Add activation triggers, monitoring, rejection protocols
**Check**: Can profile self-activate, self-correct, and refuse invalid requests?

### Pitfall 3: Vague Domain Focus

**Problem**: Focus areas are generic ("AI systems", "architecture")
**Solution**: Narrow to specific frameworks/patterns (see examples)
**Check**: Could two different experts have same focus areas? If yes, too vague.

### Pitfall 4: Missing Autonomy

**Problem**: Profile defers to user, doesn't assert expertise
**Solution**: Add 8-12 autonomy observations with specific assertion patterns
**Check**: Does profile say "As a [archetype], I need to..." or just "I'll help"?

### Pitfall 5: Weak Monitoring

**Problem**: No self-correction mechanisms
**Solution**: Add 5-8 monitoring observations for bias, drift, quality
**Check**: Can profile detect when it's making mistakes?

### Pitfall 6: Composite Complexity

**Problem**: Created HMAS when singular would suffice
**Solution**: Use singular unless coordination genuinely adds value
**Check**: Are specialists' domains truly distinct with minimal overlap?

## Testing Your Profile

### Functional Tests

1. **Activation Test**: Does profile activate on appropriate triggers?
2. **Autonomy Test**: Does profile assert expertise vs defer?
3. **Boundary Test**: Does profile refuse out-of-scope requests?
4. **Monitoring Test**: Does profile catch its own mistakes?
5. **Quality Test**: Are observations visible in behavior?

### Comparison Tests

**Compare your profile against examples**:
- Observation count: 50-70 (singular/specialist), 30-40 (System Owner)?
- Observation specificity: Domain-specific or generic?
- Autonomy: Assertive or deferential?
- Living indicators: All 4 present (triggers, monitoring, rejection, transformation)?

### Production Readiness

**Before deploying**:
- [ ] Removed all template comments
- [ ] Validated against checklist
- [ ] Tested with real use cases
- [ ] Confirmed living profile indicators
- [ ] Verified observation density
- [ ] Checked autonomy and monitoring
- [ ] Ensured domain focus is specific

## Contribution Guidelines

**When adding new examples**:
1. Follow existing structure (CLAUDE.md + metadata.json + README.md)
2. Match depth of existing examples (50-70+ observations)
3. Document design decisions in README
4. Provide metadata.json with characteristics
5. Demonstrate living profile indicators
6. Show domain adaptation patterns

**When updating templates**:
1. Maintain inline guidance structure
2. Add examples of good vs bad
3. Include quality criteria
4. Update checklists if structure changes

## Maintenance Notes

**Templates are stable** - core structure established
**Examples evolve** - update when frameworks/domains change
**Patterns emerge** - document new patterns as discovered

**Version tracking**:
- Templates: version in file header
- Examples: version in metadata.json
- Breaking changes: major version bump

## Questions and Support

**For Profile Creation Help**:
- Study examples' README files (design rationale)
- Read template inline guidance completely
- Compare your work against examples

**For Framework Questions**:
- See collaboration platform documentation
- Reference Profile Design Guidelines
- Check diary entry: `.claude/diary/2024/12/21.md`

## Summary Statistics

**Templates Created**: 3 files, ~1750 lines
**Examples Created**: 3 complete sets, ~2200 lines + documentation
**Total Observations**: 168 across all examples
**Observation Categories**: 27 unique categories across domains
**Living Profile Indicators**: 100% (all examples have all 4)

**Quality Bar**: These materials represent production-quality standards for the Profile Creator plugin. All profiles are usable, tested patterns, not theoretical designs.
