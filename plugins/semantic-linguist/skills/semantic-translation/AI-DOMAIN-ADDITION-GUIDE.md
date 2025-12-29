# AI Assistant Guide: Adding New Domains to Semantic-Linguist Knowledge Base

> **Audience:** This guide is written FOR AI Assistants who need to extend the semantic-linguist plugin with new domain knowledge.

**Purpose:** Systematic process for identifying domain-specific ambiguous terms, creating technical mappings, establishing conceptual relationships, and building decision trees for disambiguation.

---

## Table of Contents

1. [When to Add a New Domain](#when-to-add-a-new-domain)
2. [Step-by-Step Domain Addition Process](#step-by-step-domain-addition-process)
3. [Phase 1: Domain Analysis](#phase-1-domain-analysis)
4. [Phase 2: Ambiguous Terms Identification](#phase-2-ambiguous-terms-identification)
5. [Phase 3: Technical Mappings Creation](#phase-3-technical-mappings-creation)
6. [Phase 4: Ontology Graph Development](#phase-4-ontology-graph-development)
7. [Phase 5: Ambiguity Resolution](#phase-5-ambiguity-resolution)
8. [JSON Format Templates](#json-format-templates)
9. [Domain Classification Decision Trees](#domain-classification-decision-trees)
10. [Validation Checklist](#validation-checklist)

---

## When to Add a New Domain

Add a new domain when:
- User works in a specialized field not covered by existing domains
- Existing terms are frequently misinterpreted due to missing domain context
- New technology/framework becomes central to user's projects
- Cross-domain term conflicts emerge repeatedly

**Current domains covered:** Autogen, Langroid, MCP, UTCP, FastAPI, Git/Gitflow, SRE, Memory Graphs, General Software Engineering

---

## Step-by-Step Domain Addition Process

**Overview:** 5 phases, executed sequentially

1. **Domain Analysis** - Understand scope, terminology, frameworks
2. **Ambiguous Terms Identification** - Find multi-domain conflicts
3. **Technical Mappings Creation** - Document domain-specific translations
4. **Ontology Graph Development** - Model conceptual relationships
5. **Ambiguity Resolution** - Build decision trees for disambiguation

**Files Modified:**
- `skills/semantic-validation/knowledge/ambiguous-terms.json`
- `skills/semantic-validation/knowledge/technical-mappings.json`
- `skills/semantic-validation/knowledge/ontology-graph.json`

---

## Phase 1: Domain Analysis

**Goal:** Deeply understand the domain before adding it to the knowledge base.

### Analysis Steps

1. **Framework/Technology Identification**
   - What frameworks/libraries/tools define this domain?
   - What are the core abstractions?
   - What are the common operations?

2. **Terminology Inventory**
   - List domain-specific terms (20-30 key terms)
   - Identify overloaded terms (words with different meanings in different contexts)
   - Find synonyms (different words, same concept)

3. **Usage Pattern Analysis**
   - How do users typically phrase requests in this domain?
   - What are the most common user triggers? ("create X", "add Y", "configure Z")
   - What are typical ambiguities users encounter?

4. **Cross-Domain Relationship Mapping**
   - Which existing domains overlap with this new domain?
   - What concepts map across domains? (e.g., "tool" in Autogen vs MCP vs UTCP)
   - Where do conflicts arise?

**Example: Adding FastAPI Domain**

```markdown
Frameworks: FastAPI (Python web framework)
Core Abstractions: Application, PathOperation, Dependency, Pydantic models
Common Operations: Routing, validation, dependency injection, async operations

Key Terms:
- endpoint (ambiguous: API endpoint vs network endpoint vs path operation)
- dependency (ambiguous: Depends() vs package dependency vs architectural dependency)
- model (ambiguous: Pydantic model vs AI model vs database model)
- validation (ambiguous: Pydantic validation vs input validation vs business logic validation)

User Triggers:
- "create an api"
- "add validation"
- "define endpoint"
- "inject dependency"

Cross-Domain Overlaps:
- MCP: Both have "resource" concept (MCP resource vs REST resource)
- General: "API" is generic (FastAPI server vs general API design)
```

### Deliverable

**Domain Analysis Document** containing:
- Framework summary
- 20-30 key terms with ambiguity notes
- Common user phrases
- Cross-domain mappings

---

## Phase 2: Ambiguous Terms Identification

**Goal:** Identify terms that have different meanings in different domains and would cause user-AI miscommunication.

### Ambiguity Criteria

A term is ambiguous if:
- It appears in 2+ domains with different meanings
- Users frequently misstate it (meta-questions, vague phrasing)
- Context is required to determine correct interpretation
- Incorrect interpretation would lead to wrong implementation

### Ambiguity Score Calculation

**Formula:** `(number_of_domains × context_dependency) / 10`

- **number_of_domains**: How many distinct interpretations exist
- **context_dependency**: How much context is needed (1-5 scale)
  - 1: Clear from keyword alone
  - 3: Framework name provides clarity
  - 5: Requires deep conversation context

**Examples:**
- "agent" (Autogen, Langroid, general AI) → 3 domains × 3 context → 0.9 ambiguity
- "tool" (Autogen, Langroid, MCP, UTCP, CLI, general) → 6 domains × 4 context → 2.4 (capped at 1.0) → 1.0 ambiguity
- "merge" (Git, GitHub PR, Gitflow, data merge) → 4 domains × 4 context → 1.6 (capped at 1.0) → 0.8 ambiguity

**Normalization:** Cap at 1.0, round to 2 decimals

### Term Categories

Categorize each ambiguous term:

- **domain_specific**: Unique to one framework (e.g., "ConversableAgent" is Autogen-only)
- **multi_domain**: Appears in multiple domains with different meanings (e.g., "tool")
- **meta_question**: User uncertainty patterns (e.g., "making sense?", "is this right?")
- **vague_action_verb**: Non-specific verbs (e.g., "make it portable", "fix it")
- **infrastructure_type**: System component ambiguity (e.g., "server", "container")
- **knowledge_structure**: Data organization ambiguity (e.g., "memory", "graph")
- **git_operation**: Version control operations (e.g., "merge", "rebase")
- **sre_concept**: Reliability/observability terms (e.g., "observability", "SLI")

### Ambiguous Terms JSON Structure

```json
{
  "term": {
    "ambiguity_score": 0.75,
    "category": "multi_domain",
    "contexts": ["domain1", "domain2", "domain3"],
    "user_triggers": ["phrase user might say 1", "phrase user might say 2"],
    "domains": {
      "domain1": ["meaning1 in domain1", "meaning2 in domain1"],
      "domain2": {
        "types": ["subtype1", "subtype2"],
        "patterns": ["pattern1", "pattern2"]
      },
      "domain3": "simple string meaning"
    },
    "clarification_needed": ["Question 1?", "Question 2?"]
  }
}
```

### Deliverable

**Add entries to `ambiguous-terms.json`** for each identified ambiguous term.

**Checklist per term:**
- [ ] Ambiguity score calculated (0.0-1.0)
- [ ] Category assigned
- [ ] Contexts listed (all applicable domains)
- [ ] User triggers documented (3-5 common phrases)
- [ ] Domain-specific meanings detailed
- [ ] Clarification questions formulated (2-4 questions)

---

## Phase 3: Technical Mappings Creation

**Goal:** Document domain-specific technical translations for each concept, operation, and pattern.

### Mapping Structure

Organize by domain → subcategory → concept → details

**Example Pattern:**

```json
{
  "new_domain": {
    "subcategory_1": {
      "concept_name": {
        "purpose": "What this does",
        "use_cases": ["when to use 1", "when to use 2"],
        "pattern": "How it works / typical usage pattern",
        "signature": "Code signature or invocation pattern",
        "tools": ["tool1", "tool2"],
        "similar_to": {
          "other_domain": "equivalent concept in other domain"
        }
      }
    }
  }
}
```

### Subcategory Guidelines

Choose subcategories that reflect domain structure:
- **Frameworks:** Agent creation, communication, tool integration
- **APIs:** Routing, validation, authentication, async operations
- **Version Control:** Core operations, workflows, collaboration
- **SRE:** Observability, reliability, incident management
- **Memory Systems:** Graph types, storage patterns, retrieval patterns

**Rule:** 3-6 subcategories per domain, each with 3-10 concepts

### Technical Mapping JSON Template

```json
{
  "domain_name": {
    "subcategory_name": {
      "ConceptName": {
        "purpose": "Brief description (1 sentence)",
        "use_cases": ["use case 1", "use case 2", "use case 3"],
        "pattern": "Typical usage pattern or workflow",
        "signature": "Code signature, command syntax, or invocation format",
        "components": ["component1", "component2"],
        "tools": ["tool1", "tool2"],
        "similar_to": {
          "domain1": "equivalent in domain1",
          "domain2": "equivalent in domain2"
        }
      }
    }
  }
}
```

### Cross-Domain Equivalents Section

**Always update `cross_domain_equivalents`** when adding a new domain.

Map concepts that exist across multiple domains:

```json
{
  "cross_domain_equivalents": {
    "concept_name": {
      "autogen": "Autogen equivalent",
      "langroid": "Langroid equivalent",
      "new_domain": "New domain equivalent",
      "general": "General term"
    }
  }
}
```

**Examples:**
- `tool_agent`: Maps AssistantAgent (Autogen) ↔ ToolAgent (Langroid) ↔ MCP client with tools ↔ UTCP-enabled agent
- `data_source`: Maps MCP Resource ↔ FastAPI endpoint ↔ general data retrieval mechanism

### Deliverable

**Add section to `technical-mappings.json`** with comprehensive domain translations.

**Checklist:**
- [ ] Domain section created with 3-6 subcategories
- [ ] Each subcategory has 3-10 concepts fully documented
- [ ] Cross-domain equivalents updated
- [ ] Similar concepts from other domains referenced
- [ ] Code signatures/patterns provided for technical precision

---

## Phase 4: Ontology Graph Development

**Goal:** Model conceptual relationships, hierarchies, and cross-domain connections.

### Ontology Components

1. **Domain-Specific Classes/Concepts**
   - Type classification (abstract_base, concrete_class, pattern, component, etc.)
   - Parent-child relationships (inheritance, specialization)
   - Relationship modeling (IS_A, HAS_A, USES, PROVIDES, ENABLES, etc.)
   - Cross-domain equivalents

2. **Conceptual Relationships**
   - Abstract concepts that span domains (e.g., "tool_use", "orchestration", "observability")
   - Implementation variations across domains
   - Integration points

3. **Ambiguity Resolution Graph**
   - Disambiguation questions
   - Decision trees for choosing correct interpretation

### Domain Ontology JSON Template

```json
{
  "domain_name": {
    "ConceptName": {
      "type": "concrete_class | abstract_base | pattern | component | orchestration_object",
      "parent": "ParentConcept (if applicable)",
      "children": ["ChildConcept1", "ChildConcept2"],
      "purpose": "What this concept represents",
      "relationships": {
        "IS_A": "parent or abstraction",
        "HAS_A": ["attribute1", "attribute2"],
        "CAN_DO": ["capability1", "capability2"],
        "USES": "dependencies",
        "PROVIDES": "what it offers",
        "ENABLES": "what it makes possible",
        "INTEGRATES_WITH": ["integration1", "integration2"],
        "SIMILAR_TO": {
          "other_domain": "equivalent concept"
        }
      },
      "cross_domain_equivalent": {
        "domain1": "equivalent1",
        "domain2": "equivalent2",
        "general": "general term"
      }
    }
  }
}
```

### Relationship Types

Use precise relationship types:
- **IS_A**: Inheritance/specialization (AssistantAgent IS_A ConversableAgent)
- **HAS_A**: Composition/attributes (Agent HAS_A llm_config)
- **CAN_DO**: Capabilities/methods (Agent CAN_DO send, receive)
- **USES**: Dependencies (ToolAgent USES ToolMessage)
- **PROVIDES**: What it offers (MCP Server PROVIDES tools to clients)
- **ENABLES**: What it makes possible (GroupChat ENABLES multi-party conversation)
- **INTEGRATES_WITH**: External integrations (AssistantAgent INTEGRATES_WITH MCP tools)
- **SIMILAR_TO**: Cross-domain equivalents (for disambiguation)

### Conceptual Relationships Template

Add abstract concepts that the new domain implements:

```json
{
  "conceptual_relationships": {
    "new_abstract_concept": {
      "abstract_concept": "High-level description",
      "patterns": {
        "pattern1": "Description",
        "pattern2": "Description"
      },
      "implementations": {
        "domain1": "How domain1 implements this",
        "new_domain": "How new domain implements this",
        "general": "General approach"
      },
      "enables": {
        "capability1": "What it enables",
        "capability2": "What it enables"
      }
    }
  }
}
```

**Examples of Abstract Concepts:**
- `tool_use`: How different frameworks enable function calling
- `orchestration`: How multiple agents/tasks are coordinated
- `data_validation`: How data correctness is ensured
- `knowledge_retrieval`: How information is found and retrieved

### Deliverable

**Add to `ontology-graph.json`:**
1. Domain-specific ontology section with all major concepts
2. New conceptual relationships (if domain introduces new abstract patterns)
3. Updates to existing conceptual relationships (new implementation examples)

**Checklist:**
- [ ] All major domain concepts modeled with relationships
- [ ] Type classifications accurate (class, pattern, component, etc.)
- [ ] Parent-child hierarchies established
- [ ] Cross-domain equivalents mapped
- [ ] At least 1 new conceptual relationship added (if applicable)
- [ ] Existing conceptual relationships updated with new domain examples

---

## Phase 5: Ambiguity Resolution

**Goal:** Build decision trees to guide disambiguation when ambiguous terms are detected.

### Decision Tree Structure

For each major ambiguous term in the new domain, create a decision tree:

```json
{
  "ambiguity_resolution_graph": {
    "ambiguous_term": {
      "disambiguation_questions": [
        "Question 1 to narrow context?",
        "Question 2 to identify domain?",
        "Question 3 to determine specific variant?"
      ],
      "decision_tree": {
        "dimension1": {
          "option1": "Interpretation for option1",
          "option2": {
            "sub_option1": "Specific interpretation",
            "sub_option2": "Another specific interpretation"
          }
        },
        "dimension2": {
          "case1": "domain1 approach",
          "case2": "domain2 approach",
          "case3": "new_domain approach"
        }
      }
    }
  }
}
```

### Question Formulation Guidelines

**Good disambiguation questions:**
- Narrow scope quickly (framework, domain, purpose)
- Ask about concrete artifacts ("What operation?", "What kind of server?")
- Avoid vague questions ("What do you want?")

**Examples:**
- "Which framework? (Autogen, Langroid, MCP)"
- "What type of memory? (episodic, semantic, vector)"
- "What operations? (routing, validation, authentication)"
- "For humans or AI agents?"

### Decision Tree Best Practices

1. **Start broad, narrow progressively**
   - First level: Framework/domain identification
   - Second level: Concept category
   - Third level: Specific variant

2. **Include all domains where term appears**
   - Even if new domain doesn't use this term, update existing decision trees to acknowledge the new domain

3. **Provide concrete outcomes**
   - Terminal nodes should be specific implementations, not vague categories
   - Include code patterns or command syntax where applicable

**Example Decision Tree:**

```json
{
  "tool": {
    "disambiguation_questions": [
      "Which framework?",
      "What should the tool do?",
      "Is it for AI agents or general use?"
    ],
    "decision_tree": {
      "framework": {
        "autogen": "register_for_llm() + register_for_execution()",
        "langroid": "ToolMessage subclass",
        "mcp": "MCP server with tool schema",
        "utcp": "Universal tool schema + adapters",
        "new_domain": "New domain tool pattern"
      },
      "purpose": {
        "ai_agents": "MCP or UTCP tool",
        "general_automation": "CLI tool or script"
      }
    }
  }
}
```

### Deliverable

**Update `ambiguity_resolution_graph` in `ontology-graph.json`:**
1. Add decision trees for new ambiguous terms from new domain
2. Update existing decision trees to include new domain options

**Checklist:**
- [ ] 3-5 disambiguation questions per ambiguous term
- [ ] Decision trees cover all domain variants
- [ ] Outcomes are concrete and actionable
- [ ] Existing decision trees updated with new domain

---

## JSON Format Templates

### Complete Template: Adding "NewDomain"

#### 1. ambiguous-terms.json

```json
{
  "new_ambiguous_term": {
    "ambiguity_score": 0.72,
    "category": "multi_domain",
    "contexts": ["new_domain", "existing_domain", "general"],
    "user_triggers": ["user phrase 1", "user phrase 2", "user phrase 3"],
    "domains": {
      "new_domain": {
        "types": ["type1", "type2"],
        "patterns": ["pattern1", "pattern2"],
        "use_cases": ["use_case1", "use_case2"]
      },
      "existing_domain": ["meaning in existing domain"],
      "general": "general meaning"
    },
    "clarification_needed": [
      "Which domain applies? (new_domain, existing_domain, general)",
      "What specific type? (type1, type2)",
      "What's the use case?"
    ]
  }
}
```

#### 2. technical-mappings.json

```json
{
  "new_domain": {
    "subcategory1": {
      "Concept1": {
        "purpose": "What this concept does",
        "use_cases": ["use_case1", "use_case2"],
        "pattern": "Typical usage pattern",
        "signature": "Code signature or command syntax",
        "components": ["component1", "component2"],
        "tools": ["tool1", "tool2"],
        "similar_to": {
          "existing_domain": "equivalent concept"
        }
      }
    },
    "subcategory2": {
      "Concept2": {
        "purpose": "What this does",
        "types": {
          "type1": "Description of type1",
          "type2": "Description of type2"
        },
        "workflow": "Step1 → Step2 → Step3",
        "examples": ["example1", "example2"]
      }
    }
  },
  "cross_domain_equivalents": {
    "shared_concept": {
      "existing_domain": "Existing implementation",
      "new_domain": "New domain implementation",
      "general": "General term"
    }
  }
}
```

#### 3. ontology-graph.json

```json
{
  "new_domain": {
    "CoreConcept": {
      "type": "concrete_class",
      "parent": "AbstractBase (if applicable)",
      "children": ["SpecializedConcept1", "SpecializedConcept2"],
      "purpose": "What this represents",
      "relationships": {
        "IS_A": "parent class or abstraction",
        "HAS_A": ["attribute1", "attribute2"],
        "CAN_DO": ["operation1", "operation2"],
        "PROVIDES": ["service1", "service2"],
        "INTEGRATES_WITH": {
          "existing_domain": "integration point"
        }
      },
      "cross_domain_equivalent": {
        "existing_domain": "Equivalent concept",
        "general": "General term"
      }
    }
  },
  "conceptual_relationships": {
    "new_abstract_concept": {
      "abstract_concept": "High-level description",
      "patterns": {
        "pattern1": "Pattern description",
        "pattern2": "Pattern description"
      },
      "implementations": {
        "existing_domain": "Existing implementation",
        "new_domain": "New domain implementation",
        "general": "General approach"
      }
    }
  },
  "ambiguity_resolution_graph": {
    "ambiguous_term": {
      "disambiguation_questions": [
        "Question 1?",
        "Question 2?",
        "Question 3?"
      ],
      "decision_tree": {
        "dimension1": {
          "option1": "new_domain interpretation",
          "option2": "existing_domain interpretation"
        }
      }
    }
  }
}
```

---

## Domain Classification Decision Trees

### Decision Tree 1: Is This a New Domain or Extension?

```
User mentions new technology/framework
│
├─ Does this framework exist in knowledge base?
│  ├─ YES → EXTEND existing domain
│  └─ NO → Check if it's a subdomain or truly new
│     │
│     ├─ Is it a variant of existing domain?
│     │  ├─ YES (e.g., FastAPI variant of general Python web)
│     │  │   → CREATE new domain section (FastAPI is distinct enough)
│     │  └─ NO → CREATE new domain section
│     │
│     └─ Does it introduce fundamentally new concepts?
│        ├─ YES → CREATE new domain with new conceptual relationships
│        └─ NO → EXTEND closest existing domain
```

**Example:**
- **FastAPI** → New domain (distinct from Flask/Django, introduces dependency injection patterns)
- **Strawberry GraphQL** → Extend existing GraphQL/API domain (not fundamentally different)
- **UTCP** → New domain (introduces universal tool calling abstraction)

### Decision Tree 2: Ambiguity Score Assignment

```
Term appears in conversation
│
├─ In how many domains does it have different meanings?
│  ├─ 1 domain → NOT ambiguous, don't add
│  ├─ 2-3 domains → Calculate: (2-3 × context_dependency) / 10
│  └─ 4+ domains → Calculate: (4+ × context_dependency) / 10, cap at 1.0
│
└─ How much context is needed to disambiguate?
   ├─ Keyword alone is clear → context_dependency = 1
   ├─ Framework name provides clarity → context_dependency = 3
   ├─ Requires understanding of operation → context_dependency = 4
   └─ Needs deep conversation context → context_dependency = 5
```

**Example Calculations:**
- "endpoint" (FastAPI vs MCP vs network) → 3 domains × 3 context = 0.9
- "validation" (FastAPI Pydantic vs input vs business logic) → 3 domains × 4 context = 1.2 → cap at 1.0
- "server" (MCP server vs web server vs general) → 3 domains × 2 context = 0.6

### Decision Tree 3: Category Assignment

```
Ambiguous term identified
│
├─ Is it unique to ONE framework with specific implementation?
│  └─ YES → category: "domain_specific"
│
├─ Does it appear in MULTIPLE domains with different meanings?
│  └─ YES → category: "multi_domain"
│
├─ Is it a meta-question pattern (e.g., "making sense?", "is this right?")?
│  └─ YES → category: "meta_question"
│
├─ Is it a vague action verb (e.g., "make it X", "fix it")?
│  └─ YES → category: "vague_action_verb"
│
├─ Is it about system infrastructure (server, container, cluster)?
│  └─ YES → category: "infrastructure_type"
│
├─ Is it about data/knowledge organization (memory, graph, database)?
│  └─ YES → category: "knowledge_structure"
│
├─ Is it a version control operation (merge, rebase, commit, branch)?
│  └─ YES → category: "git_operation"
│
└─ Is it an SRE/observability concept (logs, metrics, SLI, observability)?
   └─ YES → category: "sre_concept"
```

### Decision Tree 4: Subcategory Organization

```
Creating technical mappings for new domain
│
├─ What type of domain is this?
│  │
│  ├─ AI Framework (Autogen, Langroid)
│  │  → Subcategories: agent_creation, communication, tool_integration, orchestration
│  │
│  ├─ Protocol (MCP, UTCP)
│  │  → Subcategories: server_types, components, integration_patterns, protocol_components
│  │
│  ├─ Web Framework (FastAPI)
│  │  → Subcategories: routing, dependency_injection, validation, async_operations
│  │
│  ├─ Version Control (Git, Gitflow)
│  │  → Subcategories: core_operations, workflows, collaboration, branching_patterns
│  │
│  ├─ SRE/Observability
│  │  → Subcategories: observability, reliability_patterns, incident_management
│  │
│  └─ Memory/Knowledge Systems
│     → Subcategories: graph_types, storage_patterns, retrieval_patterns
```

---

## Validation Checklist

Before finalizing domain addition, verify:

### Phase 1: Domain Analysis
- [ ] Framework/technology clearly identified
- [ ] 20-30 key terms inventoried
- [ ] Common user phrases documented
- [ ] Cross-domain overlaps mapped

### Phase 2: Ambiguous Terms
- [ ] All ambiguous terms identified (10-20 per domain typical)
- [ ] Ambiguity scores calculated correctly (0.0-1.0)
- [ ] Categories assigned appropriately
- [ ] User triggers documented (3-5 per term)
- [ ] Domain-specific meanings detailed
- [ ] Clarification questions formulated (2-4 per term)
- [ ] Entries added to `ambiguous-terms.json`

### Phase 3: Technical Mappings
- [ ] Domain section created with 3-6 subcategories
- [ ] Each subcategory has 3-10 concepts
- [ ] All concepts have: purpose, use_cases, pattern/signature
- [ ] Cross-domain equivalents updated
- [ ] Similar concepts from other domains referenced
- [ ] Entries added to `technical-mappings.json`

### Phase 4: Ontology Graph
- [ ] 5-10 major domain concepts modeled
- [ ] Type classifications correct (class, pattern, component, etc.)
- [ ] Relationships comprehensive (IS_A, HAS_A, CAN_DO, etc.)
- [ ] Cross-domain equivalents mapped
- [ ] At least 1 new conceptual relationship added (if applicable)
- [ ] Existing conceptual relationships updated
- [ ] Entries added to `ontology-graph.json`

### Phase 5: Ambiguity Resolution
- [ ] Decision trees created for 3-5 key ambiguous terms
- [ ] 3-5 disambiguation questions per tree
- [ ] All domain variants covered in decision trees
- [ ] Outcomes are concrete and actionable
- [ ] Existing decision trees updated with new domain
- [ ] Entries added to `ambiguity_resolution_graph` in `ontology-graph.json`

### Cross-Cutting Validation
- [ ] All JSON files are valid (no syntax errors)
- [ ] Cross-references between files are consistent
- [ ] Domain name used consistently across all files
- [ ] No duplicate entries
- [ ] Formatting follows existing patterns

---

## Example Workflow: Adding "Kubernetes" Domain

### Step 1: Domain Analysis

```markdown
**Framework:** Kubernetes (container orchestration)

**Core Abstractions:**
- Pod (smallest deployable unit)
- Service (network abstraction)
- Deployment (declarative updates)
- ConfigMap/Secret (configuration management)
- Namespace (resource isolation)

**Key Terms (partial list):**
- "pod" (ambiguous: Kubernetes pod vs podcast vs seed pod)
- "service" (ambiguous: Kubernetes Service vs general service vs MCP server)
- "deployment" (ambiguous: Kubernetes Deployment vs general deployment vs software release)
- "container" (ambiguous: Kubernetes container vs Docker container vs general containerization)
- "namespace" (ambiguous: Kubernetes namespace vs programming namespace vs DNS namespace)

**User Triggers:**
- "create a pod"
- "deploy to kubernetes"
- "configure service"
- "add namespace"

**Cross-Domain Overlaps:**
- General Software Engineering: "service", "container", "deployment"
- SRE: "observability", "health checks", "scaling"
```

### Step 2: Ambiguous Terms Identification

```json
{
  "pod": {
    "ambiguity_score": 0.72,
    "category": "multi_domain",
    "contexts": ["kubernetes", "general", "biology"],
    "user_triggers": ["create a pod", "deploy pod", "pod configuration"],
    "domains": {
      "kubernetes": {
        "definition": "Smallest deployable unit in Kubernetes",
        "contains": ["one or more containers", "shared storage", "network"],
        "lifecycle": "created, running, succeeded, failed, unknown"
      },
      "general": ["podcast", "group of whales/dolphins"],
      "biology": "seed pod"
    },
    "clarification_needed": [
      "Are you working with Kubernetes?",
      "Do you mean Kubernetes pod or something else?",
      "What should the pod contain? (containers, config)"
    ]
  },
  "service": {
    "ambiguity_score": 0.85,
    "category": "multi_domain",
    "contexts": ["kubernetes", "mcp", "general", "microservices"],
    "user_triggers": ["create service", "expose service", "service configuration"],
    "domains": {
      "kubernetes": {
        "types": ["ClusterIP", "NodePort", "LoadBalancer", "ExternalName"],
        "purpose": "Abstract way to expose pods as network service"
      },
      "mcp": "MCP server providing tools/resources",
      "microservices": "Independent deployable service",
      "general": "General software service or daemon"
    },
    "clarification_needed": [
      "Kubernetes Service, MCP server, or general service?",
      "What type of Kubernetes Service? (ClusterIP, NodePort, LoadBalancer)",
      "What should the service expose?"
    ]
  }
}
```

### Step 3: Technical Mappings

```json
{
  "kubernetes": {
    "workload_resources": {
      "Pod": {
        "purpose": "Smallest deployable unit in Kubernetes",
        "use_cases": ["run single container", "run tightly coupled containers", "sidecar pattern"],
        "pattern": "Declarative YAML definition → kubectl apply → scheduler assigns to node",
        "signature": "apiVersion: v1, kind: Pod, metadata, spec",
        "components": ["containers", "volumes", "init containers (optional)"],
        "lifecycle_states": ["Pending", "Running", "Succeeded", "Failed", "Unknown"]
      },
      "Deployment": {
        "purpose": "Declarative updates for Pods and ReplicaSets",
        "use_cases": ["rolling updates", "rollbacks", "scaling"],
        "pattern": "Desired state → Deployment controller → create/update Pods",
        "signature": "apiVersion: apps/v1, kind: Deployment, spec.replicas, spec.template",
        "features": ["rolling updates", "rollback", "pause/resume", "scaling"]
      }
    },
    "networking": {
      "Service": {
        "purpose": "Abstract way to expose Pods as network service",
        "types": {
          "ClusterIP": "Internal cluster IP (default)",
          "NodePort": "Expose on each Node's IP at static port",
          "LoadBalancer": "Cloud provider load balancer",
          "ExternalName": "Map to DNS name"
        },
        "pattern": "Label selector → match Pods → expose via service",
        "signature": "apiVersion: v1, kind: Service, spec.type, spec.selector"
      }
    }
  },
  "cross_domain_equivalents": {
    "container_unit": {
      "kubernetes": "Pod (one or more containers)",
      "docker": "Single container",
      "general": "Containerization"
    },
    "service_abstraction": {
      "kubernetes": "Kubernetes Service",
      "mcp": "MCP server",
      "microservices": "Microservice",
      "general": "Network service"
    }
  }
}
```

### Step 4: Ontology Graph

```json
{
  "kubernetes": {
    "Pod": {
      "type": "workload_resource",
      "purpose": "Smallest deployable unit",
      "relationships": {
        "IS_A": "Kubernetes resource",
        "HAS_A": ["containers", "volumes", "metadata"],
        "MANAGED_BY": "kubelet on node",
        "EXPOSED_BY": "Service",
        "CREATED_BY": ["Deployment", "StatefulSet", "DaemonSet", "Job"],
        "INTEGRATES_WITH": {
          "sre": "Pod metrics and logs for observability"
        }
      },
      "cross_domain_equivalent": {
        "docker": "Container",
        "general": "Application instance"
      }
    },
    "Service": {
      "type": "networking_resource",
      "purpose": "Expose Pods as network service",
      "relationships": {
        "IS_A": "Kubernetes resource",
        "HAS_A": ["selector", "ports", "type"],
        "EXPOSES": "Pods (via label selector)",
        "TYPES": ["ClusterIP", "NodePort", "LoadBalancer", "ExternalName"],
        "SIMILAR_TO": {
          "mcp": "MCP server (both expose functionality)",
          "microservices": "Service mesh entry point"
        }
      },
      "cross_domain_equivalent": {
        "mcp": "MCP server",
        "general": "Network service abstraction"
      }
    }
  },
  "conceptual_relationships": {
    "container_orchestration": {
      "abstract_concept": "Automate deployment, scaling, and management of containers",
      "patterns": {
        "declarative": "Describe desired state, system ensures it",
        "imperative": "Execute specific commands",
        "self_healing": "Restart failed containers, reschedule"
      },
      "implementations": {
        "kubernetes": "Declarative YAML, controllers maintain desired state",
        "docker_swarm": "Docker native orchestration",
        "general": "Container management platforms"
      },
      "enables": {
        "scaling": "Horizontal pod autoscaling",
        "high_availability": "Replica sets, health checks",
        "rolling_updates": "Zero-downtime deployments"
      }
    }
  },
  "ambiguity_resolution_graph": {
    "service": {
      "disambiguation_questions": [
        "Are you working with Kubernetes?",
        "Kubernetes Service, MCP server, microservice, or general service?",
        "What type of Kubernetes Service? (ClusterIP, NodePort, LoadBalancer)"
      ],
      "decision_tree": {
        "platform": {
          "kubernetes": {
            "ClusterIP": "Internal cluster service",
            "NodePort": "Expose on node port",
            "LoadBalancer": "Cloud load balancer",
            "ExternalName": "DNS CNAME mapping"
          },
          "mcp": "MCP server with tools/resources",
          "microservices": "Independent deployable service",
          "general": "Software service or daemon"
        }
      }
    },
    "pod": {
      "disambiguation_questions": [
        "Kubernetes pod or something else?",
        "What containers should it run?",
        "How should it be exposed?"
      ],
      "decision_tree": {
        "context": {
          "kubernetes": "Kubernetes Pod resource",
          "general": "Podcast or group (non-technical)",
          "biology": "Seed pod (non-technical)"
        }
      }
    }
  }
}
```

---

## Best Practices

1. **Start Small, Iterate**
   - Add 10-15 ambiguous terms initially
   - Expand based on actual user confusion patterns
   - Don't try to be exhaustive on first pass

2. **Focus on High-Impact Terms**
   - Prioritize terms that cause frequent miscommunication
   - Terms with ambiguity score > 0.7 are critical
   - Terms with 3+ domain meanings need immediate disambiguation

3. **Maintain Consistency**
   - Use same naming conventions across all files
   - Keep structure parallel to existing domains
   - Follow JSON formatting of existing entries

4. **Test Decision Trees**
   - Mentally walk through user conversations
   - Ensure decision trees cover common paths
   - Validate that outcomes are specific enough to implement

5. **Update Incrementally**
   - Don't update all 3 files at once
   - Phase 2 → Phase 3 → Phase 4 → Phase 5 sequentially
   - Validate each file after modification

6. **Document Rationale**
   - Leave comments (if JSON supports) or separate notes on why scores/categories were chosen
   - Document unusual mappings or non-obvious cross-domain equivalents

---

## Common Pitfalls

**Pitfall 1: Over-Ambitious First Pass**
- **Problem:** Trying to add 50+ terms for a new domain in one go
- **Solution:** Start with 10-15 highest-impact terms, expand iteratively

**Pitfall 2: Ambiguity Score Inconsistency**
- **Problem:** Different scoring logic for different terms
- **Solution:** Always use formula: `(domains × context_dependency) / 10`, cap at 1.0

**Pitfall 3: Vague Decision Tree Outcomes**
- **Problem:** Decision tree ends with "use appropriate method" (not actionable)
- **Solution:** Outcomes must be concrete: "ConversableAgent", "git merge --no-ff", "Pydantic model validation"

**Pitfall 4: Missing Cross-Domain Updates**
- **Problem:** Adding new domain but not updating `cross_domain_equivalents` section
- **Solution:** Always check if new concepts map to existing concepts in other domains

**Pitfall 5: Incomplete Relationship Modeling**
- **Problem:** Only modeling IS_A relationships, ignoring HAS_A, USES, PROVIDES
- **Solution:** Use full relationship vocabulary to capture nuanced connections

---

## Conclusion

Adding a new domain requires systematic analysis across 5 phases:
1. **Domain Analysis** - Understand the domain deeply
2. **Ambiguous Terms Identification** - Find multi-domain conflicts
3. **Technical Mappings Creation** - Document domain-specific translations
4. **Ontology Graph Development** - Model conceptual relationships
5. **Ambiguity Resolution** - Build decision trees for disambiguation

Follow the templates, validate at each phase, and iterate based on real user confusion patterns.

**Key Success Metric:** Reduction in user meta-questions ("making sense?") and clarification rounds after domain addition.
