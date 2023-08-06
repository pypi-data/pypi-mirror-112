from .client_functions import get, post
from .pagination import pageQuery, PaginatedResponse
from .exceptions import SignalBoxException


def create_feature(access_token: str, base_url: str, common_id: str, name: str):
    json_params = {
        "commonId": common_id,
        "name": name,
    }
    r = post(f'{base_url}/api/features',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def get_feature(access_token: str, base_url: str, id):
    r = get(f'{base_url}/api/features/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def set_feature_value(access_token: str, base_url: str, user_id, feature_id: str, value):
    json_params = {
        "value": value,
    }
    r = post(f'{base_url}/api/trackedusers/{user_id}/features/{feature_id}',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)

def get_feature_value(access_token: str, base_url: str, user_id, feature_id: str, version: int):
    version_qs = f'?version={version}' if version is not None else ""
    r = get(f'{base_url}/api/trackedusers/{user_id}/features/{feature_id}{version_qs}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)
