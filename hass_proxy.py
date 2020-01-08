import os
import json
import traceback
from functools import reduce
from urllib import request

HASS_URL = os.environ.get('HASS_URL')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

def dict_get(dictionary, dotted_key):
    keys = dotted_key.split('.')
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)

def lambda_handler(event, context):
    try:
        if not HASS_URL:
            raise Exception('HASS_URL env variable not set')
        bearer_token = BEARER_TOKEN or \
            dict_get(event, 'directive.endpoint.scope.token') or \
            dict_get(event, 'directive.payload.grantee.token') or \
            dict_get(event, 'directive.payload.scope.token')
        if not bearer_token:
            raise Exception('Bearer token not found')
        url = HASS_URL.rstrip('/') + '/api/alexa/smart_home'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }
        req = request.Request(url, data=json.dumps(event).encode('utf-8'), headers=headers)
        r = request.urlopen(req)
        return json.load(r)
    except Exception as e:
        traceback.print_exc()
        raise e
