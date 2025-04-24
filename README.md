# Tavily MCP Server

Basic FastAPI-based server application that provides endpoints for interacting with the Tavily API. The server includes API key authentication and uses the `fastapi-mcp` library to create a remote SSE MCP server out of it.

## Installation

To install the project's dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the server, use the following command:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://127.0.0.1:8000`.

## API Key

The server requires two API keys:

- `API_KEY`: The API key for accessing the server's endpoints.
- `TAVILY_API_KEY`: The API key for accessing the Tavily API.

Set these API keys as environment variables before running the server.

## Endpoints

### `/tavily-search`

Perform a search using the Tavily API.

- **Method**: POST
- **Request Body**: `TavilySearchRequest`
  - `query` (str): The search query.
  - `search_depth` (Literal["basic", "advanced"], optional): The depth of the search. Defaults to "basic".
  - `topic` (Literal["general", "news"], optional): The topic of the search. Defaults to "general".
  - `days` (int, optional): The number of days to search. Defaults to 3.
  - `time_range` (Literal["day", "week", "month", "year", "d", "w", "m", "y"], optional): The time range of the search. Defaults to "day".
  - `max_results` (int, optional): The maximum number of results to return. Defaults to 10.
  - `include_images` (bool, optional): Whether to include images in the results. Defaults to False.
  - `include_image_descriptions` (bool, optional): Whether to include image descriptions in the results. Defaults to False.
  - `include_raw_content` (bool, optional): Whether to include raw content in the results. Defaults to False.
  - `include_domains` (list[str], optional): A list of domains to include in the search. Defaults to an empty list.
  - `exclude_domains` (list[str], optional): A list of domains to exclude from the search. Defaults to an empty list.
- **Response**: `TavilyResponse`

### `/tavily-extract`

Extract content from URLs using the Tavily API.

- **Method**: POST
- **Request Body**: `TavilyExtractRequest`
  - `urls` (list[str]): A list of URLs to extract content from.
  - `extract_depth` (Literal["basic", "advanced"], optional): The depth of the extraction. Defaults to "basic".
  - `include_images` (bool, optional): Whether to include images in the extraction. Defaults to False.
- **Response**: `TavilyResponse`

