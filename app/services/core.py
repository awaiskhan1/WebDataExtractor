from typing import Optional, Dict, Any
import httpx
from pydantic import BaseModel, Field, model_dump_json

class WebsiteData(BaseModel):
    url: str = Field(..., description="URL of the website to extract data from")
    headers: Optional[Dict[str, str]] = Field(None, description="Optional HTTP headers for the request")

class ExtractionResult(BaseModel):
    success: bool
    output: Optional[Dict[str, Any]]
    error: Optional[str]
    metadata: Dict[str, Any]

async def fetch_data(url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response

async def extract_website_data(data: WebsiteData) -> ExtractionResult:
    try:
        response = await fetch_data(data.url, data.headers)
        data_output = response.json()
        return ExtractionResult(success=True, output=data_output, error=None, metadata={"status_code": response.status_code})
    except httpx.HTTPStatusError as e:
        return ExtractionResult(success=False, output=None, error=str(e), metadata={"status_code": e.response.status_code})
    except Exception as e:
        return ExtractionResult(success=False, output=None, error=str(e), metadata={})

# Example usage
async def main():
    data = WebsiteData(url="https://example.com")
    result = await extract_website_data(data)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())