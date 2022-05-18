from django.apps import AppConfig

from django_wfscript.domains import DomainConfig, CoreConfig


class WfscriptCore(AppConfig, DomainConfig, CoreConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    def identify_namespaces(self):
        from content.core import core_root_namespace
        return [core_root_namespace]
