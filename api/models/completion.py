from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field


class Completion(BaseModel):
    model: str = Field(..., example="text-davinci-002")
    prompt: Union[str, List[str], List[List[int]]] = Field(..., example="Translate the following English text to French: '{}")
    temperature: Optional[float] = Field(None, example=0.8)
    max_tokens: Optional[int] = Field(None, example=60)
    top_p: Optional[float] = Field(None, example=1)
    n: Optional[int] = Field(None, example=1)
    stream: Optional[bool] = Field(None, example=False)
    logprobs: Optional[int] = Field(None, example=5)
    echo: Optional[bool] = Field(None, example=False)
    stop: Optional[Union[str, List[str]]] = Field(None, example=".")
    presence_penalty: Optional[float] = Field(None, example=0)
    frequency_penalty: Optional[float] = Field(None, example=0)
    best_of: Optional[int] = Field(None, example=1)
    logit_bias: Optional[Dict[int, float]] = Field(None, example={50256: -100})
    user: Optional[str] = Field(None, example="user1234")
