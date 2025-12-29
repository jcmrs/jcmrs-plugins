# UTCP-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise UTCP (Universal Tool Calling Protocol) implementations.

## Overview

UTCP (Universal Tool Calling Protocol) is a framework-agnostic standard for defining and calling tools across different AI frameworks. Key concepts include:
- **Universal tool schemas**: Framework-independent tool definitions
- **Framework adapters**: UTCP adapters for OpenAI, Anthropic, Langchain, etc.
- **Tool invocation**: Standardized calling mechanism across frameworks
- **Portability**: Write once, use across multiple AI platforms

Common ambiguities arise when users conflate UTCP's universal approach with framework-specific implementations (OpenAI tools, Anthropic tools, function calling).

---

## Example 1: "set up tool calling"

### User Request
```
"I need to set up tool calling for my AI agent"
```

### Ambiguity Detected
- "tool calling" - UTCP universal calling vs framework-specific implementations
- Need to clarify if they want framework-agnostic (UTCP) or specific platform

### Semantic Validation Process

**Step 1: Domain Identified**
- User needs tool calling capability
- Unclear if they want portability (UTCP) or single-platform (OpenAI/Anthropic)

**Step 2: Query Knowledge**
- UTCP: Framework-agnostic, write once, run anywhere
- Framework-specific: Optimized for single platform, simpler if only using one

**Step 3: Present Options**
```
"Tool calling" can be implemented two ways:

1. **UTCP Universal Tool Calling** (framework-agnostic)
   - Write tool definitions once
   - Use across OpenAI, Anthropic, Langchain, etc.
   - UTCP adapters handle framework differences
   - Best for: Multi-framework projects, portability, future flexibility
   - Trade-off: Additional abstraction layer

2. **Framework-Specific Tool Calling**
   - OpenAI tools: Function calling with OpenAI API
   - Anthropic tools: Tool use with Claude API
   - Optimized for single platform
   - Best for: Single-framework projects, simplicity
   - Trade-off: Vendor lock-in, rewrite for other platforms

Are you building for one AI platform or need portability across multiple?"
```

**Step 4: User Clarifies**
```
User: "I might switch between OpenAI and Anthropic, want to avoid rewriting tools"
```

**Step 5: Validated Translation**
```
"That's exactly what UTCP solves! Here's how to define universal tools:

**1. Define tool with UTCP universal schema:**
```python
from utcp import Tool, ToolParameter

# Universal tool definition (works across all frameworks)
search_tool = Tool(
    name="search_web",
    description="Search the web for information",
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="Search query",
            required=True
        ),
        ToolParameter(
            name="num_results",
            type="integer",
            description="Number of results to return",
            required=False,
            default=10
        )
    ]
)

# Implementation (framework-agnostic)
def search_web(query: str, num_results: int = 10) -> str:
    """Actual search logic"""
    results = perform_search(query, num_results)
    return format_results(results)
```

**2. Use with OpenAI (via UTCP adapter):**
```python
from utcp.adapters import OpenAIAdapter

# Convert UTCP tool to OpenAI format
openai_adapter = OpenAIAdapter()
openai_tools = openai_adapter.convert_tools([search_tool])

# Use with OpenAI API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Search for Python tutorials"}],
    tools=openai_tools,  # UTCP tool converted to OpenAI format
    tool_choice="auto"
)

# Handle tool calls (UTCP adapter handles format differences)
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        # UTCP adapter extracts arguments
        result = openai_adapter.execute_tool(search_tool, tool_call, search_web)
```

**3. Switch to Anthropic (same tool definition!):**
```python
from utcp.adapters import AnthropicAdapter

# Same UTCP tool, different adapter
anthropic_adapter = AnthropicAdapter()
anthropic_tools = anthropic_adapter.convert_tools([search_tool])

# Use with Anthropic API
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Search for Python tutorials"}],
    tools=anthropic_tools,  # Same tool, Anthropic format
    max_tokens=1000
)

# Handle tool calls (UTCP adapter handles format differences)
if response.stop_reason == "tool_use":
    for content_block in response.content:
        if content_block.type == "tool_use":
            # UTCP adapter extracts arguments
            result = anthropic_adapter.execute_tool(search_tool, content_block, search_web)
```

**Benefits:**
- Tool defined once, works everywhere
- Switch AI providers without changing tool code
- UTCP adapters handle API differences (parameter formats, response structures)
- Future-proof: Add new framework support via adapters"
```

---

## Example 2: "tool schema format"

### User Request
```
"What's the difference between UTCP schema and OpenAI schema?"
```

### Ambiguity Detected
- Confusion between universal schema (UTCP) and framework-specific schemas
- Need to explain schema portability

### Semantic Validation Process

**Step 1: Explain Distinction**
```
There are three types of tool schemas to understand:

1. **UTCP Universal Schema** (framework-agnostic)
   - Defines tools in neutral format
   - Example: UTCP Tool object with parameters
   - Portable: Works across all AI frameworks
   - Converted to framework-specific format by adapters

2. **OpenAI Tool Schema** (OpenAI-specific)
   - JSON format for OpenAI's function calling
   - Example: {"type": "function", "function": {...}}
   - Only works with OpenAI API
   - Not portable to other frameworks

3. **Anthropic Tool Schema** (Anthropic-specific)
   - JSON format for Claude's tool use
   - Example: {"name": "...", "description": "...", "input_schema": {...}}
   - Only works with Anthropic API
   - Not portable to other frameworks

**Key insight:** UTCP schema is the source of truth, adapters generate framework schemas
```

**Step 2: Show Comparison**
```
"Here's the same tool in all three formats:

**UTCP Universal Schema:**
```python
from utcp import Tool, ToolParameter

tool = Tool(
    name="get_weather",
    description="Get current weather for a location",
    parameters=[
        ToolParameter(
            name="location",
            type="string",
            description="City name",
            required=True
        ),
        ToolParameter(
            name="units",
            type="string",
            description="Temperature units (celsius/fahrenheit)",
            required=False,
            default="celsius",
            enum=["celsius", "fahrenheit"]
        )
    ]
)
```

**OpenAI Schema (generated by UTCP OpenAI adapter):**
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City name"
        },
        "units": {
          "type": "string",
          "description": "Temperature units (celsius/fahrenheit)",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

**Anthropic Schema (generated by UTCP Anthropic adapter):**
```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name"
      },
      "units": {
        "type": "string",
        "description": "Temperature units (celsius/fahrenheit)",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

**Workflow:**
1. Define tool once in UTCP universal format
2. UTCP adapter converts to framework-specific schema
3. Use generated schema with framework API
4. No manual schema writing/conversion needed"
```

---

## Example 3: "create adapter for new framework"

### User Request
```
"I want to use UTCP tools with a new AI framework"
```

### Ambiguity Detected
- "new AI framework" - need to understand if UTCP adapter exists or needs creation
- Unclear if they want to use existing adapter or build new one

### Semantic Validation Process

**Step 1: Clarify Scenario**
```
"UTCP supports multiple frameworks via adapters. Two scenarios:

1. **Framework already has UTCP adapter**
   - Existing adapters: OpenAI, Anthropic, Langchain, Haystack
   - Just import and use the adapter
   - Example: `from utcp.adapters import OpenAIAdapter`
   - No custom code needed

2. **Framework needs new UTCP adapter**
   - Framework not yet supported by UTCP
   - Need to implement custom adapter
   - Example: Building adapter for new AI platform
   - Requires understanding framework's tool calling API

Which framework are you working with?"
```

**Step 2: User Clarifies**
```
User: "I'm using a custom AI framework that's not in the UTCP adapter list"
```

**Step 3: Validated Translation**
```
"You'll need to create a custom UTCP adapter! Here's how:

**1. Understand UTCP Adapter Interface:**
```python
from utcp import Tool, Adapter, ToolCall

class CustomAdapter(Adapter):
    """Adapter for your custom AI framework"""

    def convert_tool(self, tool: Tool) -> dict:
        """Convert UTCP Tool to framework-specific schema"""
        raise NotImplementedError

    def convert_tools(self, tools: list[Tool]) -> list[dict]:
        """Convert multiple tools"""
        return [self.convert_tool(tool) for tool in tools]

    def extract_tool_calls(self, response: any) -> list[ToolCall]:
        """Extract tool calls from framework's API response"""
        raise NotImplementedError

    def execute_tool(self, tool: Tool, tool_call: ToolCall, implementation: callable) -> any:
        """Execute tool with extracted arguments"""
        raise NotImplementedError
```

**2. Implement Custom Adapter:**
```python
from utcp import Tool, Adapter, ToolCall

class MyFrameworkAdapter(Adapter):
    """UTCP adapter for MyFramework AI platform"""

    def convert_tool(self, tool: Tool) -> dict:
        """Convert UTCP Tool to MyFramework schema"""
        # Map UTCP format to your framework's format
        framework_schema = {
            "tool_name": tool.name,
            "tool_description": tool.description,
            "inputs": {}
        }

        for param in tool.parameters:
            framework_schema["inputs"][param.name] = {
                "type": param.type,
                "desc": param.description,
                "mandatory": param.required
            }
            if param.default:
                framework_schema["inputs"][param.name]["default_value"] = param.default

        return framework_schema

    def extract_tool_calls(self, response: any) -> list[ToolCall]:
        """Extract tool calls from MyFramework response"""
        tool_calls = []

        # Parse framework's response format
        if hasattr(response, 'tool_requests'):
            for request in response.tool_requests:
                tool_calls.append(ToolCall(
                    id=request.request_id,
                    name=request.tool_name,
                    arguments=request.input_values
                ))

        return tool_calls

    def execute_tool(self, tool: Tool, tool_call: ToolCall, implementation: callable) -> any:
        """Execute tool with extracted arguments"""
        # Extract arguments from framework's format
        kwargs = {}
        for param in tool.parameters:
            if param.name in tool_call.arguments:
                kwargs[param.name] = tool_call.arguments[param.name]
            elif param.default:
                kwargs[param.name] = param.default

        # Call implementation
        result = implementation(**kwargs)

        return result
```

**3. Use Custom Adapter:**
```python
# Define UTCP tools
from utcp import Tool, ToolParameter

search_tool = Tool(
    name="search_web",
    description="Search the web",
    parameters=[ToolParameter(name="query", type="string", required=True)]
)

# Use custom adapter
adapter = MyFrameworkAdapter()
framework_tools = adapter.convert_tools([search_tool])

# Call your framework's API
response = my_framework_client.chat(
    prompt="Search for UTCP documentation",
    tools=framework_tools
)

# Extract and execute tool calls
tool_calls = adapter.extract_tool_calls(response)
for tool_call in tool_calls:
    result = adapter.execute_tool(search_tool, tool_call, search_web_implementation)
```

**Adapter checklist:**
- [ ] convert_tool() maps UTCP → framework schema
- [ ] extract_tool_calls() parses framework response
- [ ] execute_tool() calls implementation with correct arguments
- [ ] Handles optional parameters and defaults
- [ ] Error handling for invalid tool calls"
```

---

## Example 4: "utcp vs function calling"

### User Request
```
"Is UTCP the same as function calling?"
```

### Ambiguity Detected
- Confusion between UTCP (protocol/standard) and function calling (feature)
- Need to clarify relationship

### Semantic Validation Process

**Step 1: Explain Relationship**
```
UTCP and function calling are related but different:

**Function Calling** (Feature):
- AI capability to call functions/tools
- Implemented by: OpenAI (function calling), Anthropic (tool use), etc.
- Each framework has its own API format
- Example: OpenAI's `tools` parameter in chat completions

**UTCP** (Protocol/Standard):
- Framework-agnostic way to define tools
- Abstraction layer above function calling
- Works with any AI framework that supports function calling
- Provides portability and standardization

**Relationship:**
UTCP uses function calling features, but provides universal interface

**Analogy:**
- Function calling = Each car manufacturer's engine API
- UTCP = Universal adapter that works with all engines
```

**Step 2: Show How UTCP Wraps Function Calling**
```
"Here's how UTCP relates to framework function calling:

**Without UTCP (direct framework function calling):**
```python
# OpenAI-specific code
openai_tools = [{
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search web",
        "parameters": {...}
    }
}]

openai_response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=openai_tools
)

# Anthropic-specific code (different format!)
anthropic_tools = [{
    "name": "search",
    "description": "Search web",
    "input_schema": {...}
}]

anthropic_response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...],
    tools=anthropic_tools
)

# Problem: Two different schemas, two different APIs
```

**With UTCP (universal interface):**
```python
from utcp import Tool, ToolParameter
from utcp.adapters import OpenAIAdapter, AnthropicAdapter

# Define tool once (universal)
search_tool = Tool(
    name="search",
    description="Search web",
    parameters=[ToolParameter(name="query", type="string", required=True)]
)

# Use with OpenAI (UTCP handles function calling API)
openai_adapter = OpenAIAdapter()
openai_tools = openai_adapter.convert_tools([search_tool])
openai_response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=openai_tools  # UTCP-generated, OpenAI-compatible
)

# Use with Anthropic (same tool, UTCP handles tool use API)
anthropic_adapter = AnthropicAdapter()
anthropic_tools = anthropic_adapter.convert_tools([search_tool])
anthropic_response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...],
    tools=anthropic_tools  # UTCP-generated, Anthropic-compatible
)

# Benefit: One tool definition, works with both function calling systems
```

**Summary:**
- Function calling = Framework-specific feature
- UTCP = Universal layer that works with all function calling implementations
- UTCP doesn't replace function calling, it standardizes it"
```

---

## Example 5: "portable tools across frameworks"

### User Request
```
"I have tools in OpenAI format, can I use them with Anthropic?"
```

### Ambiguity Detected
- User has OpenAI-specific tools, wants portability
- Need to explain conversion process via UTCP

### Semantic Validation Process

**Step 1: Clarify Current State**
```
"You have OpenAI-formatted tools and want to use them with Anthropic. Two approaches:

1. **Manual conversion** (tedious, error-prone)
   - Manually rewrite OpenAI schema to Anthropic schema
   - Different field names, structure, format
   - Maintain two versions going forward
   - Not recommended

2. **UTCP conversion** (automated, maintainable)
   - Convert OpenAI schema → UTCP universal schema
   - UTCP adapter generates Anthropic schema
   - Future framework changes easy
   - Recommended approach

Which approach would you prefer?"
```

**Step 2: User Chooses UTCP**
```
User: "UTCP sounds better, how do I convert my OpenAI tools?"
```

**Step 3: Validated Translation**
```
"Here's how to migrate OpenAI tools to UTCP:

**Step 1: Current OpenAI tools**
```python
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]
```

**Step 2: Convert to UTCP universal format**
```python
from utcp import Tool, ToolParameter

# Convert manually (one-time migration)
utcp_tools = [
    Tool(
        name="get_weather",
        description="Get weather for location",
        parameters=[
            ToolParameter(
                name="location",
                type="string",
                description="City name",
                required=True
            ),
            ToolParameter(
                name="units",
                type="string",
                description="Temperature units",
                required=False,
                enum=["celsius", "fahrenheit"]
            )
        ]
    ),
    Tool(
        name="search_web",
        description="Search the web",
        parameters=[
            ToolParameter(
                name="query",
                type="string",
                description="Search query",
                required=True
            )
        ]
    )
]
```

**Step 3: Use with both OpenAI and Anthropic**
```python
from utcp.adapters import OpenAIAdapter, AnthropicAdapter

# OpenAI (generate OpenAI schema from UTCP)
openai_adapter = OpenAIAdapter()
openai_schema = openai_adapter.convert_tools(utcp_tools)

response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=openai_schema
)

# Anthropic (generate Anthropic schema from UTCP)
anthropic_adapter = AnthropicAdapter()
anthropic_schema = anthropic_adapter.convert_tools(utcp_tools)

response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...],
    tools=anthropic_schema
)
```

**Migration benefits:**
- Define tools once in UTCP format
- Generate OpenAI/Anthropic schemas automatically
- Switch frameworks without rewriting tools
- Add new frameworks (Langchain, etc.) easily
- Maintain single source of truth"
```

---

## Example 6: "tool invocation vs function call"

### User Request
```
"What's the difference between UTCP tool invocation and a function call?"
```

### Ambiguity Detected
- Confusion between UTCP invocation (protocol concept) and Python function call
- Need to clarify layers

### Semantic Validation Process

**Step 1: Explain Layers**
```
There are three layers to understand:

1. **UTCP Tool Invocation** (protocol layer)
   - AI requests tool execution via framework
   - UTCP adapter handles framework-specific request format
   - Example: Claude requests tool "search_web" with arguments
   - Not actual code execution yet

2. **Function Call** (implementation layer)
   - Actual Python function execution
   - Your implementation code runs
   - Example: search_web("Python tutorials") executes search logic
   - Real computation happens here

3. **Adapter Bridge** (connection layer)
   - UTCP adapter connects invocation → function call
   - Extracts arguments from framework format
   - Calls Python function with correct parameters
   - Returns result to framework

**Flow:** AI tool invocation → UTCP adapter → Python function call → Result
```

**Step 2: Show Complete Flow**
```
"Here's the complete invocation flow:

**1. Define UTCP tool and implementation:**
```python
from utcp import Tool, ToolParameter

# UTCP tool definition (protocol layer)
search_tool = Tool(
    name="search_web",
    description="Search the web",
    parameters=[
        ToolParameter(name="query", type="string", required=True),
        ToolParameter(name="num_results", type="integer", required=False, default=5)
    ]
)

# Python implementation (function layer)
def search_web_impl(query: str, num_results: int = 5) -> str:
    """Actual search logic"""
    results = api_search(query, num_results)
    return format_results(results)
```

**2. AI makes tool invocation:**
```python
from utcp.adapters import AnthropicAdapter

adapter = AnthropicAdapter()
anthropic_tools = adapter.convert_tools([search_tool])

# AI receives tools and decides to invoke
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Search for Python tutorials"}],
    tools=anthropic_tools
)

# Response contains tool_use block (invocation request)
# {
#   "type": "tool_use",
#   "id": "toolu_123",
#   "name": "search_web",
#   "input": {"query": "Python tutorials", "num_results": 5}
# }
```

**3. UTCP adapter bridges to function call:**
```python
# Extract tool invocations from response
tool_calls = adapter.extract_tool_calls(response)

for tool_call in tool_calls:
    # tool_call.name = "search_web"
    # tool_call.arguments = {"query": "Python tutorials", "num_results": 5}

    # Adapter calls Python function with extracted arguments
    result = adapter.execute_tool(
        search_tool,      # UTCP tool definition
        tool_call,        # Invocation from AI
        search_web_impl   # Python function to execute
    )

    # result = search_web_impl(query="Python tutorials", num_results=5)
    # Python function executes, returns search results
```

**Key distinctions:**
- **Tool invocation** = AI requesting tool execution (framework API layer)
- **Function call** = Actual Python code execution (implementation layer)
- **UTCP adapter** = Bridges the two (extracts arguments, calls function, formats result)

**Without UTCP:** You manually parse framework responses and call functions
**With UTCP:** Adapter handles parsing and calling automatically"
```

---

## Pattern Summary

Common UTCP ambiguity patterns:

1. **"tool calling"** → UTCP universal calling (framework-agnostic) vs framework-specific (OpenAI/Anthropic)
2. **"tool schema"** → UTCP universal schema vs framework-specific schemas (OpenAI/Anthropic formats)
3. **"adapter"** → UTCP framework adapter (converts schemas/handles invocations) vs general adapter pattern
4. **"invocation"** → UTCP tool invocation (AI requesting execution) vs Python function call (actual execution)
5. **"function calling"** → AI framework feature (OpenAI/Anthropic) vs UTCP protocol (universal layer)
6. **"portable tools"** → UTCP tools (work across frameworks) vs framework-specific tools (locked to one platform)

**Key insights:**
- **UTCP = Universal layer** above framework-specific function calling
- **Adapters bridge** UTCP universal format ↔ framework-specific formats
- **Define once, run anywhere** - core UTCP value proposition
- **Invocation ≠ execution** - invocation is request, execution is running code

Always clarify if user wants framework-agnostic (UTCP) or single-platform (framework-specific) before implementing!
