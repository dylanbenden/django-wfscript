from django.apps import apps

core_domain = apps.get_app_config('wfscript_api')
core_domain.build_method_map()