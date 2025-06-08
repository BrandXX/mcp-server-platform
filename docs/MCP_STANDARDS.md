# MCP Standards and Specifications

This document defines the standards, specifications, and best practices for developing Model Context Protocol (MCP) servers in this platform, with specific considerations for Open-WebUI integration.

## 📋 MCP Protocol Overview

### What is MCP?
Model Context Protocol (MCP) is a standardized protocol for AI agents to interact with external tools and services. It provides:

- **Standardized Communication**: Consistent interface between AI models and tools
- **Tool Discovery**: Automatic detection of available capabilities
- **Type Safety**: Structured data exchange with validation
- **Error Handling**: Robust error reporting and recovery

### MCP Components
1. **MCP Server**: Provides tools and resources to AI agents
2. **MCP Client**: Consumes tools (typically an AI assistant)
3. **MCPO (MCP OpenAPI Proxy)**: Converts MCP to REST API for Open-WebUI

## 🏗️ Server Architecture Standards

### Directory Structure
```
mcp/servers/your-server/
├── pyproject.toml          # UV dependencies and metadata
├── your-server.py          # Main server implementation
├── run_uv.sh              # UV runner script
├── README.md              # Server documentation
└── tests/                 # Optional: server-specific tests
```

### File Naming Conventions
- **Server File**: `{server-name}.py` (matches directory name)
- **Runner Script**: `run_uv.sh` (standardized name)
- **Configuration**: `pyproject.toml` (UV standard)
- **Documentation**: `README.md` (GitHub standard)

### Import Standards
```python
#!/usr/bin/env python3
"""
Server Name - Brief Description

Longer description of what this server does and how it integrates
with Open-WebUI and other AI assistants.
"""

# Standard library imports first
import os
import sys
from typing import Optional, List, Dict, Any

# Third-party imports
from fastmcp import FastMCP

# Local imports (if any)
# from .utils import helper_function
```

## 🔧 Tool Implementation Standards

### Tool Definition
```python
@mcp.tool()
def tool_name(
    required_param: str,
    optional_param: Optional[str] = None,
    numeric_param: int = 10
) -> str:
    """
    Brief tool description for AI agents.
    
    This tool performs [specific function] and is useful for [use cases].
    
    Args:
        required_param: Description of required parameter
        optional_param: Description of optional parameter (default: None)
        numeric_param: Description with default value (default: 10)
        
    Returns:
        Description of return value and format
        
    Raises:
        ValueError: When input validation fails
        ConnectionError: When external service is unavailable
    """
    # Implementation here
    return result
```

### Parameter Standards
- **Type Hints**: Always use type hints for parameters and returns
- **Validation**: Validate all inputs before processing
- **Defaults**: Provide sensible defaults for optional parameters
- **Documentation**: Clear descriptions for AI agent understanding

### Return Value Standards
```python
# Good: Structured, informative response
def get_weather(city: str) -> str:
    return f"""Current Weather for {city}:
🌡️ Temperature: 72°F (22°C)
💧 Humidity: 65%
🌤️ Conditions: Partly cloudy
🌬️ Wind: 8 mph NW"""

# Avoid: Raw data dumps or unclear formats
def get_weather_bad(city: str) -> dict:
    return {"temp": 72, "humid": 65, "cond": "pc"}
```

## 🌐 Open-WebUI Integration Standards

### Tool Naming for Open-WebUI
- **Descriptive Names**: Use clear, descriptive tool names
- **Consistent Prefixes**: Group related tools with prefixes
- **Avoid Conflicts**: Ensure unique names across servers

### Response Formatting
```python
# Optimal for Open-WebUI display
def format_response(data: dict) -> str:
    """Format response for optimal Open-WebUI display"""
    response = []
    
    # Use emojis for visual appeal
    response.append(f"🎯 **Result Summary**")
    
    # Structure information clearly
    for key, value in data.items():
        response.append(f"• **{key.title()}**: {value}")
    
    # Add helpful context
    response.append(f"\n💡 *Updated: {datetime.now().strftime('%H:%M:%S')}*")
    
    return "\n".join(response)
```

### Error Handling for Open-WebUI
```python
def handle_api_error(error: Exception) -> str:
    """Handle errors gracefully for Open-WebUI"""
    if isinstance(error, ConnectionError):
        return "🔌 **Connection Error**: Unable to reach external service. Please try again later."
    elif isinstance(error, ValueError):
        return f"⚠️ **Input Error**: {str(error)}"
    else:
        return f"❌ **Unexpected Error**: {str(error)}"
```

## 📦 Dependency Management Standards

### pyproject.toml Structure
```toml
[project]
name = "server-name-mcp-server"
version = "0.1.0"
description = "Brief description of server functionality"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
keywords = ["mcp", "category", "functionality"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.25.0",  # Prefer httpx for async HTTP
    # Add other dependencies with version constraints
]

[project.urls]
Homepage = "https://github.com/your-org/mcp-servers"
Repository = "https://github.com/your-org/mcp-servers"
Documentation = "https://github.com/your-org/mcp-servers/tree/main/mcp/servers/server-name"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0"
]

[tool.mcp-server]
# Custom metadata for MCP server management
title = "Server Display Title"
category = "category"
tags = ["tag1", "tag2", "functionality"]
env_vars = [
    {name = "API_KEY", required = true, description = "API key for external service"},
    {name = "TIMEOUT", required = false, default = "30", description = "Request timeout in seconds"}
]
```

### Dependency Selection Guidelines
- **FastMCP**: Required for all MCP servers
- **HTTP Clients**: Prefer `httpx` over `requests` for async support
- **Data Processing**: Use standard library when possible
- **External APIs**: Pin versions for stability
- **Development**: Include testing dependencies in dev section

## 🔒 Security Standards

### API Key Management
```python
import os

def get_api_key(key_name: str) -> str:
    """Securely retrieve API key from environment"""
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"Missing required environment variable: {key_name}")
    return api_key

# Usage
API_KEY = get_api_key("OPENWEATHER_API_KEY")
```

### Input Validation
```python
def validate_city_name(city: str) -> str:
    """Validate and sanitize city name input"""
    if not city or not city.strip():
        raise ValueError("City name cannot be empty")
    
    # Remove potentially dangerous characters
    sanitized = "".join(c for c in city if c.isalnum() or c in " ,-.")
    
    if len(sanitized) > 100:
        raise ValueError("City name too long")
    
    return sanitized.strip()
```

### Error Information Disclosure
```python
def safe_error_message(error: Exception, debug: bool = False) -> str:
    """Return safe error message without sensitive information"""
    if debug:
        return str(error)  # Full error in development
    else:
        return "An error occurred. Please try again."  # Generic in production
```

## 📊 Performance Standards

### Response Time Targets
- **Status Checks**: < 10ms
- **Simple Operations**: < 100ms
- **API Calls**: < 2 seconds
- **Complex Processing**: < 5 seconds

### Optimization Techniques
```python
# Use async for I/O operations
import asyncio
import httpx

async def fetch_data(url: str) -> dict:
    """Async HTTP request for better performance"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(param: str) -> str:
    """Cache expensive computations"""
    # Expensive operation here
    return result
```

## 🧪 Testing Standards

### Test Structure
```python
#!/usr/bin/env python3
"""
Test suite for Server Name MCP server
"""

import pytest
from your_server import mcp, tool_function

def test_tool_function_success():
    """Test successful tool execution"""
    result = tool_function("valid_input")
    assert "expected_content" in result
    assert isinstance(result, str)

def test_tool_function_validation():
    """Test input validation"""
    with pytest.raises(ValueError):
        tool_function("")

def test_tool_function_error_handling():
    """Test error handling"""
    # Test various error conditions
    pass
```

### Test Coverage Requirements
- **Happy Path**: Test successful operations
- **Input Validation**: Test parameter validation
- **Error Handling**: Test error conditions
- **Edge Cases**: Test boundary conditions
- **Integration**: Test with MCPO if possible

## 📚 Documentation Standards

### README.md Structure
```markdown
# Server Name MCP Server

Brief description of server functionality and purpose.

## Features
- Feature 1
- Feature 2

## Tools
### tool_name(param: type) -> type
Description of tool functionality.

## Configuration
### Environment Variables
- `API_KEY`: Required API key
- `TIMEOUT`: Optional timeout setting

## Installation
Instructions for UV-based installation.

## Usage Examples
Practical examples of tool usage.
```

### Code Documentation
- **Docstrings**: Comprehensive docstrings for all public functions
- **Type Hints**: Complete type annotations
- **Comments**: Explain complex logic
- **Examples**: Include usage examples in docstrings

## 🔄 Versioning and Updates

### Version Management
- **Semantic Versioning**: Use semver (major.minor.patch)
- **Breaking Changes**: Increment major version
- **New Features**: Increment minor version
- **Bug Fixes**: Increment patch version

### Update Process
1. **Test Changes**: Run full test suite
2. **Update Version**: Increment version in pyproject.toml
3. **Update Documentation**: Reflect changes in README
4. **Test Integration**: Verify MCPO integration
5. **Deploy**: Update container configuration

This standards document ensures consistency, quality, and maintainability across all MCP servers in the platform.
