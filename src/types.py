from pydantic import BaseModel
from typing import Optional


class TicketRequest(BaseModel):
    """Request model for ticket generation"""

    issue_text: str
    max_length: Optional[int] = 512
    temperature: Optional[float] = 0.7


class TicketResponse(BaseModel):
    """Response model for ticket generation"""

    generated_ticket: str
    status: str
