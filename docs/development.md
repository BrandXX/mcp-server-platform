# Legacy Development Guide

⚠️ **This document contains legacy information. For current development practices, see:**
- **[DEVELOPMENT.md](DEVELOPMENT.md)**: Modern development workflow
- **[SERVER_CREATION.md](SERVER_CREATION.md)**: Step-by-step server creation
- **[MCP_STANDARDS.md](MCP_STANDARDS.md)**: Current standards and best practices

## Historical Context

This document describes the legacy development approach used before the migration to the modern UV-based architecture. It's preserved for reference but should not be used for new development.

### Legacy Tool Creation (Deprecated)

The old approach used the `/scripts` directory and manual dependency management:

1. Create a Python script in the `/scripts` directory
2. Use the FastMCP framework:
   ```python
   from mcp.server.fastmcp import FastMCP

   app = FastMCP(
       title="Your Tool Name",
       description="Tool description",
       version="0.1.0",
   )

   @app.tool()
   def your_function(param: str) -> str:
       """Function documentation"""
       # Implementation
       return result

   if __name__ == "__main__":
       app.run()
   ```

3. Add an entry to `config/mcpo.json`:
   ```json
   "your_tool_id": {
     "title": "Your Tool Name",
     "description": "Tool description",
     "command": "python",
     "args": ["/scripts/your_tool.py"],
     "preload": true
   }
   ```

### Modern Approach (Current)

The current approach uses the `/mcp/servers/` structure with UV dependency management. See the current documentation for details.

## Legacy Dependency Management (Deprecated)

The old system used manual dependency checking and installation:

### Old Dependency System
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dependency_utils import ensure_dependencies

REQUIRED_PACKAGES = ["requests", "beautifulsoup4"]

@app.tool()
def my_tool_function(param: str) -> str:
    deps_error = ensure_dependencies(REQUIRED_PACKAGES)
    if deps_error:
        return deps_error
    # ... rest of code
```

### Why It Was Replaced

The legacy dependency system had several issues:
- **Slow**: pip-based installation took seconds
- **Complex**: Required custom utility functions
- **Error-prone**: Manual dependency tracking
- **Maintenance**: Required updating dependency_utils.py

### Modern Alternative

The current UV-based system provides:
- **⚡ Speed**: Millisecond package installation
- **🔒 Isolation**: Per-server virtual environments
- **📦 Standards**: Standard pyproject.toml configuration
- **🔄 Reliability**: Deterministic dependency resolution

See [DEVELOPMENT.md](DEVELOPMENT.md) for current best practices.

## Migration Notes

If you have legacy tools using the old system:

1. **Create New Server**: Use the modern `/mcp/servers/` structure
2. **Convert Dependencies**: Move from `dependency_utils` to `pyproject.toml`
3. **Update Configuration**: Change `mcpo.json` to point to new location
4. **Test Thoroughly**: Verify functionality with new system
5. **Remove Legacy**: Clean up old files after migration

For detailed migration instructions, see the development documentation.
