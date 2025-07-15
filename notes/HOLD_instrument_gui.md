# Goal: instrument the crucial parts of the openhands server

I want to find out how the agent works. I want to see every LLM call, and the loop of making calls, and decisions that it makes.

## FIRST PRIORITY

get built-in litellm instrumentation working!

The [instruction](https://docs.litellm.ai/docs/observability/opentelemetry_integration) page says to add: `litellm.callbacks = ["otel"]`

**ANSWER: Add it in `openhands/core/logger.py`**

This file already imports and configures litellm (lines 24-40). Add the callback line right after the existing litellm configuration:

```python
# Around line 41, after the existing litellm config:
litellm.callbacks = ["otel"]
```

This is the perfect spot because:

1. litellm is already imported here
2. Other litellm global settings are configured here (suppress_debug_info, set_verbose)
3. This runs early in the application startup
4. It's centralized with other logging configuration

## FOR LATER - STOP HERE

### 1. Main Agent Execution Loop

**Location**: `openhands/core/loop.py` - `run_agent_until_done()`

- Simple loop that runs until agent reaches terminal state
- Sleeps 1 second between checks
- **Instrument**: Loop iterations, state transitions, total execution time

**Location**: `openhands/controller/agent_controller.py` - `_step()` method

- Core agent step execution (line ~758)
- Checks agent state, handles pending actions
- Calls `self.agent.step(self.state)` to get next action
- **Instrument**: Step timing, action generation, state changes

### 2. LLM Call Chain (THE CRITICAL PATH)

**Location**: `openhands/agenthub/codeact_agent/codeact_agent.py` - `step()` method

- Line ~150: Main agent decision point
- Line ~191: Builds messages from conversation history
- Line ~197: **THE LLM CALL** - `self.llm.completion(**params)`
- Line ~199: Parses response into actions
- **Instrument**: Prompt construction, LLM latency, response parsing

**Location**: `openhands/llm/llm.py` - `wrapper()` function (line ~220)

- Actual LLM completion call with retry logic
- Line ~299: Records start time for latency
- Line ~314: Makes the litellm call
- **Instrument**: Request/response, tokens, cost, retries, latency

### 3. Action Execution & Observation Loop

**Location**: `openhands/runtime/base.py` - `_handle_action()` method

- Line ~335: Handles incoming actions from agent
- Line ~345: Executes action in runtime environment
- Returns observations back to agent
- **Instrument**: Action type, execution time, success/failure

### 4. Event Flow & Communication

**Location**: `openhands/events/stream.py` - `add_event()` method

- Line ~164: All events flow through here
- Assigns IDs, timestamps, sources to events
- **Instrument**: Event throughput, queue depth, processing latency

### 5. Agent State Management

**Location**: `openhands/controller/agent_controller.py` - `set_agent_state_to()` method

- Line ~568: State transitions (RUNNING, WAITING, ERROR, etc.)
- Critical for understanding agent lifecycle
- **Instrument**: State duration, transition reasons

## The Decision-Making Flow to Instrument

```
1. AgentController._step()
   ↓
2. CodeActAgent.step(state)
   ↓
3. _get_messages() - builds prompt from history
   ↓
4. llm.completion() - THE LLM CALL
   ↓
5. response_to_actions() - parses LLM response
   ↓
6. Action added to EventStream
   ↓
7. Runtime._handle_action() - executes action
   ↓
8. Observation returned to EventStream
   ↓
9. State updated with action/observation
   ↓
10. Loop continues...
```

## Specific Instrumentation Points

### LLM Calls (High Priority)

- **File**: `openhands/llm/llm.py`, line ~314
- **What**: Every completion call with prompt, response, tokens, cost
- **Why**: Core AI decision-making visibility

### Agent Steps (High Priority)

- **File**: `openhands/controller/agent_controller.py`, line ~758
- **What**: Step timing, action generated, state before/after
- **Why**: Agent behavior and performance

### Action Execution (Medium Priority)

- **File**: `openhands/runtime/base.py`, line ~335
- **What**: Action type, execution time, success/error
- **Why**: Understanding what agent actually does

### Event Processing (Medium Priority)

- **File**: `openhands/events/stream.py`, line ~164
- **What**: Event throughput, queue metrics
- **Why**: System performance and bottlenecks
