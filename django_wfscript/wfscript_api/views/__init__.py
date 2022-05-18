from django.apps import apps

from django_wfscript.constants.domains import DomainKeyword

core_domain = apps.get_app_config(DomainKeyword.CORE_DOMAIN)
core_domain.setup()