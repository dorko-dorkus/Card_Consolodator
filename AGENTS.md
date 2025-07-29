# Guidelines for Agents

This repository contains a Flask backend and two React Native projects (`frontend` and `mobile`). When modifying code, follow these rules:

- Run automated tests before committing changes:
  - `cd backend && pytest`
  - `cd frontend && npm test`
  - `cd mobile && npm test`
- Follow PEP8 style for Python files. Use `black` if available.
- Format JavaScript/TypeScript files with Prettier where possible.
- Mention the tests you executed in the PR description.

