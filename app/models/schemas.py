from pydantic import BaseModel, Field, Optional
from typing import List

class WebsiteURL(BaseModel):
    url: str = Field(..., description="The URL of the website to be scraped")

class DataField(BaseModel):
    key: str = Field(..., description="The key for the data field")
    value: str = Field(..., description="The value of the data field")

class ExtractionResult(BaseModel):
    success: bool = Field(..., description="Whether the extraction was successful")
    output: Optional[List[DataField]] = None
    error: Optional[str] = None
    metadata: dict = Field(default_factory=dict, description="Additional metadata about the extraction")

# Example usage:
example_extraction_result = ExtractionResult(
    success=True,
    output=[
        DataField(key="title", value="Example Website"),
        DataField(key="description", value="This is an example website for scraping.")
    ],
    metadata={"source": "web_scraper"}
)