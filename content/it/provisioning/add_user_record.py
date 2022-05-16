from wfscript.names.decorators import action_identity


@action_identity('it/provisioning::add_user_record==production')
def add_user_record_1_0(first_name, last_name, department):
    return f'{first_name.lower()}.{last_name.lower()}'
