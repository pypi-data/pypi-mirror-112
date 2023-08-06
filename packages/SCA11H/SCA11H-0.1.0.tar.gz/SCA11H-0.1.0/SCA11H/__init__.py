def get_argument_name(var):
    # Some python magic to get the original variable name (https://stackoverflow.com/a/2749881)
    import inspect
    stack_locals = inspect.stack()[2][0].f_locals
    for name in stack_locals:
        if id(var) == id(stack_locals[name]):
            return name

    return None
