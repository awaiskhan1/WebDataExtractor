from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractRequest(BaseModel):
    url: str = Field(..., description="The URL to extract data from")
    extract_type: str = Field(default="text", description="Type of extraction")

class ExtractResponse(BaseModel):
    success: bool = Field(..., description="Whether extraction was successful")
    output: Optional[str] = None
    error: Optional[str] = None

class OrganizeRequest(BaseModel):
    data: str = Field(..., description="Data to organize")
    format: str = Field(default="json", description="Output format")

class OrganizeResponse(BaseModel):
    success: bool = Field(..., description="Whether organization was successful")
    output: Optional[str] = None
    error: Optional[str] = None