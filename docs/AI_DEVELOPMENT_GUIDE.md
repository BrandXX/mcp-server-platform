# AI-Assisted Development Guide

This guide is specifically designed for AI agents and human developers working together to create MCP servers in this platform. It provides structured approaches, common patterns, and best practices for successful AI-assisted development.

## 🤖 For AI Agents: Understanding This Platform

### Platform Overview
This is a **Model Context Protocol (MCP) Server Development Platform** that:
- Creates tools that AI assistants (like you) can use
- Uses modern Python with UV for fast dependency management
- Integrates with Open-WebUI for user interaction
- Follows strict standards for consistency and reliability

### Key Concepts for AI Agents
1. **MCP Server**: A program that provides tools to AI assistants
2. **Tool**: A specific function an AI can call (like getting weather data)
3. **Open-WebUI**: The interface where users interact with AI assistants
4. **UV**: A fast Python package manager (replaces pip)
5. **MCPO**: The proxy that converts between protocols

### Your Role as an AI Agent
When helping with development, you should:
- **Follow Standards**: Always use the patterns in [MCP_STANDARDS.md](MCP_STANDARDS.md)
- **Use Templates**: Start with templates in `mcp/shared/templates/`
- **Test Thoroughly**: Run tests after making changes
- **Document Everything**: Create clear documentation for humans

## 🏗️ Development Workflow for AI Agents

### Step 1: Understand the Request
When a human asks you to create an MCP server:

1. **Clarify Purpose**: What should this server do?
2. **Identify Tools**: What specific functions are needed?
3. **Check Dependencies**: What external services or packages are required?
4. **Plan Integration**: How will it work with Open-WebUI?

### Step 2: Use the Standard Structure
Always create servers in this structure:
```
mcp/servers/server-name/
├── pyproject.toml          # Dependencies and metadata
├── server-name.py          # Main implementation
├── run_uv.sh              # UV runner script
└── README.md              # Documentation
```

### Step 3: Follow the Implementation Pattern
```python
#!/usr/bin/env python3
"""
Server Name - Brief Description

Detailed description for AI agents and humans.
"""

import os
from typing import Optional
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Server Name")

@mcp.tool()
def tool_name(param: str, optional_param: Optional[str] = None) -> str:
    """
    Tool description for AI agents.
    
    Args:
        param: Description of required parameter
        optional_param: Description of optional parameter
        
    Returns:
        Description of return value
    """
    # Implementation here
    return result

if __name__ == "__main__":
    mcp.run()
```

### Step 4: Create Supporting Files
1. **pyproject.toml**: Use the template and add required dependencies
2. **run_uv.sh**: Copy and modify the standard runner script
3. **README.md**: Document the server for humans
4. **Configuration**: Add to `config/mcpo.json`

### Step 5: Test and Validate
1. **Run Tests**: Use `python tests/test_mcp_structure.py`
2. **Test Endpoints**: Verify API responses
3. **Check Integration**: Ensure Open-WebUI compatibility

## 🎯 Common Development Patterns

### Pattern 1: API Integration Server
For servers that call external APIs:

```python
import httpx
import os

API_KEY = os.getenv("API_KEY")

async def fetch_data(endpoint: str) -> dict:
    """Standard async API call pattern"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = await client.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_data(query: str) -> str:
    """Get data from external API"""
    try:
        data = await fetch_data(f"https://api.example.com/search?q={query}")
        return format_response(data)
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### Pattern 2: Data Processing Server
For servers that process or transform data:

```python
from typing import List, Dict

@mcp.tool()
def process_data(input_data: str, format_type: str = "json") -> str:
    """Process and format data"""
    try:
        # Validate input
        if not input_data.strip():
            raise ValueError("Input data cannot be empty")
        
        # Process data
        processed = transform_data(input_data)
        
        # Format output
        if format_type == "json":
            return json.dumps(processed, indent=2)
        else:
            return format_as_text(processed)
            
    except Exception as e:
        return f"❌ Processing Error: {str(e)}"
```

### Pattern 3: Status and Health Checks
Every server should have a status check:

```python
@mcp.tool()
def get_server_status() -> str:
    """Check server status and configuration"""
    status_info = [
        f"🎯 **{SERVER_NAME} Status**",
        "=" * 40,
        f"✅ Server: Online",
        f"🔑 API Key: {'Configured' if API_KEY else 'Missing'}",
        f"🕐 Server Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "🛠️ **Available Tools:**"
    ]
    
    # Add tool list dynamically
    for tool_name in get_tool_names():
        status_info.append(f"• {tool_name}")
    
    return "\n".join(status_info)
```

## 🔧 AI Agent Best Practices

### Code Quality
- **Type Hints**: Always use type hints for parameters and returns
- **Error Handling**: Wrap external calls in try-catch blocks
- **Input Validation**: Validate all user inputs
- **Documentation**: Write clear docstrings for AI understanding

### Open-WebUI Optimization
- **Formatted Responses**: Use markdown formatting for better display
- **Emojis**: Use emojis to make responses visually appealing
- **Structure**: Organize information with headers and lists
- **Context**: Provide helpful context and next steps

### Performance Considerations
- **Async Operations**: Use async/await for I/O operations
- **Caching**: Cache expensive computations when appropriate
- **Timeouts**: Set reasonable timeouts for external calls
- **Resource Management**: Clean up resources properly

### Security Practices
- **Environment Variables**: Store secrets in environment variables
- **Input Sanitization**: Clean and validate all inputs
- **Error Messages**: Don't expose sensitive information in errors
- **API Keys**: Never hardcode API keys

## 🧪 Testing Guidelines for AI Agents

### Test Creation Pattern
When creating tests for your servers:

```python
#!/usr/bin/env python3
"""
Test suite for Server Name
"""

import pytest
from your_server import mcp, tool_function

def test_tool_success():
    """Test successful operation"""
    result = tool_function("valid_input")
    assert "expected_content" in result
    assert isinstance(result, str)

def test_tool_validation():
    """Test input validation"""
    with pytest.raises(ValueError):
        tool_function("")

def test_tool_error_handling():
    """Test error conditions"""
    # Test various error scenarios
    pass
```

### Integration Testing
Always test integration with MCPO:

```bash
# Test endpoint directly
curl -X POST "http://localhost:8989/server-name/tool-name" \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'
```

## 🚨 Common Pitfalls for AI Agents

### Avoid These Mistakes
1. **Wrong Directory Structure**: Don't put servers in `/scripts/`
2. **Missing Dependencies**: Always update `pyproject.toml`
3. **No Error Handling**: Always handle exceptions gracefully
4. **Poor Documentation**: Write clear docstrings and README
5. **Hardcoded Values**: Use environment variables for configuration
6. **No Testing**: Always create and run tests

### Debug Common Issues
- **Import Errors**: Check `pyproject.toml` dependencies
- **Permission Errors**: Ensure `run_uv.sh` is executable
- **API Errors**: Verify environment variables are set
- **Container Issues**: Check Docker logs with `docker compose logs mcpo`

## 📚 Resources for AI Agents

### Essential Documentation
- **[MCP_STANDARDS.md](MCP_STANDARDS.md)**: Protocol specifications and standards
- **[SERVER_CREATION.md](SERVER_CREATION.md)**: Step-by-step tutorial
- **[DEVELOPMENT.md](DEVELOPMENT.md)**: Complete development workflow
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System design overview

### Templates and Examples
- **Templates**: `mcp/shared/templates/`
- **Working Example**: `mcp/servers/openweather/`
- **Test Examples**: `tests/test_openweather.py`

### Validation Tools
- **System Tests**: `python tests/test_mcp_structure.py`
- **Cleanup Tools**: `python tests/cleanup_data_mounts.py`
- **Health Checks**: Built into MCPO

## 🎯 Success Criteria

A successful MCP server created by an AI agent should:

✅ **Follow Standards**: Use the correct directory structure and patterns
✅ **Work Correctly**: Pass all tests and respond to API calls
✅ **Handle Errors**: Gracefully handle all error conditions
✅ **Be Documented**: Include comprehensive documentation
✅ **Integrate Well**: Work seamlessly with Open-WebUI
✅ **Perform Well**: Respond quickly and efficiently

This guide ensures AI agents can successfully contribute to MCP server development while maintaining high quality and consistency standards.
