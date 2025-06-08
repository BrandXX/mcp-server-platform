#!/usr/bin/env python3
"""
Comprehensive test suite for the new MCP server structure

This test validates:
- All MCP server endpoints
- Container mounts and structure
- Performance metrics
- UV dependency management
- New directory organization

Usage:
    python tests/test_mcp_structure.py
"""

import requests
import json
import time
import sys
import subprocess
from datetime import datetime

class Colors:
    """ANSI color codes for better output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print("=" * len(text))

def print_test(text):
    """Print a test name"""
    print(f"\n{Colors.PURPLE}📡 Testing: {text}{Colors.END}")
    print("-" * 40)

def print_success(text):
    """Print success message"""
    print(f"   {Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"   {Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"   {Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"   {Colors.CYAN}📄 {text}{Colors.END}")

def test_server_endpoints():
    """Test all available server endpoints"""
    
    base_url = "http://localhost:8989"
    
    tests = [
        {
            "name": "Time Server - Current Time",
            "endpoint": f"{base_url}/time/get_current_time",
            "payload": {"timezone": "America/Phoenix"},
            "expected_keys": ["timezone", "datetime"]
        },
        {
            "name": "OpenWeather - Status Check",
            "endpoint": f"{base_url}/openweather/check_openweather_status",
            "payload": {},
            "expected_content": ["API Key", "Dependencies"]
        },
        {
            "name": "OpenWeather - Current Weather",
            "endpoint": f"{base_url}/openweather/get_current_weather",
            "payload": {"city": "London"},
            "expected_content": ["Current Weather", "°F", "Humidity"]
        },
        {
            "name": "OpenWeather - Weather Forecast",
            "endpoint": f"{base_url}/openweather/get_forecast",
            "payload": {"city": "Tokyo", "days": 3},
            "expected_content": ["Forecast", "📅"]
        }
    ]
    
    print_header("🧪 Testing MCP Server Endpoints")
    
    success_count = 0
    total_tests = len(tests)
    
    for test in tests:
        print_test(test['name'])
        
        try:
            start_time = time.time()
            response = requests.post(
                test['endpoint'],
                json=test['payload'],
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            print(f"   Status: {response.status_code} ({response_time:.1f}ms)")
            
            if response.status_code == 200:
                result = response.text
                print_success("SUCCESS")
                success_count += 1
                
                # Validate expected content
                if 'expected_keys' in test:
                    try:
                        data = json.loads(result)
                        for key in test['expected_keys']:
                            if key in str(data):
                                print_success(f"Found expected key: {key}")
                            else:
                                print_warning(f"Missing expected key: {key}")
                    except json.JSONDecodeError:
                        pass
                
                if 'expected_content' in test:
                    for content in test['expected_content']:
                        if content in result:
                            print_success(f"Found expected content: {content}")
                        else:
                            print_warning(f"Missing expected content: {content}")
                
                # Show first few lines of response
                if result:
                    lines = result.strip('"').replace('\\n', '\n').split('\n')[:3]
                    for line in lines:
                        if line.strip():
                            print_info(line.strip())
                    if len(lines) > 3:
                        print_info("...")
            else:
                print_error(f"FAILED: {response.status_code}")
                if response.text:
                    print_info(response.text[:100] + "...")
                    
        except Exception as e:
            print_error(f"ERROR: {e}")
    
    print(f"\n{Colors.BOLD}📊 Endpoint Test Results: {success_count}/{total_tests} passed{Colors.END}")
    return success_count == total_tests

def test_container_structure():
    """Test that container structure and mounts are working correctly"""
    print_header("🔍 Testing Container Structure & Mounts")
    
    tests = [
        {
            "name": "MCP Servers Directory",
            "command": ["docker", "exec", "mcpo", "ls", "-la", "/mcp/servers/"],
            "expected": "openweather"
        },
        {
            "name": "OpenWeather Server Files",
            "command": ["docker", "exec", "mcpo", "ls", "-la", "/mcp/servers/openweather/"],
            "expected": ["pyproject.toml", "openweather.py", "run_uv.sh"]
        },
        {
            "name": "UV Cache Directory",
            "command": ["docker", "exec", "mcpo", "ls", "-la", "/memory/"],
            "expected": ".uv-cache"
        },
        {
            "name": "Working Directory Structure",
            "command": ["docker", "exec", "mcpo", "ls", "-la", "/memory/mcp-servers/"],
            "expected": "openweather"
        }
    ]
    
    success_count = 0
    
    for test in tests:
        print_test(test['name'])
        
        try:
            result = subprocess.run(
                test['command'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                expected = test['expected']
                if isinstance(expected, list):
                    all_found = all(item in result.stdout for item in expected)
                    if all_found:
                        print_success("All expected items found")
                        success_count += 1
                        for item in expected:
                            print_info(f"✓ {item}")
                    else:
                        print_warning("Some expected items missing")
                        for item in expected:
                            if item in result.stdout:
                                print_info(f"✓ {item}")
                            else:
                                print_info(f"✗ {item}")
                else:
                    if expected in result.stdout:
                        print_success(f"Found: {expected}")
                        success_count += 1
                    else:
                        print_warning(f"Not found: {expected}")
            else:
                print_error(f"Command failed: {result.stderr}")
                
        except Exception as e:
            print_error(f"Test error: {e}")
    
    print(f"\n{Colors.BOLD}📊 Structure Test Results: {success_count}/{len(tests)} passed{Colors.END}")
    return success_count == len(tests)

def test_performance():
    """Test the performance of the new structure"""
    print_header("⚡ Performance Testing")
    
    endpoint = "http://localhost:8989/openweather/check_openweather_status"
    
    print_test("Response Time Analysis")
    
    # Warm up
    try:
        requests.post(endpoint, json={}, timeout=5)
        print_info("Warm-up request completed")
    except:
        print_warning("Warm-up request failed")
    
    # Time multiple requests
    times = []
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.post(endpoint, json={}, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                print(f"   Request {i+1}: {response_time:.1f}ms ✅")
            else:
                print_error(f"Request {i+1}: Failed ({response.status_code})")
        except Exception as e:
            print_error(f"Request {i+1}: Error - {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n{Colors.BOLD}📊 Performance Metrics:{Colors.END}")
        print(f"   Average: {avg_time:.1f}ms")
        print(f"   Minimum: {min_time:.1f}ms")
        print(f"   Maximum: {max_time:.1f}ms")
        
        if avg_time < 10:
            print_success("🚀 Excellent performance!")
            return True
        elif avg_time < 50:
            print_success("✅ Good performance")
            return True
        else:
            print_warning("⚠️  Performance could be improved")
            return False
    else:
        print_error("No successful requests for performance analysis")
        return False

def main():
    """Run all tests"""
    print(f"{Colors.BOLD}{Colors.CYAN}🚀 MCP Server Structure - Comprehensive Test Suite{Colors.END}")
    print(f"{Colors.CYAN}Testing new mcp/servers/ structure with UV dependency management{Colors.END}")
    print(f"{Colors.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    # Run all test suites
    endpoint_success = test_server_endpoints()
    structure_success = test_container_structure()
    performance_success = test_performance()
    
    # Final summary
    print_header("✨ Test Summary")
    
    total_success = endpoint_success and structure_success and performance_success
    
    if total_success:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! New structure is working perfectly!{Colors.END}")
        print(f"{Colors.GREEN}✅ Endpoints: Working{Colors.END}")
        print(f"{Colors.GREEN}✅ Structure: Validated{Colors.END}")
        print(f"{Colors.GREEN}✅ Performance: Excellent{Colors.END}")
        sys.exit(0)
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please review the results above.{Colors.END}")
        print(f"{Colors.YELLOW}Endpoints: {'✅' if endpoint_success else '❌'}{Colors.END}")
        print(f"{Colors.YELLOW}Structure: {'✅' if structure_success else '❌'}{Colors.END}")
        print(f"{Colors.YELLOW}Performance: {'✅' if performance_success else '❌'}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
