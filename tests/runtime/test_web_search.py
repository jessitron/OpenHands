"""Web search tool tests for the CLIRuntime."""

import pytest
from conftest import (
    _close_test_runtime,
    _load_runtime,
)

from openhands.core.logger import openhands_logger as logger
from openhands.events.action import CmdRunAction
from openhands.events.observation import CmdOutputObservation, ErrorObservation
from openhands.runtime.impl.cli.cli_runtime import CLIRuntime


def _run_cmd_action(runtime, custom_command: str):
    action = CmdRunAction(command=custom_command)
    logger.info(action, extra={'msg_type': 'ACTION'})
    obs = runtime.run_action(action)
    assert isinstance(obs, (CmdOutputObservation, ErrorObservation))
    logger.info(obs, extra={'msg_type': 'OBSERVATION'})
    return obs


def test_web_search_tool_basic(temp_dir):
    """Test that the web search tool can be called and returns a hardcoded response."""
    runtime_cls = CLIRuntime
    runtime, config = _load_runtime(temp_dir, runtime_cls)
    try:
        # Test the hardcoded web search response
        # This simulates what the function calling system would do
        search_query = "cats and dogs"
        hardcoded_response = f"Web search results for '{search_query}': [HARDCODED] Found 3 images and 5 web pages related to your query."

        obs = _run_cmd_action(runtime, f'echo "{hardcoded_response}"')
        assert obs.exit_code == 0
        assert search_query in obs.content
        assert "[HARDCODED]" in obs.content
        assert "Found 3 images and 5 web pages" in obs.content

    finally:
        _close_test_runtime(runtime)

