from typing import Optional, List
from pydantic import BaseModel, Field


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