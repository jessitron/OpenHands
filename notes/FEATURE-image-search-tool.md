# Active work: add a tool for Bravo web search to the CLI

I want the CLI to be able to search the web and find images.
We would do this with an MCP, but that isn't fully implemented in CLI mode, trust me on this.
Instead, we will add a hard-coded tool. This will be well-suited to what I want to demonstrate, which is: how the new feature shows up in traces.

It should be a lot like the bash execution tool defined in openhands/agenthub/codeact_agent/tools/bash.py

It will be added to the agent in openhands/agenthub/codeact_agent/codeact_agent.py, _get_tools method.

The actual shell command is run in openhands/runtime/impl/cli/cli_runtime.py, method _execute_shell_command

there are tests in tests/runtime/test_bash.py for the shell command. We'll want to create a test file there, but it will be much simpler and work only for the CLIRuntime.

Please only execute actions specified in this file, and add any answers and recommendations to this file. This is the record of our feature implementation.

## Step 1, Outline of a Tool

First, let's implement a tool that does nothing except return a hardcoded string. This will get the structure of the tool in place.

The tool implementation will be stubbed out, but let's make the CLI think it has this tool.

What will you need to do to implement a new tool called WebSearchTool?

### Analysis and Implementation Plan

Based on my analysis of the codebase, here's what needs to be done to implement a new `WebSearchTool`:

#### 1. Tool Definition Structure
Following the pattern of existing tools like `bash.py`, I need to create:
- A tool definition file: `openhands/agenthub/codeact_agent/tools/web_search.py`
- A tool name constant in `openhands/llm/tool_names.py`
- Integration in the agent's `_get_tools()` method in `codeact_agent.py`
- Function calling support in `function_calling.py`
- A corresponding action class if needed
- Tests in `tests/runtime/test_web_search.py`

#### 2. Tool Components Needed
- **Tool Definition**: A `ChatCompletionToolParam` object with function name, description, and parameters
- **Tool Name Constant**: Add `WEB_SEARCH_TOOL_NAME = 'web_search'` to `tool_names.py`
- **Function Calling Handler**: Add a case in `response_to_actions()` to convert tool calls to actions
- **Action Class**: Create a new action class or reuse existing ones (likely `CmdRunAction`)
- **Runtime Integration**: Handle the tool execution in `cli_runtime.py`

#### 3. Implementation Steps
1. Create the tool definition with hardcoded response
2. Add tool name constant
3. Integrate tool into agent's tool list
4. Add function calling support
5. Create basic tests
6. Test the integration

#### 4. Tool Structure Pattern
Looking at `bash.py`, the pattern is:
```python
def create_web_search_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=WEB_SEARCH_TOOL_NAME,
            description="Search the web for images and information",
            parameters={
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The search query to execute',
                    },
                },
                'required': ['query'],
            },
        ),
    )
```

This analysis shows that implementing a new tool requires coordinated changes across multiple files, following the established patterns in the codebase.

## Step 1 Implementation - COMPLETED ✅

I have successfully implemented the basic WebSearchTool structure with a hardcoded response. Here's what was accomplished:

### Files Created/Modified:
1. **`openhands/agenthub/codeact_agent/tools/web_search.py`** - Tool definition with hardcoded response
2. **`openhands/llm/tool_names.py`** - Added `WEB_SEARCH_TOOL_NAME = 'web_search'`
3. **`openhands/agenthub/codeact_agent/codeact_agent.py`** - Integrated tool into agent's `_get_tools()` method
4. **`openhands/agenthub/codeact_agent/function_calling.py`** - Added function calling support
5. **`openhands/agenthub/codeact_agent/tools/__init__.py`** - Exported the new tool
6. **`tests/runtime/test_web_search.py`** - Basic tests for the tool

### Verification Results:
- ✅ Tool creation works correctly
- ✅ Web search tool is loaded in the agent (shows up in tool list)
- ✅ Function calling logic processes web search requests
- ✅ Hardcoded response is generated correctly
- ✅ Tool has proper parameters (requires 'query')

### Current Behavior:
When the agent receives a web search tool call with a query like "cats and dogs", it generates a `CmdRunAction` with the command:
```bash
echo "Web search results for 'cats and dogs': [HARDCODED] Found 3 images and 5 web pages related to your query."
```

The tool is now fully integrated into the CLI agent and ready for the next step of implementation.

## Summary

✅ **Step 1 Complete**: Basic WebSearchTool with hardcoded response has been successfully implemented and integrated into the OpenHands CLI agent.

### What was accomplished:
- Created a complete tool definition following OpenHands patterns
- Integrated the tool into the agent's tool registry
- Added function calling support to convert tool calls to actions
- Verified the tool appears in the agent's tool list (7 tools total including web_search)
- Confirmed the tool generates appropriate CmdRunAction responses
- All integration tests pass

### Current functionality:
When an LLM calls the web_search tool with a query, it generates a bash command that echoes a hardcoded response. This demonstrates that:
1. The tool is properly registered and available to the agent
2. Function calling correctly processes web search requests
3. The tool integrates seamlessly with the existing CLI runtime
4. The response format is consistent with other tools

### Next steps for full implementation:
1. Replace the hardcoded response with actual Bravo web search API calls
2. Add proper error handling for network requests
3. Format search results (images, titles, descriptions) appropriately
4. Add configuration for search parameters (number of results, etc.)
5. Implement proper testing with mock API responses
6. Add tracing/logging for search operations

The foundation is solid and ready for the actual web search implementation.

## Testing the Implementation

To run the web search tool tests:

```bash
cd /workspaces/openhands
poetry install --with test
poetry run python -m pytest tests/runtime/test_web_search.py -v
```

This will run the test suite that verifies:
- Basic web search tool functionality with hardcoded responses
- Different query types and special characters handling
- Integration with CLIRuntime

## Now make it better

Look, don't reuse CmdRunAction. This is not a command run, it is a new thing. It is a WebSearchAction, and it needs a new _execute_web_search function like _execute_shell_command in openhands/runtime/impl/cli/cli_runtime.py

Make it a new WebSearchObservation etc, give it all the structure of a real tool. The hardcoded response value should be in its new _execute_web_search function.

