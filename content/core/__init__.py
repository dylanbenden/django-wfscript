from wfscript.names.store import NameStore

from .materials import add_material

core_root_namespace = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[add_material],
    contained_namespaces=[]
)
