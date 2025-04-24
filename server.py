# main.py
from fastapi_mcp import FastApiMCP, AuthConfig
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Literal
import requests
import os

# Get the API key from an environment variable
API_KEY = os.environ.get("API_KEY")

# Define the API key security scheme
api_key_header = APIKeyHeader(name="api_key", auto_error=False)

app = FastAPI()

# Define a dependency to check the API
async def get_api_key(
    api_key_header: str = Depends(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403, detail="Invalid API key"
        )


# Load API key from environment variable
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise Exception("TAVILY_API_KEY environment variable is required")

# Define base URLs for Tavily API
baseURLs = {
    "search": "https://api.tavily.com/search",
    "extract": "https://api.tavily.com/extract"
}

# request and response models
class TavilySearchRequest(BaseModel):
    query: str
    search_depth: Literal["basic","advanced"] = "basic"
    topic: Literal["general","news"] = "general"
    days: int = 3
    time_range: Literal["day", "week", "month", "year", "d", "w", "m", "y"] = "day"
    max_results: int = 10
    include_images: bool = False
    include_image_descriptions: bool = False
    include_raw_content: bool = False
    include_domains: list[str] = []
    exclude_domains: list[str] = []

class TavilyExtractRequest(BaseModel):
    urls: list[str]
    extract_depth: Literal["basic","advanced"] = "basic"
    include_images: bool = False

class Result(BaseModel):
    title: str | None = None
    url: str | None = None
    content: str | None = None
    score: float | None = None
    published_date: str | None = None
    raw_content: str | None = None

class Image(BaseModel):
    url: str | None = None
    description: str | None = None

class TavilyResponse(BaseModel):
    query: str | None = None
    follow_up_questions: list[str] | None = []
    answer: str | None = ""
    images: list[str | Image] | None = []
    results: list[Result] = []


# Define endpoint Tavily search
@app.post("/tavily-search")
async def tavily_search(request: TavilySearchRequest, api_key: str = Depends(get_api_key)) -> TavilyResponse:
    """
    Perform a search using the Tavily API.

    Args
        request (TavilySearchRequest): The search request parameters.

    Returns:
        TavilyResponse: The search results from the Tavily API.

    Raises:
        HTTPException: If the request to the Tavily API fails.
    """
    try:
        
        # Prepare request parameters
        params = {
            "query": request.query,
            "search_depth": request.search_depth,
            "topic": request.topic,
            "days": request.days,
            "time_range": request.time_range,
            "max_results": request.max_results,
            "include_images": request.include_images,
            "include_image_descriptions": request.include_image_descriptions,
            "include_raw_content": request.include_raw_content,
            "include_domains": request.include_domains,
            "exclude_domains": request.exclude_domains
        }
        
        # Make the request to the Tavily API with Authorization header
        headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        }
        
        # Send to Tavily API
        response = requests.post(baseURLs["search"], json=params, headers=headers)
        
        # Check if response was successful
        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=500, detail="Tavily API error")
        
        # Return formatted response
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define endpoint for Tavily extract
@app.post("/tavily-extract")
async def tavily_extract(request: TavilyExtractRequest, api_key: str = Depends(get_api_key)) -> TavilyResponse:
    """
    Extract content from URLs using the Tavily API.
    Args:
        request (TavilyExtractRequest): The extraction request parameters.

    Returns:
        TavilyResponse: The extraction results from the Tavily API.

    Raises:
        HTTPException: If the request to the Tavily API fails.
 """
    try:
        # Prepare parameters
        params = {
            "urls": request.urls,
            "extract_depth": request.extract_depth,
            "include_images": request.include_images
        }
        
        # Make the request to the Tavily API with Authorization header
        headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        }
        
        # Send request to Tavily API
        response = requests.post(baseURLs["extract"], json=params, headers=headers)
        
        # Check if response was successful
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Tavily API error")
        
        # Return formatted response
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


mcp = FastApiMCP(
    app,
    name="Tavily Protected MCP",
    auth_config=AuthConfig(
        dependencies=[Depends(get_api_key)],
    ),
)
mcp.mount()
