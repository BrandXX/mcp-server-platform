---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 🔄 Steps to Reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior
A clear and concise description of what you expected to happen.

## ❌ Actual Behavior
A clear and concise description of what actually happened.

## 📸 Screenshots
If applicable, add screenshots to help explain your problem.

## 🖥️ Environment
**Platform Information:**
- OS: [e.g. Ubuntu 22.04, macOS 14.0, Windows 11]
- Docker Version: [e.g. 24.0.6]
- Python Version: [e.g. 3.11.5]
- UV Version: [e.g. 0.1.0]

**MCP Server Information:**
- Server Name: [e.g. openweather, time, memory]
- Server Version: [e.g. 0.2.0]
- Configuration: [relevant config from mcpo.json]

**Container Information:**
- MCPO Container Status: [running/stopped/error]
- Container Logs: [if relevant]

## 📋 Additional Context
Add any other context about the problem here.

## 🔍 Logs
Please include relevant logs:

**MCPO Logs:**
```
[Paste MCPO container logs here]
```

**Server Logs:**
```
[Paste specific server logs here]
```

**Test Output:**
```
[Paste test output if applicable]
```

## 🧪 Testing
- [ ] I have run the test suite: `python tests/test_mcp_structure.py`
- [ ] I have tested with a minimal configuration
- [ ] I have checked the server status: `curl http://localhost:8989/time`

## 🔧 Attempted Solutions
Describe any solutions you've already tried:
- [ ] Restarted containers
- [ ] Checked environment variables
- [ ] Reviewed configuration files
- [ ] Consulted documentation

## 📚 Related Documentation
Link to any relevant documentation or issues:
- Documentation: [link to relevant docs]
- Related Issues: [link to related issues]

## 🎯 Impact
- **Severity**: [Low/Medium/High/Critical]
- **Frequency**: [Always/Often/Sometimes/Rarely]
- **Workaround Available**: [Yes/No - describe if yes]

---

**Note**: Please search existing issues before creating a new one. Include as much detail as possible to help us reproduce and fix the issue quickly.
