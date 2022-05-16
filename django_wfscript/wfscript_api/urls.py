from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views.run import RunMethod

urlpatterns = [
    path('run/', csrf_exempt(RunMethod.as_view()), name='run-method'),
]