""" Contains logging related functions
"""


def log(log_inst, level, message, *args):
    """ Log the message.
    """
    if level == 'info':
        log_inst.info(message, *args)
    elif level == 'warn':
        log_inst.warning(message, *args)
    elif level == 'error':
        log_inst.error(message, *args)


def add_person(log_inst, level, *args):
    """ Log add person action. 
    """
    master_key, person, storage = args
    message = 'Added Value (%s) to Key (%s) in %s.'
    person_info = ', '.join([person.name, str(person.age)])
    log(log_inst, level, message, person_info, master_key, storage)


def get_people(log_inst, level, *args):
    """ Log get people action.
    """
    master_key, people, storage = args
    people = str(people)
    message = 'Fetched Key (%s) having Values (%s) from %s.'
    log(log_inst, level, message, master_key, people, storage)