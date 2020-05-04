def Set(*rest):
    """Using python's built-in "set" function is dangerous!! if you
    pass it a string on accident, it produces a set of all the
    characters in the string, instead of producing a set containing a
    string."""
    # if isinstance(rest[0], map):
    #     return set(rest[0])
    # elif len(rest) == 1 and type(rest[0]).__name__ == 'list':
    if len(rest) == 1 and type(rest[0]).__name__ == 'list':
        return set(rest[0])
    return set(rest)
