import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from django_wfscript.constants.models import FieldLength


class Run(models.Model):
    identity = models.CharField(max_length=FieldLength.UUID, unique=True)
    method = models.CharField(max_length=FieldLength.IDENTITY)
    state = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    resume_method = models.CharField(max_length=FieldLength.IDENTITY)
    resume_step = models.CharField(max_length=FieldLength.NAME)
    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.identity:
            self.identity = str(uuid.uuid4())
        super(Run, self).save(*args, **kwargs)
