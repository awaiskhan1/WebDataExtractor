# WebDataExtractor TECH_SPEC.md

## Executive Summary
WebDataExtractor is a complex, enterprise-grade multi-agent AI system designed to extract and organize data from websites into structured formats for further AI analysis and automation. The system will utilize an Orchestrator pattern with multiple specialized agents, including a Planner for task definition, an Executor for data extraction, and a Validator for data validation. PostgreSQL, Redis, and Pinecone/Qdrant will be used for database management, caching, and vector embeddings respectively.

## 1. System Design

### Architecture Type
**Monolith vs Microservices:**
- **Architecture Type:** Monolithic
- **Justification:** A monolithic architecture is suitable for this project due to the complexity and interdependencies between different components of WebDataExtractor. It simplifies deployment, testing, and maintenance.

### High-Level Component Diagram Description
```
+-------------------+
|    Orchestrator   |
|  (FastAPI + Celery)|
+---------+---------+
          |
          v
+---------+---------+
|     Planner     |
|  (AI/LLM Agent) |
+---------+---------+
          |
          v
+---------+---------+
|   Executor    |
|  (Web Scraping)|
+---------+---------+
          |
          v
+---------+---------+
|   Validator   |
|  (Data Cleaning)|
+-------------------+
```

- **Orchestrator:** Manages and coordinates the workflow between the Planner, Executor, and Validator.
- **Planner:** Defines tasks based on user input or predefined rules. Uses AI/LLM to generate extraction strategies.
- **Executor:** Executes data extraction from websites using web scraping techniques.
- **Validator:** Validates the extracted data for accuracy and quality.

### Technology Choices with Reasoning
- **Backend:** FastAPI + Celery + Redis
  - **FastAPI:** Provides a robust, performant API framework for building RESTful services.
  - **Celery:** Enables asynchronous task processing, which is essential for handling long-running scraping tasks.
  - **Redis:** Acts as an in-memory data store for caching and message queuing.

- **AI/LLM:** LangChain or custom agent framework with Ollama/OpenAI
  - LangChain provides a comprehensive toolkit for building AI applications, including natural language generation and understanding.
  - Custom agent frameworks allow for tailored solutions to specific data extraction needs.

- **Frontend:** Not applicable in this monolithic design.
- **Monitoring:** Prometheus + Grafana
  - Prometheus collects metrics from the system for real-time monitoring.
  - Grafana visualizes these metrics, providing a comprehensive dashboard for system health and performance.
- **Deployment:** Docker Compose → Kubernetes
  - Docker Compose simplifies multi-container deployment for development and testing environments.
  - Kubernetes provides production-grade orchestration for managing containerized applications.

## 2. Data Models

### Database Type Decision
**Database Type:** PostgreSQL with Redis and Pinecone/Qdrant
- **PostgreSQL:** Suitable for transactional data storage, such as user information, extraction tasks, and validation results.
- **Redis:** Ideal for caching frequently accessed data, queues, and real-time state management.
- **Pinecone/Qdrant:** Used for storing vector embeddings of extracted data for advanced AI analysis.

### Schema Definitions (Mongoose for MongoDB, Prisma for SQL)
#### PostgreSQL Schemas
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);

CREATE TABLE extraction_tasks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    url TEXT NOT NULL,
    status ENUM('pending', 'in_progress', 'completed', 'failed') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE extracted_data (
    id SERIAL PRIMARY KEY,
    task_id INT REFERENCES extraction_tasks(id),
    data JSONB NOT NULL,
    embedding FLOAT4[][], -- Vector embedding
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Redis Data Structures
- **User Sessions:** Hashes for storing user session information.
- **Task Queues:** Lists for queuing tasks for execution.

#### Pinecone/Qdrant Embeddings
- Store vector embeddings of extracted data for similarity search and retrieval.

### Relationships and Indexes
- **Users & Extraction Tasks:** One-to-Many relationship (one user can have multiple extraction tasks).
- **Extraction Tasks & Extracted Data:** One-to-Many relationship (one task can generate multiple pieces of data).
- **Indexes:** Create indexes on frequently queried columns for performance optimization.

## 3. API Contract

### RESTful Endpoints with HTTP Methods
```plaintext
GET /api/tasks - Retrieve all extraction tasks
POST /api/tasks - Create a new extraction task
GET /api/tasks/{id} - Retrieve details of a specific task
PUT /api/tasks/{id} - Update the status or URL of a task
DELETE /api/tasks/{id} - Delete an extraction task

GET /api/data - Retrieve all extracted data
POST /api/data - Add new extracted data
GET /api/data/{id} - Retrieve details of a specific piece of data
PUT /api/data/{id} - Update the data or status of a piece of data
DELETE /api/data/{id} - Delete an piece of data
```

### Request/Response Schemas
#### Create Extraction Task (POST /api/tasks)
```json
{
  "url": "https://example.com"
}
```
```json
{
  "id": 1,
  "user_id": 1,
  "url": "https://example.com",
  "status": "pending",
  "created_at": "2023-04-01T12:34:56Z"
}
```

#### Retrieve Extracted Data (GET /api/data)
```json
{
  "id": 1,
  "task_id": 1,
  "data": {
    "title": "Example Page",
    "content": "This is an example page."
  },
  "embedding": [[0.1, 0.2], [0.3, 0.4]],
  "created_at": "2023-04-01T12:35:56Z"
}
```

### Authentication Flow
- **Authentication Method:** JWT (JSON Web Tokens)
- **Token Generation:** Users receive a JWT upon successful authentication.
- **Token Validation:** Middleware validates the token for all protected endpoints.

## 4. DevOps Strategy

### Dockerfile Requirements
```dockerfile
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 6379

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml Structure
```yaml
version: '3.8'

services:
  web:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - redis

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A main.celery worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

### CI/CD Pipeline Steps
1. **Code Push:** Code changes are pushed to the repository.
2. **Build Docker Images:** Automated build of Docker images for each service.
3. **Test Application:** Run unit tests and integration tests.
4. **Deploy to Staging:** Deploy the application to a staging environment.
5. **Monitor Performance:** Monitor system performance using Prometheus and Grafana.
6. **Promote to Production:** Promote the application from staging to production.

### Environment Variables Needed
```plaintext
DB_HOST=postgres
DB_NAME=webdataextractor
DB_USER=webdatauser
DB_PASSWORD=webdatapassword
REDIS_HOST=redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
SECRET_KEY=mysecretkey
```

## 5. Security Considerations

### Input Validation Strategy
- **Validation:** All inputs are validated using Pydantic models to ensure data integrity.
- **Sanitization:** Sanitize user inputs to prevent SQL injection, XSS, and other common vulnerabilities.

### Authentication Method
- **JWT:** JWT is used for authentication and authorization.
- **Token Expiry:** Tokens expire after a certain period (e.g., 24 hours) to enhance security.

### Rate Limiting
- **Rate Limiter:** Implement rate limiting using middleware to prevent abuse of the API.
- **Configuration:** Configure rate limits based on user roles (e.g., higher limits for admins).

## Estimated Complexity Score
**Complexity Score:** 8/10

WebDataExtractor is a highly complex system with multiple agents, data pipelines, and integrations. The monolithic architecture simplifies development but requires careful management of dependencies and performance optimization.