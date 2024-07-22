from fastapi import APIRouter, FastAPI, HTTPException, Body, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.trace import TracerProvider

import os
import requests
from openai import OpenAI

client = OpenAI()

from api.models.completion import Completion

# Import OpenTelemetry and helper functions
from api.utils.otel_instrumentation import tracer, tokens_counter, prompt_tokens_counter, completion_tokens_counter
from api.utils.helpers import filter_none_values, mask_api_key


router = APIRouter()

@router.post("/")
async def create_completion(deployment_id: str, completion: Completion, request: Request, api_version: Optional[str] = "2023-05-15"):
    # Get the API key from the request headers
    api_key = request.headers.get('openai-api-key')

    # Mask the API key
    api_key = mask_api_key(api_key)
    
    with tracer.start_as_current_span("openai_completion"):
        data = filter_none_values(completion)
        print(f"completion={completion}, data={data}")
        response = client.completions.create(**data)

        # example response
        # 
        # {
        #   "id": "cmpl-7aQ9J49MLph16NRVBGXry9F8NEmGb",
        #   "object": "text_completion",
        #   "created": 1688914681,
        #   "model": "text-davinci-003",
        #   "choices": [
        #     {
        #       "text": "",
        #       "index": 0,
        #       "logprobs": null,
        #       "finish_reason": "stop"
        #     }
        #   ],
        #   "usage": {
        #     "prompt_tokens": 10,
        #     "total_tokens": 10
        #   }
        # }        

        print(f"response={response}")
        attributes = {"model": completion.model, "completion_id": response.id, "api_key": api_key}
        # Increment the counter for the number of tokens generated
        # Add the API key to the metrics labels
        tokens_counter.add(response.usage.total_tokens, attributes)

        # Record the prompt tokens
        # Add the completion ID to the metrics labels
        prompt_tokens_counter.add(response.usage.prompt_tokens, attributes)
    
    return response
