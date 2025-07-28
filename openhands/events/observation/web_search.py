from dataclasses import dataclass

from openhands.core.schema import ObservationType
from openhands.events.observation.observation import Observation


@dataclass
class WebSearchObservation(Observation):
    """This data class represents the result of a web search operation."""

    query: str
    content: str
    observation: str = ObservationType.WEB_SEARCH

    def __init__(self, query: str, content: str) -> None:
        super().__init__(content)
        self.query = query
        self.content = content

    @property
    def message(self) -> str:
        return f'Web search completed for query: {self.query}'

    def __str__(self) -> str:
        ret = f'**WebSearchObservation (source={self.source})**\n'
        ret += f'QUERY: {self.query}\n'
        ret += '--BEGIN WEB SEARCH RESULTS--\n'
        ret += f'{self.content}\n'
        ret += '--END WEB SEARCH RESULTS--'
        return ret

    def to_agent_observation(self) -> str:
        """Return the content formatted for the agent."""
        return self.content
