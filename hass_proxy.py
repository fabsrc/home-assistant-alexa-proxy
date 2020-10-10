import os
import ssl
import json
import traceback
from urllib import request
from functools import reduce

HASS_URL = os.environ.get('HASS_URL')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
VERIFY_SSL = os.environ.get('VERIFY_SSL') != 'false'

def dict_get(dictionary, dotted_key):
    keys = dotted_key.split('.')
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)

def lambda_handler(event, context):
    try:
        assert HASS_URL, 'HASS_URL environment variable is not set'

        bearer_token = BEARER_TOKEN or \
            dict_get(event, 'directive.endpoint.scope.token') or \
            dict_get(event, 'directive.payload.grantee.token') or \
            dict_get(event, 'directive.payload.scope.token')
        assert bearer_token, 'Bearer token missing'

        url = HASS_URL.rstrip('/') + '/api/alexa/smart_home'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }
        req = request.Request(url, data=json.dumps(event).encode('utf-8'), headers=headers)
        context = ssl.create_default_context()

        if VERIFY_SSL is False:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        r = request.urlopen(req, context=context)
        return json.load(r)
    except Exception as e:
        traceback.print_exc()
        raise e
