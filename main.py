from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
import os
import requests

# Environment Variables for the OpenAI API.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", 'https://api.openai.com/v1/completions')

class ModelPrompt(BaseModel):
    model: str
    prompt: Union[str, List[str], List[int], List[List[int]]]
    suffix: Optional[str] = Field(None)
    max_tokens: Optional[int] = Field(16)
    temperature: Optional[float] = Field(1)
    top_p: Optional[float] = Field(1)
    n: Optional[int] = Field(1)
    stream: Optional[bool] = Field(False)
    logprobs: Optional[int] = Field(None)
    echo: Optional[bool] = Field(False)
    stop: Optional[Union[str, List[str]]] = Field(None)
    presence_penalty: Optional[float] = Field(0)
    frequency_penalty: Optional[float] = Field(0)
    best_of: Optional[int] = Field(1)
    logit_bias: Optional[Dict[str, int]] = Field(None)
    user: Optional[str] = Field(None)

app = FastAPI()

@app.post("/api/v1/completions/")
async def generate_completion(prompt_details: ModelPrompt):
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json=prompt_details.dict(exclude_unset=True)
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()