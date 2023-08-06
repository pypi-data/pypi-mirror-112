
from .client_functions import get, post
from .pagination import pageQuery, PaginatedResponse
from .exceptions import SignalBoxException

def create_parameter(access_token: str, base_url: str, common_id: str, name: str, parameter_type: str, description: str):
    json_params = {
        "commonId": common_id,
        "name": name,
        "parameterType": parameter_type,
        "description": description,
    }
    r = post(f'{base_url}/api/parameters',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)