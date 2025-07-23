from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from routes import astra, create, search, model
from src.types import TicketRequest, TicketResponse
from helpers.model_loader import load_t5_model, get_model_and_tokenizer, cleanup_model
from helpers.predictor import predict_ticket, validate_prediction_request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        load_t5_model()
        logger.info("Application startup completed")
    except Exception as e:
        logger.error(f"Failed to load model on startup: {str(e)}")
        raise e

    yield

    # Shutdown
    cleanup_model()
    logger.info("Application shutdown completed")


# Create FastAPI app instance
app = FastAPI(
    title="SautiDesk Model API",
    description="API for SautiDesk model predictions and data management",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"message": "SautiDesk Model API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_instance, tokenizer = get_model_and_tokenizer()
    model_status = (
        "loaded"
        if model_instance is not None and tokenizer is not None
        else "not_loaded"
    )

    return {
        "status": "healthy",
        "service": "SautiDesk Model API",
        "model_status": model_status,
        "device": (
            str(model_instance.device) if model_instance is not None else "unknown"
        ),
    }


@app.post("/predict", response_model=TicketResponse)
async def generate_ticket(request: TicketRequest):
    """Generate a ticket from issue description"""
    # Get model and tokenizer
    model_instance, tokenizer = get_model_and_tokenizer()

    if model_instance is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Validate and normalize request parameters
        max_length, temperature = validate_prediction_request(
            request.issue_text, request.max_length, request.temperature
        )

        # Generate ticket
        generated_ticket = predict_ticket(
            request.issue_text,
            model_instance,
            tokenizer,
            max_length=max_length,
            temperature=temperature,
        )

        return TicketResponse(generated_ticket=generated_ticket, status="success")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error generating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate ticket")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
