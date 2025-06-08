# MCPO Configuration

This directory contains configuration files and templates for the MCPO (MCP OpenAPI Proxy) server.

## 📁 Files Overview

### **Active Configuration**
- **`mcpo.json`** - Main configuration file used by MCPO server
- **`.env`** - Environment variables (create from `.env.example`)

### **Templates & Examples**
- **`mcpo-config-template.json`** - Comprehensive configuration templates for all server types
- **`mcpo-examples.json`** - Real-world configuration examples
- **`README.md`** - This documentation file

## 🚀 Quick Start

### **1. Basic Setup**
```bash
# Copy environment template
cp ../.env.example .env

# Edit with your API keys
nano .env
```

### **2. Add a New Server**
1. Choose appropriate template from `mcpo-config-template.json`
2. Copy template to `mcpo.json` under `mcpServers`
3. Replace placeholder values with your configuration
4. Restart MCPO container: `docker compose restart mcpo`

### **3. Test Configuration**
```bash
# Test server endpoint
curl http://localhost:8989/your-server-name

# Check server status
curl http://localhost:8989/time
```

## 📋 Server Types

### **Local UV-based Servers**
```json
{
  "your-server": {
    "title": "Your Custom Server",
    "description": "Description of your server",
    "command": "bash",
    "args": ["/mcp/servers/your-server/run_uv.sh"],
    "preload": true,
    "env": {
      "API_KEY": "your_api_key"
    }
  }
}
```

### **External Package Servers**
```json
{
  "time-server": {
    "title": "Time Server",
    "description": "Current time utilities",
    "command": "uvx",
    "args": ["mcp-server-time"],
    "preload": true
  }
}
```

### **Remote HTTP Servers**
```json
{
  "remote-service": {
    "title": "Remote Service",
    "description": "External MCP service",
    "url": "https://api.service.com/mcp",
    "server_type": "http",
    "headers": {
      "Authorization": "Bearer your_token"
    },
    "preload": false
  }
}
```

## 🔧 Configuration Fields

### **Required Fields**
- **`title`** - Human-readable server name
- **`description`** - Brief description of functionality

### **Execution Methods**
Choose one:
- **Command-based**: `command`, `args`, `env`
- **URL-based**: `url`, `server_type`, `headers`

### **Optional Fields**
- **`preload`** - Start server immediately (default: false)
- **`timeout`** - Request timeout in seconds
- **`retry_attempts`** - Number of retry attempts
- **`metadata`** - Additional server information

## 🔒 Security Best Practices

### **Environment Variables**
```bash
# .env file
OPENWEATHER_API_KEY=your_actual_api_key
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### **Configuration Reference**
```json
{
  "env": {
    "API_KEY": "placeholder_value"
  }
}
```

**Never commit real API keys to version control!**

## 📊 Server Categories

### **🌤️ Weather & Environment**
- OpenWeather API integration
- Climate data services
- Environmental monitoring

### **🗄️ Database & Storage**
- PostgreSQL, MySQL, MongoDB connectors
- Redis cache integration
- File system operations

### **🔧 Development Tools**
- GitHub API integration
- Code formatting and linting
- CI/CD pipeline tools

### **💬 Communication**
- Slack workspace integration
- Email services
- Notification systems

### **🤖 AI & ML Services**
- External AI API integration
- Machine learning model serving
- Data processing pipelines

## 🧪 Testing Configuration

### **Validate JSON**
```bash
# Check JSON syntax
python -m json.tool mcpo.json

# Validate against schema
# (Future: JSON schema validation)
```

### **Test Server Connection**
```bash
# Basic connectivity
curl -f http://localhost:8989/server-name || echo "Server not responding"

# Check server status
docker logs mcpo | grep "server-name"
```

### **Debug Common Issues**
1. **Server not starting**: Check logs for dependency issues
2. **Authentication errors**: Verify API keys in .env file
3. **Connection timeouts**: Adjust timeout values
4. **Permission errors**: Check file permissions for local servers

## 📚 Examples

See `mcpo-examples.json` for complete, real-world configuration examples including:
- Weather services (OpenWeather)
- Development tools (GitHub integration)
- Database connectors (PostgreSQL)
- Communication tools (Slack)
- File system operations
- Remote AI services

## 🔄 Migration from template.txt

The old `template.txt` has been replaced with comprehensive JSON templates:

**Old format** (template.txt):
```
Simple text with comments
Limited examples
Mixed format
```

**New format** (JSON templates):
```
✅ Valid JSON format
✅ Comprehensive templates for all server types
✅ Real-world examples
✅ Detailed documentation
✅ Schema validation ready
```

## 📖 Related Documentation

- **[Project Structure](../docs/STRUCTURE.md)** - Overall project organization
- **[MCP Standards](../docs/MCP_STANDARDS.md)** - MCP server development standards
- **[Security Guide](../docs/SECURITY.md)** - Security best practices
- **[Development Guide](../docs/DEVELOPMENT.md)** - Development workflow

---

For questions or issues with configuration, please refer to the project documentation or create an issue in the GitHub repository.
