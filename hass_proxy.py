import os
import json
import traceback
from functools import reduce
from urllib.parse import urljoin
from botocore.vendored import requests

HASS_URL = os.environ.get('HASS_URL')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

def dict_get(dictionary, dotted_key):
    keys = dotted_key.split('.')
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)

def lambda_handler(event, context):
    try:
        if not HASS_URL:
            raise Exception('HASS_URL env variable not set')
        url = urljoin(HASS_URL, '/api/alexa/smart_home')
        bearer_token = BEARER_TOKEN or dict_get(event, 'directive.endpoint.scope.token') or dict_get(event, 'directive.payload.scope.token')
        if not bearer_token:
            raise Exception('Bearer token not found')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }
        r = requests.post(url, data=json.dumps(event), headers=headers)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        traceback.print_exc()
        raise e
