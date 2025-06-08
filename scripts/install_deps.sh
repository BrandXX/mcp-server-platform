#!/bin/bash

# Minimal startup script for MCPO
# Dependencies are now managed by UV per-tool

echo "Starting MCPO server..."
echo "Dependencies are managed by UV per-tool"

# Start the MCPO server with the provided arguments
exec mcpo "$@"
