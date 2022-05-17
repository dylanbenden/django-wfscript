from wfscript.names.decorators import action_identity


@action_identity('hr/onboarding::add_staff_record==production')
def add_staff_record_1_0(first_name, last_name, department):
    return 'USR-123'
