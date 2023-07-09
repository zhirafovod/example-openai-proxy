from pydantic import BaseModel
from typing import Dict

def filter_none_values(model: BaseModel) -> Dict:
    """
    Takes in a Pydantic model, converts it to a dictionary, and removes keys with None values.
    """
    data_dict = model.dict()
    filtered_dict = {k: v for k, v in data_dict.items() if v is not None}
    
    return filtered_dict

def mask_api_key(api_key):
    """ Masks the API key for privacy """
    if api_key:
        return api_key[:3] + '...' + api_key[-4:]
    else: 
        return "None"

