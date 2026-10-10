from pydantic import BaseModel, Field

class ChatQueryRequest(BaseModel):
    """The request body for a chat query."""
    query: str = Field(..., min_length=1)

class ChatQueryResponse(BaseModel):
    """The response body for a chat query."""
    response: str 
    agent: str
    