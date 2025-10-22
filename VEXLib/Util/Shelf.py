try:
    import ujson as json
except Exception:
    try:
        import json
    except Exception:
        json = None

try:
    import _thread
except Exception:
    _thread = None


def _quote_field(s):
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    if any([bad_char in s for bad_char in [",", '"', "\n", "\r", "\t"]]):
        return '"' + s.replace('"', '""') + '"'
    return s


def _unquote_field(s):
    if not s:
        return ""
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1].replace('""', '"')
    return s


def _serialize_value(v):
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
    s = (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return '"' + s + '"'


def _deserialize_value(s: str):
    if s is None or s == "":
        return ""
    if json is not None:
        try:
            return json.loads(s)
        except Exception:
            pass
    sl = s.strip()
    if sl == "null":
        return None
    if sl == "true":
        return True
    if sl == "false":
        return False
    try:
        if "." not in sl:
            return int(sl)
        return float(sl)
    except Exception:
        pass
    if len(sl) >= 2 and sl[0] == '"' and sl[-1] == '"':
        inner = sl[1:-1]
        inner = (
            inner.replace("\\\\", "\\")
            .replace('\\"', '"')
            .replace("\\n", "\n")
            .replace("\\r", "\r")
        )
        return inner
    return sl


def _read_lines(path):
    try:
        f = open(path, "r")
    except Exception:
        return []
    lines = []
    try:
        for ln in f:
            if ln.endswith("\n"):
                ln = ln[:-1]
            lines.append(ln)
    finally:
        try:
            f.close()
        except Exception:
            pass
    return lines


def _write_file(path, contents):
    f = open(path, "w")
    try:
        for ln in contents:
            f.write(ln + "\n")
        f.flush()
    finally:
        try:
            f.close()
        except Exception:
            pass


def _parse_csv_line(line):
    fields = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == '"':
            i += 1
            buf = []
            while i < n:
                ch = line[i]
                if ch == '"':
                    ni = i + 1
                    if ni < n and line[ni] == '"':
                        buf.append('"')
                        i = ni + 1
                        continue
                    else:
                        i += 1
                        break
                else:
                    buf.append(ch)
                    i += 1
            fields.append("".join(buf))
            if i < n and line[i] == ",":
                i += 1
        else:
            j = i
            while j < n and line[j] != ",":
                j += 1
            fields.append(line[i:j])
            i = j + 1 if j < n else j
    if len(fields) == 0:
        return "", ""
    if len(fields) == 1:
        return fields[0], ""
    return fields[0], fields[1]


class Shelf(object):
    def __init__(self, path, create=True):
        self.path = path
        if _thread is not None:
            try:
                self._lock = _thread.allocate_lock()
            except Exception:
                self._lock = None
        else:
            self._lock = None
        if self._lock is None:

            class _DummyLock(object):
                def acquire(self, *a, **k):
                    return True

                def release(self, *a, **k):
                    return True

            self._lock = _DummyLock()
        if create:
            try:
                f = open(self.path, "r")
                f.close()
            except Exception:
                try:
                    f = open(self.path, "w")
                    f.close()
                except Exception:
                    pass

    def _read_dict(self):
        d = {}
        lines = _read_lines(self.path)
        for ln in lines:
            if not ln:
                continue
            k, v = _parse_csv_line(ln)
            d[_unquote_field(k)] = _unquote_field(v)
        return d

    def _write_dict(self, d):
        contents = []
        keys = list(d.keys())
        try:
            keys.sort()
        except Exception:
            pass
        for k in keys:
            kval = _quote_field(k)
            vfield = _quote_field(d[k])
            contents.append(kval + "," + vfield)
        _write_file(self.path, contents)

    def set(self, key, value):
        self._lock.acquire()
        try:
            d = self._read_dict()
            d[key] = _serialize_value(value)
            self._write_dict(d)
        finally:
            self._lock.release()

    def get(self, key, default=None):
        self._lock.acquire()
        try:
            d = self._read_dict()
            if key not in d:
                return default
            return _deserialize_value(d[key])
        finally:
            self._lock.release()

    def delete(self, key):
        self._lock.acquire()
        try:
            d = self._read_dict()
            if key in d:
                del d[key]
                self._write_dict(d)
                return True
            return False
        finally:
            self._lock.release()

    def keys(self):
        self._lock.acquire()
        try:
            return list(self._read_dict().keys())
        finally:
            self._lock.release()

    def items(self):
        self._lock.acquire()
        try:
            d = self._read_dict()
            return [(k, _deserialize_value(d[k])) for k in d]
        finally:
            self._lock.release()
