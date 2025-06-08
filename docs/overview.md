# MCPO Overview

MCPO (Model Context Protocol Orchestrator) is a Docker-based service that provides various tools to AI models through the Model Context Protocol.

## Architecture

MCPO runs as a container that hosts multiple MCP servers. Each server provides a specific capability like weather information, time services, or scaffolding tools.

The service is configured through a JSON configuration file and exposes its API on port 8000 (mapped to 8989 on the host).

## Integration

MCPO integrates with Open WebUI, allowing AI models to access tools through a standardized interface.