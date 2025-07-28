from dataclasses import dataclass
from typing import ClassVar

from openhands.core.schema import ActionType
from openhands.events.action.action import (
    Action,
    ActionConfirmationStatus,
    ActionSecurityRisk,
)


@dataclass
class WebSearchAction(Action):
    query: str
    thought: str = ''
    action: str = ActionType.WEB_SEARCH
    runnable: ClassVar[bool] = True
    confirmation_state: ActionConfirmationStatus = ActionConfirmationStatus.CONFIRMED
    security_risk: ActionSecurityRisk | None = None

    @property
    def message(self) -> str:
        return f'Searching the web for: {self.query}'

    def __str__(self) -> str:
        ret = f'**WebSearchAction (source={self.source})**\n'
        if self.thought:
            ret += f'THOUGHT: {self.thought}\n'
        ret += f'QUERY: {self.query}'
        return ret
