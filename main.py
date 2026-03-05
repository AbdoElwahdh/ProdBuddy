"""FastAPI Application Entry Point"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.tasks_routes import router as tasks_router
from app.api.routes.ideas_routes import router as ideas_router
from app.api.routes.notes_routes import router as notes_router
from app.api.routes.shopitems_routes import router as shopitems_router
from app.api.routes.dashboard_routes import router as dashboard_router

# Initialize FastAPI App
app = FastAPI(
    title="ProdBuddy API",
    version="1.0.0",
    description="API for task management"
)

# CORS Middleware (Allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(ideas_router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(shopitems_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "AgenticAI API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the API with uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
