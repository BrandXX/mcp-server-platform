# Project Structure

This document provides a comprehensive overview of the MCP Server Development Platform project structure, explaining the purpose and organization of each directory and key file.

## 📁 **Root Directory Structure**

```
mcp-server-platform/
├── 📄 README.md                    # Project overview and quick start
├── 📄 LICENSE                      # MIT license
├── 📄 CONTRIBUTING.md               # Contribution guidelines
├── 📄 docker-compose.yml           # Container orchestration
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore patterns
├── 📁 mcp/                         # MCP server ecosystem
├── 📁 docs/                        # Project documentation
├── 📁 tests/                       # Test suite
├── 📁 config/                      # MCPO configuration
├── 📁 data/                        # Runtime data and cache
└── 📁 scripts/                     # Legacy/utility scripts
```

## 🏗️ **MCP Server Ecosystem (`mcp/`)**

The core of the platform, containing all MCP servers and shared resources.

```
mcp/
├── servers/                        # Individual MCP server implementations
│   ├── openweather/               # Weather server (example)
│   │   ├── pyproject.toml         # UV dependencies and metadata
│   │   ├── openweather.py         # Server implementation
│   │   ├── run_uv.sh             # UV runner script
│   │   └── README.md             # Server documentation
│   └── [future-servers]/         # Additional servers (planned)
└── shared/                        # Shared resources and utilities
    ├── templates/                 # Server creation templates
    │   ├── pyproject.toml.template
    │   └── README.md.template
    ├── utils/                     # Common utilities (planned)
    ├── configs/                   # Shared configurations (planned)
    └── docs/                      # MCP-specific documentation
        └── README.md              # MCP servers overview
```

### **MCP Server Standards**
Each server follows this structure:
- **`pyproject.toml`**: UV dependencies, metadata, and custom MCP configuration
- **`{server-name}.py`**: Main server implementation using FastMCP
- **`run_uv.sh`**: UV environment setup and execution script
- **`README.md`**: Server documentation with usage examples
- **`tests/`**: Optional server-specific tests

## 📚 **Documentation (`docs/`)**

Comprehensive documentation covering all aspects of the platform.

```
docs/
├── README.md                      # Documentation index and navigation
├── STRUCTURE.md                   # This file - project structure guide
├── ROADMAP.md                     # Project roadmap and future plans
├── CLI_TOOL_SUMMARY.md           # CLI tool quick reference
├── OPEN_WEBUI_INTEGRATION.md     # Open-WebUI integration summary
├── ARCHITECTURE.md                # System architecture and design
├── DEVELOPMENT.md                 # Development workflow guide
├── SERVER_CREATION.md             # Step-by-step server creation
├── MCP_STANDARDS.md               # MCP protocol standards
├── AI_DEVELOPMENT_GUIDE.md        # AI-assisted development guide
├── SECURITY.md                    # Security best practices
├── configuration.md               # Legacy configuration docs
├── development.md                 # Legacy development notes
├── overview.md                    # Legacy overview
└── tools.md                       # Legacy tools documentation
```

### **Documentation Categories**
- **🚀 Getting Started**: README, DEVELOPMENT, SERVER_CREATION
- **📋 Standards**: MCP_STANDARDS, ARCHITECTURE, SECURITY
- **🗺️ Planning**: ROADMAP, CLI_TOOL_SUMMARY, OPEN_WEBUI_INTEGRATION
- **🤖 AI Development**: AI_DEVELOPMENT_GUIDE
- **📖 Legacy**: configuration, development, overview, tools

## 🧪 **Testing (`tests/`)**

Comprehensive test suite for validation and quality assurance.

```
tests/
├── README.md                      # Testing framework documentation
├── test_mcp_structure.py          # Comprehensive system tests
├── test_openweather.py            # OpenWeather server tests
└── cleanup_data_mounts.py         # Data cleanup utility
```

### **Test Categories**
- **System Tests**: Overall platform validation
- **Server Tests**: Individual MCP server testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Response time and load testing

## ⚙️ **Configuration (`config/`)**

MCPO configuration and templates.

```
config/
├── mcpo.json                      # Main MCPO server configuration
└── template.txt                   # Configuration template examples
```

### **Configuration Files**
- **`mcpo.json`**: Defines available MCP servers for Open-WebUI
- **`template.txt`**: Example configurations for different server types

## 💾 **Data & Runtime (`data/`)**

Runtime data, cache, and working directories.

```
data/
├── mcp-servers/                   # Working copies of MCP servers
│   └── openweather/              # Runtime OpenWeather server files
└── .uv-cache/                    # UV package cache (auto-generated)
```

### **Data Management**
- **Read-only mounts**: Source code from `mcp/servers/`
- **Read-write mounts**: Working directories in `data/`
- **Cache optimization**: UV cache for fast dependency resolution

## 🔧 **Scripts (`scripts/`)**

Legacy and utility scripts.

```
scripts/
└── install_deps.sh                # Legacy dependency installation
```

### **Script Categories**
- **Legacy Scripts**: Older dependency management (being phased out)
- **Utility Scripts**: Helper scripts for development and deployment

## 🐳 **Container Structure**

Docker volume mounts and container organization:

```
Container Mounts:
├── /config          ← ./config (read-only)
├── /mcp             ← ./mcp (read-only)
├── /memory          ← ./data (read-write)
├── /scripts         ← ./scripts (read-only)
└── /home/userx/host ← ${HOME}/host (read-write)
```

### **Security Model**
- **Source code**: Read-only mounts prevent container modification
- **Working data**: Read-write mounts for runtime operations
- **Environment variables**: Secure API key management via .env files

## 📦 **Package Management**

Modern UV-based dependency management:

```
UV Structure:
├── pyproject.toml files          # Dependency specifications
├── .uv-cache/                    # Package cache
└── Virtual environments          # Isolated per-server environments
```

### **Benefits**
- **Speed**: ~15ms package installation vs seconds with pip
- **Isolation**: Each server has its own environment
- **Reliability**: Deterministic dependency resolution

## 🔄 **Development Workflow**

Standard development paths through the structure:

1. **Server Creation**: `mcp/shared/templates/` → `mcp/servers/new-server/`
2. **Configuration**: Add to `config/mcpo.json`
3. **Testing**: Run tests from `tests/`
4. **Documentation**: Update relevant docs in `docs/`
5. **Deployment**: Container picks up changes automatically

## 🎯 **Future Structure (Planned)**

Upcoming additions to the structure:

```
mcp-server-platform/ (Future)
├── mcp/
│   ├── cli/                       # CLI tool implementation
│   ├── servers/
│   │   ├── database/             # Database connector servers
│   │   ├── filesystem/           # File system servers
│   │   └── api-integrations/     # Third-party API servers
│   └── shared/
│       ├── ui-components/        # Open-WebUI components
│       └── monitoring/           # Monitoring utilities
├── .github/
│   └── workflows/                # CI/CD pipelines
└── k8s/                          # Kubernetes manifests
```

## 📋 **File Naming Conventions**

- **Documentation**: `UPPERCASE.md` for major docs, `lowercase.md` for specific guides
- **Python files**: `snake_case.py` for all Python modules
- **Configuration**: `lowercase.json` for config files
- **Scripts**: `snake_case.sh` for shell scripts
- **Templates**: `name.template` for template files

## 🔍 **Navigation Tips**

- **Start here**: `README.md` for project overview
- **Development**: `docs/DEVELOPMENT.md` for workflow
- **Architecture**: `docs/ARCHITECTURE.md` for system design
- **Standards**: `docs/MCP_STANDARDS.md` for development standards
- **Planning**: `docs/ROADMAP.md` for future direction

This structure provides a scalable, maintainable foundation for the MCP Server Development Platform while supporting both current functionality and future enhancements.
