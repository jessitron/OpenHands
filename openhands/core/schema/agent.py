from enum import Enum


class AgentState(str, Enum):
    LOADING = 'loading'
    """The agent is loading.
    """

    RUNNING = 'running'
    """The agent is running.
    """

    AWAITING_USER_INPUT = 'awaiting_user_input'
    """The agent is awaiting user input. Begin here after boot. this could be permission for action or for clarification, Ray says
    """

    PAUSED = 'paused'
    """The agent is temporarily paused and can be resumed.

    This is a resumable state that preserves the agent's context, memory, and pending actions.
    The agent can be resumed using commands like /resume in CLI and will continue from where it left off.
    """

    STOPPED = 'stopped'
    """The agent is completely stopped and cannot be resumed.

    This is a terminal state that ends the agent session. When stopped, the agent's state is reset,
    pending actions are cleared, and the session must be restarted to continue working.
    """

    FINISHED = 'finished'
    """The agent is finished with the current task.
    """

    REJECTED = 'rejected'
    """The agent rejects the task.
    """

    ERROR = 'error'
    """An error occurred during the task.
    """

    AWAITING_USER_CONFIRMATION = 'awaiting_user_confirmation'
    """The agent is awaiting user confirmation.
    """

    USER_CONFIRMED = 'user_confirmed'
    """The user confirmed the agent's action.
    """

    USER_REJECTED = 'user_rejected'
    """The user rejected the agent's action.
    """

    RATE_LIMITED = 'rate_limited'
    """The agent is rate limited.
    """
