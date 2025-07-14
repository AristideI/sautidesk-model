from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import astra, create, search, model

# Create FastAPI app instance
app = FastAPI(
    title="SautiDesk Model API",
    description="API for SautiDesk model predictions and data management",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(astra.router, prefix="/astra", tags=["astra"])
app.include_router(create.router, prefix="/create", tags=["create"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(model.router, prefix="/model", tags=["model"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello World", "service": "SautiDesk Model API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SautiDesk Model API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
