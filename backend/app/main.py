from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard, threats, clusters, ai

app = FastAPI(
    title="KubeZap API",
    description="GitOps-Native Security Gate for Kubernetes",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_tags=[
        {"name": "Dashboard", "description": "Real-time security metrics"},
        {"name": "Threats", "description": "Vulnerability management"},
        {"name": "Clusters", "description": "Multi-cluster operations"},
        {"name": "AI", "description": "AI-powered analysis"},
    ]
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(threats.router, prefix="/api/v1")
app.include_router(clusters.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "KubeZap API is running safely."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
