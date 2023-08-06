def enum_from_value(enum_type, value: object):
    for t in enum_type:
        if t.value == value:
            return t

    raise Exception('Unexpected %s value: %s' % (enum_type.__name__, value))


def enum_from_name(enum_type, name: str):
    for t in enum_type:
        if t.name == name:
            return t

    raise Exception('Unexpected %s name: %s' % (enum_type.__name__, name))
