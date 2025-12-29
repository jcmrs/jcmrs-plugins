# Decision Trees for Semantic Validation

Detailed decision trees and flowcharts for systematic semantic validation and ambiguity resolution.

## Overview

These decision trees provide step-by-step guidance for analyzing user messages, detecting ambiguities, querying knowledge sources, and engaging in clarification dialogues. Use these trees to make systematic decisions during semantic validation.

## Master Decision Tree

```
┌─────────────────────────────────┐
│   User Message Received         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Initial Message Analysis        │
│ - Extract key terms             │
│ - Identify domain signals       │
│ - Detect action verbs           │
│ - Note scope indicators         │
└────────────┬────────────────────┘
             │
             ▼
        ┌────┴─────┐
        │ Contains │
        │meta-ques │ Yes ─────────┐
        │ tion?    │              │
        └────┬─────┘              │
             │No                  │
             ▼                    ▼
    ┌────────────────┐  ┌──────────────────┐
    │ Contains       │  │ HIGH Confidence  │
    │ ambiguous      │  │ Ambiguity        │
    │ action verb?   │  │ - "am I making   │
    └────┬───────────┘  │   sense?"        │
         │              │ - "does this     │
         │              │   make sense?"   │
         ▼              │ - "non-technical │
    ┌────┴─────┐       │   user"          │
    │   Yes    │       └────────┬─────────┘
    └────┬─────┘                │
         │                       │
         │                       ▼
         │              ┌──────────────────┐
         │              │ VALIDATE         │
         │              │ IMMEDIATELY      │
         │              │ - Query last     │
         │              │   5-10 messages  │
         │              │ - Identify       │
         │              │   ambiguities    │
         │              │ - Ask            │
         │              │   clarifying     │
         │              │   questions      │
         │              └─────────────────┘
         │
         ▼
┌────────────────────────┐
│ Analyze action verb    │
│ - "make it talk"       │
│ - "create api"         │
│ - "check for gaps"     │
│ - "make it portable"   │
└────────┬───────────────┘
         │
         ▼
    ┌────┴─────┐
    │ Domain   │  Yes ─────────┐
    │ context  │               │
    │ clear?   │               ▼
    └────┬─────┘     ┌──────────────────┐
         │No          │ Query Knowledge  │
         │            │ - Static domain  │
         │            │   knowledge      │
         │            │ - Technical      │
         │            │   mappings       │
         │            │ - Ontology       │
         │            │   graph          │
         │            └────────┬─────────┘
         │                     │
         ▼                     ▼
┌────────────────┐    ┌───────────────────┐
│ ASK: Which     │    │ Translation       │
│ framework/     │    │ found?            │
│ library are    │    └────────┬──────────┘
│ you using?     │             │
└────────────────┘             ▼
                      ┌────────┴─────┐
                      │  Multiple    │  Yes ──┐
                      │translations? │        │
                      └────────┬─────┘        │
                               │No             │
                               │               ▼
                               │     ┌──────────────────┐
                               │     │ Present Options  │
                               │     │ - List all       │
                               │     │ - Rank by        │
                               │     │   confidence     │
                               │     │ - Provide        │
                               │     │   context        │
                               │     └────────┬─────────┘
                               │              │
                               │              ▼
                               │     ┌──────────────────┐
                               │     │ User Selects     │
                               ▼     └────────┬─────────┘
                      ┌──────────────────┐    │
                      │ Confirm with     │◄───┘
                      │ User             │
                      │ "Did you mean    │
                      │  [technical      │
                      │   term]?"        │
                      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ User Confirms    │
                      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ Proceed with     │
                      │ Validated        │
                      │ Terminology      │
                      └──────────────────┘
```

## Ambiguity Detection Decision Tree

```
┌─────────────────────────────────┐
│ Analyze User Message            │
│ for Ambiguity Signals           │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Pattern Matching                      │
│ Check against known patterns:         │
│ 1. Meta-questions                     │
│ 2. Vague action verbs                 │
│ 3. Unclear scope                      │
│ 4. Domain confusion                   │
│ 5. Invented terms                     │
│ 6. Unclear references                 │
└────────────┬─────────────────────────┘
             │
             ▼
        ┌────┴─────┐
        │ Pattern  │  No ──────────┐
        │ detected?│               │
        └────┬─────┘               │
             │Yes                  │
             ▼                     ▼
┌─────────────────────┐  ┌──────────────┐
│ Calculate           │  │ LOW          │
│ Confidence Score    │  │ Confidence   │
│ - Pattern strength  │  │ < 30%        │
│ - Context clarity   │  │              │
│ - Domain signals    │  │ Monitor but  │
│ - Reference clarity │  │ don't        │
└────────┬────────────┘  │ interrupt    │
         │               └──────────────┘
         ▼
    ┌────┴─────┐
    │Confidence│
    │  score?  │
    └────┬─────┘
         │
   ┌─────┼─────┬─────────┐
   │     │     │         │
   │     │     │         │
 >80%  50-80% 30-50%   <30%
   │     │     │         │
   │     │     │         │
   ▼     ▼     ▼         ▼
┌────┐┌────┐┌────┐  ┌────────┐
│HIGH││MED ││LOW │  │IGNORE  │
└──┬─┘└──┬─┘└──┬─┘  └────────┘
   │     │     │
   │     │     │
   ▼     ▼     ▼
┌──────────────────────────┐
│ VALIDATE                 │
│ IMMEDIATELY              │
│ - No questions asked     │
│ - Trigger validation     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ VALIDATE IF              │
│ MULTIPLE                 │
│ INTERPRETATIONS          │
│ - Check knowledge        │
│ - If >1 option, validate │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ MONITOR                  │
│ - Watch for additional   │
│   signals                │
│ - May validate if        │
│   combined with other    │
│   ambiguities            │
└──────────────────────────┘
```

## Knowledge Query Decision Tree

```
┌─────────────────────────────────┐
│ Ambiguity Detected              │
│ Need to translate to precise    │
│ technical terminology           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ QUERY 1: Static Knowledge       │
│ Fastest, always available       │
│                                  │
│ Check:                           │
│ - knowledge/ambiguous-terms.json │
│ - knowledge/technical-mappings   │
│   .json                          │
│ - knowledge/ontology-graph.json  │
└────────────┬────────────────────┘
             │
             ▼
        ┌────┴─────┐
        │ Found?   │  Yes ─────────┐
        │          │               │
        └────┬─────┘               │
             │No                   │
             │                     ▼
             │           ┌──────────────────┐
             │           │ Sufficient?      │
             │           └────────┬─────────┘
             │                    │
             │                ┌───┴───┐
             │                │       │
             │               Yes      No
             │                │       │
             ▼                │       ▼
┌─────────────────────────┐  │  ┌─────────────────┐
│ QUERY 2: External Docs  │  │  │ QUERY 2:        │
│ Current, authoritative  │  │  │ External Docs   │
│                         │  │  └────────┬────────┘
│ Try:                    │  │           │
│ - WebFetch official     │  │           │
│   docs                  │  │           │
│ - context7 API refs     │  │           │
│ - deepwiki if available │  │           │
└────────┬────────────────┘  │           │
         │                   │           │
         ▼                   │           ▼
    ┌────┴─────┐            │      ┌─────────┐
    │ Found?   │  Yes ──────┼─────►│ Combine │
    │          │            │      │ Results │
    └────┬─────┘            │      └────┬────┘
         │No                │           │
         │                  │           │
         ▼                  │           │
┌─────────────────────────┐│           │
│ QUERY 3: Codebase       ││           │
│ Project-specific usage  ││           │
│                         ││           │
│ Use:                    ││           │
│ - LSP symbol lookup     ││           │
│ - Grep for patterns     ││           │
│ - Find actual usage     ││           │
└────────┬────────────────┘│           │
         │                 │           │
         ▼                 │           │
    ┌────┴─────┐           │           │
    │ Found?   │  Yes ─────┼──────────►│
    │          │           │           │
    └────┬─────┘           │           │
         │No               │           │
         │                 │           │
         ▼                 ▼           ▼
┌────────────────────────────────────────┐
│ Aggregate Results                       │
│ - Combine all sources                   │
│ - Rank by:                              │
│   1. Codebase (most specific)           │
│   2. External docs (most current)       │
│   3. Static knowledge (most reliable)   │
│ - Remove duplicates                     │
│ - Calculate confidence scores           │
└────────────┬───────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Results Analysis                          │
└────────────┬─────────────────────────────┘
             │
        ┌────┴─────┐
        │ How many │
        │ results? │
        └────┬─────┘
             │
   ┌─────────┼──────────┬─────────┐
   │         │          │         │
   0         1        2-3       4+
   │         │          │         │
   ▼         ▼          ▼         ▼
┌────┐  ┌────────┐ ┌────────┐ ┌──────┐
│ASK │  │CONFIRM │ │OPTIONS │ │FILTER│
│OPEN│  │w/ USER │ │Present │ │Top 3 │
│-END│  │        │ │ranked  │ │Then  │
│    │  │        │ │list    │ │present│
└────┘  └────────┘ └────────┘ └──────┘
```

## Clarification Dialogue Decision Tree

```
┌─────────────────────────────────┐
│ Need to Clarify with User       │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Determine Clarification Type     │
└────────────┬─────────────────────┘
             │
        ┌────┴─────────┬──────────────┬─────────────┐
        │              │              │             │
        ▼              ▼              ▼             ▼
┌────────────┐  ┌────────────┐ ┌───────────┐ ┌──────────┐
│ DOMAIN     │  │ SCOPE      │ │ OPTION    │ │ OPEN     │
│ Unclear    │  │ Unclear    │ │ Selection │ │ -ENDED   │
│ which      │  │ what type  │ │ multiple  │ │ No idea  │
│ framework? │  │ of X?      │ │ viable    │ │ what     │
│            │  │            │ │ interpre  │ │ they     │
│            │  │            │ │ -tations  │ │ mean     │
└────┬───────┘  └────┬───────┘ └─────┬─────┘ └────┬─────┘
     │              │              │            │
     ▼              ▼              ▼            ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐ ┌────────────┐
│ASK:      │  │ASK:      │  │PRESENT:     │ │ASK:        │
│"Which    │  │"What type│  │"[Term]      │ │"Can you    │
│framework │  │ of [X]?  │  │could mean:  │ │explain     │
│are you   │  │          │  │             │ │what you    │
│using?"   │  │- Option A│  │1. [Tech A]  │ │mean by     │
│          │  │- Option B│  │   [Context] │ │[term]?"    │
│- Autogen │  │- Option C│  │             │ │            │
│- Langroid│  │          │  │2. [Tech B]  │ │Or:         │
│- Other   │  │Which did │  │   [Context] │ │"Could you  │
│          │  │you mean?"│  │             │ │give an     │
└────┬─────┘  └────┬─────┘  │3. [Tech C]  │ │example?"   │
     │              │        │   [Context] │ └────┬───────┘
     │              │        │             │      │
     │              │        │Which one?"  │      │
     │              │        └──────┬──────┘      │
     │              │               │             │
     ▼              ▼               ▼             ▼
┌────────────────────────────────────────────────────┐
│ User Responds                                      │
└────────────┬───────────────────────────────────────┘
             │
             ▼
        ┌────┴─────┐
        │ Clear?   │  Yes ────────┐
        │          │              │
        └────┬─────┘              │
             │No                  │
             │                    ▼
             ▼           ┌──────────────────┐
    ┌────────────────┐  │ VALIDATE         │
    │ Iteration      │  │ UNDERSTANDING    │
    │ Count?         │  │                  │
    └────┬───────────┘  │ "So you want to  │
         │              │  [restate in     │
    ┌────┴───┐         │   precise terms] │
    │  < 3   │  Yes ─┐ │                  │
    └────┬───┘       │ │ Is that correct?"│
         │No         │ └────────┬─────────┘
         │           │          │
         ▼           │          ▼
┌────────────────┐  │ ┌──────────────────┐
│ ESCALATE       │  │ │ User Confirms    │
│                │  │ └────────┬─────────┘
│"I'm not sure   │  │          │
│I understand.   │  │          ▼
│Could you       │  │ ┌──────────────────┐
│provide a       │  │ │ PROCEED          │
│concrete        │  │ │ with Validated   │
│example or      │  │ │ Terminology      │
│reference?"     │  │ └──────────────────┘
└────────────────┘  │
                    │
                    ▼
           ┌──────────────────┐
           │ FOLLOW-UP        │
           │ CLARIFICATION    │
           │ Ask more         │
           │ specific         │
           │ question         │
           └──────────────────┘
```

## Domain Identification Decision Tree

```
┌─────────────────────────────────┐
│ User Request Analyzed           │
│ Domain Unknown                  │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Look for Domain Signals          │
│ - Framework names mentioned      │
│ - Library-specific terminology   │
│ - Import statements              │
│ - Project structure              │
└────────────┬─────────────────────┘
             │
        ┌────┴─────┐
        │ Signals  │  Yes ─────────┐
        │ found?   │               │
        └────┬─────┘               │
             │No                   │
             │                     ▼
             │           ┌──────────────────┐
             │           │ Infer from       │
             │           │ Signals          │
             │           │                  │
             │           │ "ConversableAgent"│
             │           │ → Autogen        │
             │           │                  │
             │           │ "ChatAgent"      │
             │           │ → Langroid       │
             │           └────────┬─────────┘
             │                    │
             │                    ▼
             │           ┌──────────────────┐
             │           │ Confidence?      │
             │           └────────┬─────────┘
             │                    │
             │              ┌─────┴─────┐
             │              │           │
             │            High         Low
             │              │           │
             │              │           │
             ▼              ▼           ▼
    ┌────────────┐ ┌──────────┐ ┌───────────┐
    │ ASK        │ │ CONFIRM  │ │ ASK       │
    │ EXPLICITLY │ │          │ │ EXPLICITLY│
    │            │ │ "I see   │ │           │
    │"Which     │ │ you're   │ │ "Which    │
    │framework  │ │ using    │ │ framework │
    │are you    │ │ [domain] │ │ are you   │
    │using?     │ │          │ │ using?"   │
    │           │ │ Is that  │ │           │
    │- Autogen  │ │ correct?"│ │ (No       │
    │- Langroid │ │          │ │ options)  │
    │- Other    │ └────┬─────┘ └───────────┘
    │           │      │
    │ (Please   │      ▼
    │ specify)" │ ┌──────────────┐
    └─────┬─────┘ │ User Confirms│
          │       │ or Corrects  │
          │       └──────┬───────┘
          │              │
          ▼              ▼
    ┌──────────────────────┐
    │ User Specifies Domain│
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Load Domain          │
    │ Knowledge            │
    │                      │
    │ - Domain ontologies  │
    │ - Technical mappings │
    │ - Known ambiguities  │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Set Domain Context   │
    │ for Session          │
    │                      │
    │ Remember for future  │
    │ messages in this     │
    │ conversation         │
    └──────────────────────┘
```

## Confidence Scoring Decision Tree

```
┌─────────────────────────────────┐
│ Calculate Confidence Score      │
│ for Ambiguity Detection         │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Analyze Multiple Factors         │
└────────────┬─────────────────────┘
             │
       ┌─────┴─────┬─────────┬─────────┐
       │           │         │         │
       ▼           ▼         ▼         ▼
┌──────────┐┌──────────┐┌──────┐┌─────────┐
│ Pattern  ││ Context  ││Domain││Reference│
│ Strength ││ Clarity  ││Signals││ Clarity │
│          ││          ││      ││         │
│ Known    ││ Recent   ││Frame-││ Clear   │
│ ambiguous││ messages ││work  ││ ante-   │
│ patterns?││ provide  ││men-  ││ cedents?│
│          ││ context? ││tioned││         │
│ +30 pts  ││ +20 pts  ││+15pts││ -20 pts │
└────┬─────┘└────┬─────┘└──┬───┘└────┬────┘
     │           │         │         │
     └─────┬─────┴────┬────┴────┬────┘
           │          │         │
           ▼          ▼         ▼
    ┌──────────────────────────────┐
    │ Sum Confidence Score (0-100) │
    └────────────┬─────────────────┘
                 │
            ┌────┴────┬────────┬────────┐
            │         │        │        │
          >80%     50-80%   30-50%    <30%
            │         │        │        │
            │         │        │        │
            ▼         ▼        ▼        ▼
      ┌─────────┐┌───────┐┌──────┐┌────────┐
      │ HIGH    ││MEDIUM ││ LOW  ││ IGNORE │
      │         ││       ││      ││        │
      │Validate ││Check  ││Watch ││Proceed │
      │immedi-  ││if >1  ││for   ││normally│
      │ately    ││option ││more  ││        │
      │         ││then   ││signals││       │
      │         ││validate││      ││        │
      └─────────┘└───────┘└──────┘└────────┘
```

## Summary

These decision trees provide systematic guidance for:

1. **Initial message analysis** - Detecting ambiguity signals
2. **Knowledge querying** - Three-tier query workflow
3. **Clarification dialogue** - Conversational validation
4. **Domain identification** - Framework/library detection
5. **Confidence scoring** - Determining when to intervene

Use these trees to make consistent, reliable decisions during semantic validation processes.
