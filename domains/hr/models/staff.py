from django.db import models
from wfscript.materials.mixin import WorkflowMaterial

from django_wfscript.constants.models import FieldLength


class Staff(models.Model, WorkflowMaterial):
    model_identity = 'hr/staff'
    identity_field = 'pk'
    # todo: make emergency_contacts private/hidden to actions

    employee_id = models.CharField(max_length=FieldLength.NAME, unique=True)
    first_name = models.CharField(max_length=FieldLength.NAME)
    last_name = models.CharField(max_length=FieldLength.NAME)
    internal_email = models.CharField(max_length=FieldLength.NAME, unique=True)
    external_email = models.CharField(max_length=FieldLength.NAME, unique=True)

    def add_emergency_contact(self, contact_name, contact_info):
        EmergencyContact.objects.create(staff=self, contact_name=contact_name, contact_info=contact_info)


class EmergencyContact(models.Model):  # Note: not directly exposed a material, but available via Staff object
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='emergency_contacts')
    contact_name = models.CharField(max_length=FieldLength.NAME)
    contact_info = models.CharField(max_length=FieldLength.NAME)