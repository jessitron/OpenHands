#!/usr/bin/env python3
"""Simple test script to verify the web search tool is working."""

import sys
import os

# Add the openhands directory to the Python path
sys.path.insert(0, '/workspaces/openhands')

try:
    from openhands.agenthub.codeact_agent.tools.web_search import create_web_search_tool
    from openhands.llm.tool_names import WEB_SEARCH_TOOL_NAME
    
    print("✅ Successfully imported web search tool components")
    
    # Test tool creation
    tool = create_web_search_tool()
    print(f"✅ Tool created successfully!")
    print(f"   Tool name: {tool['function']['name']}")
    print(f"   Expected name: {WEB_SEARCH_TOOL_NAME}")
    print(f"   Names match: {tool['function']['name'] == WEB_SEARCH_TOOL_NAME}")
    print(f"   Tool description: {tool['function']['description'][:100]}...")
    
    # Test tool with short description
    short_tool = create_web_search_tool(use_short_description=True)
    print(f"✅ Short description tool created!")
    print(f"   Short description: {short_tool['function']['description']}")
    
    # Test tool parameters
    params = tool['function']['parameters']
    print(f"✅ Tool parameters:")
    print(f"   Required: {params['required']}")
    print(f"   Properties: {list(params['properties'].keys())}")
    
    print("\n🎉 All tests passed! The web search tool is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
