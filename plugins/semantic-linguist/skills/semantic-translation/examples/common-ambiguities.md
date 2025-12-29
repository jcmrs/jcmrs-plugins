# Common Cross-Domain Ambiguities

Frequent ambiguous patterns that appear across multiple domains and frameworks.

## Meta-Questions (User Triggers)

### "am I making sense?"

**Intent:** User seeking validation of their explanation

**Response Pattern:**
```
"Let me verify I understand. Based on your recent messages:

- You want to [summarize key point 1]
- Using [technology/framework mentioned]
- With [specific requirement]

I noticed '[ambiguous term]' could mean:
- Option A: [precise interpretation]
- Option B: [precise interpretation]

Which interpretation is correct?"
```

**Example:**
```
User: "I'm trying to create a system where agents collaborate on tasks.
      Am I making sense?"

Response: "Yes, I understand you want multi-agent collaboration. I notice
'collaborate on tasks' could mean different things:

In Autogen:
- GroupChat for simultaneous multi-agent conversation
- Sequential agent handoff (agent A → agent B)

In Langroid:
- Task delegation hierarchy
- Parent task with multiple subtasks

Which framework are you using, and which collaboration pattern?"
```

### "does this make sense?"

**Intent:** User uncertain about their approach

**Response Pattern:**
```
"Your approach [summary of their description] makes sense for [use case].

One clarification needed: '[ambiguous aspect]'
- Did you mean [Option A] or [Option B]?

This will help me provide more specific guidance."
```

## Vague Action Verbs

### "make it work"

**Ambiguity:** What specifically isn't working?

**Clarification Template:**
```
"To help you make it work, I need to understand what's not working:

1. **Error/Exception?** - Share the error message
2. **Wrong behavior?** - Describe expected vs actual behavior
3. **Not executing?** - Is it running at all?
4. **Configuration issue?** - Setup or installation problem?

What specifically is the issue?"
```

### "make it faster"

**Ambiguity:** Which performance metric?

**Clarification Template:**
```
"'Faster' could mean different optimizations:

1. **Response time** (latency)
   - Reduce time from request to response
   - Solutions: Caching, query optimization, async

2. **Throughput** (requests/second)
   - Handle more concurrent requests
   - Solutions: Load balancing, horizontal scaling

3. **Startup time** (cold start)
   - Reduce initialization time
   - Solutions: Lazy loading, pre-compilation

4. **Processing time** (execution)
   - Speed up core algorithm
   - Solutions: Algorithm optimization, parallelization

Which metric are you trying to optimize?"
```

### "make it secure"

**Ambiguity:** Which security aspect?

**Clarification Template:**
```
"Security has multiple aspects:

1. **Authentication** - Verify user identity
   - Solutions: JWT, OAuth, API keys

2. **Authorization** - Control access to resources
   - Solutions: RBAC, permissions, policies

3. **Data protection** - Encrypt sensitive data
   - Solutions: TLS/SSL, encryption at rest

4. **Input validation** - Prevent injection attacks
   - Solutions: Sanitization, parameterized queries

5. **Secrets management** - Protect credentials
   - Solutions: Vault, env vars, key management

Which security concern are you addressing?"
```

## Generic Technical Terms

### "component"

**Ambiguity:** Type of component?

**Context-Dependent Interpretations:**
- **Frontend:** UI component (React, Vue, Svelte)
- **Backend:** Service component, module
- **Architecture:** System component, microservice
- **Code:** Class, function, module

**Clarification:** "What kind of component? UI component, backend service, or code module?"

### "service"

**Ambiguity:** Service type?

**Context-Dependent Interpretations:**
- **Microservices:** Independent deployable service
- **Backend:** API service, application service
- **System:** OS service, daemon
- **Cloud:** AWS/Azure service

**Clarification:** "Do you mean a microservice, backend API service, or cloud service?"

### "module"

**Ambiguity:** Module type?

**Context-Dependent Interpretations:**
- **Python:** .py file, package
- **JavaScript:** ES module, npm package
- **Architecture:** Logical module, code organization
- **System:** Loadable module, plugin

**Clarification:** "What type of module? Python module, npm package, or logical code module?"

## Scope Ambiguities

### "add validation"

**Clarification Template:**
```
"Validation has different scopes:

1. **Input validation** (user input, API params)
   - Check types, formats, ranges
   - Tools: Pydantic, Zod, JSON Schema

2. **Business logic validation** (rules, constraints)
   - Enforce business rules
   - Custom validation functions

3. **Schema validation** (database, API contracts)
   - Ensure data structure compliance
   - ORM validators, OpenAPI

Which level of validation do you need?"
```

### "improve performance"

See "make it faster" above - same pattern.

### "add logging"

**Clarification Template:**
```
"Logging serves different purposes:

1. **Debug logging** (development)
   - Verbose, detailed logs
   - Level: DEBUG

2. **Application logging** (production monitoring)
   - Structured logs, errors, warnings
   - Level: INFO, WARNING, ERROR

3. **Audit logging** (compliance, security)
   - Immutable logs, who did what when
   - Never rotated or deleted

4. **Performance logging** (metrics, tracing)
   - Timing, performance metrics
   - Tools: APM, distributed tracing

What's the purpose of the logging?"
```

## Domain Confusion

### "agent" (multi-domain term)

**Possible Meanings:**
- **Autogen:** ConversableAgent, AssistantAgent, UserProxyAgent
- **Langroid:** ChatAgent, ToolAgent
- **General AI:** AI agent, chatbot
- **Business:** User agent, sales agent
- **System:** Software agent, daemon

**Clarification:** "Which framework's agent? Autogen, Langroid, or general AI agent?"

### "task" (multi-domain term)

**Possible Meanings:**
- **Langroid:** Task object for orchestration
- **Autogen:** General task/goal for agent
- **Celery:** Async task queue job
- **General:** Todo item, work item

**Clarification:** "Do you mean Langroid Task object, async task queue job, or general task concept?"

### "tool" (multi-domain term)

**Possible Meanings:**
- **Autogen:** Function calling (register_for_llm)
- **Langroid:** ToolMessage
- **General:** CLI tool, utility, library
- **LangChain:** Tool interface

**Clarification:** "Which framework's tool system? Autogen function calling, Langroid ToolMessage, or general utility?"

## Unclear References

### "use that"

**Problem:** Ambiguous antecedent

**Clarification:** "Which component are you referring to? [List recent mentioned components]"

### "like before"

**Problem:** Unclear which previous instance

**Clarification:** "Like in which file/section? Can you point me to the specific example?"

### "the thing" / "it"

**Problem:** Non-specific reference

**Clarification:** "Which specific component/variable/function?"

## Pattern Recognition

### High-Ambiguity Signals

Trigger validation when detecting:
- Vague action verbs: "make it X", "do the thing"
- Generic technical terms without context: "component", "service"
- Meta-questions: "am I making sense?", "does this make sense?"
- Unclear references: "that", "it", "the thing"
- Domain-crossing: Mixing framework-specific terms
- Invented terms: Words not in technical vocabulary

### Low-Ambiguity Signals

Low risk, probably don't need validation:
- Specific technical terms: "ConversableAgent", "FastAPI"
- Clear context: Recent messages establish domain
- Precise language: "HTTP REST API server", "Autogen GroupChat"
- Code examples provided: Shows exact intent

## Summary

Common cross-domain ambiguities require:

1. **Context detection** - Identify domain/framework
2. **Pattern matching** - Recognize ambiguous patterns
3. **Clarification** - Ask specific questions
4. **Validation** - Confirm understanding before implementing

Use these patterns to quickly identify and resolve ambiguities across different technical domains.
