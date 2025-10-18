# Repository Guidelines

## Project Structure & Module Organization
- **Backend**: `backend/app` hosts Flask factories, route blueprints, services, and utilities; `backend/run.py` and `backend/wsgi.py` provide local and production entrypoints.
- **Frontend**: `frontend/src` contains the React UI organised by feature modules; static assets live under `frontend/public`.
- **Docs & Config**: Functional specs stay in `doc/`; runtime settings originate from `config.yml` (copy `config.example.yml`), and logs write to `logs/`.
- **Environments**: Keep dependencies inside `venv/` or a per-platform equivalent to avoid polluting the system interpreter.

## Build, Test & Development Commands
- **Bootstrap**: `python -m venv venv && venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix) then `pip install -r backend/requirements.txt`.
- **Backend Dev**: `python backend/run.py` respects `CONFIG_PATH` (defaults to `config.yml`) and honours Flask `debug` toggles for auto-reload.
- **Frontend Dev**: `cd frontend && npm install && npm run dev` runs the Vite server on `http://localhost:5173`.
- **Full Stack Shortcut**: `./start_dev.sh` or `start_dev.bat` seeds env vars and starts both services with aligned ports.

## Coding Style & Naming Conventions
- **Python**: Follow PEP 8 with four-space indents; format with `black backend/` and lint via `flake8 backend/` before commits.
- **Modules**: Use `snake_case` for files and functions, `PascalCase` for classes, and keep Blueprint registrations close to their route definitions.
- **Frontend**: Name components in `PascalCase`, hooks/utilities in `camelCase`, and collocate styles or tests beside the component folder.
- **Config**: Create `config.local.yml` for machine-specific overrides; never commit tokens or Redis credentials.

## Testing Guidelines
- **Backend Tests**: Place suites in `backend/tests/` using filenames like `test_<feature>.py`; run `pytest backend/tests -q` for fast iteration.
- **Coverage**: Target >=80% by executing `pytest --cov=backend/app backend/tests/` and reviewing the generated HTML report.
- **Frontend Checks**: Use `npm run lint` to enforce JSX/TSX standards; add React Testing Library specs when adding stateful components.
- **Isolation**: Stub outbound ZSXQ APIs and Redis calls so tests pass without external services.

## Commit & Pull Request Guidelines
- **Commits**: Write imperative titles (e.g., `feat: add leaderboard endpoint`) and keep each commit focused on one logical change.
- **Branches**: Use `feature/<topic>`, `fix/<issue-id>`, or `chore/<task>` to signal scope and owners.
- **Pull Requests**: Summarise intent, link issues, list config updates, and attach screenshots or JSON samples when UI or API payloads change.
- **Quality Gate**: Confirm `pytest` and `npm run lint` succeed before requesting review; mention the commands in the PR checklist.

## Configuration & Secrets
- **Secrets**: Copy `config.example.yml` to `config.yml`, fill `token` and `group_id`, and exclude actual credentials from commits.
- **Environment Variables**: Override paths with `CONFIG_PATH` and use shell env vars for Redis hosts instead of editing code.
- **Logging**: Watch `logs/app.log` during debugging and trim or rotate large files prior to submitting a PR.
