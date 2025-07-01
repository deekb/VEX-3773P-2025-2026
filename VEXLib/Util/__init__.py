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


def enumerate(iterable, start=0):
    # Create an iterator for the iterable
    it = iter(iterable)

    # Start the index from the given value
    index = start

    while True:
        try:
            # Get the next item from the iterator
            value = next(it)
            # Yield the index and the item as a tuple
            yield index, value
            # Increment the index
            index += 1
        except StopIteration:
            # Stop iteration when the iterable is exhausted
            break
