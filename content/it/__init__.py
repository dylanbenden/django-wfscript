from wfscript.names.store import NameStore

from .provisioning import add_user_record

it_root_namespace = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[add_user_record],
    contained_namespaces=[]
)
