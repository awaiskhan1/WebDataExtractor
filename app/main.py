from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
import httpx
from aiosqlite import connect as aiosqlite_connect
from rich import print
from typer import run
from typing import Optional
from .src.orchestrator import Orchestrator
from .src.agents.base_agent import BaseAgent
from .src.agents.extractor_agent import ExtractorAgent
from .src.agents.organizer_agent import OrganizerAgent

app = FastAPI()

# Dependency for getting the orchestrator instance
async def get_orchestrator():
    return await Orchestrator.setup()

# Middleware to log each request and response
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request path: {request.url.path}")
    response = await call_next(request)
    print(f"Response status code: {response.status_code}")
    return response

# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Background task function to handle data extraction and organization
async def background_task(orchestrator: Orchestrator):
    await orchestrator.run()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Data Extraction API"}

@app.post("/extract/")
async def extract_data(url: str = Field(..., description="URL of the website to extract data from"), background_tasks: BackgroundTasks = Depends()):
    async with aiosqlite_connect("data.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS extracted_data (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, data TEXT)")
    
    orchestrator = await get_orchestrator()
    extractor_agent = ExtractorAgent(url=url)
    organizer_agent = OrganizerAgent()

    # Add agents to the orchestrator
    orchestrator.add_agent(extractor_agent)
    orchestrator.add_agent(organizer_agent)

    background_tasks.add_task(background_task, orchestrator=orchestrator)
    return {"message": "Data extraction started in the background"}

# Lifespan event handler to initialize the database
@app.on_event("startup")
async def startup():
    async with aiosqlite_connect("data.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS extracted_data (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, data TEXT)")

if __name__ == "__main__":
    run(app)