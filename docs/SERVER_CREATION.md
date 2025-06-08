# MCP Server Creation Tutorial

This step-by-step tutorial guides you through creating a new MCP server from scratch, using a practical example that demonstrates all key concepts and best practices.

## 🎯 Tutorial Goal

We'll create a **"Quote of the Day" MCP server** that:
- Fetches inspirational quotes from an API
- Provides different quote categories
- Demonstrates proper error handling
- Shows Open-WebUI integration best practices

## 📋 Prerequisites

- Development environment set up (see [DEVELOPMENT.md](DEVELOPMENT.md))
- Basic Python knowledge
- Understanding of MCP concepts (see [MCP_STANDARDS.md](MCP_STANDARDS.md))

## 🚀 Step 1: Project Setup

### Create Server Directory
```bash
# Navigate to servers directory
cd mcp/servers

# Create new server directory
mkdir quote-of-the-day
cd quote-of-the-day
```

### Copy Template Files
```bash
# Copy templates from shared directory
cp ../../shared/templates/pyproject.toml.template pyproject.toml
cp ../../shared/templates/README.md.template README.md
```

## 🔧 Step 2: Configure Dependencies

Edit `pyproject.toml`:
```toml
[project]
name = "quote-of-the-day-mcp-server"
version = "0.1.0"
description = "MCP server providing inspirational quotes and daily motivation"
authors = [
    {name = "MCP Developer", email = "dev@example.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
keywords = ["mcp", "quotes", "inspiration", "motivation"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0"
]

[project.urls]
Homepage = "https://github.com/your-org/mcp-servers"
Repository = "https://github.com/your-org/mcp-servers"
Documentation = "https://github.com/your-org/mcp-servers/tree/main/mcp/servers/quote-of-the-day"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0"
]

[tool.mcp-server]
title = "Quote of the Day"
category = "inspiration"
tags = ["quotes", "motivation", "daily", "inspiration"]
env_vars = [
    {name = "QUOTES_API_KEY", required = false, description = "Optional API key for premium quotes service"},
    {name = "DEFAULT_CATEGORY", required = false, default = "inspirational", description = "Default quote category"}
]
```

## 💻 Step 3: Implement the Server

Create `quote-of-the-day.py`:
```python
#!/usr/bin/env python3
"""
Quote of the Day MCP Server

Provides inspirational quotes and daily motivation through various tools.
Integrates with Open-WebUI to deliver motivational content to AI assistants.
"""

import os
import random
from datetime import datetime
from typing import Optional, List
import httpx
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Quote of the Day")

# Configuration
QUOTES_API_KEY = os.getenv("QUOTES_API_KEY")
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "inspirational")

# Fallback quotes for offline operation
FALLBACK_QUOTES = [
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "inspirational"
    },
    {
        "text": "Innovation distinguishes between a leader and a follower.",
        "author": "Steve Jobs", 
        "category": "innovation"
    },
    {
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "category": "motivation"
    }
]

def validate_category(category: str) -> str:
    """Validate and sanitize category input"""
    if not category or not category.strip():
        return DEFAULT_CATEGORY
    
    # Sanitize input
    sanitized = "".join(c for c in category.lower() if c.isalnum() or c in "-_")
    
    # Valid categories
    valid_categories = [
        "inspirational", "motivation", "success", "innovation", 
        "leadership", "wisdom", "life", "happiness"
    ]
    
    return sanitized if sanitized in valid_categories else DEFAULT_CATEGORY

async def fetch_quote_from_api(category: str) -> Optional[dict]:
    """Fetch quote from external API with error handling"""
    try:
        # Example API call (replace with actual API)
        url = f"https://api.quotable.io/random?tags={category}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "text": data.get("content", ""),
                    "author": data.get("author", "Unknown"),
                    "category": category
                }
    except Exception as e:
        print(f"API fetch failed: {e}")
    
    return None

def get_fallback_quote(category: str) -> dict:
    """Get fallback quote when API is unavailable"""
    # Filter by category or return random
    category_quotes = [q for q in FALLBACK_QUOTES if q["category"] == category]
    
    if category_quotes:
        return random.choice(category_quotes)
    else:
        return random.choice(FALLBACK_QUOTES)

def format_quote_response(quote: dict) -> str:
    """Format quote for optimal Open-WebUI display"""
    return f"""✨ **Quote of the Day**

> *"{quote['text']}"*

**— {quote['author']}**

📂 Category: {quote['category'].title()}
🕐 Retrieved: {datetime.now().strftime('%H:%M:%S')}

💡 *Need more inspiration? Ask for quotes in different categories!*"""

@mcp.tool()
async def get_daily_quote(category: Optional[str] = None) -> str:
    """
    Get an inspirational quote for the day.
    
    Fetches a motivational quote from various categories to inspire and motivate.
    Perfect for starting the day with positive energy or finding motivation.
    
    Args:
        category: Quote category (inspirational, motivation, success, innovation, 
                 leadership, wisdom, life, happiness). Defaults to 'inspirational'
        
    Returns:
        Formatted inspirational quote with author and metadata
        
    Raises:
        ValueError: When category is invalid
    """
    try:
        # Validate and set category
        validated_category = validate_category(category or DEFAULT_CATEGORY)
        
        # Try to fetch from API first
        quote = await fetch_quote_from_api(validated_category)
        
        # Fall back to local quotes if API fails
        if not quote:
            quote = get_fallback_quote(validated_category)
        
        return format_quote_response(quote)
        
    except Exception as e:
        return f"❌ **Error**: Unable to fetch quote. {str(e)}"

@mcp.tool()
def list_quote_categories() -> str:
    """
    List available quote categories.
    
    Shows all available categories for quotes, helping users discover
    different types of inspirational content.
    
    Returns:
        Formatted list of available quote categories with descriptions
    """
    categories = {
        "inspirational": "General inspirational and uplifting quotes",
        "motivation": "Quotes focused on motivation and drive",
        "success": "Quotes about achieving success and goals",
        "innovation": "Quotes about creativity and innovation",
        "leadership": "Quotes about leadership and management",
        "wisdom": "Wise sayings and philosophical thoughts",
        "life": "Quotes about life experiences and lessons",
        "happiness": "Quotes focused on joy and happiness"
    }
    
    response = ["📚 **Available Quote Categories**\n"]
    
    for category, description in categories.items():
        response.append(f"• **{category.title()}**: {description}")
    
    response.append(f"\n💡 *Use `get_daily_quote(category='category_name')` to get quotes from a specific category.*")
    
    return "\n".join(response)

@mcp.tool()
def get_quote_server_status() -> str:
    """
    Check the status of the Quote of the Day server.
    
    Provides information about server configuration, available features,
    and current operational status.
    
    Returns:
        Formatted status information about the quote server
    """
    status_info = [
        "🎯 **Quote of the Day Server Status**",
        "=" * 40,
        f"✅ Server: Online and operational",
        f"📂 Default Category: {DEFAULT_CATEGORY}",
        f"🔑 API Key: {'Configured' if QUOTES_API_KEY else 'Not configured (using fallback quotes)'}",
        f"📊 Fallback Quotes: {len(FALLBACK_QUOTES)} available",
        f"🕐 Server Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "🛠️ **Available Tools:**",
        "• get_daily_quote() - Get inspirational quotes",
        "• list_quote_categories() - Show available categories", 
        "• get_quote_server_status() - This status check",
        "",
        "💡 *Ready to provide daily inspiration and motivation!*"
    ]
    
    return "\n".join(status_info)

if __name__ == "__main__":
    mcp.run()
```

## 🏃 Step 4: Create Runner Script

Create `run_uv.sh`:
```bash
#!/bin/bash

# UV Runner Script for Quote of the Day MCP Server
set -e

# Define paths
SERVER_DIR="/mcp/servers/quote-of-the-day"
WORK_DIR="/memory/mcp-servers/quote-of-the-day"
CACHE_DIR="/memory/.uv-cache"

# Create working directory if it doesn't exist
mkdir -p "$WORK_DIR"
mkdir -p "$CACHE_DIR"

# Copy project files to writable location if they don't exist or are newer
if [ ! -f "$WORK_DIR/pyproject.toml" ] || [ "$SERVER_DIR/pyproject.toml" -nt "$WORK_DIR/pyproject.toml" ]; then
    echo "Copying pyproject.toml..."
    cp "$SERVER_DIR/pyproject.toml" "$WORK_DIR/"
fi

if [ ! -f "$WORK_DIR/quote-of-the-day.py" ] || [ "$SERVER_DIR/quote-of-the-day.py" -nt "$WORK_DIR/quote-of-the-day.py" ]; then
    echo "Copying quote-of-the-day.py..."
    cp "$SERVER_DIR/quote-of-the-day.py" "$WORK_DIR/"
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
exec uv run --no-sync python quote-of-the-day.py
```

Make it executable:
```bash
chmod +x run_uv.sh
```

## ⚙️ Step 5: Configure MCPO Integration

Add to `config/mcpo.json`:
```json
{
  "mcpServers": {
    "quote-of-the-day": {
      "title": "Quote of the Day",
      "description": "Daily inspirational quotes and motivation",
      "command": "bash",
      "args": ["/mcp/servers/quote-of-the-day/run_uv.sh"],
      "preload": true,
      "env": {
        "DEFAULT_CATEGORY": "inspirational"
      }
    }
  }
}
```

## 🧪 Step 6: Test Your Server

### Local Testing
```bash
# Test locally first
cd mcp/servers/quote-of-the-day
uv run python quote-of-the-day.py
```

### Container Testing
```bash
# Restart container
docker compose restart mcpo

# Test endpoints
curl -X POST "http://localhost:8989/quote-of-the-day/get_daily_quote" \
  -H "Content-Type: application/json" \
  -d '{}'

curl -X POST "http://localhost:8989/quote-of-the-day/list_quote_categories" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Comprehensive Testing
```bash
# Run system tests
python tests/test_mcp_structure.py
```

## 📚 Step 7: Document Your Server

Update `README.md`:
```markdown
# Quote of the Day MCP Server

Provides daily inspirational quotes and motivation through the Model Context Protocol.

## Features

- 🎯 Daily inspirational quotes
- 📚 Multiple quote categories
- 🔄 Fallback quotes for offline operation
- ✨ Open-WebUI optimized formatting

## Tools

### get_daily_quote(category: Optional[str]) -> str
Get an inspirational quote for the day from various categories.

### list_quote_categories() -> str
List all available quote categories with descriptions.

### get_quote_server_status() -> str
Check server status and configuration.

## Configuration

### Environment Variables
- `QUOTES_API_KEY`: Optional API key for premium quotes service
- `DEFAULT_CATEGORY`: Default quote category (default: "inspirational")

## Installation

This server uses UV for dependency management and is automatically configured in the MCP platform.

## Usage Examples

```python
# Get a daily quote
get_daily_quote()

# Get a motivational quote
get_daily_quote(category="motivation")

# List available categories
list_quote_categories()
```
```

## 🎉 Congratulations!

You've successfully created a complete MCP server! Your server now:

- ✅ Follows MCP standards and best practices
- ✅ Integrates with Open-WebUI
- ✅ Uses UV for fast dependency management
- ✅ Includes comprehensive error handling
- ✅ Provides helpful documentation
- ✅ Is ready for production use

## 🚀 Next Steps

1. **Add Tests**: Create specific tests for your server
2. **Enhance Features**: Add more tools and functionality
3. **Optimize Performance**: Monitor and improve response times
4. **Share**: Contribute your server to the community

This tutorial demonstrates the complete process of creating professional MCP servers in this platform.
