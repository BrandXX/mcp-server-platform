# Development Guide

This guide provides comprehensive instructions for developing MCP servers in this platform, optimized for both human developers and AI agents.

## 🏗️ Development Environment Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Git
- Basic understanding of MCP (Model Context Protocol)

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd mcp-server-platform

# Start the development environment
docker compose up -d

# Verify setup
python tests/test_mcp_structure.py
```

## 🎯 Development Workflow

### 1. Planning Phase
Before creating a new MCP server:

1. **Define Purpose**: What functionality will your server provide?
2. **Identify Dependencies**: What Python packages are needed?
3. **Plan Tools**: What MCP tools will be exposed?
4. **Consider Integration**: How will it work with Open-WebUI?

### 2. Server Creation Process

#### Step 1: Create Server Directory
```bash
# Create new server directory
mkdir -p mcp/servers/your-server-name
cd mcp/servers/your-server-name
```

#### Step 2: Copy Templates
```bash
# Copy template files
cp ../../shared/templates/pyproject.toml.template pyproject.toml
cp ../../shared/templates/README.md.template README.md
```

#### Step 3: Configure Dependencies
Edit `pyproject.toml`:
```toml
[project]
name = "your-server-name-mcp-server"
version = "0.1.0"
description = "Your server description"
dependencies = [
    "fastmcp>=2.0.0",
    "your-required-packages>=1.0.0"
]
```

#### Step 4: Implement Server
Create your server implementation following MCP standards:
```python
#!/usr/bin/env python3
"""
Your MCP Server Implementation
"""

from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Your Server Name")

@mcp.tool()
def your_tool_function(param: str) -> str:
    """
    Tool description for AI agents
    
    Args:
        param: Parameter description
        
    Returns:
        Result description
    """
    # Implementation here
    return f"Result: {param}"

if __name__ == "__main__":
    mcp.run()
```

#### Step 5: Create Runner Script
Create `run_uv.sh`:
```bash
#!/bin/bash
set -e

# Define paths
SERVER_DIR="/mcp/servers/your-server-name"
WORK_DIR="/memory/mcp-servers/your-server-name"
CACHE_DIR="/memory/.uv-cache"

# Create working directory
mkdir -p "$WORK_DIR" "$CACHE_DIR"

# Copy files if newer
if [ ! -f "$WORK_DIR/pyproject.toml" ] || [ "$SERVER_DIR/pyproject.toml" -nt "$WORK_DIR/pyproject.toml" ]; then
    cp "$SERVER_DIR/pyproject.toml" "$WORK_DIR/"
fi

if [ ! -f "$WORK_DIR/your-server.py" ] || [ "$SERVER_DIR/your-server.py" -nt "$WORK_DIR/your-server.py" ]; then
    cp "$SERVER_DIR/your-server.py" "$WORK_DIR/"
fi

# Set UV cache and run
export UV_CACHE_DIR="$CACHE_DIR"
cd "$WORK_DIR"

# Install dependencies if needed
if [ ! -f "$WORK_DIR/.uv-installed" ]; then
    uv sync --no-dev
    touch "$WORK_DIR/.uv-installed"
fi

# Run server
exec uv run --no-sync python your-server.py
```

#### Step 6: Make Executable
```bash
chmod +x run_uv.sh
```

### 3. Configuration Integration

Add your server to `config/mcpo.json`:
```json
{
  "mcpServers": {
    "your-server-name": {
      "title": "Your Server Title",
      "description": "Server description for Open-WebUI",
      "command": "bash",
      "args": ["/mcp/servers/your-server-name/run_uv.sh"],
      "preload": true,
      "env": {
        "API_KEY": "your-api-key-if-needed"
      }
    }
  }
}
```

### 4. Testing and Validation

#### Local Testing
```bash
# Test your server locally
cd mcp/servers/your-server-name
uv run python your-server.py

# Run comprehensive tests
python tests/test_mcp_structure.py

# Create specific tests for your server
cp tests/test_openweather.py tests/test_your_server.py
# Edit the test file for your server
```

#### Container Testing
```bash
# Restart container with new configuration
docker compose restart mcpo

# Test endpoints
curl -X POST "http://localhost:8989/your-server-name/your_tool_function" \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'
```

## 🔧 Development Best Practices

### Code Organization
- **Single Responsibility**: Each server should have a focused purpose
- **Clear Naming**: Use descriptive names for tools and parameters
- **Documentation**: Include comprehensive docstrings
- **Error Handling**: Implement robust error handling

### Dependency Management
- **Use UV**: Leverage UV for fast dependency management
- **Pin Versions**: Specify exact versions for reproducibility
- **Minimal Dependencies**: Only include necessary packages
- **Security**: Regularly update dependencies

### Testing Strategy
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test server endpoints
- **Performance Tests**: Monitor response times
- **Error Tests**: Validate error handling

### Documentation Requirements
- **README.md**: Server-specific documentation
- **Tool Descriptions**: Clear descriptions for AI agents
- **Usage Examples**: Practical examples
- **Configuration**: Environment variable documentation

## 🐛 Debugging and Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check container logs
docker compose logs mcpo

# Verify file permissions
docker exec mcpo ls -la /mcp/servers/your-server-name/

# Test UV environment
docker exec mcpo bash -c "cd /mcp/servers/your-server-name && uv run python --version"
```

#### Dependencies Not Installing
```bash
# Clear UV cache
docker exec mcpo rm -rf /memory/.uv-cache

# Restart container
docker compose restart mcpo

# Check pyproject.toml syntax
uv check mcp/servers/your-server-name/pyproject.toml
```

#### API Endpoints Not Working
```bash
# Test MCPO health
curl http://localhost:8989/time

# Check server configuration
cat config/mcpo.json | jq '.mcpServers.your-server-name'

# Verify server is loaded
docker compose logs mcpo | grep "your-server-name"
```

### Debugging Tools
- **Container Logs**: `docker compose logs mcpo`
- **Test Suite**: `python tests/test_mcp_structure.py`
- **Health Checks**: Built-in endpoint monitoring
- **Performance Monitoring**: Response time tracking

## 🚀 Deployment Considerations

### Environment Variables
- Store sensitive data in environment variables
- Use `.env` files for local development
- Document all required variables

### Performance Optimization
- **UV Caching**: Leverage UV cache for faster startups
- **Preloading**: Use `"preload": true` for frequently used servers
- **Resource Limits**: Set appropriate container limits

### Security
- **Input Validation**: Validate all inputs
- **API Keys**: Secure API key management
- **Container Isolation**: Leverage container security
- **Read-only Mounts**: Use read-only file system mounts

## 📚 Additional Resources

- [MCP Standards](MCP_STANDARDS.md): Protocol specifications
- [Server Creation](SERVER_CREATION.md): Step-by-step tutorial
- [Architecture](ARCHITECTURE.md): System design overview
- [Testing Guide](../tests/README.md): Testing framework details

## 🤝 Contributing Guidelines

1. **Follow Standards**: Adhere to MCP and project standards
2. **Test Thoroughly**: Ensure all tests pass
3. **Document Changes**: Update relevant documentation
4. **Code Review**: Submit pull requests for review
5. **Performance**: Monitor and optimize performance

This development guide provides the foundation for successful MCP server development in this platform.
