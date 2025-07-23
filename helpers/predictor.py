import logging
import torch
from fastapi import HTTPException
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Optional

logger = logging.getLogger(__name__)


def predict_ticket(
    issue_text: str,
    model: T5ForConditionalGeneration,
    tokenizer: T5Tokenizer,
    max_length: int = 512,
    temperature: float = 0.7,
) -> str:
    """
    Generate ticket from issue text using T5 model

    Args:
        issue_text: The issue description text
        model: Loaded T5 model instance
        tokenizer: Loaded T5 tokenizer instance
        max_length: Maximum length of generated text
        temperature: Sampling temperature for generation

    Returns:
        Generated ticket text

    Raises:
        HTTPException: If prediction fails
    """
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


def validate_prediction_request(
    issue_text: str, max_length: Optional[int], temperature: Optional[float]
) -> tuple[int, float]:
    """
    Validate and normalize prediction request parameters

    Args:
        issue_text: The issue description text
        max_length: Optional max length parameter
        temperature: Optional temperature parameter

    Returns:
        Tuple of (max_length, temperature) with default values applied

    Raises:
        HTTPException: If validation fails
    """
    if not issue_text or not issue_text.strip():
        raise HTTPException(status_code=400, detail="Issue text cannot be empty")

    # Apply default values if None
    final_max_length = max_length if max_length is not None else 512
    final_temperature = temperature if temperature is not None else 0.7

    # Validate ranges
    if final_max_length <= 0:
        raise HTTPException(status_code=400, detail="max_length must be positive")

    if final_temperature <= 0 or final_temperature > 2.0:
        raise HTTPException(
            status_code=400, detail="temperature must be between 0 and 2.0"
        )

    return final_max_length, final_temperature
