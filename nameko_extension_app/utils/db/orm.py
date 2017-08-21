""" db related operations
"""


def person_exists(session, model, column, value):
    """ Get if person exists
    """
    return bool(session.query(model).filter(column==value).count())


def add_people(session, records):
    """ Add person
    """
    for record in records:
        session.add(record)
    session.commit()


def get_all_people(session, model):
    """ Get all people
    """
    return session.query(model).all()