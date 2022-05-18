from django.db import models
from wfscript.materials.mixin import WorkflowMaterial

from django_wfscript.constants.models import FieldLength


class User(models.Model, WorkflowMaterial):
    model_identity = 'it/user'
    identity_field = 'id'


    user_name = models.CharField(max_length=FieldLength.NAME, unique=True)
    first_name = models.CharField(max_length=FieldLength.NAME)
    last_name = models.CharField(max_length=FieldLength.NAME)

    @property
    def email(self):
        return f'{self.user_name}@example_corp.com'

    def save(self, *args, **kwargs):
        if not self.user_name:
            self.user_name = f'{self.first_name}.{self.last_name}'
        super(User, self).save(*args, **kwargs)