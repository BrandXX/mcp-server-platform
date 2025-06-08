# Pull Request

## 📋 Description
Brief description of the changes in this PR.

**Type of Change:**
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test addition/improvement

## 🔗 Related Issues
Fixes #(issue number)
Closes #(issue number)
Related to #(issue number)

## 🔄 Changes Made
Detailed description of the changes:

### **Added:**
- New feature X
- New tool Y
- New documentation Z

### **Changed:**
- Modified behavior of A
- Updated configuration B
- Improved performance of C

### **Removed:**
- Deprecated feature D
- Unused code E

### **Fixed:**
- Bug in component F
- Issue with configuration G

## 🧪 Testing
Describe the tests you ran to verify your changes:

### **Test Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.11.5]
- Docker: [e.g. 24.0.6]
- UV: [e.g. 0.1.0]

### **Tests Performed:**
- [ ] Unit tests pass: `python -m pytest`
- [ ] Integration tests pass: `python tests/test_mcp_structure.py`
- [ ] Server-specific tests pass: `python tests/test_openweather.py`
- [ ] Manual testing completed
- [ ] Performance testing (if applicable)

### **Test Results:**
```
[Paste relevant test output here]
```

## 📸 Screenshots/Examples
If applicable, add screenshots or examples to demonstrate the changes.

**Before:**
```
[Show before state]
```

**After:**
```
[Show after state]
```

## 📚 Documentation
- [ ] Code is self-documenting with clear variable names and structure
- [ ] Docstrings added/updated for new functions and classes
- [ ] README.md updated (if applicable)
- [ ] Documentation in `docs/` updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] API documentation updated (if applicable)

## ✅ Checklist
Please check all applicable items:

### **Code Quality:**
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors

### **Testing:**
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested the changes in a Docker environment

### **Documentation:**
- [ ] I have made corresponding changes to the documentation
- [ ] My changes are reflected in the CHANGELOG.md
- [ ] Any new environment variables are documented in .env.example

### **Security:**
- [ ] I have reviewed my changes for security implications
- [ ] No sensitive information (API keys, passwords) is exposed
- [ ] Environment variables are used for configuration

### **MCP Standards:**
- [ ] New MCP servers follow the standards in `docs/MCP_STANDARDS.md`
- [ ] Server structure follows the template in `mcp/shared/templates/`
- [ ] UV-based dependency management is used
- [ ] Proper error handling is implemented

## 🔍 Review Focus
What should reviewers focus on?
- [ ] Logic correctness
- [ ] Performance implications
- [ ] Security considerations
- [ ] Documentation completeness
- [ ] Test coverage
- [ ] Breaking changes

## 🚀 Deployment Notes
Any special considerations for deployment:
- [ ] Requires environment variable updates
- [ ] Requires configuration changes
- [ ] Requires database migrations
- [ ] Requires container restart
- [ ] No special deployment requirements

## 📊 Performance Impact
If applicable, describe the performance impact:
- **Memory usage:** [Increase/Decrease/No change]
- **Response time:** [Faster/Slower/No change]
- **Resource consumption:** [More/Less/Same]

## 🔮 Future Considerations
Any follow-up work or considerations for future development:
- [ ] Additional features to implement
- [ ] Performance optimizations to consider
- [ ] Documentation improvements needed
- [ ] Related issues to address

---

**Note:** Please ensure your PR is ready for review before marking it as ready. Draft PRs are welcome for early feedback.
