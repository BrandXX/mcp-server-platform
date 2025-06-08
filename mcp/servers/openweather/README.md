# OpenWeather MCP Server

A Model Context Protocol (MCP) server that provides current weather conditions and 5-day forecasts using the OpenWeatherMap API.

## Features

- **Current Weather**: Get real-time weather conditions for any city
- **5-Day Forecast**: Extended weather forecasts with detailed information
- **Multiple Units**: Support for imperial and metric units
- **Smart City Input**: Handles various city name formats
- **Error Handling**: Comprehensive error handling and validation

## Tools

### `get_current_weather(city: str) -> str`
Get current weather conditions for the specified city.

**Parameters:**
- `city`: City name (e.g., "London", "New York", "Tokyo")

**Returns:** Formatted weather information including temperature, humidity, wind, and more.

### `get_forecast(city: str, days: int = 5) -> str`
Get weather forecast for the specified city.

**Parameters:**
- `city`: City name
- `days`: Number of days (1-5, default: 5)

**Returns:** Detailed forecast with daily summaries and time-specific conditions.

### `check_openweather_status() -> str`
Check the status of the OpenWeather tool and its dependencies.

**Returns:** Status information including API key configuration and dependencies.

## Configuration

### Environment Variables

- `OPENWEATHER_API_KEY` (required): Your OpenWeatherMap API key
- `UNITS` (optional): Temperature units - "imperial" (default) or "metric"

### Getting an API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Set the `OPENWEATHER_API_KEY` environment variable

## Installation

This server uses UV for dependency management:

```bash
# Install dependencies
uv sync

# Run the server
uv run python openweather.py
```

## Usage Examples

```python
# Get current weather
get_current_weather("London")

# Get 3-day forecast
get_forecast("New York", 3)

# Check status
check_openweather_status()
```

## Dependencies

- `httpx`: Modern HTTP client for API requests
- `fastmcp`: FastMCP framework for MCP server development

## Version

Current version: 0.2.0

## License

MIT License
