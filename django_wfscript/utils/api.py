import json

from wfscript.constants.payload import PayloadKey

from django_wfscript.utils.payload import hash_request_body
from django_wfscript.wfscript_api.models import Payload, Response
from django_wfscript.wfscript_api.views import core_domain


def api_run_method(request_body):
    payload_hash = hash_request_body(request_body)
    try:
        # if we've seen this payload already, idempotently repeat our last response
        payload = Payload.objects.get(md5=payload_hash)
        return dict(payload.response.data, **{PayloadKey.DUPLICATE: True})
    except Payload.DoesNotExist:
        payload_data = json.loads(request_body)
        method_identity = payload_data[PayloadKey.METHOD]
        method_executor = core_domain.get_method_executor(method_identity)
        response_data = method_executor.run(input_data=payload_data[PayloadKey.INPUT])
        payload = Payload.objects.create(md5=payload_hash)
        Response.objects.create(payload=payload, data=response_data)
        return dict(payload.response.data, **{PayloadKey.DUPLICATE: False})