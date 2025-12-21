# /validate-profile - Validate Operational Domain Profile

Run Phase 5 validation checklist on an existing profile to verify quality and completeness.

## Usage

```bash
/validate-profile <path-to-profile>
```

## Arguments

- `path` (required): Path to profile file (CLAUDE.md, AGENTS.md, etc.)

## Behavior

Loads the specified profile and runs the **Phase 5 Validation Checklist** to verify:

### Quality Checklist

**Execution Protocol:**
- ✅ 8+ autonomy observations (self-assertion, expertise claiming)
- ✅ Monitoring observations present (bias detection, drift monitoring)

**Behavioral Programming:**
- ✅ Inheritance relations exist (COLLABORATION base or equivalent)
- ✅ 4+ methodology techniques per domain area
- ✅ Observations structured by category (4-5 per category)

**Structural Completeness:**
- ✅ Identity section present (archetype, prime directive)
- ✅ Focus areas defined (3-5 domains with clear boundaries)
- ✅ Domain knowledge graphs listed (5+ sources)
- ✅ Operational methodology defined (process steps)
- ✅ Tooling interface specified (authorized tools)
- ✅ Artifacts section complete (inputs and outputs)

**Living Profile Indicators:**
- ✅ Activation triggers present (condition-specific patterns)
- ✅ Self-monitoring mechanisms defined
- ✅ Rejection protocols exist (blocks invalid requests)
- ✅ Transformation logic present (adapts behavior based on context)

**Constraints Validation (if specified):**
- ✅ Hallucination prevention measures present
- ✅ Peer review requirements defined (if applicable)
- ✅ Security-first constraints applied (if applicable)
- ✅ Systematic validation enforced (if applicable)

**Multi-Role Profiles (HMAS only):**
- ✅ System Owner reporting hierarchy complete
- ✅ Backroom profiles have clear specialization
- ✅ Delegation protocols defined
- ✅ Expertise boundaries clear between roles

## Output Format

**Validation Passed:**
```
✅ Profile validation PASSED

Quality Score: X/Y checks passed

Strengths:
- [Identified strong areas]

Recommendations:
- [Optional improvements]
```

**Validation Failed:**
```
❌ Profile validation FAILED

Failed Checks:
- [ ] Check 1: [Specific issue]
- [ ] Check 2: [Specific issue]

Diagnostic:
[Detailed explanation of what's missing or insufficient]

Suggestions:
1. [Specific fix for issue 1]
2. [Specific fix for issue 2]

Manual Fix:
Edit [file:line] to address [specific issue]
```

## When to Use

**Recommended scenarios:**
- After manually editing an existing profile
- Before deploying profile to production environment
- When profile behavior seems inconsistent or shallow
- Periodic quality audits of domain profiles
- After extending profile with new capabilities

## Validation Philosophy

The validator enforces the distinction between **living operational profiles** and **dead documentation**:

**Will FAIL if profile lacks:**
- Activation triggers (just describes without triggering)
- Self-monitoring (no bias/drift detection)
- Rejection protocols (accepts everything)
- Transformation logic (static, doesn't adapt)
- Behavioral observations (just procedures, no constraints)

**Will PASS profiles with:**
- Auto-active patterns based on conditions
- Explicit monitoring for problematic patterns
- Clear boundaries and rejection criteria
- Context-aware behavior adaptation
- Rich observation layers guiding formulation

## Integration with /create-profile

The same validation logic runs automatically in `/create-profile` Phase 5 with auto-regeneration (max 3 attempts). Using `/validate-profile` manually allows you to:
- Validate profiles created outside the pipeline
- Re-validate profiles after manual edits
- Audit quality without regeneration attempts

## Examples

```bash
# Validate singular profile
/validate-profile CLAUDE.md

# Validate System Owner in HMAS
/validate-profile CLAUDE.md

# Validate backroom specialist
/validate-profile Researcher.md

# Validate after manual edits
/validate-profile docs/profiles/custom-profile.md
```

## Current Implementation Status

**Status:** Not Yet Implemented

This command definition exists but validation logic is not implemented. Implementation requires:
- Profile parsing and structure detection
- Checklist evaluation logic
- Diagnostic message generation
- Suggestion synthesis based on failures

## Related Commands

- `/create-profile` - Generate new profile with built-in Phase 5 validation
- Future: `/enhance-profile [path] [aspect]` - Add missing elements to existing profile
- Future: `/audit-profiles [directory]` - Batch validate multiple profiles

## Design Reference

Complete validation checklist specification: `.claude/conversations/2024/12/21-profile-creator-skill-design.md`
