from django.apps import AppConfig

from content import CONTENT_ROOT
from django_wfscript.domains import DomainConfig


class ITDomain(AppConfig, DomainConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domains.it'
    content_root = CONTENT_ROOT

    def identify_namespaces(self):
        from content.it import it_root_namespace
        return [it_root_namespace]
