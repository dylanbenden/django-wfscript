import json

from wfscript.constants.payload import PayloadKey

from django_wfscript.utils.payload import hash_request_body
from django_wfscript.wfscript_api.models import Payload, Response, Run
from django_wfscript.wfscript_api.views import core_domain


def be_idempotent(payload_hash):
    try:
        payload = Payload.objects.get(md5=payload_hash)
        return dict(payload.response.data, **{PayloadKey.DUPLICATE: True})
    except Payload.DoesNotExist:
        pass


def confirm_resume_info(payload_data, run):
    if not payload_data[PayloadKey.RESUME]:
        raise RuntimeError(f'If {PayloadKey.RUN_ID} is provided, {PayloadKey.RESUME} must be provided as well')
    else:
        provided_method = payload_data[PayloadKey.RESUME].get(PayloadKey.METHOD)
        if run.resume_method != provided_method:
            RuntimeError(f'Next method for Run {run.identity} is {run.resume_method}; '
                         f'Provided: {provided_method}')
        provided_step = payload_data[PayloadKey.RESUME].get(PayloadKey.STEP)
        if run.resume_step != provided_step:
            RuntimeError(f'Next step for Run {run.identity} is {run.resume_step}; '
                         f'Provided: {provided_step}')


def load_run_and_confirm_resume_info(payload_data):
    run = Run.objects.get(identity=payload_data[PayloadKey.RUN_ID])
    confirm_resume_info(payload_data, run)
    return run


def handle_resume_state(run, response_data):
    if response_data[PayloadKey.RESUME]:
        if PayloadKey.STATE in response_data[PayloadKey.RESUME]:
            run.state = response_data[PayloadKey.RESUME].pop(PayloadKey.STATE)
        run.resume_method = response_data[PayloadKey.RESUME][PayloadKey.METHOD]
        run.resume_step = response_data[PayloadKey.RESUME][PayloadKey.STEP]
        run.save()


def api_run_method(request_body):
    payload_hash = hash_request_body(request_body)
    duplicate_results = be_idempotent(payload_hash)
    if duplicate_results:
        return duplicate_results
    else:
        payload_data = json.loads(request_body)
        method_identity = payload_data[PayloadKey.METHOD]
        if payload_data.get(PayloadKey.RUN_ID):
            run = load_run_and_confirm_resume_info(payload_data)
        else:
            run = Run.objects.create(method=method_identity)
        payload = Payload.objects.create(md5=payload_hash, run=run, data=payload_data)
        method_executor = core_domain.get_method_executor(method_identity)
        response_data = method_executor.run(input_data=payload_data[PayloadKey.INPUT],
                                            state=run.state,
                                            resume_info=payload_data.get(PayloadKey.RESUME, {}))
        response_data[PayloadKey.RUN_ID] = run.identity
        handle_resume_state(run, response_data)
        Response.objects.create(payload=payload, data=response_data)
        return dict(response_data, **{PayloadKey.DUPLICATE: False})