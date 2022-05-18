import json
from datetime import datetime

from django.test import TestCase, Client
from wfscript.constants.payload import PayloadKey

from domains.hr.models import Staff, EmergencyContact
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
        assert second_output[PayloadKey.DUPLICATE] is True
        # everything else besides "duplicate" is identical
        assert second_output == dict(first_output, **{PayloadKey.DUPLICATE: True})


    def test_run_api_multi_step(self):
        client = Client()
        method = 'hr/onboarding::onboard_user==1.0'
        first_step_payload = {
            PayloadKey.METHOD: method,
            PayloadKey.INPUT: {
                'first_name': 'Kathryn',
                'last_name': 'Janeway',
                'department': 'Operations',
                'level': 'Captain'
            }
        }
        api_args = '/api/run/', json.dumps(first_step_payload)
        api_kwargs = {'content_type': 'application/json'}

        # Initial conditions: no staff, no emergency contacts
        assert Staff.objects.all().count() == 0
        assert EmergencyContact.objects.all().count() == 0

        # First step
        expected_staff_identity = 'hr/staff::1'
        first_step_output = client.post(*api_args, **api_kwargs).json()
        assert Staff.objects.all().count() == 1
        new_staff = Staff.objects.all().first()
        assert new_staff.identity == expected_staff_identity
        run_id = first_step_output[PayloadKey.RUN_ID]
        resume_info = first_step_output[PayloadKey.RESUME]
        assert first_step_output[PayloadKey.RESULT] == {'new_staff': expected_staff_identity}
        assert is_uuid(run_id) is True
        assert resume_info == {
            PayloadKey.METHOD: 'hr/onboarding::onboard_user==1.0',
            PayloadKey.STEP: 'create_staff_record'
        }
        assert EmergencyContact.objects.all().count() == 0

        # Second step
        second_step_payload = {
            PayloadKey.METHOD: method,
            PayloadKey.INPUT: {
                'emergency_contacts': [
                    {
                        'contact_name': 'Chakotay',
                        'contact_info': 'chakotay@alumns.maquis.org'
                    },
                    {
                        'contact_name': 'Tuvok',
                        'contact_info': 'tuvok@security.voyager.ufop'
                    },
                ]
            },
            PayloadKey.RUN_ID: run_id,
            PayloadKey.RESUME: resume_info
        }
        api_args = '/api/run/', json.dumps(second_step_payload)
        second_step_output = client.post(*api_args, **api_kwargs).json()
        assert second_step_output[PayloadKey.RESULT] == {'new_staff': expected_staff_identity,
                                                         'status': 'Onboarding complete'}
        assert second_step_output[PayloadKey.RUN_ID] == run_id
        assert second_step_output[PayloadKey.RESUME] == {}
        assert Staff.objects.all().count() == 1
        assert EmergencyContact.objects.all().count() == 2

