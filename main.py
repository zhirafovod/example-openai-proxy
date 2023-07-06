from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.trace import TracerProvider

import os
import requests
import openai

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
metrics.set_meter_provider(MeterProvider())

# Get the Tracer and Meter
tracer = trace.get_tracer("openai.tracer")
meter = metrics.get_meter("openai.meter")

# Create a Counter instrument
tokens_counter = meter.create_counter(
    "tokens_counter",
    description="The number of tokens generated by model",
    unit="1",
)

# Environment Variables for the OpenAI API.

class Message(BaseModel):
    role: str = Field(..., example="system")
    content: Optional[str] = Field(None, example="You are a helpful assistant.")
    name: Optional[str] = Field(None, example="my_function")
    function_call: Optional[dict] = Field(None, example={"name": "my_function"})

class ChatCompletion(BaseModel):
    model: str = Field(..., example="gpt-3.5-turbo")
    messages: List[Message]
    temperature: Optional[float] = Field(None, example=0.5)
    max_tokens: Optional[int] = Field(None, example=100)

app = FastAPI()

@app.post("/openai/deployments/{deployment_id}/chat/completions")
async def create_chat_completion(deployment_id: str, chat_completion: ChatCompletion, api_version: Optional[str] = "2023-05-15"):
    with tracer.start_as_current_span("openai_chat_completion"):
        response = openai.ChatCompletion.create(
            model=chat_completion.model,
            messages=[message.dict(exclude_none=True) for message in chat_completion.messages],
            temperature=chat_completion.temperature,
            max_tokens=chat_completion.max_tokens
        )
        
        # Increment the counter for the number of tokens generated
        tokens_counter.add(response['usage']['total_tokens'], {"model": chat_completion.model})
    
    return response

FastAPIInstrumentor.instrument_app(app)