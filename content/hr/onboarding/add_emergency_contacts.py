from wfscript.names.decorators import action_identity


@action_identity('hr/onboarding::add_emergency_contacts==production')
def add_emergency_contacts_1_0(user_id, contacts):
    pass
