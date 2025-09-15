try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        json = None


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
    str_x = str(x)
    return "0" * (n - len(str_x)) + str_x


# noinspection PyShadowingBuiltins
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


def quote_field(s):
    ONE_DOUBLE_QUOTE = '"'
    TWO_DOUBLE_QUOTES = ONE_DOUBLE_QUOTE * 2
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    if any([bad_char in s for bad_char in [",", ONE_DOUBLE_QUOTE, "\n", "\r", "\t"]]):
        return ONE_DOUBLE_QUOTE + s.replace(ONE_DOUBLE_QUOTE, TWO_DOUBLE_QUOTES) + ONE_DOUBLE_QUOTE
    return s

def unquote_field(s):
    ONE_DOUBLE_QUOTE = '"'
    TWO_DOUBLE_QUOTES = ONE_DOUBLE_QUOTE * 2
    if not s:
        return ""
    if len(s) >= 2 and s[0] == ONE_DOUBLE_QUOTE and s[-1] == ONE_DOUBLE_QUOTE:
        return s[1:-1].replace(TWO_DOUBLE_QUOTES, ONE_DOUBLE_QUOTE)
    return s

def serialize_value(v):
    ONE_DOUBLE_QUOTE = '"'
    if json is not None:
        try:
            return json.dumps(v)
        except Exception:
            pass
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    s = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
    return ONE_DOUBLE_QUOTE + s + ONE_DOUBLE_QUOTE

def deserialize_value(s):
    if s is None or s == '':
        return ''
    if json is not None:
        try:
            return json.loads(s)
        except Exception:
            pass
    sl = s.strip()
    if sl == 'null':
        return None
    if sl == 'true':
        return True
    if sl == 'false':
        return False
    try:
        if '.' not in sl:
            return int(sl)
        return float(sl)
    except Exception:
        pass
    if len(sl) >= 2 and sl[0] == '"' and sl[-1] == '"':
        inner = sl[1:-1]
        inner = inner.replace('\\\\', '\\').replace('\\"', '"').replace('\\n', '\n').replace('\\r', '\r')
        return inner
    return sl


def read_lines(path):
    try:
        file = open(path, "r")
    except (OSError, FileNotFoundError):
        return []
    lines = []
    try:
        for line in file:
            if line.endswith('\n'):
                line = line[:-1]
            lines.append(line)
    finally:
        file.close()
