from django.apps import AppConfig

from content import CONTENT_ROOT
from django_wfscript.domains import DomainConfig


class HRDomain(AppConfig, DomainConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domains.hr'
    content_root = CONTENT_ROOT

    def identify_namespaces(self):
        from content.hr import hr_root_namespace
        return [hr_root_namespace]
