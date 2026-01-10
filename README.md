# WebDataExtractor

WebDataExtractor is a production-grade multi-agent AI system designed to extract and organize data from websites into structured formats for AI analysis and automation. This README provides an overview of the architecture, setup instructions, API documentation, and deployment guide.

## Architecture

WebDataExtractor consists of several components:

1. **Agents**: Each agent is responsible for extracting data from a specific website.
2. **Orchestrator**: Manages the lifecycle of agents and coordinates their execution.
3. **Database**: Stores extracted data in an SQLite database for easy querying and analysis.

### Agents

The base agent class `BaseAgent` defines an abstract method `execute()` that each agent must implement. The `Result` dataclass is used to encapsulate the results of agent execution, including success status, output, error information, and metadata.

# src/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Optional, Any

class Result:
    def __init__(
        self,
        success: bool,
        output: Optional[Any] = None,
        error: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        self.success = success
        self.output = output
        self.error = error
        self.metadata = metadata

class BaseAgent(ABC):
    @abstractmethod
    async def execute(self) -> Result:
        pass

### Orchestrator

The `Orchestrator` class manages the lifecycle of agents, ensuring they are executed in sequence and their results are stored in the database.

# src/orchestrator.py

from src.agents import BaseAgent
from aiosqlite import connect
import asyncio

class Orchestrator:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)

    async def run(self):
        for agent in self.agents:
            result = await agent.execute()
            if result.success:
                await self.store_result(result)
            else:
                print(f"Error executing {agent.__class__.__name__}: {result.error}")

    async def store_result(self, result: Result):
        async with connect('data.db') as db:
            cursor = await db.cursor()
            await cursor.execute(
                "INSERT INTO results (output, error, metadata) VALUES (?, ?, ?)",
                (result.output, result.error, result.metadata),
            )
            await db.commit()

async def main():
    orchestrator = Orchestrator()
    # Add agents to the orchestrator
    orchestrator.add_agent(MyAgent())
    orchestrator.add_agent(AnotherAgent())
    
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(main())

### Database

The SQLite database is used to store the extracted data. The `store_result` method in the `Orchestrator` class handles this storage.

## Setup

To set up WebDataExtractor, follow these steps:

1. **Install Dependencies**:
    pip install pydantic httpx aiosqlite rich typer python-dotenv

2. **Create Database**:
    Run the following script to create the database and tables.
    import aiosqlite

    async def init_db():
        async with aiosqlite.connect('data.db') as db:
            await db.execute(
                "CREATE TABLE results (id INTEGER PRIMARY KEY AUTOINCREMENT, output TEXT, error TEXT, metadata TEXT)"
            )
            await db.commit()

    asyncio.run(init_db())

## API Docs

WebDataExtractor provides an API to interact with the agents and orchestrator. The documentation is available via FastAPI.

# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.base_agent import BaseAgent
from src.orchestrator import Orchestrator
import asyncio

app = FastAPI()

class AgentRequest(BaseModel):
    name: str
    data: dict

@app.post("/run-agent/")
async def run_agent(agent_request: AgentRequest):
    try:
        agent_class = globals()[agent_request.name]
        agent_instance = agent_class(data=agent_request.data)
        orchestrator = Orchestrator()
        orchestrator.add_agent(agent_instance)
        await orchestrator.run()
        return {"message": "Agent executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/")
async def get_results():
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute("SELECT * FROM results")
        rows = await cursor.fetchall()
        return {"results": [dict(row) for row in rows]}

## Deployment Guide

To deploy WebDataExtractor, follow these steps:

1. **Build the Application**:
    python main.py

2. **Run the API Server**:
    The FastAPI server will run on `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

3. **Deploy to Production**:
    For production deployment, consider using a WSGI server like Gunicorn or Uvicorn with an appropriate web server like Nginx.

This README provides a comprehensive overview of WebDataExtractor's architecture, setup instructions, API documentation, and deployment guide.