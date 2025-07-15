# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Build and Setup

- `make build` - Complete project build including environment setup and dependencies
- `make setup-config` - Interactive setup of config.toml for LLM API key and workspace
- `make setup-config-basic` - Create basic config.toml with default workspace

### Running the Application

- `make run` - Start full application (backend on port 3000, frontend on port 3001)
- `make start-backend` - Start backend server only
- `make start-frontend` - Start frontend server only
- `make openhands-cloud-run` - Run for cloud deployment (binds to 0.0.0.0)

### Development Tools

- `make lint` - Run all linters (frontend and backend)
- `make lint-backend` - Run Python linters (ruff, pre-commit hooks)
- `make lint-frontend` - Run frontend linters (eslint, prettier)
- `make test` - Run frontend tests
- `make test-frontend` - Run frontend tests specifically

### Frontend Development

- `cd frontend && npm run dev` - Start frontend dev server
- `cd frontend && npm run build` - Build frontend
- `cd frontend && npm run test` - Run frontend tests
- `cd frontend && npm run typecheck` - Run TypeScript type checking

### Backend Development

- `poetry run pytest ./tests/unit/test_*.py` - Run unit tests
- `poetry run uvicorn openhands.server.listen:app --reload` - Start backend with hot reload

### Docker Development

- `make docker-dev` - Build and run in Docker container
- `make docker-run` - Run application in Docker

### Dependency Management

- `poetry add <package>` - Add Python dependency
- `poetry lock --no-update` - Update poetry.lock after adding dependencies
- `cd frontend && npm install <package>` - Add frontend dependency

## Observability

When running locally, traces go to Honeycomb in environment banana. Datasets include openhands, openhands-cli, and openhands-runtime.

### Get a recent trace

Use the Honeycomb MCP. Run a query for trace.trace_id and name, where meta.signal_type=trace, in the last 10-30 minutes. Then fetch a trace by trace ID.
Link me to the trace in this format: https://ui.honeycomb.io/modernity/environments/banana/trace?trace_id=<traceId>

## High-Level Architecture

### Project Structure

OpenHands is a full-stack application with Python backend and React frontend:

- **Backend (`/openhands/`)**: Python-based AI agent platform using FastAPI
- **Frontend (`/frontend/`)**: React application with TypeScript, Vite, and TailwindCSS
- **Runtime (`/openhands/runtime/`)**: Sandboxed execution environment with Docker support
- **Agents (`/openhands/agenthub/`)**: Different AI agent implementations (CodeAct, Browsing, etc.)

### Key Backend Components

- **Server (`/openhands/server/`)**: FastAPI application with WebSocket support
- **Controller (`/openhands/controller/`)**: Agent orchestration and state management
- **Events (`/openhands/events/`)**: Event-driven architecture for actions and observations
- **LLM (`/openhands/llm/`)**: Language model integration with litellm
- **Runtime (`/openhands/runtime/`)**: Sandboxed execution environment
- **Memory (`/openhands/memory/`)**: Conversation memory and context management

### Key Frontend Components

- **Routes (`/frontend/src/routes/`)**: React Router v7 with file-based routing
- **State (`/frontend/src/state/`)**: Redux Toolkit for state management
- **Services (`/frontend/src/services/`)**: API communication and business logic
- **Components**: Reusable UI components with HeroUI and TailwindCSS

### Agent System

- **CodeAct Agent**: Primary agent for code execution and file manipulation
- **Browsing Agent**: Web browsing capabilities with Playwright
- **Microagents**: Specialized agents for specific tasks (stored in `/microagents/`)

### Communication Flow

1. Frontend connects to backend via WebSocket
2. User messages trigger agent actions
3. Agent executes actions in sandboxed runtime
4. Results flow back through observation events
5. UI updates in real-time via WebSocket

### Configuration

- **Backend**: `config.toml` for core settings, LLM configuration
- **Frontend**: Environment variables via Vite
- **Runtime**: Docker containers for isolated execution

### Testing

- **Frontend**: Vitest with React Testing Library
- **Backend**: pytest with unit and integration tests
- **E2E**: Playwright tests for full application flows

### Development Environment

- Python 3.12 with Poetry for dependency management
- Node.js 22+ with npm for frontend dependencies
- Docker required for runtime sandboxing
- Pre-commit hooks for code quality

### Key Technologies

- **Backend**: FastAPI, uvicorn, litellm, docker, pydantic
- **Frontend**: React 19, TypeScript, Vite, TailwindCSS, Redux Toolkit
- **Runtime**: Docker, bash, tmux for terminal sessions
- **AI**: OpenAI API, Anthropic Claude, and other LLM providers via litellm
