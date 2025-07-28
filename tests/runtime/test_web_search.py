"""Web search tool tests for the CLIRuntime."""

import pytest
from conftest import (
    _close_test_runtime,
    _load_runtime,
)

from openhands.core.logger import openhands_logger as logger
from openhands.events.action import WebSearchAction
from openhands.events.observation import ErrorObservation, WebSearchObservation
from openhands.events.tool import ToolCallMetadata
from openhands.runtime.impl.cli.cli_runtime import CLIRuntime


def _run_web_search_action(runtime, query: str):
    action = WebSearchAction(query=query)
    logger.info(action, extra={'msg_type': 'ACTION'})
    obs = runtime.run_action(action)
    assert isinstance(obs, (WebSearchObservation, ErrorObservation))
    logger.info(obs, extra={'msg_type': 'OBSERVATION'})
    return obs


def test_web_search_tool_basic(temp_dir):
    """Test that the web search tool can be called and returns a hardcoded response."""
    runtime_cls = CLIRuntime
    runtime, config = _load_runtime(temp_dir, runtime_cls)
    try:
        # Test the web search functionality directly
        search_query = "cats and dogs"

        obs = _run_web_search_action(runtime, search_query)
        # print the observation so I can see it
        assert isinstance(obs, WebSearchObservation)
        assert obs.query == search_query
        print(f"Type of obs.content: {type(obs.content)}")
        print(f"obs.content: {repr(obs.content)}")
        assert search_query in obs.content

    finally:
        _close_test_runtime(runtime)

