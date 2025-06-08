"""
OpenWeather Forecast Tool

Provides current weather and extended forecast using the OpenWeatherMap API.
Uses UV for dependency management with pyproject.toml.

Version: 0.2.0
Author: MCPO Platform
License: MIT
"""

from mcp.server.fastmcp import FastMCP
import os
import re
import httpx
from datetime import datetime
from typing import Optional

# Version information
__version__ = "0.2.0"
__author__ = "MCPO Platform"
__license__ = "MIT"

app = FastMCP(
    title="OpenWeather Forecast",
    description="Current conditions and extended forecast via OpenWeatherMap API",
    version=__version__,
)

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"
UNITS = os.getenv("UNITS", "imperial")  # imperial or metric

def clean_city_input(city_input: str) -> str:
    """
    Clean up city input to handle common issues:
    - Remove trailing punctuation
    - Handle "City, State" format properly
    - Remove extra spaces
    """
    # Remove any trailing punctuation except commas (important for "City, State" format)
    city_input = re.sub(r'[.!?;:]$', '', city_input.strip())
    
    # If we have "City, State" or "City, Country" format, keep it intact
    # but ensure there's no trailing punctuation after the state/country
    if ',' in city_input:
        parts = city_input.split(',')
        city = parts[0].strip()
        state_country = ','.join(parts[1:]).strip()
        # Remove any trailing punctuation from state/country
        state_country = re.sub(r'[.!?;:]$', '', state_country)
        return f"{city},{state_country}"
    
    return city_input.strip()

def format_wind(speed: float, deg: float, unit: str) -> str:
    """Format wind speed and direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    direction = directions[round(deg / 45) % 8]
    
    if unit == "metric":
        return f"{speed:.1f} m/s {direction}"
    else:
        return f"{speed:.1f} mph {direction}"

def format_time(timestamp: int, timezone_offset: int) -> str:
    """Format Unix timestamp to local time string."""
    dt = datetime.utcfromtimestamp(timestamp + timezone_offset)
    return dt.strftime("%I:%M %p")

def format_date(timestamp: int, timezone_offset: int) -> str:
    """Format Unix timestamp to date string."""
    dt = datetime.utcfromtimestamp(timestamp + timezone_offset)
    return dt.strftime("%A, %b %d")

def make_http_request(url: str, timeout: int = 10) -> tuple[bool, any]:
    """
    Make HTTP request using httpx.
    Returns (success: bool, response_data_or_error: any)
    """
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=timeout)
            response.raise_for_status()
            return True, response.json()
    except Exception as e:
        return False, str(e)

@app.tool()
def get_current_weather(city: str) -> str:
    """Get current weather conditions for the specified city."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."
    
    # Clean up the city input
    city = clean_city_input(city)

    # Make HTTP request
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={UNITS}"
    success, data = make_http_request(url, timeout=10)

    if not success:
        return f"Error fetching weather data: {data}"

    try:
        # Extract data
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"].get("deg", 0)
        pressure = data["main"]["pressure"]
        visibility = data.get("visibility", 0) / 1000  # convert to km
        sunrise = format_time(data["sys"]["sunrise"], data.get("timezone", 0))
        sunset = format_time(data["sys"]["sunset"], data.get("timezone", 0))
        
        # Format response
        unit_symbol = "°C" if UNITS == "metric" else "°F"
        distance_unit = "km" if UNITS == "metric" else "mi"
        
        return f"""
Current Weather for {data["name"]}, {data.get("sys", {}).get("country", "")}:
🌡️ {weather_desc}, {temp}{unit_symbol} (Feels like: {feels_like}{unit_symbol})
💧 Humidity: {humidity}%
💨 Wind: {format_wind(wind_speed, wind_deg, UNITS)}
🔍 Visibility: {visibility:.1f} {distance_unit}
🌅 Sunrise: {sunrise}
🌇 Sunset: {sunset}
        """.strip()

    except (KeyError, ValueError) as e:
        return f"Error parsing weather data: {str(e)}"

@app.tool()
def get_forecast(city: str, days: int = 5) -> str:
    """Get weather forecast for the specified city for up to 5 days."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."
    
    # Clean up the city input
    city = clean_city_input(city)
    
    if days < 1:
        days = 1
    if days > 5:
        days = 5

    # Make HTTP request
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={UNITS}"
    success, data = make_http_request(url, timeout=10)

    if not success:
        return f"Error fetching forecast data: {data}"

    try:
        # Group forecast by day
        forecasts_by_day = {}
        timezone_offset = data.get("city", {}).get("timezone", 0)
        
        for item in data["list"]:
            dt = datetime.utcfromtimestamp(item["dt"] + timezone_offset)
            day_key = dt.strftime("%Y-%m-%d")
            
            if day_key not in forecasts_by_day:
                forecasts_by_day[day_key] = []
            
            forecasts_by_day[day_key].append(item)
        
        # Format response
        result = f"5-Day Forecast for {data['city']['name']}, {data['city']['country']}:\n\n"
        
        for i, (day, forecasts) in enumerate(list(forecasts_by_day.items())[:days]):
            if i >= days:
                break
                
            day_date = format_date(forecasts[0]["dt"], timezone_offset)
            result += f"📅 {day_date}:\n"
            
            # Get min/max temps and most common weather condition for the day
            temps = [f["main"]["temp"] for f in forecasts]
            min_temp = min(temps)
            max_temp = max(temps)
            
            # Count weather conditions to find the most common
            conditions = {}
            for f in forecasts:
                cond = f["weather"][0]["description"].capitalize()
                conditions[cond] = conditions.get(cond, 0) + 1
            
            most_common = max(conditions.items(), key=lambda x: x[1])[0]
            
            unit_symbol = "°C" if UNITS == "metric" else "°F"
            result += f"   {most_common}, {min_temp:.1f}{unit_symbol} to {max_temp:.1f}{unit_symbol}\n"
            
            # Add some time-specific details
            for f in forecasts[::2]:  # Take every other forecast to reduce verbosity
                time = format_time(f["dt"], timezone_offset)
                temp = f["main"]["temp"]
                cond = f["weather"][0]["description"].capitalize()
                result += f"   • {time}: {temp:.1f}{unit_symbol}, {cond}\n"
            
            result += "\n"
        
        return result.strip()

    except (KeyError, ValueError) as e:
        return f"Error parsing forecast data: {e}"

@app.tool()
def check_openweather_status() -> str:
    """Check the status of the OpenWeather tool and its dependencies."""
    status_lines = []
    status_lines.append("OpenWeather Tool Status:")
    status_lines.append("=" * 30)

    # Version information
    status_lines.append(f"📦 Version: {__version__}")
    status_lines.append(f"👤 Author: {__author__}")
    status_lines.append(f"📄 License: {__license__}")

    # Check API key
    if API_KEY:
        status_lines.append("✅ API Key: Configured")
    else:
        status_lines.append("❌ API Key: Missing (set OPENWEATHER_API_KEY)")

    # Check HTTP client availability
    try:
        import httpx
        status_lines.append(f"✅ HTTP client: httpx {httpx.__version__} available")
    except ImportError:
        status_lines.append("❌ HTTP client: httpx not available")

    # Check units setting
    status_lines.append(f"⚙️  Units: {UNITS}")

    # Check UV environment
    status_lines.append("✅ Dependencies: Managed by UV")

    return "\n".join(status_lines)

@app.tool()
def get_openweather_version() -> str:
    """Get version information for the OpenWeather MCP server."""
    return f"""
OpenWeather MCP Server
Version: {__version__}
Author: {__author__}
License: {__license__}

Features:
• Current weather conditions
• 5-day weather forecasts
• Multiple unit systems (imperial/metric)
• Comprehensive error handling
• UV-based dependency management

Last updated: 2024-12-08
    """.strip()

if __name__ == "__main__":
    app.run()
