import json
from datetime import datetime

from django.test import TestCase, Client
from wfscript.constants.payload import PayloadKey

from ...utils.payload import is_uuid
from ...wfscript_api.models import Payload, Response


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

        assert Payload.objects.count() == 0
        assert Response.objects.count() == 0

        # first call
        first_output = client.post(*api_args, **api_kwargs).json()
        assert first_output[PayloadKey.RESULT] == {'first_name': 'Kathryn',
                                             'last_name': 'Janeway',
                                             'user_name': 'kathryn.janeway'}
        assert first_output[PayloadKey.RESUME] == dict()
        assert isinstance(datetime.fromisoformat(first_output[PayloadKey.TIMESTAMP]), datetime)
        assert is_uuid(first_output[PayloadKey.RUN_ID]) is True
        assert first_output[PayloadKey.DUPLICATE] is False

        assert Payload.objects.count() == 1
        assert Response.objects.count() == 1
        
        # second (duplicate) call
        second_output = client.post(*api_args, **api_kwargs).json()
        assert first_output[PayloadKey.DUPLICATE] is True
        # everything else besides "duplicate" is identical
        assert second_output == dict(first_output, **{PayloadKey.DUPLICATE: True})


        import ipdb; ipdb.set_trace()
        pass
