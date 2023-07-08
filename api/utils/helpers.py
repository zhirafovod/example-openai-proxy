def mask_api_key(api_key):
    """ Masks the API key for privacy """
    if api_key:
        return api_key[:3] + '...' + api_key[-4:]
    else: 
        return "None"
