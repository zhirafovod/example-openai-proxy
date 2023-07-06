from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
import os
import requests
import openai
import ptvsd

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
    response = openai.ChatCompletion.create(
        model=chat_completion.model,
        messages=[message.dict(exclude_none=True) for message in chat_completion.messages],
        temperature=chat_completion.temperature,
        max_tokens=chat_completion.max_tokens
    )

    return response

# if __name__ == "__main__":
#     ptvsd.enable_attach(address=('localhost', 5678))
#     ptvsd.wait_for_attach()  # Only include this line if you want to wait until debugger is attached before running your application.
#     uvicorn.run(app, host="0.0.0.0", port=8000)