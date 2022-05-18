from wfscript.names.store import NameStore

from .onboarding import add_emergency_contacts

hr_root_namespace = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[add_emergency_contacts],
    contained_namespaces=[]
)
