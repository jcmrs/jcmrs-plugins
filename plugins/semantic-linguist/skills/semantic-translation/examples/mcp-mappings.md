# MCP-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise MCP (Model Context Protocol) implementations.

## Overview

MCP (Model Context Protocol) is a protocol for connecting AI assistants to external data sources and tools. Key concepts include:
- **Server types**: SSE (Server-Sent Events), stdio (process-based), HTTP, WebSocket
- **Components**: Tools (functions AI can call), Resources (data/content), Prompts (templates), Sampling (request generation)
- **Integration modes**: Local server, remote server, managed server

Common ambiguities arise when users use general terms like "server", "resource", "prompt", or "tool" without specifying MCP-specific context.

---

## Example 1: "set up an mcp server"

### User Request
```
"I need to set up an MCP server for my project"
```

### Ambiguity Detected
- "mcp server" - which server type? (SSE, stdio, HTTP, WebSocket)
- Unclear integration mode and use case

### Semantic Validation Process

**Step 1: Domain Identified**
- User context: Working with MCP protocol
- Needs clarification on server type

**Step 2: Query Knowledge**
- Static: MCP supports 4 server types with different characteristics
- Ontology: Server type selection depends on deployment and integration needs

**Step 3: Present Options**
```
MCP supports 4 server types, each for different scenarios:

1. **SSE (Server-Sent Events) server**
   - Web-based, real-time updates
   - Best for: Browser integrations, cloud deployments
   - Example: MCP server running on web platform with HTTP/SSE transport
   - Connection: Claude Desktop connects via HTTPS URL

2. **stdio server**
   - Process-based communication via standard input/output
   - Best for: Local tools, command-line utilities, desktop integrations
   - Example: Local Python script MCP server
   - Connection: Claude Desktop launches process and communicates via stdin/stdout

3. **HTTP server**
   - Traditional request-response HTTP API
   - Best for: RESTful integrations, stateless operations
   - Example: MCP server exposing HTTP endpoints
   - Connection: Claude Desktop makes HTTP requests

4. **WebSocket server**
   - Bidirectional, persistent connection
   - Best for: Real-time collaboration, streaming data
   - Example: MCP server with continuous updates
   - Connection: Claude Desktop maintains WebSocket connection

Which integration scenario matches your needs?"
```

**Step 4: User Clarifies**
```
User: "I want to run a local Python script that Claude can call"
```

**Step 5: Validated Translation**
```
"That's a stdio server - perfect for local Python tools! Here's the setup:

**1. Create MCP server (Python example):**
```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("my-local-tools")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_files",
            description="Search files in directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "directory": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_files":
        query = arguments["query"]
        directory = arguments.get("directory", ".")
        # Your search logic here
        results = perform_search(query, directory)
        return [TextContent(type="text", text=results)]

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))
```

**2. Configure in Claude Desktop (.mcp.json):**
```json
{
  "mcpServers": {
    "my-local-tools": {
      "command": "python",
      "args": ["/path/to/your/server.py"]
    }
  }
}
```

Claude Desktop will:
1. Launch your Python script as subprocess
2. Communicate via stdin/stdout
3. Call your tools when needed
4. Terminate process when session ends"
```

---

## Example 2: "add resources to mcp"

### User Request
```
"I want to expose some resources through MCP"
```

### Ambiguity Detected
- "resources" - could mean MCP resources (data/content) or system resources (CPU/memory)
- Need to clarify what data to expose and how

### Semantic Validation Process

**Step 1: Analyze Context**
- User working with MCP protocol
- "resources" in MCP context = data/content exposed to AI
- Need to understand what data they want to expose

**Step 2: Present Options**
```
In MCP, "resources" are data/content you expose to the AI assistant. This is different from system resources like CPU/memory.

**MCP Resource types:**

1. **Static resources** (fixed content)
   - File contents, configuration data, documentation
   - URI pattern: `file:///path/to/resource`
   - Example: Expose project README.md
   - Use case: AI reads project documentation

2. **Dynamic resources** (generated content)
   - Database query results, API responses, computed data
   - URI pattern: `custom://resource-type/identifier`
   - Example: `db://users/active` returns active users
   - Use case: AI accesses live data

3. **Template resources** (parameterized)
   - Resources with variable components
   - URI pattern with variables: `logs://{date}/{level}`
   - Example: `logs://2024-12-01/error`
   - Use case: AI queries specific log combinations

What type of data do you want to expose?"
```

**Step 3: User Clarifies**
```
User: "I want Claude to be able to read files from my project directory"
```

**Step 4: Validated Translation**
```
"That's static file resources! Here's how to expose files via MCP:

```python
from mcp.server import Server
from mcp.types import Resource, TextContent
import os

app = Server("file-resources")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available file resources"""
    project_dir = "/path/to/project"
    resources = []

    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.md', '.txt', '.py')):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, project_dir)
                resources.append(
                    Resource(
                        uri=f"file:///{relative_path}",
                        name=relative_path,
                        description=f"Project file: {relative_path}",
                        mimeType="text/plain"
                    )
                )

    return resources

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read file content"""
    # Extract path from URI
    path = uri.replace("file:///", "")
    full_path = os.path.join("/path/to/project", path)

    with open(full_path, 'r') as f:
        content = f.read()

    return content
```

**How it works:**
1. AI calls `list_resources()` to see available files
2. AI selects resource by URI: `file:///src/main.py`
3. Server reads and returns file content
4. AI uses content to answer questions about your project"
```

---

## Example 3: "use mcp prompts"

### User Request
```
"How do I use prompts in MCP?"
```

### Ambiguity Detected
- "prompts" - could mean MCP prompt templates or LLM prompts
- Need to clarify MCP-specific prompt system

### Semantic Validation Process

**Step 1: Clarify Context**
```
"In MCP, there are two types of 'prompts':

1. **MCP Prompt Templates** (structured prompt definitions)
   - Pre-defined prompt templates with variables
   - Server provides, AI uses them
   - Example: "analyze_code" prompt template with {language} and {code} variables
   - Use case: Standardized prompts for common tasks

2. **LLM Prompts** (text sent to language model)
   - General prompt text sent to Claude/GPT
   - Not MCP-specific
   - Example: "Analyze this Python code: ..."
   - Use case: Regular AI conversation

Which are you asking about?"
```

**Step 2: User Clarifies**
```
User: "I want to create reusable prompt templates with variables"
```

**Step 3: Validated Translation**
```
"That's MCP Prompt Templates! Here's how to define them:

```python
from mcp.server import Server
from mcp.types import Prompt, PromptMessage, TextContent

app = Server("prompt-templates")

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="analyze_code",
            description="Analyze code for issues and improvements",
            arguments=[
                {
                    "name": "language",
                    "description": "Programming language",
                    "required": True
                },
                {
                    "name": "code",
                    "description": "Code to analyze",
                    "required": True
                }
            ]
        ),
        Prompt(
            name="review_pr",
            description="Review pull request changes",
            arguments=[
                {
                    "name": "diff",
                    "description": "Git diff content",
                    "required": True
                },
                {
                    "name": "focus",
                    "description": "Review focus area",
                    "required": False
                }
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> PromptMessage:
    if name == "analyze_code":
        language = arguments["language"]
        code = arguments["code"]

        return PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"""Analyze this {language} code for:
- Potential bugs and errors
- Performance issues
- Best practice violations
- Security vulnerabilities

Code:
```{language}
{code}
```

Provide specific, actionable feedback."""
            )
        )

    elif name == "review_pr":
        diff = arguments["diff"]
        focus = arguments.get("focus", "general code quality")

        return PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"""Review this pull request with focus on: {focus}

Diff:
{diff}

Provide:
1. Summary of changes
2. Issues found
3. Suggestions for improvement"""
            )
        )
```

**Usage flow:**
1. AI sees available prompts via `list_prompts()`
2. User selects "analyze_code" prompt
3. AI fills variables: {language: "Python", code: "..."}
4. Server returns complete prompt text
5. AI uses generated prompt for analysis"
```

---

## Example 4: "mcp tool vs function"

### User Request
```
"What's the difference between an MCP tool and a regular function?"
```

### Ambiguity Detected
- Confusion between MCP tool definitions and Python functions
- Need to clarify MCP tool system

### Semantic Validation Process

**Step 1: Explain Distinction**
```
"MCP tools" and "regular functions" are related but different:

**MCP Tool (Definition)**:
- Schema describing function to AI
- Metadata: name, description, parameters
- Declared via @app.call_tool() decorator
- AI sees this and can request to call it

**Regular Python Function**:
- Actual implementation code
- Lives in your Python script
- Not automatically visible to AI
- Executed when MCP tool called

**Relationship:**
MCP Tool → Wrapper/Interface → Python Function

Example flow:
1. You define MCP tool "search_files" (schema)
2. You implement Python function search_files_impl() (logic)
3. AI sees tool schema, requests to call it
4. MCP server routes call to your function
5. Function executes, returns result to AI
```

**Step 2: Provide Implementation Example**
```
"Here's how they work together:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("tools-demo")

# 1. Regular Python function (implementation)
def search_files_impl(query: str, file_type: str) -> str:
    """Actual search logic"""
    # Your implementation
    results = []
    for file in os.listdir('.'):
        if file_type in file and query in read_file(file):
            results.append(file)
    return '\n'.join(results)

# 2. MCP Tool definition (schema for AI)
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_files",  # Tool name AI uses
            description="Search files by content and type",  # What AI sees
            inputSchema={  # Parameters AI must provide
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term"
                    },
                    "file_type": {
                        "type": "string",
                        "description": "File extension"
                    }
                },
                "required": ["query", "file_type"]
            }
        )
    ]

# 3. Connect tool to function (routing)
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_files":
        # Extract arguments from AI request
        query = arguments["query"]
        file_type = arguments["file_type"]

        # Call actual Python function
        results = search_files_impl(query, file_type)

        # Return results to AI
        return [TextContent(type="text", text=results)]
```

**Summary:**
- MCP Tool = What AI sees (schema/interface)
- Python Function = What executes (implementation)
- @app.call_tool() = Connects them (routing)
```

---

## Example 5: "mcp sampling"

### User Request
```
"What is MCP sampling and when would I use it?"
```

### Ambiguity Detected
- "sampling" - could mean MCP sampling feature or statistical sampling
- Need to clarify MCP-specific sampling capability

### Semantic Validation Process

**Step 1: Clarify Concept**
```
"Sampling" has different meanings depending on context:

**MCP Sampling Feature**:
- Server can request AI to generate text/responses
- Use case: Server asks AI "How would you analyze this?"
- Direction: Server → AI (reverse of normal tool calling)
- Example: Grammar checker asks AI to rephrase text

**Statistical Sampling**:
- Selecting subset of data for analysis
- Use case: Random sample of 1000 from 1M records
- Not MCP-specific, general data science concept

The MCP-specific feature is **sampling** - where your server can ask the AI to generate content.
```

**Step 2: Explain Use Cases**
```
"MCP Sampling is useful when:

1. **Content generation**
   - Server needs AI-generated text
   - Example: Documentation generator asks AI to write examples

2. **Code completion**
   - Server provides context, AI suggests code
   - Example: IDE plugin asks AI for function implementation

3. **Interactive workflows**
   - Multi-step process where server guides AI
   - Example: Interview bot asks AI to generate follow-up questions

4. **Validation/refinement**
   - Server asks AI to improve its own output
   - Example: Translation tool asks AI to refine translation

Is your server providing data to AI (tools/resources) or requesting AI-generated content (sampling)?"
```

**Step 3: User Clarifies**
```
User: "I want my server to ask Claude to generate code examples"
```

**Step 4: Validated Translation**
```
"That's MCP sampling! Here's how to implement it:

```python
from mcp.server import Server
from mcp.client import Client

app = Server("code-generator")

# Server can request AI to generate content
async def generate_code_example(language: str, description: str):
    """Ask AI to generate code via sampling"""

    # Create sampling request
    prompt = f"Write a {language} code example that {description}"

    # Request AI generation
    response = await app.sample(
        messages=[{
            "role": "user",
            "content": prompt
        }],
        maxTokens=500,
        temperature=0.7
    )

    generated_code = response.content
    return generated_code

# Example usage in a tool
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "create_example":
        language = arguments["language"]
        description = arguments["description"]

        # Server asks AI to generate
        code = await generate_code_example(language, description)

        return [TextContent(
            type="text",
            text=f"Generated example:\n\n```{language}\n{code}\n```"
        )]
```

**Workflow:**
1. User asks MCP tool to create code example
2. MCP server sends sampling request to Claude
3. Claude generates code based on description
4. Server receives generated code
5. Server returns code to user

This is **reverse direction** from normal tools:
- Normal: AI calls your functions
- Sampling: Your server requests AI generation"
```

---

## Example 6: "connect mcp to database"

### User Request
```
"I want to connect MCP to my database"
```

### Ambiguity Detected
- "connect to database" - expose database as resources or create database query tool?
- Need to clarify integration pattern

### Semantic Validation Process

**Step 1: Present Options**
```
"There are two ways to integrate databases with MCP:

1. **Database as Resources** (read-only data access)
   - Expose tables/views as MCP resources
   - AI reads data via resource URIs
   - Example: `db://users/all` returns all users
   - Best for: Data exploration, reporting, read queries
   - Pattern: Resource-based

2. **Database Query Tool** (dynamic querying)
   - Expose query function as MCP tool
   - AI constructs SQL queries and executes them
   - Example: Tool "query_db" with SQL parameter
   - Best for: Complex queries, joins, filtering
   - Pattern: Tool-based

Which approach fits your use case?"
```

**Step 2: User Clarifies**
```
User: "I want Claude to be able to query the database with SQL"
```

**Step 3: Validated Translation**
```
"That's the Database Query Tool pattern! Here's the implementation:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import sqlite3  # Or your database library

app = Server("database-access")

# Database connection
def get_db_connection():
    return sqlite3.connect('/path/to/database.db')

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_database",
            description="Execute SQL SELECT query on database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum rows to return",
                        "default": 100
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_table_schema",
            description="Get schema information for a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of table"
                    }
                },
                "required": ["table_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "query_database":
        query = arguments["query"]
        limit = arguments.get("limit", 100)

        # Validate query is SELECT only (security)
        if not query.strip().upper().startswith("SELECT"):
            return [TextContent(
                type="text",
                text="Error: Only SELECT queries allowed"
            )]

        # Execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"{query} LIMIT {limit}")

        # Format results
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        result = f"Columns: {', '.join(columns)}\n\n"
        for row in rows:
            result += f"{row}\n"

        conn.close()
        return [TextContent(type="text", text=result)]

    elif name == "get_table_schema":
        table_name = arguments["table_name"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()

        result = f"Schema for {table_name}:\n"
        for col in schema:
            result += f"- {col[1]} ({col[2]})\n"

        conn.close()
        return [TextContent(type="text", text=result)]
```

**Security considerations:**
- Only allow SELECT queries (block UPDATE, DELETE, DROP)
- Add query result limits
- Validate table/column names
- Use parameterized queries to prevent SQL injection
- Consider read-only database user

**Usage flow:**
1. AI calls `get_table_schema` to understand database structure
2. AI constructs SQL query based on user question
3. AI calls `query_database` with SQL
4. Server executes query safely
5. Results returned to AI for analysis"
```

---

## Pattern Summary

Common MCP ambiguity patterns:

1. **"mcp server"** → Which type? stdio (local process), SSE (web-based), HTTP, WebSocket
2. **"resource"** → MCP resource (data/content exposed) vs system resource (CPU/memory)
3. **"prompt"** → MCP prompt template (structured) vs LLM prompt (text)
4. **"tool"** → MCP tool definition (schema) vs Python function (implementation)
5. **"sampling"** → MCP sampling (server requests AI generation) vs statistical sampling
6. **"connect database"** → Resources (read-only data) vs Tool (query execution)

**Key distinctions:**
- **Server types** differ in transport mechanism and deployment
- **Resources** = data AI reads | **Tools** = functions AI calls | **Prompts** = templates AI uses
- **Sampling** reverses direction: server requests AI, not AI calls server

Always clarify integration pattern and MCP component type before implementing!
