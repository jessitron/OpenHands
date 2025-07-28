"""Web search tool tests for the CLIRuntime."""

import pytest
from conftest import (
    _close_test_runtime,
    _load_runtime,
)

from openhands.core.logger import openhands_logger as logger
from openhands.events.action import WebSearchAction
from openhands.events.observation import ErrorObservation, WebSearchObservation
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
        assert isinstance(obs, WebSearchObservation)
        assert obs.query == search_query
        assert search_query in obs.content
        assert "[HARDCODED]" in obs.content
        assert "Found 3 images and 5 web pages" in obs.content

    finally:
        _close_test_runtime(runtime)


def test_web_search_tool_different_queries(temp_dir):
    """Test that the web search tool works with different query types."""
    runtime_cls = CLIRuntime
    runtime, config = _load_runtime(temp_dir, runtime_cls)
    try:
        # Test with different query types
        test_queries = [
            "python programming",
            "machine learning algorithms",
            "web development best practices",
            "special characters: @#$%^&*()",
        ]

        for query in test_queries:
            obs = _run_web_search_action(runtime, query)
            assert isinstance(obs, WebSearchObservation)
            assert obs.query == query
            assert query in obs.content
            assert "[HARDCODED]" in obs.content

    finally:
        _close_test_runtime(runtime)


def test_web_search_tool_empty_query(temp_dir):
    """Test that the web search tool handles empty queries."""
    runtime_cls = CLIRuntime
    runtime, config = _load_runtime(temp_dir, runtime_cls)
    try:
        # Test with empty query
        obs = _run_web_search_action(runtime, "")
        assert isinstance(obs, WebSearchObservation)
        assert obs.query == ""
        assert "[HARDCODED]" in obs.content

    finally:
        _close_test_runtime(runtime)

