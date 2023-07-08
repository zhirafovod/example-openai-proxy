from fastapi import APIRouter, FastAPI, HTTPException, Body, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.trace import TracerProvider

import os
import requests
import openai

from api.models.completion import Completion

# Import OpenTelemetry and helper functions
from api.utils.otel_instrumentation import tracer, tokens_counter, prompt_tokens_counter, completion_tokens_counter
from api.utils.helpers import mask_api_key


router = APIRouter()

@router.post("/")
async def create_chat_completion(deployment_id: str, completion: Completion, request: Request, api_version: Optional[str] = "2023-05-15"):
    # Get the API key from the request headers
    api_key = request.headers.get('openai-api-key')
    
    api_key = mask_api_key(api_key)
    
    with tracer.start_as_current_span("openai_chat_completion"):
        response = openai.ChatCompletion.create(
            model=completion.model,
            messages=[message.dict(exclude_none=True) for message in completion.messages],
            temperature=completion.temperature,
            max_tokens=completion.max_tokens
        )

        attributes = {"model": completion.model, "chat_completion_id": response['id'], "api_key": api_key}
        # Increment the counter for the number of tokens generated
        # Add the API key to the metrics labels
        tokens_counter.add(response['usage']['total_tokens'], attributes)

        # Record the prompt and completion tokens
        # Add the chat completion ID to the metrics labels
        prompt_tokens_counter.add(response['usage']['prompt_tokens'], attributes)
        completion_tokens_counter.add(response['usage']['completion_tokens'], attributes)
    
    return response