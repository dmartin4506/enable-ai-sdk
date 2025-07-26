# Contributing to EnableAI SDK

Thank you for your interest in contributing to the EnableAI SDK! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- pip

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/dmartin4506/enable-ai-sdk.git
   cd enable-ai-sdk
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests to ensure everything works**
   ```bash
   pytest
   ```

## 📝 Development Guidelines

### Code Style

We use [Black](https://black.readthedocs.io/) for code formatting and [flake8](https://flake8.pycqa.org/) for linting.

- **Format code with Black:**
  ```bash
  black enable_ai_sdk/ tests/ examples/
  ```

- **Check code style with flake8:**
  ```bash
  flake8 enable_ai_sdk/ tests/ examples/
  ```

### Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Use descriptive test names and docstrings
- Mock external API calls in tests

Example test structure:
```python
def test_new_feature():
    """Test description of what the test does"""
    # Arrange
    client = EnableAIClient(api_key="test-key")
    
    # Act
    result = client.new_feature()
    
    # Assert
    assert result is not None
    assert result.status == "success"
```

### Documentation

- Update README.md for new features
- Add docstrings to all public functions and classes
- Include usage examples for new functionality
- Update CHANGELOG.md for significant changes

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(client): add new analytics endpoint
fix(auth): handle expired API keys properly
docs(readme): update installation instructions
```

## 🔧 Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=enable_ai_sdk

# Check code style
black --check enable_ai_sdk/ tests/ examples/
flake8 enable_ai_sdk/ tests/ examples/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat(scope): description of changes"
```

### 5. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots for UI changes (if applicable)

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Environment details:**
   - Python version
   - SDK version
   - Operating system

2. **Steps to reproduce:**
   - Clear, step-by-step instructions
   - Code example if possible

3. **Expected vs actual behavior:**
   - What you expected to happen
   - What actually happened

4. **Additional context:**
   - Error messages and stack traces
   - API responses (if applicable)

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if needed)
- [ ] Commit messages follow conventional format
- [ ] No sensitive information is included

## 🏗️ Project Structure

```
enable-ai-sdk/
├── enable_ai_sdk/          # Main SDK package
│   ├── __init__.py         # Package initialization
│   ├── client.py           # Main client class
│   ├── models.py           # Data models
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_client.py      # Client tests
├── examples/               # Usage examples
│   ├── basic_usage.py
│   └── flask_integration.py
├── docs/                   # Documentation
├── README.md               # Main documentation
├── LICENSE                 # MIT license
├── setup.py               # Package setup
├── pyproject.toml         # Modern Python packaging
├── requirements.txt        # Dependencies
└── CHANGELOG.md           # Version history
```

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's code of conduct

## 📞 Getting Help

- **GitHub Issues:** For bug reports and feature requests
- **GitHub Discussions:** For questions and general discussion
- **Email:** support@weenable.ai for urgent issues

## 🎯 Areas for Contribution

We welcome contributions in these areas:

- **New Features:** Additional SDK functionality
- **Documentation:** Improving guides and examples
- **Testing:** Adding test coverage
- **Performance:** Optimizing existing code
- **Examples:** Creating new usage examples
- **Bug Fixes:** Resolving reported issues

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to the EnableAI SDK! 🚀 