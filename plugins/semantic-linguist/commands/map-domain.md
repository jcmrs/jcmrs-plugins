---
name: map-domain
description: Provide conversational complete reference of domain mappings between Autogen, Langroid, and general concepts with cross-domain translations
---

# Map Domain Command

Provide comprehensive domain mapping reference to translate between Autogen, Langroid, and general AI agent concepts.

## Process

1. **Identify User's Context**
   - Detect current domain from conversation (Autogen, Langroid, or general)
   - Identify target domain (if user is switching or learning new framework)
   - Determine user's experience level (technical vs non-technical)

2. **Load Domain Knowledge**
   - Read `skills/semantic-validation/knowledge/ontology-graph.json`
   - Read `skills/semantic-validation/knowledge/technical-mappings.json`
   - Load cross-domain equivalents

3. **Present Conversational Complete Reference**

   Start with overview:
   ```
   # Domain Mapping Reference

   I'll show you how concepts translate between frameworks.

   **Current context**: [detected domain]
   **Available domains**: Autogen, Langroid, General AI concepts

   Let me know if you want:
   1. Complete reference (all mappings)
   2. Specific concept mapping (e.g., "how does Autogen's ConversableAgent map to Langroid?")
   3. Domain-specific deep dive (all Autogen patterns)
   4. Cross-framework comparison (same concept across all domains)
   ```

4. **Provide Requested Mapping Type**

   **Option 1: Complete Reference**
   ```markdown
   ## Core Concepts Across Frameworks

   ### Agent Types

   | Concept | Autogen | Langroid | General |
   |---------|---------|----------|---------|
   | Basic agent | ConversableAgent | ChatAgent | AI conversational agent |
   | Tool-enabled agent | AssistantAgent | ToolAgent pattern | Function-calling agent |
   | Human proxy | UserProxyAgent | Task with interactive=True | Human-in-loop agent |
   | Orchestrator | GroupChatManager | Parent Task | Multi-agent coordinator |

   ### Communication Patterns

   | Pattern | Autogen | Langroid | General |
   |---------|---------|----------|---------|
   | One-to-one | send() / initiate_chat() | Task.run() | Direct messaging |
   | Multi-party | GroupChat + GroupChatManager | Task hierarchy | Multi-agent system |

   ### Tool/Function Calling

   | Aspect | Autogen | Langroid | General |
   |--------|---------|----------|---------|
   | Definition | Function with type hints | ToolMessage subclass | Tool schema |
   | Registration | @register_for_llm() | Auto-detection | Tool registry |
   | Execution | @register_for_execution() | ToolMessage.handle() | Tool executor |

   [Continue with comprehensive mappings...]

   **Want to dive deeper into any concept? Just ask!**
   ```

   **Option 2: Specific Concept**
   ```markdown
   ## Mapping: [Concept Name]

   ### What it is (General)
   [Plain language explanation]

   ### Autogen Implementation
   - **Class/Method**: [name]
   - **Purpose**: [what it does]
   - **Use cases**: [when to use]
   - **Key methods**: [list]
   - **Example**:
     ```python
     [code example]
     ```

   ### Langroid Implementation
   - **Class/Pattern**: [name]
   - **Purpose**: [what it does]
   - **Use cases**: [when to use]
   - **Key methods**: [list]
   - **Example**:
     ```python
     [code example]
     ```

   ### Conceptual Relationship
   - Both solve: [problem]
   - Key difference: [how they differ]
   - Choose Autogen if: [scenario]
   - Choose Langroid if: [scenario]

   ### Cross-Domain Translation
   If you're moving from [framework A] to [framework B]:
   - Instead of [A concept], use [B equivalent]
   - Pattern changes from [A pattern] to [B pattern]
   ```

   **Option 3: Domain-Specific Deep Dive**
   ```markdown
   ## [Framework] Complete Patterns

   ### Agent Hierarchy
   [Detailed class hierarchy with relationships]

   ### Communication Patterns
   [All messaging patterns with code examples]

   ### Tool Integration
   [Complete tool calling workflow]

   ### Orchestration
   [Multi-agent coordination patterns]

   [Include ontology graph visualization as markdown tree]
   ```

   **Option 4: Cross-Framework Comparison**
   ```markdown
   ## [Concept] Across All Frameworks

   ### Problem Statement
   [What problem this solves]

   ### Autogen Approach
   - Philosophy: [design philosophy]
   - Implementation: [how it works]
   - Code pattern: [example]
   - Pros: [benefits]
   - Cons: [limitations]

   ### Langroid Approach
   - Philosophy: [design philosophy]
   - Implementation: [how it works]
   - Code pattern: [example]
   - Pros: [benefits]
   - Cons: [limitations]

   ### General Pattern
   - Abstract concept: [explanation]
   - When to use: [scenarios]
   - Alternatives: [other approaches]

   ### Migration Guide
   From Autogen to Langroid:
   1. [Step 1]
   2. [Step 2]

   From Langroid to Autogen:
   1. [Step 1]
   2. [Step 2]
   ```

5. **Interactive Follow-Up**

   After presenting information, offer:
   ```
   What would you like to explore next?
   - Dive deeper into [related concept]
   - See code examples for [specific pattern]
   - Compare with [alternative framework]
   - Get clarification on [ambiguous term]
   - Continue with current understanding
   ```

## Usage Examples

**Basic usage (presents options):**
```
/map-domain
```

**Specific concept:**
```
/map-domain ConversableAgent
```

**Framework comparison:**
```
/map-domain autogen vs langroid
```

**After command, user can request:**
```
show me tool calling patterns
```
or
```
how do I migrate from Autogen to Langroid?
```
or
```
explain GroupChat in simple terms
```

## Data Sources

- **ontology-graph.json**: Conceptual hierarchies and relationships
- **technical-mappings.json**: Precise technical translations
- **ambiguous-terms.json**: User phrase to technical term mappings
- **references/domain-ontologies.md**: Detailed relationship graphs
- **references/translation-patterns.md**: Common translation patterns

## Output Format

- **Conversational introduction**: Detect context, present options
- **Structured reference**: Tables, hierarchies, code examples
- **Interactive navigation**: User can drill down or switch topics
- **Always contextual**: Adapt to user's current framework and goals

## Important Principles

- **User-directed**: Present complete reference, user chooses depth
- **Conversational**: Not a dry reference dump, but guided exploration
- **Multi-modal**: Tables, code, explanations, visualizations
- **Cross-linkable**: Connect related concepts naturally
- **No assumptions**: If unclear which framework user wants, ask
- **Practical focus**: Include code examples and use cases
- **Jargon translation**: Always explain technical terms

## Integration

- Works standalone or after semantic validation
- Can be triggered from `/validate-terminology` findings
- References same knowledge base as validation workflow
- Complements clarification process with comprehensive mappings
