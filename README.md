# Surf MCP Server

MCP server for people who surf waves and the web.

## Features

- Fetch tide information for any location using latitude and longitude
- Support for date-specific tide queries
- Detailed tide data including high/low tides and station information
- Automatic time zone handling (UTC)

## Prerequisites

- Python 3.x
- Storm Glass API key

## Getting Your Storm Glass API Key

1. Visit [Storm Glass](https://stormglass.io/)
2. Click "Try for Free" or "Sign In" to create an account
3. Once registered, you'll receive your API key

Note on API Usage Limits:
- Free tier: 10 requests per day
- Paid plans available:
  - Small: 500 requests/day (€19/month)
  - Medium: 5000 requests/day (€49/month)
  - Large: 25,000 requests/day (€129/month)
  - Enterprise: Custom plans available

Choose a plan based on your usage requirements. The free tier is suitable for testing and personal use.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ravinahp/surf-mcp.git
cd surf-mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

Note: We use `uv` instead of pip since the project uses `pyproject.toml` for dependency management.

## Configure as MCP Server

To add this tool as an MCP server, you'll need to modify your Claude desktop configuration file. This configuration includes your Storm Glass API key, so you won't need to set it up separately.

The configuration file location depends on your operating system:

- MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Add the following configuration to your JSON file:

```json
{
    "surf-mcp": {
        "command": "uv",
        "args": [
            "--directory",
            "/Users/YOUR_USERNAME/Code/surf-mcp",
            "run",
            "surf-mcp"
        ],
        "env": {
            "STORMGLASS_API_KEY": "your_api_key_here"
        }
    }
}
```

⚠️ IMPORTANT: 
1. Replace `YOUR_USERNAME` with your actual system username
2. Replace `your_api_key_here` with your actual Storm Glass API key
3. Make sure the directory path matches your local installation

## Deployment

### Building

To prepare the package:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package:
```bash
uv build
```
This will create distributions in the `dist/` directory.

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging experience, we strongly recommend using the MCP Inspector.

You can launch the MCP Inspector with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/surf-mcp run surf-mcp
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

The Inspector provides:
- Real-time request/response monitoring
- Input/output validation
- Error tracking
- Performance metrics

## Usage

The service provides a FastMCP tool for getting tide information:

```python
@mcp.tool()
async def get_tides(latitude: float, longitude: float, date: str) -> str:
    """Get tide information for a specific location and date."""
```

### Parameters:
- `latitude`: Float value representing the location's latitude
- `longitude`: Float value representing the location's longitude
- `date`: Date string in YYYY-MM-DD format

### Example Response:
```
Tide Times:
Time: 2024-01-20T00:30:00+00:00 (UTC)
Type: HIGH tide
Height: 1.52m

Time: 2024-01-20T06:45:00+00:00 (UTC)
Type: LOW tide
Height: 0.25m

Station Information:
Name: Sample Station
Distance: 20.5km from requested location
```

## Use Cases

### Example #1: Finding the Best Surf Time

You can use this tool to determine the optimal surfing time at your favorite beach & the closest station. Generally, the best surfing conditions are during incoming (rising) tides, about 2 hours before high tide. 

Example prompt to Claude:

<img width="693" alt="Screenshot 2025-01-07 at 12 55 47 PM" src="https://github.com/user-attachments/assets/f605494a-9842-40b9-a9f2-cfcfae0cb908" />

Note: Different beaches may have different optimal tide conditions based on their specific geography and break type. This tool also provides station distance information which should be considered alongside tide information. (ie. longer station distance means higher change of innacuracy - you can ask Claude for this as well when prompting). 

## Error Handling

The service includes robust error handling for:
- API request failures
- Invalid coordinates
- Missing or invalid API keys
- Network timeouts

