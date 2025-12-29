# Translation Patterns: Ambiguous → Precise

Extensive catalog of ambiguous terminology mapped to precise technical concepts. Use these patterns for quick translation during semantic validation.

## Overview

This document provides comprehensive translation patterns organized by:
1. **Common ambiguities** - Frequently encountered vague terms
2. **Domain-specific translations** - Framework-specific interpretations
3. **Context clues** - Signals that indicate which translation to use
4. **Clarification templates** - How to present options to users

## Top-Tier Ambiguities (User-Reported)

### 1. "make it talk"

**Ambiguity Score:** 0.9 (very high)

**Possible Interpretations:**

| Interpretation | Domain | Technical Term | Context Clues |
|----------------|--------|----------------|---------------|
| Send message | Autogen | `ConversableAgent.send()` | Single message, one recipient |
| Enable conversation | Autogen | Register `ConversableAgent` | Create agent capability |
| Group chat | Autogen | `GroupChat` + `GroupChatManager` | Multiple agents, conversation |
| LLM response | Langroid | `agent.llm_response()` | Generate text response |
| Agent reply | Langroid | `agent.agent_response()` | Agent logic response |
| Speech synthesis | General | TTS API, speech library | Audio output mentioned |
| Chat interface | General | UI component | Frontend, user interaction |
| Console output | General | `print()`, `console.log()` | Simple display |

**Clarification Template:**
```
"'make it talk' could mean several things:

1. **Send a message** (Autogen: ConversableAgent.send())
   - Send a single message to another agent
   - Example: agent.send("Hello", recipient)

2. **Enable conversation capability** (Autogen: ConversableAgent)
   - Create an agent that can participate in conversations
   - Example: ConversableAgent(name="...", system_message="...")

3. **Set up group chat** (Autogen: GroupChat)
   - Multi-party conversation among multiple agents
   - Example: GroupChat([agent1, agent2, agent3])

Which kind of communication are you looking for?"
```

### 2. "we need an api"

**Ambiguity Score:** 0.85 (very high)

**Possible Interpretations:**

| Interpretation | Domain | Technical Term | Context Clues |
|----------------|--------|----------------|---------------|
| REST API server | Backend | Express, FastAPI, Flask | "handle requests", "endpoints" |
| GraphQL API | Backend | Apollo Server, Strawberry | "queries", "mutations", "schema" |
| API client | Integration | requests, axios, fetch | "call external", "consume", "integrate with" |
| API design/spec | Documentation | OpenAPI, Swagger | "documentation", "spec", "contract" |
| Internal API | Architecture | Module interface, class methods | "clean interface", "module boundary" |
| Webhook API | Event-driven | Webhook handlers | "receive events", "callbacks" |
| RPC API | Distributed | gRPC, tRPC | "remote procedure", "type-safe" |

**Clarification Template:**
```
"'API' can mean different things depending on context:

1. **HTTP REST API server** (to handle incoming requests)
   - Framework: Express (Node.js), FastAPI (Python), etc.
   - Use case: Build backend service that responds to HTTP requests

2. **API client** (to call external services)
   - Library: axios, requests, fetch
   - Use case: Integrate with external APIs (GitHub, Stripe, etc.)

3. **API design/specification** (OpenAPI/Swagger docs)
   - Tools: OpenAPI, Swagger, Postman
   - Use case: Document API contract for frontend/clients

4. **Internal API/interface** (code architecture)
   - Concept: Module boundaries, clean interfaces
   - Use case: Organize code with clear public interfaces

Which type of API are you building?"
```

### 3. "make it portable"

**Ambiguity Score:** 0.88 (very high)

**Possible Interpretations:**

| Interpretation | Domain | Technical Term | Context Clues |
|----------------|--------|----------------|---------------|
| Containerization | DevOps | Docker, Podman, container image | "deployment", "infrastructure" |
| Cross-platform | Build | Windows/Mac/Linux compatibility | "operating systems", "platform" |
| Dependency vendoring | Packaging | Bundle dependencies in package | "dependencies", "standalone" |
| Standalone executable | Distribution | PyInstaller, pkg, Electron | "binary", "executable", "no install" |
| Cloud-portable | Infrastructure | Terraform, Kubernetes manifests | "cloud provider", "migration" |
| Source portable | Code | POSIX-compliant, cross-platform code | "source code", "compile anywhere" |

**Clarification Template:**
```
"'Portable' has multiple interpretations:

1. **Containerized** (Docker/Podman)
   - Package app + dependencies in container
   - Run anywhere with container runtime
   - Best for: Server applications, microservices

2. **Cross-platform** (Windows/Mac/Linux)
   - Build native versions for each OS
   - Ensure dependencies available on all platforms
   - Best for: Desktop applications, CLI tools

3. **Dependency vendoring** (bundled dependencies)
   - Include all dependencies in distribution
   - No external installation required
   - Best for: Python packages, Node modules

4. **Standalone executable** (single binary)
   - Compile to single executable file
   - No runtime dependencies
   - Best for: CLI tools, utilities

What kind of portability do you need?"
```

### 4. "check for gaps"

**Ambiguity Score:** 0.82 (high)

**Possible Interpretations:**

| Interpretation | Domain | Technical Term | Context Clues |
|----------------|--------|----------------|---------------|
| Code coverage gaps | Testing | Coverage report, uncovered lines | "tests", "coverage", "untested" |
| Documentation gaps | Docs | Missing docstrings, incomplete guides | "documentation", "readme", "docs" |
| Feature gaps | Product | Missing functionality, incomplete features | "requirements", "features", "backlog" |
| Security gaps | Security | Vulnerabilities, security holes | "security", "vulnerabilities", "CVE" |
| Data gaps | Data | Missing data, incomplete records | "data quality", "missing values", "null" |
| Logic gaps | Code Review | Edge cases, error handling | "logic", "edge cases", "validation" |
| Dependency gaps | Dependencies | Outdated packages, missing libs | "dependencies", "packages", "versions" |

**Clarification Template:**
```
"'Check for gaps' could mean different types of analysis:

1. **Test coverage gaps** (uncovered code)
   - Tool: pytest --cov, jest --coverage
   - Find: Lines/functions without tests
   - Output: Coverage report with missing tests

2. **Documentation gaps** (missing/incomplete docs)
   - Check: Docstrings, README, API docs
   - Find: Undocumented functions, unclear guides
   - Output: List of items needing documentation

3. **Feature gaps** (incomplete functionality)
   - Compare: Requirements vs implemented features
   - Find: Missing features, incomplete workflows
   - Output: Feature backlog, TODO items

4. **Security gaps** (vulnerabilities)
   - Tool: SAST, dependency scanners
   - Find: Security vulnerabilities, unsafe code
   - Output: Security report, CVE list

Which type of gap analysis did you have in mind?"
```

### 5. "am I making sense?" (User Trigger)

**Ambiguity Score:** N/A (meta-question, not technical ambiguity)

**Intent:** User seeking validation of their explanation

**Response Pattern:**
```
"Let me verify I understand correctly. Based on your recent messages:

- [Summarize key point 1 from conversation]
- [Summarize key point 2 from conversation]
- [Summarize key point 3 from conversation]

I noticed some terminology that could be clarified:
- '[Ambiguous term 1]' - Did you mean [precise option A] or [precise option B]?
- '[Ambiguous term 2]' - This could refer to [technical concept X]

Does this match what you were trying to communicate?"
```

**Process:**
1. Analyze last 5-10 messages in conversation
2. Extract main points and intentions
3. Identify any ambiguous terminology used
4. Present summary + clarifying questions
5. Wait for user confirmation

## Generic Ambiguous Action Verbs

### "make it [X]"

Pattern of vague action verbs that need clarification:

| User Says | Likely Means | Domain Context | Clarification Needed |
|-----------|--------------|----------------|----------------------|
| "make it work" | Fix bug, implement feature, configure correctly | Any | What specifically isn't working? |
| "make it faster" | Optimize performance, reduce latency, cache | Performance | Which metric? Response time, throughput, etc. |
| "make it secure" | Add authentication, encryption, input validation | Security | Which security aspect? Auth, data protection, etc. |
| "make it pretty" | UI styling, UX improvements, visual design | Frontend | Specific elements or general styling? |
| "make it scalable" | Horizontal scaling, load balancing, optimization | Architecture | Expected scale? Concurrent users, data volume? |
| "make it better" | Improve (unspecified aspect) | Any | Better in what way? Performance, UX, reliability? |

**Standard Clarification:**
```
"'Make it [X]' is a bit general. Could you specify:
- What aspect needs to be [X]?
- What would [X] look like in concrete terms?
- Are there specific metrics or goals for [X]?"
```

## Domain-Specific Patterns

### Autogen-Specific Translations

#### Agent Creation Patterns

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "create an agent" | ConversableAgent instantiation | `ConversableAgent(name="...", system_message="...", llm_config={...})` |
| "agent with tools" | AssistantAgent with register_for_llm | `AssistantAgent(...)` + `@agent.register_for_llm()` |
| "human agent" | UserProxyAgent | `UserProxyAgent(human_input_mode="ALWAYS", ...)` |
| "manager agent" | GroupChatManager | `GroupChatManager(groupchat=...)` |

#### Communication Patterns

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "agent sends message" | send() method | `agent.send(message, recipient)` |
| "start conversation" | initiate_chat() | `agent.initiate_chat(recipient, message=...)` |
| "group discussion" | GroupChat | `GroupChat(agents=[...], ...)` + `manager.initiate_chat()` |
| "agent responds" | generate_reply() or receive() | Automatic in conversation loop |

#### Tool Integration

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "add a tool" | register_for_llm() decorator | `@assistant.register_for_llm()` |
| "execute function" | register_for_execution() | `@user_proxy.register_for_execution()` |
| "call external API" | Custom function + registration | Define function, register for both LLM and execution |

### Langroid-Specific Translations

#### Agent Creation

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "create agent" | ChatAgent instantiation | `ChatAgent(config=ChatAgentConfig(...))` |
| "agent with tools" | ToolAgent or @tool decorator | Define ToolMessage subclass or use @tool |
| "configure agent" | ChatAgentConfig | Set llm, vecdb, system_message in config |

#### Task Orchestration

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "run agent" | Task.run() | `task = Task(agent, ...)` + `task.run()` |
| "agent delegates" | add_subtask() | `parent_task.add_subtask(child_task)` |
| "multi-agent flow" | Task hierarchy | Parent task with multiple subtasks |
| "sequential agents" | Chain tasks | Task A → Task B → Task C via delegation |

#### Message Handling

| User Says | Precise Translation | Implementation |
|-----------|---------------------|----------------|
| "agent responds" | agent_response() | Override in custom agent |
| "LLM generates text" | llm_response() | Call llm.generate() or agent.llm_response() |
| "send message" | handle_message() | Pass message to agent.handle_message() |
| "tool call" | ToolMessage | Define ToolMessage subclass |

## Scope Ambiguities

### "add validation"

| Interpretation | Context | Implementation |
|----------------|---------|----------------|
| Input validation | User input, API parameters | Pydantic, Zod, JSON Schema |
| Business logic validation | Rules, constraints | Custom validation functions |
| Schema validation | Database, API contracts | ORM validators, OpenAPI |
| Type validation | Static typing | TypeScript, mypy, type hints |

### "improve performance"

| Interpretation | Metric | Approach |
|----------------|--------|----------|
| Reduce latency | Response time | Caching, optimize queries, async |
| Increase throughput | Requests/second | Load balancing, horizontal scaling |
| Reduce memory | Memory usage | Optimize data structures, streaming |
| Faster startup | Cold start time | Lazy loading, pre-compilation |

### "add logging"

| Interpretation | Scope | Implementation |
|----------------|-------|----------------|
| Debug logging | Development | Verbose logs, debug level |
| Application logging | Production monitoring | Structured logs, info level |
| Audit logging | Compliance, security | Immutable logs, audit trail |
| Performance logging | Metrics, tracing | APM tools, distributed tracing |

## Reference Ambiguities

### Unclear Antecedents

| User Says | Problem | Solution |
|-----------|---------|----------|
| "use that" | What does "that" refer to? | Ask: "Which component/variable?" |
| "like before" | Which previous instance? | Ask: "Like in which file/section?" |
| "the thing" | Non-specific reference | Ask: "Which specific thing?" |
| "it" (multiple possible referents) | Ambiguous pronoun | Ask: "Do you mean [A] or [B]?" |

### Generic Terms

| Generic Term | Needs Clarification | Ask |
|--------------|---------------------|-----|
| "component" | UI component? Module? Class? | "What kind of component?" |
| "service" | Backend service? API? Microservice? | "What type of service?" |
| "module" | Code module? npm package? Python module? | "What kind of module?" |
| "system" | Entire application? Subsystem? OS? | "Which system?" |

## Context Clues for Disambiguation

### Technical Signals

**Framework mentions:**
- "Autogen" → Use Autogen ontology
- "Langroid" → Use Langroid ontology
- "React" → Frontend context
- "FastAPI" → Python backend
- "Express" → Node.js backend

**Technology mentions:**
- "Docker" → Containerization context
- "Kubernetes" → Orchestration context
- "AWS/Azure/GCP" → Cloud context
- "PostgreSQL/MongoDB" → Database context

**Action verbs:**
- "deploy" → DevOps context
- "render" → Frontend context
- "query" → Database/API context
- "compile" → Build context

### Domain-Crossing Signals

**Mixed terminology indicates need for clarification:**
- Business + Technical: "customer agent" (CRM agent? AI agent?)
- Frontend + Backend: "API component" (API endpoint? API client component?)
- Infrastructure + Application: "service container" (Docker container? DI container?)

**Clarify domain before translating.**

## Translation Confidence Scoring

### High Confidence (> 0.8)

**Can translate directly with brief confirmation:**
- Clear domain context present
- User used framework-specific terminology
- Single viable interpretation
- Recent conversation provides context

**Example:**
```
User: "I'm using Autogen. How do I make the ConversableAgent send a message?"
→ HIGH confidence: send() method is the answer
→ Response: "Use agent.send(message, recipient). Like this: ..."
```

### Medium Confidence (0.5 - 0.8)

**Present 2-3 options, ranked:**
- Domain clear but term ambiguous within domain
- Multiple viable interpretations
- Context provides some hints

**Example:**
```
User: "In Autogen, how do I create an agent?"
→ MEDIUM confidence: Could be ConversableAgent, AssistantAgent, or UserProxyAgent
→ Response: "Depends on the agent's purpose:
   1. ConversableAgent (most common for chat)
   2. AssistantAgent (if you need tool calling)
   3. UserProxyAgent (if human-in-the-loop)
   Which type do you need?"
```

### Low Confidence (< 0.5)

**Ask open-ended clarification:**
- Domain unclear
- Term very generic
- Little context available

**Example:**
```
User: "How do I make it work?"
→ LOW confidence: No idea what "it" refers to or what "work" means
→ Response: "Could you provide more details?
   - What are you trying to accomplish?
   - What isn't working currently?
   - Which framework/technology are you using?"
```

## Clarification Templates by Confidence

### High Confidence Template

```
"[Technical term] is done using [precise implementation].

Example:
[code snippet]

Is this what you were looking for?"
```

### Medium Confidence Template

```
"[Ambiguous term] could mean a few things in [domain]:

1. **[Option 1]** - [Brief description]
   - Use case: [when to use]
   - Implementation: [technical term]

2. **[Option 2]** - [Brief description]
   - Use case: [when to use]
   - Implementation: [technical term]

3. **[Option 3]** - [Brief description]
   - Use case: [when to use]
   - Implementation: [technical term]

Which scenario matches your needs?"
```

### Low Confidence Template

```
"I want to make sure I understand correctly. Could you clarify:
- [Specific question 1]
- [Specific question 2]
- [Specific question 3]

This will help me provide accurate guidance."
```

## Summary

Use these translation patterns to:

1. **Quickly identify** common ambiguous terms
2. **Map to precise** technical concepts
3. **Determine confidence** level for translation
4. **Select appropriate** clarification template
5. **Present options** based on domain and context

The patterns catalog grows with usage - add new ambiguities as they're encountered.
