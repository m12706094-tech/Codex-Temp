"""Request and response schemas."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming prompt payload."""

    prompt: str = Field(..., min_length=1, description="User prompt.")


class ChatResponse(BaseModel):
    """Outgoing model response payload."""

    answer: str = Field(..., description="Model-generated answer.")
    model: str = Field(..., description="Model name used to generate the answer.")
