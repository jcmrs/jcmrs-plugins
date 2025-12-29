---
name: validate-terminology
description: Analyze recent conversation messages for ambiguous terminology and provide semantic validation with conversational summary and optional detailed report
---

# Validate Terminology Command

Analyze the last 5-10 messages in the conversation for semantic ambiguities and provide validation feedback.

## Process

1. **Retrieve Recent Messages**
   - Extract last 5-10 user messages from conversation history
   - Include Claude's responses for context

2. **Load Knowledge Base**
   - Read `skills/semantic-validation/knowledge/ambiguous-terms.json`
   - Read `skills/semantic-validation/knowledge/technical-mappings.json`
   - Read `skills/semantic-validation/knowledge/ontology-graph.json`

3. **Detect Ambiguities**
   - Scan for known ambiguous terms from knowledge base
   - Identify meta-questions ("am I making sense?", "does this make sense?")
   - Detect vague action verbs ("make it X", "do the thing")
   - Check for generic technical terms without context
   - Look for unclear references ("that", "it", "the thing")
   - Identify domain confusion (mixing framework-specific terms)

4. **Calculate Confidence Scores**
   - Meta-question detected: +100 (auto-trigger)
   - Known high-ambiguity term: +40
   - Vague action verb: +30
   - Generic term without context: +25
   - Domain confusion: +35
   - Unclear reference: +20
   - Recent conversation provides context: -20
   - Specific technical term used: -30

5. **Provide Conversational Summary**
   - **If no ambiguities found (score < 60):**
     ```
     ✅ Terminology looks clear! I didn't detect any significant ambiguities in the last [N] messages.

     The conversation has been using specific technical terms and clear references.
     ```

   - **If minor ambiguities (score 60-79):**
     ```
     ⚠️ Found some potentially ambiguous terms:

     - "[term]" could mean:
       • [Option 1] (most likely based on context)
       • [Option 2]

     Current context suggests [interpretation], but let me know if that's not what you meant.

     Want a detailed report? Just ask!
     ```

   - **If significant ambiguities (score ≥ 80):**
     ```
     🔍 Detected several ambiguous terms that might benefit from clarification:

     **High-priority:**
     - "[term 1]" (score: [X]) - Could mean:
       • [Domain 1]: [precise meaning]
       • [Domain 2]: [precise meaning]
       • [General]: [precise meaning]

     **Moderate-priority:**
     - "[term 2]" (score: [Y]) - Possible interpretations...

     Would you like me to:
     1. Clarify these terms now
     2. See a detailed analysis report
     3. Continue with my best understanding

     (Type "detailed report" for comprehensive analysis)
     ```

6. **Generate Detailed Report (if requested)**
   When user requests detailed report, provide:

   ```markdown
   # Semantic Validation Report

   ## Analysis Summary
   - **Messages analyzed**: [N]
   - **Ambiguities detected**: [count]
   - **Confidence scores**: [range]
   - **Domains detected**: [list]

   ## Detected Ambiguities

   ### 1. "[ambiguous term]" (Score: [X])

   **Category**: [vague_action_verb | unclear_scope | generic_term | meta_question | domain_confusion]

   **Possible meanings**:
   - **Autogen**: [precise translation]
     - Methods: [list]
     - Use cases: [list]
   - **Langroid**: [precise translation]
     - Methods: [list]
     - Use cases: [list]
   - **General**: [precise translation]

   **Context clues**:
   - [Relevant context from conversation]

   **Recommended clarification**:
   > "[Specific question to ask user]"

   **Why this matters**:
   [Explanation of why ambiguity is problematic]

   ---

   ### 2. [Next ambiguity]...

   ## Cross-Domain Equivalents

   If user is working across frameworks:
   - **Autogen term** → **Langroid equivalent** → **General concept**
   - [mappings from ontology-graph.json]

   ## Recommendations

   1. **Immediate clarifications needed**: [list]
   2. **Context-dependent terms**: [list]
   3. **Suggested terminology**: [precise alternatives]

   ## Next Steps

   Would you like me to:
   - Clarify specific terms now
   - Map to your target domain
   - Continue with validated understanding
   ```

## Usage Examples

**Basic usage:**
```
/validate-terminology
```

**After validation, user can request:**
```
detailed report
```
or
```
clarify [specific term]
```

## Integration

- Loads semantic-validation skill automatically
- Uses knowledge files for detection
- References ontology-graph.json for cross-domain mappings
- Conversational and non-blocking
- Always offers options, never assumes

## Output Format

- **Conversational summary** (default): 3-5 sentences with key findings
- **Detailed report** (on request): Comprehensive markdown analysis
- **Interactive follow-up**: User can ask for clarifications or mappings

## Important Principles

- **Never assume**: Present options, verify with user
- **Conversational tone**: Friendly and helpful, not prescriptive
- **Context-aware**: Consider recent conversation flow
- **Actionable**: Provide clear next steps
- **Optional detail**: Summary first, detailed report on request
