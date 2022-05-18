import os
from collections import defaultdict

from django.apps import apps
from wfscript.constants.identity import IdentityDelimeter

from django_wfscript.constants.domains import DomainKeyword


class DomainConfig(object):
    namespace_root_for_method = dict()
    namespace_root_for_action = dict()
    material_models = None

    def identify_namespaces(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement identify_namespaces()')

    def load_namespaces(self):
        for namespace_root in self.identify_namespaces():
            namespace_root.set_domain(self)
            for method_identity in namespace_root.yaml_documents.keys():
                self.namespace_root_for_method[method_identity] = namespace_root
            for action_identity in namespace_root.actions:
                self.namespace_root_for_action[action_identity] = namespace_root

    def load_models(self):
        from wfscript.materials.mixin import WorkflowMaterial
        self.material_models = dict()
        for model in self.models.values():
            if issubclass(model, WorkflowMaterial):
                self.material_models[model.model_identity] = model

    def get_method(self, identity):
        return self.namespace_root_for_method[identity].get_method(identity)

    def get_validator(self, identity, last_step_info=None):
        return self.namespace_root_for_method[identity].get_validator(identity, last_step_info)

    def get_action(self, identity):
        return self.namespace_root_for_action[identity].get_action(identity)

    def load_materials(self, identities):
        # NB: a material identifier is:
        # model_identifier::unique_id
        records = list()
        record_id_by_model_id = defaultdict(list)
        # group records by model to look up as efficiently as possible
        for model_id, record_id in [mat_id.split(IdentityDelimeter.MATERIAL) for mat_id in identities]:
            record_id_by_model_id[model_id].append(record_id)
        for model_id, record_ids in record_id_by_model_id.items():
            model = self.material_models[model_id]
            id_field = f'{model.identity_field}__in'
            records.extend([obj for obj in model.objects.filter(**{id_field: record_ids})])
        # re-order records to reflect order ids were provided in
        return sorted(records, key=lambda x: identities.index(x.identity))

    def load_material(self, identity):
        # one is not a very special case ;)
        return self.load_materials([identity])[0]


class CoreConfig(object):
    name = f'{__file__.split(os.path.sep)[-2]}.{DomainKeyword.CORE_DOMAIN}'

    domain_for_method = dict()
    domain_for_action = dict()
    domain_for_model = dict()

    def active_domains(self):
        return [d for d in apps.get_app_configs() if isinstance(d, DomainConfig)]

    def setup(self):
        if not self.domain_for_method:
            for domain in self.active_domains():
                domain.load_models()
                domain.load_namespaces()
                # todo: as part of sanity checking, ensure all importable method/action/model names are unique
                self.domain_for_method.update({k: domain for k in domain.namespace_root_for_method})
                self.domain_for_action.update({k: domain for k in domain.namespace_root_for_action})
                self.domain_for_model.update({k: domain for k in domain.material_models})

    def get_method_executor(self, identity):
        if identity in self.domain_for_method:
            return self.domain_for_method[identity].get_method(identity)

    def get_method(self, identity):
        if identity in self.domain_for_method:
            return self.domain_for_method[identity].namespace_root_for_method[identity].get_method(identity)
        raise RuntimeError(f'Unable to resolve method identity {identity}')

    def get_validator(self, identity, last_step_info=None):
        if identity in self.domain_for_method:
            return self.domain_for_method[identity].namespace_root_for_method[identity].get_validator(identity,
                                                                                                      last_step_info)
        raise RuntimeError(f'Unable to resolve validator identity {identity}')

    def get_action(self, identity):
        if identity in self.domain_for_action:
            return self.domain_for_action[identity].namespace_root_for_action[identity].get_action(identity)
        raise RuntimeError(f'Unable to resolve action identity {identity}')

    def get_material_model(self, identity):
        if identity in self.domain_for_model:
            return self.domain_for_model[identity].material_models[identity]
        raise RuntimeError(f'Unable to resolve model identity {identity}')

