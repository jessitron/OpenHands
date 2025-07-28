#!/usr/bin/env python3
"""Test script to check if the web search tool function calling works."""

import sys
import os
import json

# Add the openhands directory to the Python path
sys.path.insert(0, '/workspaces/openhands')

# Set minimal environment to avoid config issues
os.environ['OPENHANDS_DISABLE_TELEMETRY'] = '1'

try:
    from openhands.agenthub.codeact_agent.function_calling import response_to_actions
    from openhands.events.action import CmdRunAction
    
    print("✅ Successfully imported function calling components")
    
    # Create a mock ModelResponse with a web search tool call
    class MockToolCall:
        def __init__(self):
            self.id = "test_call_123"
            self.function = type('Function', (), {
                'name': 'web_search',
                'arguments': json.dumps({'query': 'test search query'})
            })()
    
    class MockMessage:
        def __init__(self):
            self.content = "I'll search for that information."
            self.tool_calls = [MockToolCall()]
    
    class MockChoice:
        def __init__(self):
            self.message = MockMessage()
    
    class MockResponse:
        def __init__(self):
            self.id = "response_123"
            self.choices = [MockChoice()]
    
    # Test the function calling
    response = MockResponse()
    actions = response_to_actions(response)
    
    print(f"✅ Function calling processed successfully!")
    print(f"   Number of actions: {len(actions)}")
    
    if len(actions) > 0:
        action = actions[0]
        print(f"   Action type: {type(action).__name__}")
        
        if isinstance(action, CmdRunAction):
            print(f"   Command: {action.command}")
            print(f"   Contains query: {'test search query' in action.command}")
            print(f"   Contains hardcoded response: {'[HARDCODED]' in action.command}")
            
            if 'test search query' in action.command and '[HARDCODED]' in action.command:
                print("🎉 Web search function calling is working correctly!")
            else:
                print("❌ Web search function calling output is not as expected")
        else:
            print(f"❌ Expected CmdRunAction, got {type(action).__name__}")
    else:
        print("❌ No actions generated from function call")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
