from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatMessage(BaseModel):
    """Schema for a chat message"""
    id: Optional[str] = None
    role: str
    content: str
    parts: Optional[List[Any]] = Field(default_factory=list)
    cache: Optional[bool] = False


class ChatRequest(BaseModel):
    """Schema for a chat request"""
    id: str
    messages: List[ChatMessage]
    isFirstPrompt: Optional[bool] = False
    conversationId: Optional[str] = None
    featurePreviews: Optional[Dict[str, bool]] = None
    errorReasoning: Optional[str] = None
    framework: Optional[str] = None
    promptMode: Optional[str] = None
    projectId: Optional[str] = None
    stripeStatus: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    usesInspectedElement: Optional[bool] = False


class StreamingResponse(BaseModel):
    """Schema for chunks in a streaming response"""
    text: str
    done: bool 