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
import math
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple

# Version information
__version__ = "0.3.0"
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
• Weather alerts and warnings
• Air quality index and pollution data
• Detailed astronomy data (sunrise, sunset, moon phases)
• Multi-city weather comparison
• Weather-based activity recommendations
• Multiple unit systems (imperial/metric)
• Comprehensive error handling
• UV-based dependency management

Last updated: 2024-12-08
    """.strip()

@app.tool()
def get_weather_alerts(city: str) -> str:
    """Get weather alerts and warnings for the specified city."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."

    # Clean up the city input
    city = clean_city_input(city)

    # First get coordinates for the city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    success, geo_data = make_http_request(geo_url, timeout=10)

    if not success or not geo_data:
        return f"Error: Could not find coordinates for {city}"

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # Get weather alerts using One Call API
    alerts_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&exclude=minutely,hourly,daily"
    success, data = make_http_request(alerts_url, timeout=10)

    if not success:
        return f"Error fetching weather alerts: {data}"

    try:
        alerts = data.get("alerts", [])

        if not alerts:
            return f"🟢 No weather alerts for {geo_data[0]['name']}, {geo_data[0].get('country', '')}"

        result = f"⚠️ Weather Alerts for {geo_data[0]['name']}, {geo_data[0].get('country', '')}:\n\n"

        for i, alert in enumerate(alerts, 1):
            sender = alert.get("sender_name", "Weather Service")
            event = alert.get("event", "Weather Alert")
            start = datetime.utcfromtimestamp(alert["start"]).strftime("%Y-%m-%d %H:%M UTC")
            end = datetime.utcfromtimestamp(alert["end"]).strftime("%Y-%m-%d %H:%M UTC")
            description = alert.get("description", "No description available")

            # Determine alert emoji based on event type
            alert_emoji = "🌪️" if "tornado" in event.lower() else \
                         "⛈️" if any(word in event.lower() for word in ["storm", "thunder", "lightning"]) else \
                         "🌨️" if any(word in event.lower() for word in ["snow", "blizzard", "ice"]) else \
                         "🌊" if "flood" in event.lower() else \
                         "🔥" if "fire" in event.lower() else \
                         "💨" if "wind" in event.lower() else "⚠️"

            result += f"{alert_emoji} Alert #{i}: {event}\n"
            result += f"📅 From: {start}\n"
            result += f"📅 To: {end}\n"
            result += f"📡 Source: {sender}\n"
            result += f"📝 Details: {description[:200]}{'...' if len(description) > 200 else ''}\n\n"

        return result.strip()

    except (KeyError, ValueError) as e:
        return f"Error parsing weather alerts: {str(e)}"

@app.tool()
def get_air_quality(city: str) -> str:
    """Get air quality index and pollution data for the specified city."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."

    # Clean up the city input
    city = clean_city_input(city)

    # First get coordinates for the city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    success, geo_data = make_http_request(geo_url, timeout=10)

    if not success or not geo_data:
        return f"Error: Could not find coordinates for {city}"

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # Get air quality data
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    success, data = make_http_request(aqi_url, timeout=10)

    if not success:
        return f"Error fetching air quality data: {data}"

    try:
        aqi_data = data["list"][0]
        aqi_index = aqi_data["main"]["aqi"]
        components = aqi_data["components"]

        # AQI level descriptions
        aqi_levels = {
            1: ("🟢 Good", "Air quality is satisfactory"),
            2: ("🟡 Fair", "Air quality is acceptable for most people"),
            3: ("🟠 Moderate", "Sensitive individuals may experience minor issues"),
            4: ("🔴 Poor", "Everyone may experience health effects"),
            5: ("🟣 Very Poor", "Health warnings of emergency conditions")
        }

        level, description = aqi_levels.get(aqi_index, ("❓ Unknown", "Unknown air quality level"))

        result = f"🌬️ Air Quality for {geo_data[0]['name']}, {geo_data[0].get('country', '')}:\n\n"
        result += f"📊 Overall AQI: {level} (Level {aqi_index}/5)\n"
        result += f"📝 {description}\n\n"
        result += "🧪 Pollutant Concentrations (μg/m³):\n"
        result += f"• CO (Carbon Monoxide): {components.get('co', 'N/A')}\n"
        result += f"• NO (Nitrogen Monoxide): {components.get('no', 'N/A')}\n"
        result += f"• NO₂ (Nitrogen Dioxide): {components.get('no2', 'N/A')}\n"
        result += f"• O₃ (Ozone): {components.get('o3', 'N/A')}\n"
        result += f"• SO₂ (Sulfur Dioxide): {components.get('so2', 'N/A')}\n"
        result += f"• PM2.5 (Fine Particles): {components.get('pm2_5', 'N/A')}\n"
        result += f"• PM10 (Coarse Particles): {components.get('pm10', 'N/A')}\n"
        result += f"• NH₃ (Ammonia): {components.get('nh3', 'N/A')}\n"

        # Add health recommendations
        if aqi_index >= 4:
            result += "\n⚠️ Health Recommendations:\n"
            result += "• Limit outdoor activities\n"
            result += "• Wear a mask when outside\n"
            result += "• Keep windows closed\n"
            result += "• Use air purifiers indoors\n"
        elif aqi_index == 3:
            result += "\n💡 Recommendations:\n"
            result += "• Sensitive individuals should limit outdoor activities\n"
            result += "• Consider wearing a mask during exercise\n"

        return result

    except (KeyError, ValueError) as e:
        return f"Error parsing air quality data: {str(e)}"

@app.tool()
def get_astronomy_data(city: str) -> str:
    """Get detailed astronomy data including sunrise, sunset, moon phase, and solar position."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."

    # Clean up the city input
    city = clean_city_input(city)

    # Get current weather data for basic astronomy info
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={UNITS}"
    success, data = make_http_request(url, timeout=10)

    if not success:
        return f"Error fetching astronomy data: {data}"

    try:
        timezone_offset = data.get("timezone", 0)
        sunrise_ts = data["sys"]["sunrise"]
        sunset_ts = data["sys"]["sunset"]

        # Calculate additional astronomy data
        now = datetime.utcnow()
        sunrise = datetime.utcfromtimestamp(sunrise_ts)
        sunset = datetime.utcfromtimestamp(sunset_ts)

        # Calculate day length
        day_length = sunset - sunrise
        hours = day_length.seconds // 3600
        minutes = (day_length.seconds % 3600) // 60

        # Calculate solar noon (midpoint between sunrise and sunset)
        solar_noon = sunrise + (sunset - sunrise) / 2

        # Simple moon phase calculation (approximate)
        # This is a simplified calculation - for production, you'd want a more accurate algorithm
        days_since_new_moon = (now - datetime(2000, 1, 6)).days % 29.53

        if days_since_new_moon < 1:
            moon_phase = "🌑 New Moon"
        elif days_since_new_moon < 7.4:
            moon_phase = "🌒 Waxing Crescent"
        elif days_since_new_moon < 8.4:
            moon_phase = "🌓 First Quarter"
        elif days_since_new_moon < 14.8:
            moon_phase = "🌔 Waxing Gibbous"
        elif days_since_new_moon < 15.8:
            moon_phase = "🌕 Full Moon"
        elif days_since_new_moon < 22.1:
            moon_phase = "🌖 Waning Gibbous"
        elif days_since_new_moon < 23.1:
            moon_phase = "🌗 Last Quarter"
        else:
            moon_phase = "🌘 Waning Crescent"

        # Calculate illumination percentage (approximate)
        illumination = abs(math.cos((days_since_new_moon / 29.53) * 2 * math.pi)) * 100

        result = f"🌌 Astronomy Data for {data['name']}, {data.get('sys', {}).get('country', '')}:\n\n"
        result += f"🌅 Sunrise: {format_time(sunrise_ts, timezone_offset)}\n"
        result += f"🌇 Sunset: {format_time(sunset_ts, timezone_offset)}\n"
        result += f"☀️ Solar Noon: {format_time(int(solar_noon.timestamp()), timezone_offset)}\n"
        result += f"⏰ Day Length: {hours}h {minutes}m\n\n"
        result += f"🌙 Moon Phase: {moon_phase}\n"
        result += f"💡 Moon Illumination: {illumination:.1f}%\n\n"

        # Calculate if it's currently day or night
        current_time = datetime.utcnow()
        if sunrise <= current_time <= sunset:
            time_to_sunset = sunset - current_time
            hours_to_sunset = time_to_sunset.seconds // 3600
            minutes_to_sunset = (time_to_sunset.seconds % 3600) // 60
            result += f"☀️ Currently: Daytime\n"
            result += f"🌇 Sunset in: {hours_to_sunset}h {minutes_to_sunset}m\n"
        else:
            # Calculate time to next sunrise
            if current_time > sunset:
                next_sunrise = sunrise + timedelta(days=1)
            else:
                next_sunrise = sunrise

            time_to_sunrise = next_sunrise - current_time
            hours_to_sunrise = time_to_sunrise.seconds // 3600
            minutes_to_sunrise = (time_to_sunrise.seconds % 3600) // 60
            result += f"🌙 Currently: Nighttime\n"
            result += f"🌅 Sunrise in: {hours_to_sunrise}h {minutes_to_sunrise}m\n"

        return result

    except (KeyError, ValueError) as e:
        return f"Error parsing astronomy data: {str(e)}"

@app.tool()
def compare_weather(cities: str) -> str:
    """Compare current weather conditions between multiple cities (comma-separated)."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."

    # Parse cities from comma-separated string
    city_list = [city.strip() for city in cities.split(",") if city.strip()]

    if len(city_list) < 2:
        return "Error: Please provide at least 2 cities separated by commas (e.g., 'London, Paris, Tokyo')"

    if len(city_list) > 5:
        return "Error: Maximum 5 cities allowed for comparison"

    weather_data = []

    # Fetch weather for each city
    for city in city_list:
        city = clean_city_input(city)
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={UNITS}"
        success, data = make_http_request(url, timeout=10)

        if success:
            try:
                weather_info = {
                    "name": f"{data['name']}, {data.get('sys', {}).get('country', '')}",
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "visibility": data.get("visibility", 0) / 1000
                }
                weather_data.append(weather_info)
            except (KeyError, ValueError):
                weather_data.append({"name": city, "error": "Failed to parse weather data"})
        else:
            weather_data.append({"name": city, "error": f"Failed to fetch data: {data}"})

    if not weather_data:
        return "Error: Could not fetch weather data for any of the specified cities"

    # Format comparison
    unit_symbol = "°C" if UNITS == "metric" else "°F"
    speed_unit = "m/s" if UNITS == "metric" else "mph"

    result = f"🌍 Weather Comparison for {len(weather_data)} Cities:\n\n"

    # Create a formatted table
    for i, data in enumerate(weather_data, 1):
        if "error" in data:
            result += f"{i}. ❌ {data['name']}: {data['error']}\n\n"
            continue

        result += f"{i}. 📍 {data['name']}:\n"
        result += f"   🌡️ {data['temp']:.1f}{unit_symbol} (feels like {data['feels_like']:.1f}{unit_symbol})\n"
        result += f"   🌤️ {data['description']}\n"
        result += f"   💧 Humidity: {data['humidity']}%\n"
        result += f"   💨 Wind: {data['wind_speed']:.1f} {speed_unit}\n"
        result += f"   👁️ Visibility: {data['visibility']:.1f} km\n"
        result += f"   🔍 Pressure: {data['pressure']} hPa\n\n"

    # Add some comparison insights
    valid_data = [d for d in weather_data if "error" not in d]
    if len(valid_data) >= 2:
        temps = [d["temp"] for d in valid_data]
        humidities = [d["humidity"] for d in valid_data]

        hottest = max(valid_data, key=lambda x: x["temp"])
        coldest = min(valid_data, key=lambda x: x["temp"])
        most_humid = max(valid_data, key=lambda x: x["humidity"])

        result += "📊 Comparison Highlights:\n"
        result += f"🔥 Hottest: {hottest['name']} ({hottest['temp']:.1f}{unit_symbol})\n"
        result += f"🧊 Coldest: {coldest['name']} ({coldest['temp']:.1f}{unit_symbol})\n"
        result += f"💧 Most Humid: {most_humid['name']} ({most_humid['humidity']}%)\n"
        result += f"📈 Temperature Range: {max(temps) - min(temps):.1f}{unit_symbol}\n"

    return result

@app.tool()
def get_weather_recommendations(city: str) -> str:
    """Get activity recommendations based on current weather conditions."""
    if not API_KEY:
        return "Error: OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."

    # Clean up the city input
    city = clean_city_input(city)

    # Get current weather data
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={UNITS}"
    success, data = make_http_request(url, timeout=10)

    if not success:
        return f"Error fetching weather data: {data}"

    try:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_main = data["weather"][0]["main"].lower()
        weather_desc = data["weather"][0]["description"].lower()
        visibility = data.get("visibility", 10000) / 1000  # convert to km

        unit_symbol = "°C" if UNITS == "metric" else "°F"
        temp_threshold_hot = 25 if UNITS == "metric" else 77
        temp_threshold_cold = 10 if UNITS == "metric" else 50
        wind_threshold = 5 if UNITS == "metric" else 11  # m/s vs mph

        result = f"🎯 Activity Recommendations for {data['name']}, {data.get('sys', {}).get('country', '')}:\n"
        result += f"Current: {temp:.1f}{unit_symbol}, {data['weather'][0]['description'].capitalize()}\n\n"

        recommendations = []
        warnings = []

        # Temperature-based recommendations
        if temp >= temp_threshold_hot:
            recommendations.extend([
                "🏊‍♀️ Swimming or water activities",
                "🍦 Enjoy ice cream or cold drinks",
                "🌳 Seek shade in parks or gardens",
                "🏠 Indoor activities during peak heat"
            ])
            if temp > (35 if UNITS == "metric" else 95):
                warnings.append("🔥 Extreme heat - limit outdoor exposure")
        elif temp <= temp_threshold_cold:
            recommendations.extend([
                "☕ Hot drinks and cozy indoor activities",
                "🧥 Layer up for outdoor activities",
                "🔥 Fireplace or heating activities",
                "🏠 Indoor sports and entertainment"
            ])
            if temp < (0 if UNITS == "metric" else 32):
                warnings.append("🧊 Freezing conditions - dress warmly")
        else:
            recommendations.extend([
                "🚶‍♀️ Perfect for walking or hiking",
                "🚴‍♂️ Great cycling weather",
                "🏃‍♀️ Ideal for outdoor exercise"
            ])

        # Weather condition-based recommendations
        if "rain" in weather_main or "drizzle" in weather_main:
            recommendations.extend([
                "☔ Bring an umbrella",
                "🏛️ Visit museums or indoor attractions",
                "📚 Perfect reading weather",
                "🎬 Movie theater or indoor entertainment"
            ])
            warnings.append("🌧️ Wet conditions - drive carefully")
        elif "snow" in weather_main:
            recommendations.extend([
                "⛷️ Skiing or snowboarding",
                "⛄ Build a snowman",
                "🛷 Sledding activities",
                "❄️ Winter photography"
            ])
            warnings.append("🌨️ Snowy conditions - check road conditions")
        elif "clear" in weather_main or "sun" in weather_desc:
            recommendations.extend([
                "📸 Perfect for photography",
                "🌻 Outdoor picnics",
                "🏖️ Beach or outdoor activities",
                "🌅 Sunrise/sunset viewing"
            ])
        elif "cloud" in weather_main:
            recommendations.extend([
                "🚶‍♀️ Comfortable for walking",
                "🏃‍♀️ Good for outdoor exercise",
                "📸 Great for landscape photography"
            ])
        elif "storm" in weather_main or "thunder" in weather_desc:
            recommendations.extend([
                "🏠 Stay indoors",
                "📱 Charge devices in case of power outage",
                "🎮 Indoor games and entertainment"
            ])
            warnings.append("⛈️ Severe weather - avoid outdoor activities")

        # Wind-based recommendations
        if wind_speed > wind_threshold:
            recommendations.append("🪁 Great for kite flying")
            if wind_speed > wind_threshold * 2:
                warnings.append("💨 Strong winds - secure loose objects")

        # Humidity-based recommendations
        if humidity > 80:
            recommendations.append("💧 High humidity - stay hydrated")
            warnings.append("🌫️ Muggy conditions - take breaks in AC")
        elif humidity < 30:
            recommendations.append("🧴 Low humidity - use moisturizer")

        # Visibility-based recommendations
        if visibility < 1:
            warnings.append("🌫️ Poor visibility - drive with caution")
        elif visibility > 10:
            recommendations.append("👁️ Excellent visibility for sightseeing")

        # Format output
        if recommendations:
            result += "✅ Recommended Activities:\n"
            for rec in recommendations[:8]:  # Limit to top 8 recommendations
                result += f"• {rec}\n"
            result += "\n"

        if warnings:
            result += "⚠️ Weather Warnings:\n"
            for warning in warnings:
                result += f"• {warning}\n"
            result += "\n"

        # Add clothing suggestions
        result += "👕 Clothing Suggestions:\n"
        if temp >= temp_threshold_hot:
            result += "• Light, breathable clothing\n• Sun hat and sunglasses\n• Sunscreen\n"
        elif temp <= temp_threshold_cold:
            result += "• Warm layers\n• Jacket or coat\n• Gloves and hat\n"
        else:
            result += "• Comfortable casual clothing\n• Light jacket if needed\n"

        if "rain" in weather_main:
            result += "• Waterproof jacket\n• Umbrella\n"

        return result.strip()

    except (KeyError, ValueError) as e:
        return f"Error parsing weather data for recommendations: {str(e)}"

if __name__ == "__main__":
    app.run()
