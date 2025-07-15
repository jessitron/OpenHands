# Current Work

I want to understand this application. I'm going to instrument it with OpenTelemetry, and get it to explain itself. (Not yet though)

I'm starting with the command-line version of the app, as described in @docs/usage/how-to/cli-mode.mdx -- but I'll be running it in development mode, as in @oh-cli

I have already added general OpenTelemetry instrumentation to the repo and to the app startup. It goes to Honeycomb, environment banana, dataset openhands-cli. If you have the Honeycomb MCP, you can find traces there. Currently, I'm only getting a few spans for jinja and HTTP libraries.

The next step in instrumentation will be custom, describing the app's flow. Before we do that, I want to understand the flow.

## Flow of the CLI app

The CLI app follows this main execution flow:

### 1. Entry Point (`openhands/cli/main.py:main()`)
- Entry point calls `main_with_loop()` which sets up event loop and exception handling
- Parses command line arguments using `parse_arguments()`
- Sets up logging level and loads configuration from TOML files and CLI args

### 2. Initial Setup (`openhands/cli/main.py:main_with_loop()`)
- Creates `FileSettingsStore` for persistent settings
- If no settings exist, runs setup flow via `run_setup_flow()` to configure LLM settings
- Loads saved settings (agent, LLM model, API key, etc.)
- Sets CLI-specific defaults like runtime='cli' and confirmation_mode=True

### 3. Session Creation (`openhands/cli/main.py:run_session()`)
Each session follows this pattern:
- **Session ID Generation**: Creates unique session ID via `generate_sid()`
- **Component Creation** (all from `openhands/core/setup.py`):
  - `create_agent()` - Creates the AI agent with LLM configuration
  - `create_runtime()` - Creates sandbox runtime environment (CLI runtime by default)
  - `create_controller()` - Creates AgentController to manage agent lifecycle
  - `create_memory()` - Creates Memory component for information retrieval
- **Repository Setup**: If selected_repo is configured, clones/initializes it
- **MCP Integration**: Adds MCP (Model Context Protocol) tools if enabled
- **Event Stream Setup**: Sets up event subscription and callbacks

### 4. Main Event Loop (`openhands/core/loop.py:run_agent_until_done()`)
- Runs until agent reaches terminal state (STOPPED, ERROR, etc.)
- Uses `controller.state.agent_state` to track current state
- Implements status callbacks for error handling

### 5. Key Components and Interactions

#### AgentController (`openhands/controller/agent_controller.py`)
- **Central orchestrator** that manages agent lifecycle and state transitions
- Handles events from event stream via `on_event()` and `_on_event()`
- Implements state machine with states like RUNNING, AWAITING_USER_INPUT, FINISHED
- Manages agent delegation for multi-agent scenarios
- Controls confirmation mode for sensitive operations

#### Event Stream (`openhands/events/stream.py`)
- **Message bus** for all communication between components
- Handles Actions (from agents) and Observations (from environment)
- Supports multiple subscribers (AGENT_CONTROLLER, MEMORY, MAIN)
- Provides event persistence and replay capabilities

#### Runtime (`openhands/runtime/base.py`)
- **Sandbox environment** providing bash shell, browser, file operations
- CLI runtime specifically provides command-line interface
- Handles action execution (CmdRunAction, FileEditAction, etc.)
- Manages plugins and microagents

#### Memory (`openhands/memory/memory.py`) 
- **Information retrieval system** that responds to RecallAction events
- Loads microagents from global, user, and repository directories
- Provides workspace context on first user message
- Handles knowledge retrieval for subsequent queries

#### Agent (`openhands/agenthub/*/`)
- **AI decision-making component** that processes state and returns actions
- Different agent types (CodeAct, browsing, etc.) in agenthub/
- Uses LLM to generate responses based on conversation history
- Implements specific behavioral patterns for different use cases

### 6. User Interaction Flow
1. User starts CLI with `openhands` command
2. System displays banner and welcome message
3. User enters task or command at prompt (`>`)
4. Commands starting with `/` are handled by `handle_commands()` 
5. Regular messages become MessageAction events
6. Agent processes message and generates response actions
7. Actions are executed in runtime, producing observations
8. Cycle continues until user exits or agent finishes

### 7. State Management
- **AgentState enum**: RUNNING, AWAITING_USER_INPUT, FINISHED, ERROR, etc.
- **State persistence**: Sessions saved to `~/.openhands/sessions`
- **Confirmation mode**: Requires user approval for sensitive operations
- **Pause/Resume**: Ctrl-P to pause, `/resume` to continue

### 8. Key Files for Instrumentation
- `openhands/cli/main.py:run_session()` - Session lifecycle
- `openhands/controller/agent_controller.py:_step()` - Agent decision steps  
- `openhands/core/loop.py:run_agent_until_done()` - Main execution loop
- `openhands/events/stream.py` - Event processing
- `openhands/runtime/base.py` - Runtime action execution
- `openhands/memory/memory.py` - Information retrieval
