import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("surf")

# Constants
STORMGLASS_API_BASE = "https://api.stormglass.io/v2"
API_KEY = os.getenv("STORMGLASS_API_KEY", "")
USER_AGENT = "surf-app/1.0"

async def make_stormglass_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Storm Glass API with proper error handling."""
    headers = {
        "Authorization": API_KEY,
        "User-Agent": USER_AGENT
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

def format_tide_data(data: dict) -> str:
    """Format tide data into a readable string."""
    if not data or "data" not in data:
        return "No tide data available."
    
    result = ["Tide Times:"]
    for tide in data["data"]:
        # Convert UTC to Costa Rica time (UTC-6)
        time_utc = tide["time"]
        time_local = f"{time_utc} (UTC)"  # You might want to add proper time conversion
        
        result.append(f"""
Time: {time_local}
Type: {tide['type'].upper()} tide
Height: {tide['height']:.2f}m
""")
    
    # Add station information
    if "meta" in data and "station" in data["meta"]:
        station = data["meta"]["station"]
        result.append(f"""
Station Information:
Name: {station['name']}
Distance: {station['distance']}km from requested location
""")
    
    return "\n".join(result)

@mcp.tool()
async def get_tides(latitude: float, longitude: float, date: str) -> str:
    """Get tide information for a specific location and date."""
    url = f"{STORMGLASS_API_BASE}/tide/extremes/point"
    params = {
        "lat": latitude,
        "lng": longitude,
        "start": f"{date}T00:00:00Z",  # Fixed UTC format
        "end": f"{date}T23:59:59Z"     # Fixed UTC format
    }
    
    # Add parameters to URL
    param_string = "&".join(f"{k}={v}" for k, v in params.items())
    full_url = f"{url}?{param_string}"
    
    data = await make_stormglass_request(full_url)
    if not data:
        return "Unable to fetch tide data for this location."
    
    return format_tide_data(data)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')