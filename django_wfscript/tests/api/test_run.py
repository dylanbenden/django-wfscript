import json

from django.test import TestCase, Client
from wfscript.constants.payload import PayloadKey

# from ...models.payload import Payload, Response
from ...utils.payload import is_uuid


class RunApiTestCase(TestCase):
    def test_run_api(self):
        client = Client()
        method = 'it/provisioning::provision_user==1.0'
        payload = {
            PayloadKey.METHOD: method,
            PayloadKey.INPUT: {
                'first_name': 'Kathryn',
                'last_name': 'Janeway',
                'department': 'Operations',
            }
        }
        api_args = '/api/run/', json.dumps(payload)
        api_kwargs = {'content_type': 'application/json'}

        output = client.post(*api_args, **api_kwargs).json()
        assert output[PayloadKey.RESULT] == {'first_name': 'Kathryn',
                                             'last_name': 'Janeway',
                                             'user_name': 'kathryn.janeway'}
        assert output[PayloadKey.RESUME] == dict()
        assert PayloadKey.TIMESTAMP in output
        assert PayloadKey.RUN_ID in output
