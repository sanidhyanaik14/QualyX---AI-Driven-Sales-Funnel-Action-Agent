'''	
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import leads, agents, webhooks

app = FastAPI(
    title='QualyX API',
    description='AI Business Action Agent',
    version='1.0.0',
    docs_url='/docs',   # Free Swagger UI — visit /docs after starting
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, 'http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(leads.router)
app.include_router(agents.router)
app.include_router(webhooks.router)

@app.get('/health')
async def health():
    return {'status': 'ok', 'service': 'QualyX', 'version': '1.0.0'}'''

# Run: uvicorn main:app --reload --port 8000

# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import leads, agents, webhooks

app = FastAPI(
    title='QualyX API',
    description='AI Business Action Agent',
    version='1.0.0',
    docs_url='/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, 'http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(leads.router)
app.include_router(agents.router)
app.include_router(webhooks.router)

@app.get('/health')
async def health():
    return {'status': 'ok', 'service': 'QualyX', 'version': '1.0.0'}