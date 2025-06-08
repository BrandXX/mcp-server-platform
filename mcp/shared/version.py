"""
Version management for MCP Server Development Platform

This module provides centralized version information and utilities
for the platform and individual MCP servers.
"""

from typing import Dict, NamedTuple
from datetime import datetime

class VersionInfo(NamedTuple):
    """Version information structure"""
    major: int
    minor: int
    patch: int
    pre_release: str = ""
    build: str = ""

    def __str__(self) -> str:
        """String representation of version"""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version += f"-{self.pre_release}"
        if self.build:
            version += f"+{self.build}"
        return version

# Platform version information
PLATFORM_VERSION = VersionInfo(0, 2, 0)
PLATFORM_NAME = "MCP Server Development Platform"
PLATFORM_AUTHOR = "MCPO Platform"
PLATFORM_LICENSE = "MIT"
PLATFORM_REPOSITORY = "https://github.com/BrandXX/mcp-server-platform"

# MCP server versions
SERVER_VERSIONS: Dict[str, VersionInfo] = {
    "openweather": VersionInfo(0, 2, 0),
    "time": VersionInfo(1, 0, 0),  # External package
    "memory": VersionInfo(1, 0, 0),  # External package
}

def get_platform_version() -> str:
    """Get the platform version string"""
    return str(PLATFORM_VERSION)

def get_platform_info() -> Dict[str, str]:
    """Get comprehensive platform information"""
    return {
        "name": PLATFORM_NAME,
        "version": str(PLATFORM_VERSION),
        "author": PLATFORM_AUTHOR,
        "license": PLATFORM_LICENSE,
        "repository": PLATFORM_REPOSITORY,
        "build_date": datetime.now().isoformat(),
    }

def get_server_version(server_name: str) -> str:
    """Get version for a specific MCP server"""
    if server_name in SERVER_VERSIONS:
        return str(SERVER_VERSIONS[server_name])
    return "unknown"

def get_all_versions() -> Dict[str, str]:
    """Get versions for all components"""
    versions = {
        "platform": str(PLATFORM_VERSION),
    }
    
    for server, version in SERVER_VERSIONS.items():
        versions[f"server_{server}"] = str(version)
    
    return versions

def format_version_info() -> str:
    """Format comprehensive version information for display"""
    info = get_platform_info()
    
    lines = [
        f"🚀 {info['name']}",
        f"📦 Version: {info['version']}",
        f"👤 Author: {info['author']}",
        f"📄 License: {info['license']}",
        f"🔗 Repository: {info['repository']}",
        "",
        "📋 MCP Servers:",
    ]
    
    for server, version in SERVER_VERSIONS.items():
        lines.append(f"  • {server}: {version}")
    
    lines.extend([
        "",
        f"🕒 Build Date: {info['build_date']}",
    ])
    
    return "\n".join(lines)

# Version validation utilities
def is_compatible_version(required: str, current: str) -> bool:
    """Check if current version is compatible with required version"""
    try:
        req_parts = [int(x) for x in required.split('.')]
        cur_parts = [int(x) for x in current.split('.')]
        
        # Major version must match
        if req_parts[0] != cur_parts[0]:
            return False
        
        # Minor version must be >= required
        if len(req_parts) > 1 and len(cur_parts) > 1:
            if cur_parts[1] < req_parts[1]:
                return False
        
        return True
    except (ValueError, IndexError):
        return False

def update_server_version(server_name: str, version: VersionInfo) -> None:
    """Update version for a specific server"""
    SERVER_VERSIONS[server_name] = version

# Export main version for easy import
__version__ = str(PLATFORM_VERSION)
__author__ = PLATFORM_AUTHOR
__license__ = PLATFORM_LICENSE

if __name__ == "__main__":
    # Print version information when run directly
    print(format_version_info())
