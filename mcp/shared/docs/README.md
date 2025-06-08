# MCP Servers

This directory contains Model Context Protocol (MCP) servers organized in a clean, scalable structure.

## Directory Structure

```
mcp/
├── servers/                    # Individual MCP servers
│   └── openweather/           # Example: OpenWeather server
│       ├── pyproject.toml     # Dependencies & metadata
│       ├── openweather.py     # Server implementation
│       ├── run_uv.sh         # UV runner script
│       └── README.md         # Server documentation
└── shared/                    # Shared resources
    ├── templates/             # Server templates
    ├── utils/                # Common utilities
    ├── configs/              # Shared configurations
    └── docs/                 # Documentation
```

## Server Standards

Each MCP server follows these conventions:

### 1. **UV-Based Dependency Management**
- Uses `pyproject.toml` for dependency specification
- UV for fast, reliable package management
- Isolated virtual environments per server

### 2. **Comprehensive Metadata**
- Rich `pyproject.toml` with proper metadata
- Custom `[tool.mcp-server]` section for MCP-specific config
- Environment variable documentation

### 3. **Documentation**
- `README.md` with usage examples
- Tool documentation
- Configuration instructions

### 4. **Runner Scripts**
- `run_uv.sh` handles UV environment setup
- Copies files to writable locations
- Manages dependency installation

## Creating New Servers

1. **Create server directory**: `mcp/servers/your-server/`
2. **Use templates**: Copy from `shared/templates/`
3. **Implement server**: Create your server code
4. **Update configuration**: Add to `mcpo.json`
5. **Document**: Create comprehensive README

## Benefits

- **🏗️ Scalable**: Easy to add new servers
- **🔧 Modern**: UV-based dependency management
- **📦 Isolated**: Each server has its own environment
- **📚 Documented**: Comprehensive documentation
- **🧹 Clean**: Clear separation of concerns

## Migration from Scripts

Legacy scripts in `/scripts/` can be gradually migrated to this structure:

1. Create new server directory
2. Convert to UV/pyproject.toml
3. Update configuration
4. Test thoroughly
5. Remove old script

This provides a clean migration path without breaking existing functionality.
