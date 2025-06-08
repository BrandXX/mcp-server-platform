# Contributing to MCP Server Development Platform

Thank you for your interest in contributing to the MCP Server Development Platform! This guide will help you get started with contributing to this AI-assisted development project.

## 🎯 Project Overview

This platform enables rapid development of Model Context Protocol (MCP) servers with:
- Modern UV-based dependency management
- Comprehensive testing framework
- AI-assisted development workflows
- Open-WebUI integration
- Production-ready deployment

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Git
- Basic understanding of MCP concepts

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-org/mcp-server-platform.git
cd mcp-server-platform

# Start the development environment
docker compose up -d

# Verify setup
python tests/test_mcp_structure.py
```

## 🤝 How to Contribute

### Types of Contributions

1. **🛠️ New MCP Servers**: Create servers for new functionality
2. **🐛 Bug Fixes**: Fix issues in existing servers or infrastructure
3. **📚 Documentation**: Improve guides, tutorials, and examples
4. **🧪 Testing**: Add tests or improve test coverage
5. **⚡ Performance**: Optimize server performance or startup times
6. **🔧 Infrastructure**: Improve development tools and workflows

### Contribution Workflow

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/your-username/mcp-server-platform.git
   cd mcp-server-platform
   git remote add upstream https://github.com/original-org/mcp-server-platform.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

3. **Make Your Changes**
   - Follow the [Development Guide](docs/DEVELOPMENT.md)
   - Adhere to [MCP Standards](docs/MCP_STANDARDS.md)
   - Use the [AI Development Guide](docs/AI_DEVELOPMENT_GUIDE.md) if working with AI

4. **Test Your Changes**
   ```bash
   # Run comprehensive tests
   python tests/test_mcp_structure.py
   
   # Test specific functionality
   python tests/test_openweather.py
   
   # Clean up if needed
   python tests/cleanup_data_mounts.py --dry-run
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new weather forecast server"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Use the pull request template
   - Include clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## 📋 Development Standards

### Code Quality
- **Type Hints**: Use type hints for all functions
- **Documentation**: Include comprehensive docstrings
- **Error Handling**: Implement robust error handling
- **Testing**: Add tests for new functionality

### MCP Server Standards
- **Directory Structure**: Use `mcp/servers/server-name/` structure
- **UV Dependencies**: Use `pyproject.toml` for dependency management
- **Runner Scripts**: Include `run_uv.sh` for UV integration
- **Documentation**: Create comprehensive `README.md`

### Commit Message Format
```
type(scope): brief description

Longer description if needed

- List specific changes
- Reference issues: Fixes #123
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

## 🧪 Testing Guidelines

### Test Requirements
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test server endpoints
- **System Tests**: Test full integration with MCPO
- **Performance Tests**: Monitor response times

### Test Structure
```python
#!/usr/bin/env python3
"""
Test suite for Your Server
"""

def test_server_functionality():
    """Test core server functionality"""
    # Test implementation
    pass

def test_error_handling():
    """Test error conditions"""
    # Error test implementation
    pass

def test_integration():
    """Test MCPO integration"""
    # Integration test implementation
    pass
```

### Running Tests
```bash
# All tests
python tests/test_mcp_structure.py

# Specific server tests
python tests/test_your_server.py

# Performance tests
python tests/test_mcp_structure.py | grep "Performance"
```

## 📚 Documentation Standards

### Required Documentation
- **README.md**: Server overview and usage
- **Docstrings**: Comprehensive function documentation
- **Type Hints**: Complete type annotations
- **Examples**: Practical usage examples

### Documentation Structure
```markdown
# Server Name

Brief description

## Features
- Feature list

## Tools
### tool_name(params) -> return_type
Tool description

## Configuration
Environment variables and setup

## Usage Examples
Practical examples
```

## 🔒 Security Guidelines

### Security Requirements
- **No Hardcoded Secrets**: Use environment variables
- **Input Validation**: Validate all user inputs
- **Error Handling**: Don't expose sensitive information
- **Dependencies**: Keep dependencies updated

### API Key Management
```python
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

## 🚀 Performance Guidelines

### Performance Targets
- **Status Checks**: < 10ms
- **Simple Operations**: < 100ms
- **API Calls**: < 2 seconds
- **Complex Processing**: < 5 seconds

### Optimization Techniques
- **Async Operations**: Use async/await for I/O
- **Caching**: Cache expensive computations
- **UV Benefits**: Leverage UV's speed advantages
- **Resource Management**: Clean up resources properly

## 🤖 AI-Assisted Development

### Working with AI Agents
- **Clear Instructions**: Provide specific requirements
- **Use Standards**: Reference [AI Development Guide](docs/AI_DEVELOPMENT_GUIDE.md)
- **Validate Output**: Always test AI-generated code
- **Iterate**: Work collaboratively to refine solutions

### AI Contribution Guidelines
- **Follow Patterns**: Use established patterns and templates
- **Test Thoroughly**: AI-generated code must pass all tests
- **Document Well**: Include clear documentation
- **Human Review**: All AI contributions need human review

## 📋 Pull Request Guidelines

### PR Requirements
- [ ] Follows coding standards
- [ ] Includes comprehensive tests
- [ ] Updates relevant documentation
- [ ] Passes all existing tests
- [ ] Includes clear description

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] README updated
- [ ] Docstrings added/updated
- [ ] Examples provided
```

## 🐛 Issue Reporting

### Bug Reports
Include:
- **Environment**: OS, Docker version, Python version
- **Steps to Reproduce**: Clear reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs**: Relevant error messages or logs

### Feature Requests
Include:
- **Use Case**: Why is this needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Implementation**: Willing to implement?

## 🏆 Recognition

### Contributors
All contributors are recognized in:
- **README.md**: Contributor list
- **Release Notes**: Contribution highlights
- **Documentation**: Author attribution

### Contribution Types
- **Code**: New servers, bug fixes, improvements
- **Documentation**: Guides, tutorials, examples
- **Testing**: Test improvements and coverage
- **Community**: Issue triage, support, feedback

## 📞 Getting Help

### Resources
- **Documentation**: Check `docs/` directory
- **Examples**: Review existing servers
- **Tests**: Look at test implementations
- **Issues**: Search existing issues

### Contact
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Discord/Slack**: For real-time chat (if available)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing to the MCP Server Development Platform! 🎉
