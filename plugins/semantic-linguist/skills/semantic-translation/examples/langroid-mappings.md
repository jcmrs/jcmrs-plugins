# Langroid-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise Langroid implementations.

## Example 1: "create an agent"

### User Request
```
"How do I create an agent in Langroid?"
```

### Semantic Validation

**Clarification:**
```
In Langroid, "create an agent" typically means ChatAgent. Do you need:

1. **Basic ChatAgent** (simple conversational agent)
2. **ToolAgent** (agent with function calling)
3. **Custom Agent** (subclass with specialized behavior)
```

**User:** "Basic agent for Q&A"

**Validated Implementation:**
```python
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig

# Configure agent
config = ChatAgentConfig(
    name="QAAgent",
    system_message="You answer questions accurately and concisely",
    llm=OpenAIGPTConfig(chat_model="gpt-4")
)

# Create agent
agent = ChatAgent(config)

# Use agent
response = agent.llm_response("What is Python?")
print(response)
```

---

## Example 2: "agent with tools"

### User Request
```
"I need an agent that can search the web"
```

### Semantic Validation

**Clarification:**
```
"Agent with tools" in Langroid uses ToolMessage. You'll need to:
1. Define a ToolMessage subclass for web search
2. Agent will automatically detect and use it
```

**Validated Implementation:**
```python
from langroid.agent.tool_message import ToolMessage
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
import pydantic

class WebSearchTool(ToolMessage):
    request: str = "web_search"
    purpose: str = "Search the web for information"
    query: str

    def handle(self) -> str:
        # Your web search implementation
        return f"Search results for: {self.query}"

# Create agent with tool
config = ChatAgentConfig(
    name="SearchAgent",
    system_message="You can search the web to answer questions"
)
agent = ChatAgent(config)

# Agent will automatically use WebSearchTool when needed
```

---

## Example 3: "multi-agent workflow"

### User Request
```
"How do I set up multiple agents to work together?"
```

### Semantic Validation

**Clarification:**
```
Langroid multi-agent workflows use Task delegation:

1. **Sequential** - Agent A → Agent B → Agent C
2. **Hierarchical** - Parent task with subtasks
3. **Parallel** - Multiple agents work simultaneously (custom coordination)
```

**User:** "Sequential workflow"

**Validated Implementation:**
```python
from langroid.agent.task import Task
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig

# Create agents
researcher = ChatAgent(ChatAgentConfig(
    name="Researcher",
    system_message="Research topics thoroughly"
))

analyst = ChatAgent(ChatAgentConfig(
    name="Analyst",
    system_message="Analyze research findings"
))

# Create tasks
research_task = Task(
    researcher,
    name="research",
    interactive=False
)

analysis_task = Task(
    analyst,
    name="analysis",
    interactive=False
)

# Set up delegation: research → analysis
research_task.add_sub_task(analysis_task)

# Run workflow
result = research_task.run("Research AI trends")
```

---

## Example 4: "agent responds to user"

### User Request
```
"How do I get the agent to respond to user input?"
```

### Semantic Validation

**Clarification:**
```
"Agent responds" could mean:
1. **LLM response** - agent.llm_response()
2. **Agent logic response** - Override agent_response()
3. **Interactive task** - Task.run() with interactive=True
```

**User:** "Interactive chat"

**Validated Implementation:**
```python
from langroid.agent.task import Task
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig

# Create agent
agent = ChatAgent(ChatAgentConfig(
    name="Assistant",
    system_message="You are a helpful assistant"
))

# Create interactive task
task = Task(
    agent,
    name="chat",
    interactive=True  # Allows human input
)

# Run (will prompt for user input)
task.run()
```

---

## Pattern Summary

Common Langroid ambiguities:

1. **"create agent"** → ChatAgent vs ToolAgent vs custom subclass
2. **"agent with tools"** → ToolMessage pattern
3. **"multi-agent"** → Task delegation hierarchy
4. **"agent responds"** → llm_response() vs agent_response() vs interactive Task
5. **"run agent"** → Task.run() orchestration

Key difference from Autogen: Langroid uses Task-based orchestration rather than direct agent-to-agent messaging.
