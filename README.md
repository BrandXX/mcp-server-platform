# MCP Server Development Platform

A modern, AI-assisted development platform for creating and deploying Model Context Protocol (MCP) servers with Open-WebUI integration. This project provides a complete development environment with UV-based dependency management, comprehensive testing, and production-ready deployment.

## 🚀 Features

- **🏗️ Modern Architecture**: Clean separation with `mcp/servers/` structure
- **⚡ UV-Powered**: Lightning-fast dependency management (packages in milliseconds)
- **🧪 Comprehensive Testing**: Automated test suites with performance monitoring
- **🔧 AI-Assisted Development**: Optimized for AI agent collaboration
- **📦 Container-Ready**: Docker-based development and deployment
- **🌐 Open-WebUI Integration**: Direct integration with AI assistant interfaces
- **📚 Rich Documentation**: Complete development guides and standards

## 🏗️ Project Structure

```
mcp-server-platform/
├── mcp/
│   ├── servers/                 # Individual MCP servers
│   │   └── openweather/        # Example: Weather server
│   │       ├── pyproject.toml  # UV dependencies
│   │       ├── openweather.py  # Server implementation
│   │       ├── run_uv.sh      # UV runner script
│   │       └── README.md      # Server documentation
│   └── shared/                 # Shared resources
│       ├── templates/          # Server templates
│       ├── utils/             # Common utilities
│       ├── configs/           # Shared configurations
│       └── docs/              # Documentation
├── tests/                      # Test suite
├── config/                     # MCPO configuration
├── docs/                       # Project documentation
└── scripts/                    # Legacy/utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local development)
- Git

### 1. Clone and Start
```bash
git clone <repository-url>
cd mcp-server-platform
docker compose up -d
```

### 2. Verify Installation
```bash
# Run comprehensive tests
python tests/test_mcp_structure.py

# Test specific functionality
python tests/test_openweather.py
```

### 3. Access Services
- **MCPO Server**: http://localhost:8989
- **API Documentation**: http://localhost:8989/docs
- **Health Check**: http://localhost:8989/time

## 🛠️ Available MCP Servers

### ⏰ Time Server
- **get_current_time**: Get current time for any timezone
- **Endpoint**: `/time/get_current_time`

### 🌦️ OpenWeather Server
- **get_current_weather**: Current weather conditions
- **get_forecast**: Multi-day weather forecasts
- **check_openweather_status**: Server health and configuration
- **Endpoints**: `/openweather/*`

### 💾 Memory Server
- **read_resource**: Read stored memories
- **write_resource**: Store new memories
- **Endpoints**: `/memory/*`

## 📖 Documentation

- **[Development Guide](docs/DEVELOPMENT.md)**: Complete development workflow
- **[MCP Standards](docs/MCP_STANDARDS.md)**: MCP/MCPO specifications and best practices
- **[Server Creation](docs/SERVER_CREATION.md)**: Step-by-step server development
- **[Testing Guide](tests/README.md)**: Testing framework and utilities
- **[Architecture](docs/ARCHITECTURE.md)**: System design and components

## 🧪 Testing

```bash
# Comprehensive system test
python tests/test_mcp_structure.py

# OpenWeather-specific tests
python tests/test_openweather.py

# Data mount cleanup
python tests/cleanup_data_mounts.py --dry-run
```

## 🤖 AI-Assisted Development

This project is optimized for AI agent collaboration:

- **Clear Structure**: Organized directories with specific purposes
- **Rich Documentation**: Comprehensive guides for AI understanding
- **Automated Testing**: Validation tools for AI-generated code
- **Template System**: Standardized patterns for consistency
- **Error Handling**: Detailed error messages and debugging tools

## 🔧 Development Workflow

1. **Create Server**: Use templates in `mcp/shared/templates/`
2. **Implement Logic**: Follow MCP standards and patterns
3. **Test Locally**: Use comprehensive test suite
4. **Deploy**: Add to MCPO configuration
5. **Validate**: Run full system tests

## 📊 Performance

- **UV Package Management**: ~15ms for dependency installation
- **API Response Times**: ~2-5ms for status checks
- **Container Startup**: ~10-15 seconds to healthy state
- **Memory Usage**: Optimized for production deployment

## 🔒 Security & Production

- **Environment Variables**: Secure API key management
- **Container Isolation**: Sandboxed server execution
- **Read-only Mounts**: Secure file system access
- **Health Checks**: Automated monitoring and recovery

## 🤝 Contributing

1. **Read Documentation**: Start with [DEVELOPMENT.md](docs/DEVELOPMENT.md)
2. **Follow Standards**: Use [MCP_STANDARDS.md](docs/MCP_STANDARDS.md)
3. **Test Thoroughly**: Run all test suites
4. **Document Changes**: Update relevant documentation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: Check `docs/` directory
- **Testing**: Run test suite for diagnostics
- **Community**: Follow contribution guidelines
