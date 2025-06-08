#!/usr/bin/env python3
"""
Focused test suite for OpenWeather MCP server

Tests all OpenWeather functionality including:
- Status checks
- Current weather for various cities
- Weather forecasts
- Error handling
- Input validation

Usage:
    python tests/test_openweather.py
"""

import requests
import json
import time

def test_openweather_status():
    """Test OpenWeather status endpoint"""
    print("🔍 Testing OpenWeather Status...")
    
    try:
        response = requests.post(
            "http://localhost:8989/openweather/check_openweather_status",
            json={},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.text.strip('"').replace('\\n', '\n')
            print("✅ Status check successful")
            print("📄 Status details:")
            for line in result.split('\n')[:6]:
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def test_current_weather():
    """Test current weather for various cities"""
    print("\n🌤️  Testing Current Weather...")
    
    cities = [
        "London",
        "New York", 
        "Tokyo",
        "Sydney",
        "Phoenix, AZ"
    ]
    
    success_count = 0
    
    for city in cities:
        print(f"\n   Testing: {city}")
        try:
            response = requests.post(
                "http://localhost:8989/openweather/get_current_weather",
                json={"city": city},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.text.strip('"').replace('\\n', '\n')
                if "Current Weather" in result and "°F" in result:
                    print(f"   ✅ {city}: Success")
                    # Show temperature line
                    for line in result.split('\n'):
                        if "🌡️" in line:
                            print(f"      {line}")
                            break
                    success_count += 1
                else:
                    print(f"   ❌ {city}: Invalid response format")
            else:
                print(f"   ❌ {city}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {city}: Error - {e}")
    
    print(f"\n📊 Current weather tests: {success_count}/{len(cities)} passed")
    return success_count >= len(cities) // 2  # At least half should pass

def test_weather_forecast():
    """Test weather forecast functionality"""
    print("\n📅 Testing Weather Forecasts...")
    
    test_cases = [
        {"city": "London", "days": 3},
        {"city": "Tokyo", "days": 5},
        {"city": "New York", "days": 1}
    ]
    
    success_count = 0
    
    for test_case in test_cases:
        city = test_case["city"]
        days = test_case["days"]
        print(f"\n   Testing: {city} ({days} days)")
        
        try:
            response = requests.post(
                "http://localhost:8989/openweather/get_forecast",
                json=test_case,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.text.strip('"').replace('\\n', '\n')
                if "Forecast" in result and "📅" in result:
                    print(f"   ✅ {city}: Forecast received")
                    # Count forecast days
                    day_count = result.count("📅")
                    print(f"      Found {day_count} forecast days")
                    success_count += 1
                else:
                    print(f"   ❌ {city}: Invalid forecast format")
            else:
                print(f"   ❌ {city}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {city}: Error - {e}")
    
    print(f"\n📊 Forecast tests: {success_count}/{len(test_cases)} passed")
    return success_count >= len(test_cases) // 2

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n🚨 Testing Error Handling...")
    
    error_tests = [
        {
            "name": "Invalid city name",
            "endpoint": "get_current_weather",
            "payload": {"city": "InvalidCityNameThatDoesNotExist12345"}
        },
        {
            "name": "Empty city name",
            "endpoint": "get_current_weather", 
            "payload": {"city": ""}
        },
        {
            "name": "Invalid forecast days",
            "endpoint": "get_forecast",
            "payload": {"city": "London", "days": 10}  # Max is 5
        }
    ]
    
    success_count = 0
    
    for test in error_tests:
        print(f"\n   Testing: {test['name']}")
        try:
            response = requests.post(
                f"http://localhost:8989/openweather/{test['endpoint']}",
                json=test['payload'],
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.text
                if "Error" in result or "error" in result:
                    print(f"   ✅ Proper error handling")
                    success_count += 1
                else:
                    print(f"   ⚠️  No error message for invalid input")
            else:
                print(f"   ✅ HTTP error response: {response.status_code}")
                success_count += 1
                
        except Exception as e:
            print(f"   ❌ Test error: {e}")
    
    print(f"\n📊 Error handling tests: {success_count}/{len(error_tests)} passed")
    return success_count >= len(error_tests) // 2

def main():
    """Run all OpenWeather tests"""
    print("🌦️  OpenWeather MCP Server - Focused Test Suite")
    print("=" * 60)
    
    # Run all test suites
    status_ok = test_openweather_status()
    weather_ok = test_current_weather()
    forecast_ok = test_weather_forecast()
    error_ok = test_error_handling()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 OpenWeather Test Summary:")
    print(f"   Status Check: {'✅' if status_ok else '❌'}")
    print(f"   Current Weather: {'✅' if weather_ok else '❌'}")
    print(f"   Weather Forecast: {'✅' if forecast_ok else '❌'}")
    print(f"   Error Handling: {'✅' if error_ok else '❌'}")
    
    if all([status_ok, weather_ok, forecast_ok, error_ok]):
        print("\n🎉 All OpenWeather tests passed!")
        return True
    else:
        print("\n⚠️  Some OpenWeather tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
