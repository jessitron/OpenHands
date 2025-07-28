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

