import requests
import urllib
from requests_toolbelt import MultipartEncoder
from requests.exceptions import HTTPError
class ParamError(Exception): 
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class APIError(Exception): 
    def __init__(self, message, error_code):
        self.message = message
        self.code = error_code
        super().__init__(self.message)

    def __str__(self):
        return f"Error code: {self.code}, {self.message}"


def short(url):
    if url is None:
        raise ParamError("You forgot URL!") 
    url = urllib.parse.quote(url, safe='')
    response = requests.get(f"https://api.shrtco.de/v2/shorten?url={url}")
    resp = response.json()
    if resp["ok"] == True:
        return resp["result"]
    else:
        raise APIError(resp["error"], resp["error_code"])

def info(code):
    if code is None:
        raise ParamError("You forgot code!") 
    code = urllib.parse.quote(code, safe='')
    response = requests.get(f"https://api.shrtco.de/v2/info?code={code}")
    resp = response.json()
    if resp["ok"] == True:
        return resp["result"]
    else:
        raise APIError(resp["error"], resp["error_code"])
            
def custom(url, code):
    if url is None:
        raise ParamError("You forgot URL!") 
    if code is None:
        raise ParamError("You forgot code!")
    formData = MultipartEncoder({'url': url,
                                'custom_code': code})
    response = requests.post(f"https://api.shrtco.de/v2/shorten", data=formData,
                            headers={'Content-Type': formData.content_type})
    resp = response.json()
    if resp["ok"] == True:
        return resp["result"]
    else:
        raise APIError(resp["error"], resp["error_code"])

def emoji(url):
    if url is None:
        raise ParamError("You forgot URL!") 
    url = urllib.parse.quote(url, safe='')
    response = requests.post(f"https://api.shrtco.de/v2/shorten?emoji&url={url}")
    resp = response.json()
    if resp["ok"] == True:
        return resp["result"]
    else:
        raise APIError(resp["error"], resp["error_code"])
    
def password(url, password):
    if url is None:
        raise ParamError("You forgot URL!") 
    if password is None:
        raise ParamError("You forgot password!")
    formData = MultipartEncoder({'url': url,
                                'password': password})
    response = requests.post(f"https://api.shrtco.de/v2/shorten", data=formData,
                            headers={'Content-Type': formData.content_type})
    resp = response.json()
    if resp["ok"] == True:
        return resp["result"]
    else:
        raise APIError(resp["error"], resp["error_code"])