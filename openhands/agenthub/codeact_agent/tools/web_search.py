from litellm import ChatCompletionToolParam, ChatCompletionToolParamFunctionChunk

from openhands.llm.tool_names import WEB_SEARCH_TOOL_NAME

_DETAILED_WEB_SEARCH_DESCRIPTION = """Search the web for images using Bravo web search.

### Usage
* Provide a search query to find relevant images
* The tool will return search results including image URLs, titles, and descriptions

### Hint
* Later, you can use wget to download images
"""

WebSearchTool = ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=WEB_SEARCH_TOOL_NAME,
            description=_DETAILED_WEB_SEARCH_DESCRIPTION,
            parameters={
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The search query to execute. Use specific and descriptive terms for better results.',
                    },
                },
                'required': ['query'],
            },
        ),
    )
