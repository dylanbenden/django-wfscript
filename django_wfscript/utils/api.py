import json

from wfscript.constants.payload import PayloadKey

from django_wfscript.wfscript_api.views import core_domain


def api_run_method(request_body):
    payload_data = json.loads(request_body)
    method_identity = payload_data[PayloadKey.METHOD]
    method_executor = core_domain.get_method_executor(method_identity)
    return method_executor.run(
        input_data=payload_data[PayloadKey.INPUT]
    )
