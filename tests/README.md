# MCP Server Test Suite

This directory contains comprehensive test scripts for validating the MCP server structure and functionality.

## Test Scripts

### `test_mcp_structure.py`
**Comprehensive system test** that validates the entire MCP server infrastructure:

- ✅ **Endpoint Testing**: All MCP server endpoints (time, memory, openweather)
- ✅ **Container Structure**: Directory mounts and file organization
- ✅ **Performance**: Response time analysis and benchmarking
- ✅ **UV Integration**: Dependency management validation

**Usage:**
```bash
python tests/test_mcp_structure.py
```

**Features:**
- Colored output for easy reading
- Detailed performance metrics
- Container mount validation
- Comprehensive error reporting

### `test_openweather.py`
**Focused OpenWeather server test** that thoroughly validates weather functionality:

- 🌤️ **Current Weather**: Multiple cities and formats
- 📅 **Weather Forecasts**: Various day ranges and locations
- 🚨 **Error Handling**: Invalid inputs and edge cases
- 🔍 **Status Validation**: Server health and configuration

**Usage:**
```bash
python tests/test_openweather.py
```

**Test Coverage:**
- 5 different cities for current weather
- Multiple forecast day ranges (1-5 days)
- Error handling with invalid inputs
- API response format validation

### `cleanup_data_mounts.py`
**Data mount cleanup utility** that helps maintain a clean data directory:

- 🧹 **Automatic Detection**: Identifies old/duplicate directories
- 🔍 **Dry Run Mode**: Preview cleanup without making changes
- 🗑️ **Safe Cleanup**: Uses container permissions to remove files
- 📊 **Detailed Reporting**: Shows what was cleaned and why

**Usage:**
```bash
# Preview what would be cleaned
python tests/cleanup_data_mounts.py --dry-run

# Perform actual cleanup
python tests/cleanup_data_mounts.py
```

## Running Tests

### Prerequisites
- MCPO container running (`docker compose up -d`)
- Python 3.10+ with `requests` library
- Network access to localhost:8989

### Quick Test
```bash
# Run comprehensive test
python tests/test_mcp_structure.py

# Run OpenWeather-specific test
python tests/test_openweather.py
```

### Expected Results

#### Successful Test Output
```
🚀 MCP Server Structure - Comprehensive Test Suite
============================================================
🧪 Testing MCP Server Endpoints
============================================================

📡 Testing: Time Server - Current Time
----------------------------------------
   Status: 200 (15.2ms)
   ✅ SUCCESS
   ✅ Found expected key: timezone
   📄 {"timezone":"America/Phoenix","datetime":"2025-06-08T01:18:55-07:00"}

📡 Testing: OpenWeather - Status Check
----------------------------------------
   Status: 200 (2.4ms)
   ✅ SUCCESS
   📄 OpenWeather Tool Status:
   📄 ✅ API Key: Configured

📊 Endpoint Test Results: 4/4 passed
```

#### Performance Benchmarks
- **Excellent**: < 10ms average response time
- **Good**: 10-50ms average response time
- **Needs Improvement**: > 50ms average response time

## Test Architecture

### Structure Validation
Tests verify the new directory organization:
```
mcp/
├── servers/
│   └── openweather/
│       ├── pyproject.toml     ✅ Tested
│       ├── openweather.py     ✅ Tested
│       └── run_uv.sh         ✅ Tested
└── shared/                    ✅ Tested
```

### Container Integration
- Volume mount validation
- UV cache directory verification
- Working directory structure
- File permissions and accessibility

### API Endpoint Coverage
- **Time Server**: Current time with timezone support
- **OpenWeather**: Status, current weather, forecasts
- **Memory Server**: Basic connectivity (may show 404 - expected)

## Troubleshooting

### Common Issues

**Container Not Running**
```bash
docker compose ps
# If not running:
docker compose up -d
```

**Network Connection Issues**
```bash
curl http://localhost:8989/time
# Should return redirect or valid response
```

**Permission Issues**
```bash
docker exec mcpo ls -la /mcp/servers/openweather/
# Should show executable run_uv.sh
```

### Debug Mode
Add debug output to tests by modifying the scripts:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new MCP servers:

1. **Add endpoint tests** to `test_mcp_structure.py`
2. **Create focused test** (like `test_openweather.py`)
3. **Update this README** with new test information
4. **Verify container structure** tests include new server

## Test Results Archive

Tests automatically include timestamps and can be used for:
- **CI/CD validation**
- **Performance regression testing**
- **Container rebuild verification**
- **Development debugging**

The test suite provides confidence that the new MCP server structure is working correctly and performing well.
