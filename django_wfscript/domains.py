from django.apps import apps


class DomainConfig(object):
    namespace_root_for_method = dict()
    namespace_roots = list()

    def identify_namespaces(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement identify_namespaces()')

    def load_namespaces(self):
        for namespace_root in self.identify_namespaces():
            namespace_root.set_domain(self)
            for method_identity in namespace_root.yaml_documents.keys():
                self.namespace_root_for_method[method_identity] = namespace_root

    def get_method(self, identity):
        return self.namespace_root_for_method[identity].get_method(identity)


class CoreConfig(object):
    domain_for_method = dict()

    def active_domains(self):
        return [d for d in apps.get_app_configs() if isinstance(d, DomainConfig)]

    def build_method_map(self):
        if not self.domain_for_method:
            for domain in self.active_domains():
                domain.load_namespaces()
                self.domain_for_method.update({k: domain for k in domain.namespace_root_for_method})

    def get_method_executor(self, identity):
        if identity in self.domain_for_method:
            return self.domain_for_method[identity].get_method(identity)