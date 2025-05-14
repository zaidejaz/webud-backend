from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from src.schemas.chat import ChatRequest, StreamingResponse
from src.utils.llm import get_llm_response
import json
import asyncio

router = APIRouter(prefix="/chat", tags=["Chat"])

async def generate_response_stream(messages):
    """
    Generate a stream of responses to simulate a chat interaction.
    In a real implementation, this would connect to an actual LLM API with streaming.
    """
    # Extract the user prompt from the last user message
    user_messages = [msg.content for msg in messages if msg.role == "user"]
    prompt = user_messages[-1] if user_messages else "Hello"
    
    # Get the initial LLM response (non-streaming in this implementation)
    # In a production environment, you'd use an API that supports streaming
    full_response = get_llm_response(prompt)
    
    # Simulate streaming by chunking the response
    chunks = []
    words = full_response.split()
    chunk_size = max(1, len(words) // 10)  # Split into ~10 chunks
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    # Stream each chunk with a small delay to simulate real-time generation
    for i, chunk in enumerate(chunks):
        done = i == len(chunks) - 1
        yield json.dumps({"text": chunk, "done": done}) + "\n"
        await asyncio.sleep(0.1)  # Small delay between chunks

@router.post("")
async def chat(request: ChatRequest):
    """
    Chat endpoint that returns a streaming response
    
    This endpoint accepts chat messages and returns a stream of responses
    that can be consumed by the frontend.
    """
    return StreamingResponse(
        generate_response_stream(request.messages),
        media_type="text/event-stream"
    )
    