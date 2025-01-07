import logging
from mcp.server.fastmcp import FastMCP
from .stormglass_api import StormGlassAPI

# Set up logging
logger = logging.getLogger(__name__)

# Initialize FastMCP server and API client
mcp = FastMCP("surf")
api = StormGlassAPI()

@mcp.tool()
async def get_tides(latitude: float, longitude: float, date: str) -> str:
    """Get tide information for a specific location and date.
    
    Args:
        latitude: Float value representing the location's latitude
        longitude: Float value representing the location's longitude
        date: Date string in YYYY-MM-DD format
        
    Returns:
        Formatted string containing tide information and station details
    """
    return await api.get_tide_data(latitude, longitude, date) 