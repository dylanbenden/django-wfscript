from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views import View

from django_wfscript.utils.api import api_run_method


class RunMethod(View):
    def post(self, request):
        return JsonResponse(api_run_method(request.body), encoder=DjangoJSONEncoder)

