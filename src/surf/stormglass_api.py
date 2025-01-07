import os
import httpx
from typing import Any
import logging
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class StormGlassAPI:
    """Handler for Storm Glass API interactions."""
    
    def __init__(self):
        self.api_base = "https://api.stormglass.io/v2"
        self.api_key = os.getenv("STORMGLASS_API_KEY", "")
        self.user_agent = "surf-app/1.0"
        
    async def make_request(self, url: str) -> dict[str, Any] | None:
        """Make a request to the Storm Glass API with proper error handling."""
        headers = {
            "Authorization": self.api_key,
            "User-Agent": self.user_agent
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"API request failed: {str(e)}")
                return None

    def format_tide_data(self, data: dict) -> str:
        """Format tide data into a readable string."""
        if not data or "data" not in data:
            return "No tide data available."
        
        result = ["Tide Times:"]
        for tide in data["data"]:
            time_utc = tide["time"]
            time_local = f"{time_utc} (UTC)"
            
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

    async def get_tide_data(self, latitude: float, longitude: float, date: str) -> str:
        """Get tide information for a specific location and date."""
        url = f"{self.api_base}/tide/extremes/point"
        params = {
            "lat": latitude,
            "lng": longitude,
            "start": f"{date}T00:00:00Z",
            "end": f"{date}T23:59:59Z"
        }
        
        param_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{url}?{param_string}"
        
        data = await self.make_request(full_url)
        if not data:
            return "Unable to fetch tide data for this location."
        
        return self.format_tide_data(data) 