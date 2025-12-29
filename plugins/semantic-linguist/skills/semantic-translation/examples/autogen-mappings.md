# Autogen-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise Autogen implementations.

## Example 1: "make it talk"

### User Request
```
"I want to make an agent that can talk to other agents"
```

### Ambiguity Detected
- "make" - vague action verb
- "talk to other agents" - unclear communication pattern

### Semantic Validation Process

**Step 1: Domain Identified**
- User context: Working with Autogen (confirmed or inferred)

**Step 2: Query Knowledge**
- Static: "talk" maps to send(), initiate_chat(), GroupChat in Autogen
- Ontology: Communication patterns in Autogen

**Step 3: Present Options**
```
In Autogen, "make an agent talk to other agents" could mean:

1. **One-to-one messaging** - ConversableAgent with send()
   - Agent sends individual messages to specific recipients
   - Example: agent1.send("Hello", agent2)
   - Use case: Direct agent-to-agent communication

2. **Initiated conversation** - initiate_chat()
   - Start a back-and-forth conversation
   - Example: agent1.initiate_chat(agent2, message="Let's discuss...")
   - Use case: Extended conversation between two agents

3. **Group conversation** - GroupChat with GroupChatManager
   - Multiple agents participate in discussion
   - Example:
     ```python
     groupchat = GroupChat(
         agents=[agent1, agent2, agent3],
         messages=[],
         max_round=10
     )
     manager = GroupChatManager(groupchat=groupchat)
     manager.initiate_chat(groupchat)
     ```
   - Use case: Multi-party discussion, brainstorming, debate

Which communication pattern do you need?"
```

**Step 4: User Clarifies**
```
User: "I want multiple agents to discuss a problem together"
```

**Step 5: Validated Translation**
```
"Perfect! You need GroupChat for multi-agent discussions. Here's how:

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

# Create agents
analyst = ConversableAgent(name="Analyst", system_message="You analyze problems...")
critic = ConversableAgent(name="Critic", system_message="You critique solutions...")
implementer = ConversableAgent(name="Implementer", system_message="You implement solutions...")

# Create group chat
groupchat = GroupChat(
    agents=[analyst, critic, implementer],
    messages=[],
    max_round=12,
    speaker_selection_method="auto"  # LLM decides who speaks next
)

# Create manager to orchestrate
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the discussion
manager.initiate_chat(
    groupchat,
    message="Let's discuss how to optimize our database queries"
)
```

The GroupChatManager will coordinate the conversation, and agents will take turns
based on the speaker_selection_method."
```

---

## Example 2: "create an api"

### User Request
```
"I need to create an API for my Autogen agents"
```

### Ambiguity Detected
- "API" - multiple interpretations (HTTP server? Interface? Tools?)
- Context: Autogen domain, but "API" is general term

### Semantic Validation Process

**Step 1: Analyze Context**
- User working with Autogen agents
- Needs some kind of "API"
- Could mean: HTTP server to trigger agents, or tool/function calling interface

**Step 2: Present Options**
```
"API" in the context of Autogen agents could mean:

1. **HTTP REST API server** (to trigger agents via web requests)
   - Framework: FastAPI, Flask (Python)
   - Use case: Web app calls agent workflows via HTTP
   - Example: POST /api/analyze → triggers analyst agent

2. **Tool/Function calling interface** (for agents to call external functions)
   - Autogen feature: register_for_llm() and register_for_execution()
   - Use case: Agents can call functions like search_web(), query_database()
   - Example: Agent requests "search_web(query)" via LLM function calling

3. **Agent interface/wrapper** (expose agents as callable interface)
   - Python class with clean interface
   - Use case: Other code can easily instantiate and use agents
   - Example: AgentAPI.run_analysis(prompt) → returns agent result

Which type of API integration do you need?"
```

**Step 3: User Clarifies**
```
User: "I want agents to be able to call external functions like database queries"
```

**Step 4: Validated Translation**
```
"That's tool/function calling in Autogen! Here's the pattern:

```python
from autogen import ConversableAgent, UserProxyAgent
import typing_extensions as typing

# Define tool function
def query_database(query: str) -> str:
    """Execute SQL query and return results"""
    # Your database logic here
    return f"Results for: {query}"

# Create agents
assistant = ConversableAgent(
    name="Assistant",
    system_message="You help users query databases",
    llm_config={"config_list": config_list}
)

user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config=False
)

# Register function for LLM to call
@assistant.register_for_llm(
    description="Query the database with SQL"
)
def query_db_llm(query: str) -> str:
    return query

# Register function for execution
@user_proxy.register_for_execution()
def query_db_execution(query: str) -> str:
    return query_database(query)

# Now assistant can request database queries via LLM function calling
user_proxy.initiate_chat(
    assistant,
    message="Can you query the database for all users created today?"
)
```

The LLM will generate a function call request, and UserProxy will execute it."
```

---

## Example 3: "agent with tools"

### User Request
```
"How do I create an Autogen agent with tools?"
```

### Ambiguity Detected
- "tools" - could mean different things in Autogen context

### Semantic Validation Process

**Step 1: Query Knowledge**
- Autogen has: function calling (register_for_llm), code execution, external tool integration
- Need to clarify which "tools" user means

**Step 2: Present Options**
```
"Tools" in Autogen can refer to:

1. **Function calling** (LLM-callable functions)
   - Most common interpretation
   - Agent: AssistantAgent with register_for_llm()
   - Use case: Agent can call Python functions via LLM

2. **Code execution** (execute generated code)
   - Built-in Autogen feature
   - Agent: UserProxyAgent with code_execution_config
   - Use case: Agent generates and executes Python/shell code

3. **External tool integration** (APIs, services)
   - Custom functions wrapping external tools
   - Combined with function calling
   - Use case: Agent calls external APIs, services

Which type of tool integration did you have in mind?"
```

**Step 3: User Clarifies**
```
User: "I want the agent to be able to search the web and query a database"
```

**Step 4: Validated Translation**
```
"That's function calling with external tools. Here's the complete pattern:

```python
from autogen import AssistantAgent, UserProxyAgent
import requests

# Define tool functions
def search_web(query: str) -> str:
    """Search the web using a search API"""
    # Your search API logic
    response = requests.get(f"https://api.search.com?q={query}")
    return response.json()["results"]

def query_database(sql: str) -> str:
    """Execute SQL query"""
    # Your database logic
    return execute_query(sql)

# Create AssistantAgent (can request function calls)
assistant = AssistantAgent(
    name="Assistant",
    system_message="You can search the web and query databases to help users",
    llm_config={"config_list": config_list, "functions": [
        {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "query_database",
            "description": "Execute SQL query",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL query"}
                },
                "required": ["sql"]
            }
        }
    ]}
)

# Create UserProxyAgent (executes functions)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map={
        "search_web": search_web,
        "query_database": query_database
    }
)

# Agent can now use both tools
user_proxy.initiate_chat(
    assistant,
    message="Search the web for Python trends, then query our database for Python projects"
)
```

The assistant will generate function calls, and user_proxy will execute them."
```

---

## Example 4: "group conversation"

### User Request
```
"I need to set up a group conversation"
```

### Ambiguity Detected
- "group conversation" - might be GroupChat object or general concept
- Need to clarify Autogen-specific implementation

### Semantic Validation Process

**Step 1: Confirm Understanding**
```
"In Autogen, group conversations are implemented with GroupChat. Is that what you're looking for?

Key features of GroupChat:
- Multiple agents participate
- GroupChatManager orchestrates conversation
- Speaker selection (auto, manual, round-robin, random)
- Conversation history maintained

If this matches what you need, I can show you how to set it up."
```

**Step 2: User Confirms**
```
User: "Yes, exactly. How do I set it up?"
```

**Step 3: Provide Implementation**
```
"Here's how to create a GroupChat in Autogen:

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

# Create participating agents
agents = [
    ConversableAgent(
        name="Researcher",
        system_message="You research topics thoroughly",
        llm_config=llm_config
    ),
    ConversableAgent(
        name="Critic",
        system_message="You critically evaluate ideas",
        llm_config=llm_config
    ),
    ConversableAgent(
        name="Synthesizer",
        system_message="You synthesize different viewpoints",
        llm_config=llm_config
    )
]

# Create GroupChat
groupchat = GroupChat(
    agents=agents,
    messages=[],
    max_round=15,  # Maximum conversation rounds
    speaker_selection_method="auto"  # Options: "auto", "manual", "random", "round_robin"
)

# Create GroupChatManager to orchestrate
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Start the group conversation
manager.initiate_chat(
    groupchat,
    message="Let's discuss the implications of AI in education"
)
```

**Speaker Selection Methods:**
- `"auto"` - LLM decides who speaks next based on conversation context (recommended)
- `"manual"` - Human selects next speaker
- `"round_robin"` - Agents take turns in order
- `"random"` - Random agent selected each round

The GroupChatManager will:
1. Broadcast message to all agents
2. Select next speaker based on method
3. Coordinate turn-taking
4. Maintain conversation history
5. Detect termination conditions"
```

---

## Example 5: "human in the loop"

### User Request
```
"I want the user to approve actions before the agent executes them"
```

### Ambiguity Detected
- "approve actions" - needs UserProxyAgent with specific configuration
- Need to clarify when approval is needed

### Semantic Validation Process

**Step 1: Clarify Scope**
```
"For human-in-the-loop workflows in Autogen, you'll use UserProxyAgent. When should the human approve?

1. **Always** - Approve every agent action
   - Setting: human_input_mode="ALWAYS"
   - Use case: Maximum control, every step requires approval

2. **On termination** - Approve only at conversation end
   - Setting: human_input_mode="TERMINATE"
   - Use case: Review final decision before completing

3. **Never (but can execute code)** - No approval, but executes code on behalf of user
   - Setting: human_input_mode="NEVER"
   - Use case: Automated workflows, agent executes without asking

Which approval pattern do you need?"
```

**Step 2: User Clarifies**
```
User: "I want to approve every action before execution"
```

**Step 3: Validated Translation**
```
"That's UserProxyAgent with human_input_mode="ALWAYS". Here's the setup:

```python
from autogen import AssistantAgent, UserProxyAgent

# Create assistant (proposes actions)
assistant = AssistantAgent(
    name="Assistant",
    system_message="You help users accomplish tasks step by step",
    llm_config={"config_list": config_list}
)

# Create user proxy (requests human approval for everything)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",  # Request input for every action
    max_consecutive_auto_reply=0,  # Always wait for human input
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Help me analyze this dataset"
)

# Workflow:
# 1. Assistant proposes an action
# 2. UserProxy asks human: "Approve this action? (yes/no)"
# 3. Human types approval or rejection
# 4. If approved, action executes
# 5. Repeat for next action
```

**How approval works:**
- After each assistant message, you'll see a prompt
- Type your response or approval
- Type "exit" to end the conversation
- The agent won't proceed without your input"
```

---

## Pattern Summary

Common Autogen ambiguity patterns:

1. **"create agent"** → Which type? ConversableAgent, AssistantAgent, UserProxyAgent
2. **"talk/communicate"** → send(), initiate_chat(), or GroupChat?
3. **"tools/functions"** → register_for_llm() + register_for_execution()
4. **"group/multi-agent"** → GroupChat + GroupChatManager
5. **"approval/human-in-loop"** → UserProxyAgent with human_input_mode

Always clarify before implementing!
