#!/usr/bin/env python3
"""Test script to check if the web search tool is loaded in the agent."""

import sys
import os

# Add the openhands directory to the Python path
sys.path.insert(0, '/workspaces/openhands')

# Set minimal environment to avoid config issues
os.environ['OPENHANDS_DISABLE_TELEMETRY'] = '1'

try:
    # Import the agent and check its tools
    from openhands.agenthub.codeact_agent.codeact_agent import CodeActAgent
    from openhands.core.config import AgentConfig
    
    print("✅ Successfully imported CodeActAgent")
    
    # Create a minimal config
    config = AgentConfig()
    
    # Create a mock LLM (we won't actually use it)
    class MockLLM:
        def __init__(self):
            self.config = type('Config', (), {'model': 'mock-model'})()
    
    llm = MockLLM()
    
    # Create the agent
    agent = CodeActAgent(llm=llm, config=config)
    
    print(f"✅ Agent created successfully!")
    print(f"   Number of tools: {len(agent.tools)}")
    
    # Check tool names
    tool_names = [tool['function']['name'] for tool in agent.tools]
    print(f"   Tool names: {tool_names}")
    
    # Check if web_search is in the tools
    if 'web_search' in tool_names:
        print("🎉 Web search tool is successfully loaded in the agent!")
        
        # Find the web search tool
        web_search_tool = None
        for tool in agent.tools:
            if tool['function']['name'] == 'web_search':
                web_search_tool = tool
                break
        
        if web_search_tool:
            print(f"   Web search tool description: {web_search_tool['function']['description'][:100]}...")
            print(f"   Web search tool parameters: {list(web_search_tool['function']['parameters']['properties'].keys())}")
    else:
        print("❌ Web search tool is NOT loaded in the agent!")
        print("   Available tools:", tool_names)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
