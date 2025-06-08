# Available MCP Servers

This document describes the MCP servers available in the platform and their capabilities.

## 🛠️ Core Servers

### ⏰ Time Server
- **ID**: `time`
- **Description**: Provides current date & time for any city or timezone
- **Implementation**: Node.js via `uvx mcp-server-time`
- **Tools**:
  - `get_current_time(timezone)`: Get current time for specified timezone

### 💾 Memory Server
- **ID**: `memory`
- **Description**: Session-based key-value store for temporary data
- **Implementation**: Node.js via `@modelcontextprotocol/server-memory`
- **Tools**:
  - `read_resource(uri)`: Read stored memory
  - `write_resource(uri, content)`: Store new memory

### 🌦️ OpenWeather Server
- **ID**: `openweather`
- **Description**: Weather data via OpenWeatherMap API
- **Implementation**: Python with UV at `/mcp/servers/openweather/`
- **Configuration**:
  - `OPENWEATHER_API_KEY`: Required API key
  - `UNITS`: Temperature units (imperial/metric, default: imperial)
- **Tools**:
  - `get_current_weather(city)`: Current weather conditions
  - `get_forecast(city, days)`: Multi-day weather forecast
  - `check_openweather_status()`: Server health and configuration

## 🏗️ Modern Architecture

### UV-Based Dependency Management
All Python servers use UV for lightning-fast dependency management:

- **⚡ Performance**: Package installation in milliseconds
- **🔒 Isolation**: Each server has its own virtual environment
- **📦 Caching**: Shared UV cache for efficiency
- **🔄 Reliability**: Deterministic dependency resolution

### Server Structure
```
mcp/servers/server-name/
├── pyproject.toml          # UV dependencies
├── server-name.py          # Server implementation
├── run_uv.sh              # UV runner script
└── README.md              # Documentation
```

### Benefits
- **Fast Startup**: UV installs packages in ~15ms
- **Clean Separation**: Each server is self-contained
- **Easy Development**: Standard Python packaging
- **Production Ready**: Robust error handling and monitoring

## 🚀 Creating New Servers

See the comprehensive guides:
- [Development Guide](DEVELOPMENT.md): Complete development workflow
- [Server Creation](SERVER_CREATION.md): Step-by-step tutorial
- [MCP Standards](MCP_STANDARDS.md): Best practices and specifications

## 🧪 Testing

All servers include comprehensive testing:
```bash
# Test all servers
python tests/test_mcp_structure.py

# Test specific server
python tests/test_openweather.py
```

## 📊 Performance

Current performance metrics:
- **UV Package Management**: ~15ms installation
- **API Response Times**: 2-5ms for status checks
- **Weather API Calls**: ~200-300ms
- **Container Startup**: ~10-15 seconds to healthy

## 🔧 Configuration

Servers are configured in `config/mcpo.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "title": "Server Display Name",
      "description": "Server description",
      "command": "bash",
      "args": ["/mcp/servers/server-name/run_uv.sh"],
      "preload": true,
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```