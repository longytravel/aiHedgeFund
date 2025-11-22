# Contributing to AIHedgeFund

Thank you for your interest in contributing to AIHedgeFund! This document provides guidelines and best practices for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository** and clone it locally
2. **Set up your development environment** following the README.md quickstart guide
3. **Create a feature branch** from `main` for your work
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request** with a clear description

## 📋 Development Workflow

### Story-Based Development

We use the BMad Method for structured development:

```bash
# 1. Create story context (if starting a new story)
/bmad:bmm:workflows:story-context

# 2. Implement the story
# ... write code, tests, documentation ...

# 3. Mark story as ready for review
/bmad:bmm:workflows:story-ready

# 4. Mark story as done after review
/bmad:bmm:workflows:story-done
```

### Branch Naming Convention

Use the following format for branch names:

- `story/1.1-project-setup` - For story implementations
- `bugfix/fix-health-check` - For bug fixes
- `docs/update-readme` - For documentation updates
- `refactor/improve-signal-bus` - For refactoring

## 🧪 Testing Requirements

All contributions must include appropriate tests:

- **Unit Tests**: For individual functions and classes
- **Integration Tests**: For API endpoints and workflows
- **Test Coverage**: Minimum 70% for new code

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend/app --cov-report=html

# Run specific test file
pytest tests/integration/test_health.py
```

## 💻 Code Quality Standards

### Python Code Style

- **Formatter**: Black (line length: 100)
- **Linter**: Ruff
- **Type Hints**: Required for all functions
- **Docstrings**: Google-style docstrings for all public functions

```bash
# Format code
black backend/app tests

# Lint code
ruff check backend/app tests

# Type check
mypy backend/app
```

### TypeScript Code Style

- **Formatter**: Prettier
- **Linter**: ESLint
- **Type Safety**: Strict mode enabled

```bash
# Format frontend code
cd frontend
npm run format

# Lint frontend code
npm run lint
```

## 📝 Commit Message Guidelines

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(api): add health check endpoint

Implement /api/health endpoint that returns system status including
database connectivity and timestamp.

Closes #123
```

```
fix(database): resolve connection pool leak

Fix issue where database connections were not being properly released
after failed queries, causing connection pool exhaustion.

Fixes #456
```

## 🔍 Pull Request Process

1. **Update Documentation**: Ensure README.md and relevant docs are updated
2. **Add Tests**: Include unit and integration tests for new features
3. **Pass CI Checks**: All tests must pass, code must meet quality standards
4. **Request Review**: Request review from at least one maintainer
5. **Address Feedback**: Respond to review comments and make requested changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Story/Issue
Closes #[issue number]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings or errors
```

## 🏗️ Architecture Guidelines

### Backend (FastAPI)

- **Async/Await**: Use async functions for I/O operations
- **Dependency Injection**: Use FastAPI's dependency injection
- **Error Handling**: Use custom exceptions from `app.core.errors`
- **Database**: Use SQLAlchemy async ORM

### Frontend (React 19)

- **Functional Components**: Use hooks, avoid class components
- **TypeScript**: Strong typing for all components
- **State Management**: Use TanStack Query for server state
- **Styling**: Use TailwindCSS utility classes

### Agents

- **Base Class**: Extend `BaseAgent` from `agents/base.py`
- **Signal Bus**: Use signal bus for agent communication
- **LLM Providers**: Use multi-provider abstraction
- **Configuration**: Make agents configurable via YAML

## 🔒 Security Guidelines

- **Never commit secrets**: Use `.env` for API keys and passwords
- **Validate inputs**: Use Pydantic models for API validation
- **Parameterize queries**: Use SQLAlchemy ORM to prevent SQL injection
- **Handle errors safely**: Don't expose sensitive information in error messages

## 📚 Documentation

All new features must include:

1. **Docstrings**: For all public functions and classes
2. **API Documentation**: OpenAPI/Swagger specs auto-generated
3. **README Updates**: Update README.md if user-facing changes
4. **Architecture Docs**: Update architecture docs for significant changes

## ❓ Questions?

- Check the [Documentation](docs/index.md)
- Review [Architecture](docs/architecture/index.md)
- Create an issue for questions or clarifications

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 🙏 Thank You!

Your contributions help make AIHedgeFund better for everyone!
