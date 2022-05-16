from django.apps import AppConfig, apps
from django_wfscript.domains import DomainConfig, CoreConfig


class WfscriptCore(AppConfig, DomainConfig, CoreConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_wfscript.wfscript_api'

    def identify_namespaces(self):
        return list()
