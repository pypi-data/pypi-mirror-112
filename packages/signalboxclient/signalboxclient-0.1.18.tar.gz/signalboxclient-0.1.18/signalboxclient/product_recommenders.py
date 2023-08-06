from typing import List
from .client_functions import get, post
from .pagination import pageQuery, PaginatedResponse
from .exceptions import SignalBoxException

def get_product_recommender(access_token: str, base_url: str, id):
    r = get(f'{base_url}/api/recommenders/ProductRecommenders/{id}', access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)


def invoke_product_recommender(access_token: str, base_url: str, id: int, common_user_id: str):
    json_params = {
        "commonUserId": common_user_id
    }
    r = post(f'{base_url}/api/recommenders/ProductRecommenders/{id}/invoke',
             json_params, access_token)
    if r.ok:
        return r.json()
    else:
        raise SignalBoxException(r.text)
