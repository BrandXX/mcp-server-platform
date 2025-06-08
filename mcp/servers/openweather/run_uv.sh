#!/bin/bash

# UV Runner Script for OpenWeather MCP Server
# This script sets up the UV environment and runs the server

set -e

# Define paths
SERVER_DIR="/mcp/servers/openweather"
WORK_DIR="/memory/mcp-servers/openweather"
CACHE_DIR="/memory/.uv-cache"

# Create working directory if it doesn't exist
mkdir -p "$WORK_DIR"
mkdir -p "$CACHE_DIR"

# Copy project files to writable location if they don't exist or are newer
if [ ! -f "$WORK_DIR/pyproject.toml" ] || [ "$SERVER_DIR/pyproject.toml" -nt "$WORK_DIR/pyproject.toml" ]; then
    echo "Copying pyproject.toml..."
    cp "$SERVER_DIR/pyproject.toml" "$WORK_DIR/"
fi

if [ ! -f "$WORK_DIR/openweather.py" ] || [ "$SERVER_DIR/openweather.py" -nt "$WORK_DIR/openweather.py" ]; then
    echo "Copying openweather.py..."
    cp "$SERVER_DIR/openweather.py" "$WORK_DIR/"
fi

# Set UV cache directory
export UV_CACHE_DIR="$CACHE_DIR"

# Change to working directory
cd "$WORK_DIR"

# Ensure dependencies are installed (only if not already done)
if [ ! -f "$WORK_DIR/.uv-installed" ]; then
    echo "Installing dependencies with UV..."
    uv sync --no-dev
    touch "$WORK_DIR/.uv-installed"
fi

# Run the server with UV (using the existing venv)
exec uv run --no-sync python openweather.py
