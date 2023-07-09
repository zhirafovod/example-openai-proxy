from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field

# Example request
#
# {
#   "model": "text-davinci-003",
#   "prompt": "Write a tagline for an ice cream shop.",
#   "max_tokens": 50,
#   "temperature": 0.7,
#   "top_p": 1,
#   "frequency_penalty": 0,
#   "presence_penalty": 0,
#   "stop": [
#     "\n"
#   ]
# }

class Completion(BaseModel):
    model: str = Field(..., example="text-davinci-003")
    prompt: str = Field(..., example="Write a tagline for an ice cream shop.")
    max_tokens: Optional[int] = Field(None, example=50)
    temperature: Optional[float] = Field(None, example=0.7)
    top_p: Optional[float] = Field(None, example=1)
    frequency_penalty: Optional[float] = Field(None, example=0)
    presence_penalty: Optional[float] = Field(None, example=0)
    stop: Optional[List[str]] = Field(None, example=["\n"])
