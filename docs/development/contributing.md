# Contributing

We welcome contributions to prostata! This document outlines the process for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Clone and Setup

```bash
git clone https://github.com/merlos/prostata.git
cd prostata

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=prostata --cov-report=html

# Run specific test file
pytest tests/test_prostata.py

# Run specific test
pytest tests/test_prostata.py::TestStats::test_set_timer
```

### Code Quality

```bash
# Format code
black prostata/ tests/

# Sort imports
isort prostata/ tests/

# Lint code
flake8 prostata/ tests/

# Type check
mypy prostata/
```

## Development Workflow

### 1. Choose an Issue

- Check the [GitHub Issues](https://github.com/merlos/prostata/issues) for open tasks
- Comment on the issue to indicate you're working on it
- Create a new branch for your work

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

- Write tests first (TDD approach recommended)
- Implement your changes
- Ensure all tests pass
- Update documentation if needed

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description

- What was changed
- Why it was changed
- Any breaking changes
"
```

### 5. Push and Create PR

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters (Black default)

### Type Hints

- Use type hints for all function parameters and return values
- Use `typing` module for complex types
- Run `mypy` to check types

### Documentation

- Use Google-style docstrings
- Document all public methods and classes
- Update documentation for any API changes

### Testing

- Write unit tests for all new functionality
- Aim for 100% code coverage
- Use descriptive test names
- Test edge cases and error conditions

## Pull Request Process

### PR Requirements

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] No linting errors (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated if needed
- [ ] Tests added for new functionality

### PR Description

Include:
- What changes were made
- Why the changes were needed
- Any breaking changes
- Screenshots/videos for UI changes (if applicable)

### Review Process

1. Automated checks run (tests, linting, etc.)
2. Code review by maintainers
3. Address review comments
4. Merge when approved

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Code sample if possible

### Feature Requests

For feature requests, please include:

- Use case description
- Proposed API
- Example usage
- Why this feature would be valuable

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## License

By contributing to prostata, you agree that your contributions will be licensed under the same license as the project (MIT License).