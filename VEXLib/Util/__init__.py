def pass_function(*args, **kwargs):
    """
    Takes any arguments and does nothing

    Args:
        *args: Takes any arguments
        **kwargs: Takes any arguments

    Returns: None
    """
    pass


def zpad_left(x, n):
    return "0" * (n - len(str(x))) + str(x)
