from litellm import ChatCompletionToolParam, ChatCompletionToolParamFunctionChunk

from openhands.llm.tool_names import WEB_SEARCH_TOOL_NAME

_DETAILED_WEB_SEARCH_DESCRIPTION = """Search the web for images and information using Bravo web search.

This tool allows you to search the web and find relevant images and information based on your query.

### Usage
* Provide a search query to find relevant web content and images
* The tool will return search results including images, titles, and descriptions
* Results are formatted for easy consumption by the agent

### Best Practices
* Use specific and descriptive search queries for better results
* Include relevant keywords related to what you're looking for
* The tool is particularly useful for finding images and visual content
"""

_SHORT_WEB_SEARCH_DESCRIPTION = """Search the web for images and information. Provide a search query to find relevant web content and images."""


def create_web_search_tool(
    use_short_description: bool = False,
) -> ChatCompletionToolParam:
    description = (
        _SHORT_WEB_SEARCH_DESCRIPTION if use_short_description else _DETAILED_WEB_SEARCH_DESCRIPTION
    )
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=WEB_SEARCH_TOOL_NAME,
            description=description,
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
