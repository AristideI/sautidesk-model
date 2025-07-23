import logging
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Global variables for model and tokenizer
model_instance: Optional[T5ForConditionalGeneration] = None
tokenizer: Optional[T5Tokenizer] = None


def load_t5_model(
    model_path: str = "notebooks/t5-ticket-output_final/checkpoint-45000",
) -> Tuple[T5ForConditionalGeneration, T5Tokenizer]:
    """
    Load T5 model and tokenizer from the specified path

    Args:
        model_path: Path to the saved model directory

    Returns:
        Tuple of (model, tokenizer)

    Raises:
        Exception: If model loading fails
    """
    global model_instance, tokenizer

    try:
        logger.info("Loading T5 model and tokenizer...")

        # Load the saved model and tokenizer
        tokenizer = T5Tokenizer.from_pretrained(model_path)
        model_instance = T5ForConditionalGeneration.from_pretrained(model_path)

        # Move model to GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_instance.to(device)
        model_instance.eval()  # Set to evaluation mode

        logger.info(f"Model loaded successfully on device: {device}")

        return model_instance, tokenizer

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e


def get_model_and_tokenizer() -> (
    Tuple[Optional[T5ForConditionalGeneration], Optional[T5Tokenizer]]
):
    """
    Get the currently loaded model and tokenizer

    Returns:
        Tuple of (model, tokenizer) or (None, None) if not loaded
    """
    return model_instance, tokenizer


def cleanup_model():
    """Clean up model resources"""
    global model_instance, tokenizer
    model_instance = None
    tokenizer = None
    logger.info("Model resources cleaned up")
