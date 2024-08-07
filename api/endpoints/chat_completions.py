from fastapi import APIRouter, FastAPI, HTTPException, Body, Request
from typing import Optional

from openai import OpenAI

client = OpenAI()
from api.models.chat_completion import ChatCompletion

# Import OpenTelemetry and helper functions
from api.utils.otel_instrumentation import tracer, tokens_counter, prompt_tokens_counter, completion_tokens_counter
from api.utils.helpers import mask_api_key

router = APIRouter()

@router.post("/")
async def create_chat_completion(chat_completion: ChatCompletion, request: Request, deployment_id: Optional[str] = "default-deployment", api_version: Optional[str] = "2023-05-15"):
    # Get the API key from the request headers
    api_key = request.headers.get('openai-api-key')
    
    api_key = mask_api_key(api_key)
    
    with tracer.start_as_current_span("openai_chat_completion"):
        response = client.chat.completions.create(model=chat_completion.model,
        messages=[message.dict(exclude_none=True) for message in chat_completion.messages],
        temperature=chat_completion.temperature,
        max_tokens=chat_completion.max_tokens)

        attributes = {"model": chat_completion.model, "chat_completion_id": response.id, "api_key": api_key}
        tokens_counter.add(response.usage.total_tokens, attributes)
        prompt_tokens_counter.add(response.usage.prompt_tokens, attributes)
        completion_tokens_counter.add(response.usage.completion_tokens, attributes)
    
    return response
