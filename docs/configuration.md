# MCPO Configuration

> **Note**: This is legacy documentation. For comprehensive configuration guides, see:
> - **[config/README.md](../config/README.md)** - Complete configuration guide
> - **[config/mcpo-config-template.json](../config/mcpo-config-template.json)** - Configuration templates
> - **[config/mcpo-examples.json](../config/mcpo-examples.json)** - Real-world examples

## Main Configuration File

MCPO is configured through `config/mcpo.json`, which defines the available MCP servers.

### Configuration Format

Each server entry follows this structure:

```json
"server_name": {
  "title": "Human-readable Title",
  "description": "Brief description of the tool",
  "command": "executable",
  "args": ["arg1", "arg2"],
  "preload": true|false,
  "env": { "ENV_VAR": "value" }
}
```

For HTTP-based servers, use this format:

```json
"server_name": {
  "title": "Human-readable Title",
  "description": "Brief description of the tool",
  "url": "https://provider.com/mcp",
  "server_type": "http" | "streamable_http",
  "headers": { "Authorization": "Bearer token" },
  "preload": false
}
```

### Docker Configuration

MCPO runs as a Docker container with these volume mappings:
- `./mcpo/config:/config:ro` - Configuration files
- `./mcpo/data:/memory` - Persistent data
- `./mcpo/scripts:/scripts:ro` - Tool scripts