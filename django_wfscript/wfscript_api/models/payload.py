from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from django_wfscript.constants.models import FieldLength


class Payload(models.Model):
    md5 = models.CharField(max_length=FieldLength.MD5, unique=True)
    data = models.JSONField(encoder=DjangoJSONEncoder)
    run = models.ForeignKey('Run', on_delete=models.PROTECT, related_name='payloads')


class Response(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    payload = models.OneToOneField(Payload, related_name='response', on_delete=models.PROTECT)
    data = models.JSONField(encoder=DjangoJSONEncoder)
