from wfscript.names.decorators import action_identity


@action_identity('hr/onboarding::add_emergency_contacts==production')
def add_emergency_contacts_1_0(staff, contacts):
    for contact in contacts:
        staff.add_emergency_contact(contact['contact_name'], contact['contact_info'])
