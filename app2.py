from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="T5 Ticket Generation API",
    description="API for generating tickets from issue descriptions using T5 model",
    version="1.0.0",
)

# Global variables for model and tokenizer
model = None
tokenizer = None


# Request/Response models
class TicketRequest(BaseModel):
    issue_text: str
    max_length: Optional[int] = 512
    temperature: Optional[float] = 0.7


class TicketResponse(BaseModel):
    generated_ticket: str
    status: str


@app.on_event("startup")
async def load_model():
    """Load the model and tokenizer on startup"""
    global model, tokenizer

    try:
        logger.info("Loading T5 model and tokenizer...")

        # Load the saved model and tokenizer
        model_path = "models/t5-ticket-model"

        tokenizer = T5Tokenizer.from_pretrained(model_path)
        model = T5ForConditionalGeneration.from_pretrained(model_path)

        # Move model to GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()  # Set to evaluation mode

        logger.info(f"Model loaded successfully on device: {device}")

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e


@app.on_event("shutdown")
async def cleanup():
    """Clean up resources on shutdown"""
    global model, tokenizer
    model = None
    tokenizer = None
    logger.info("Model resources cleaned up")


def predict_ticket(
    issue_text: str, max_length: int = 512, temperature: float = 0.7
) -> str:
    """Generate ticket from issue text"""
    try:
        # Prepare input text
        input_text = f"Generate ticket from: {issue_text}"

        # Tokenize input
        inputs = tokenizer(
            input_text, return_tensors="pt", truncation=True, padding=True
        ).to(model.device)

        # Generate output
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        # Decode and return result
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict", response_model=TicketResponse)
async def generate_ticket(request: TicketRequest):
    """Generate a ticket from issue description"""

    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not request.issue_text.strip():
        raise HTTPException(status_code=400, detail="Issue text cannot be empty")

    try:
        # Generate ticket
        generated_ticket = predict_ticket(
            request.issue_text,
            max_length=request.max_length,
            temperature=request.temperature,
        )

        return TicketResponse(generated_ticket=generated_ticket, status="success")

    except Exception as e:
        logger.error(f"Error generating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate ticket")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = (
        "loaded" if model is not None and tokenizer is not None else "not_loaded"
    )
    return {
        "status": "healthy",
        "model_status": model_status,
        "device": str(model.device) if model is not None else "unknown",
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "T5 Ticket Generation API", "docs": "/docs"}


# Example usage endpoint for testing
@app.get("/example")
async def example_usage():
    """Example of how to use the API"""
    return {
        "example_request": {
            "issue_text": "My electricity has been out since last night. Please help.",
            "max_length": 512,
            "temperature": 0.7,
        },
        "usage": "POST /predict with the above JSON body",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
