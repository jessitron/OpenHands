# Active work: add a tool for Bravo web search to the CLI

I want the CLI to be able to search the web and find images.
We would do this with an MCP, but that isn't fully implemented in CLI mode, trust me on this.
Instead, we will add a hard-coded tool. This will be well-suited to what I want to demonstrate, which is: how the new feature shows up in traces.

It should be a lot like the bash execution tool defined in openhands/agenthub/codeact_agent/tools/bash.py

It will be added to the agent in openhands/agenthub/codeact_agent/codeact_agent.py, _get_tools method.

The actual shell command is run in openhands/runtime/impl/cli/cli_runtime.py, method _execute_shell_command

Please only execute actions specified in this file, and add any answers and recommendations to this file. This is the record of our feature implementation.

## Step 1, Testing

I want to implement the actual search code first, in a way that we can test it.

Are there any tests around _execute_shell_command ?

If not, how would you recommend adding them?

### Analysis of existing tests:

Yes, there are extensive tests around `_execute_shell_command` in the CLI runtime! The main test file is `tests/runtime/test_bash.py` which contains comprehensive tests for command execution across different runtime types including CLIRuntime.

Key findings:
1. **Existing test patterns**: The tests use a helper function `_run_cmd_action()` that creates a `CmdRunAction` and calls `runtime.run_action()`, which internally calls `_execute_shell_command` for CLIRuntime.

2. **Test structure**: Tests are parameterized to run across different runtime types (CLIRuntime, DockerRuntime, etc.) using fixtures from `tests/runtime/conftest.py`.

3. **CLI-specific tests**: There are several tests specifically for CLIRuntime behavior, like `test_cliruntime_multiple_newline_commands()` and various timeout/command execution tests.

4. **Test utilities**: The `conftest.py` provides utilities like `_load_runtime()` to set up test runtimes with proper configuration.

### Recommendation for testing the image search tool:

1. **Create a dedicated test file**: `tests/unit/test_image_search_tool.py` to test the image search functionality in isolation
2. **Add integration tests**: Extend `tests/runtime/test_bash.py` or create a new file to test the tool integration with the CLI runtime
3. **Mock external dependencies**: Since we'll be calling external search APIs, we should mock those calls in unit tests
4. **Test the tool creation**: Test that the tool is properly created and added to the agent's tool list

The existing test infrastructure is robust and we can follow the same patterns used for the bash tool testing.

## Step 2, Implementation Plan

Based on the analysis of the existing bash tool implementation, here's the recommended approach:

### 2.1 Tool Structure (following bash.py pattern):
1. **Create `openhands/agenthub/codeact_agent/tools/image_search.py`**:
   - Define tool description and parameters
   - Create `create_image_search_tool()` function similar to `create_cmd_run_tool()`
   - Use proper tool name constant from `openhands/llm/tool_names.py`

### 2.2 Tool Integration:
1. **Add tool name constant** to `openhands/llm/tool_names.py`
2. **Modify `codeact_agent.py`**:
   - Import the new tool creation function
   - Add tool to `_get_tools()` method with appropriate config flag
3. **Add configuration option** for enabling/disabling the image search tool

### 2.3 Runtime Integration:
1. **Extend CLI runtime** to handle the new tool action type
2. **Implement search logic** in `cli_runtime.py` similar to how `_execute_shell_command` works
3. **Use existing shell command execution** to call external search tools (like curl with search APIs)

### 2.4 Testing Strategy:
1. **Unit tests** for tool creation and parameter validation
2. **Integration tests** for runtime execution with mocked API calls
3. **End-to-end tests** with the full agent workflow

This approach leverages the existing, well-tested infrastructure while adding the new image search capability.

## Step 3, Understanding Runtime vs CLI Runtime

**IMPORTANT CLARIFICATION**: The runtime and CLI runtime are fundamentally different:

### Runtime Architecture:
1. **Base Runtime** (`openhands/runtime/base.py`): Abstract base class that defines the interface
2. **Different Runtime Implementations**:
   - **DockerRuntime**: Runs in Docker containers with action execution server
   - **LocalRuntime**: Local execution with action execution server
   - **CLIRuntime**: Direct local execution WITHOUT action execution server
   - **KubernetesRuntime**, etc.

### Key Differences:

**DockerRuntime/LocalRuntime/etc.**:
- Use `ActionExecutionServer` with `BashSession` (tmux-based)
- Commands go through: Agent → Runtime → ActionExecutionServer → BashSession → tmux
- Persistent shell sessions with complex state management
- Support for interactive commands, timeouts, process management

**CLIRuntime**:
- Direct subprocess execution via `_execute_shell_command()`
- Commands go through: Agent → CLIRuntime → subprocess.Popen(['bash', '-c', command])
- Each command is a separate process (no persistent session)
- Simpler but more limited functionality

### For Image Search Tool:

Since we're targeting CLI mode specifically, we need to:
1. **Create the tool definition** (same as other runtimes)
2. **Handle it in CLIRuntime** by extending the `run()` method to recognize a new action type
3. **NOT use the ActionExecutionServer** - that's only for other runtimes

The tool will create a new Action type (like `CmdRunAction`) that CLIRuntime can handle directly.

## Step 4, Revised Implementation Plan

Given the CLI runtime architecture, here's the corrected approach:

### 4.1 Create New Action Type:
1. **Define `ImageSearchAction`** in `openhands/events/action/` (similar to `CmdRunAction`)
2. **Add corresponding observation type** `ImageSearchObservation`

### 4.2 Tool Definition:
1. **Create `openhands/agenthub/codeact_agent/tools/image_search.py`**
2. **Add tool name** to `openhands/llm/tool_names.py`
3. **Update function calling** in `openhands/agenthub/codeact_agent/function_calling.py` to handle the new tool

### 4.3 CLI Runtime Integration:
1. **Add `image_search()` method** to `CLIRuntime` class
2. **Method will use `_execute_shell_command()`** to call external search APIs (curl, etc.)
3. **Return `ImageSearchObservation`** with search results

### 4.4 Testing Strategy:
1. **Unit tests** for the new Action/Observation types
2. **Tool creation tests** similar to bash tool tests
3. **CLI runtime integration tests** with mocked API responses
4. **End-to-end tests** in the CLI context

This approach correctly targets the CLI runtime's direct execution model rather than trying to use the ActionExecutionServer pattern from other runtimes.

