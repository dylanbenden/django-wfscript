from wfscript.names.decorators import action_identity


@action_identity('core/materials::add_material==production')
def add_material_1_0(model_identity, **kwargs):
    from django_wfscript.wfscript_api.views import core_domain
    model = core_domain.get_material_model(model_identity)
    return model.objects.create(**kwargs)

