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

### 🌤️ OpenWeather Server (Enhanced v0.3.0)
- **ID**: `openweather`
- **Description**: Comprehensive weather intelligence with advanced features
- **Implementation**: Python with UV at `/mcp/servers/openweather/`
- **Status**: ✅ Production Ready with Advanced Features

#### **Core Weather Tools**
- **`get_current_weather(city)`**: Real-time weather conditions with rich formatting
- **`get_forecast(city, days)`**: Detailed 5-day weather forecasts

#### **🆕 Advanced Features (v0.3.0)**
- **`get_weather_recommendations(city)`**: Smart activity and clothing suggestions based on weather
- **`get_astronomy_data(city)`**: Sunrise, sunset, moon phases, solar noon calculations
- **`compare_weather(cities)`**: Multi-city weather comparison (up to 5 cities)
- **`get_air_quality(city)`**: Air quality index and pollution data with health advisories
- **`get_weather_alerts(city)`**: Severe weather warnings (requires One Call API 3.0)

#### **System Tools**
- **`check_openweather_status()`**: Comprehensive server diagnostics
- **`get_openweather_version()`**: Version and feature information

#### **Configuration**
- **Required**: `OPENWEATHER_API_KEY` (OpenWeatherMap API key)
- **Optional**: `UNITS` (imperial/metric), `DEBUG`, `API_TIMEOUT`
- **APIs Used**: Current Weather, 5-Day Forecast, Air Pollution, Geocoding

#### **Key Features**
- 🎯 **Smart Recommendations**: Weather-based activity suggestions
- 🌌 **Astronomy Data**: Moon phases, sunrise/sunset tracking
- 🌍 **Multi-City Analysis**: Compare weather across locations
- 🌬️ **Air Quality**: Pollution monitoring with health advice
- 🎨 **Rich Output**: Emoji-enhanced, structured responses
- ⚡ **High Performance**: ~2-5ms response times

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