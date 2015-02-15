import logging
import sys
import time


def next(iter):
    try:
        return iter.next()
    except StopIteration:
        return None


progress = True

def progress_iter(fmt, iter):
    count = 0
    t0 = 0
    for count, item in enumerate(iter, start=1):
        if progress:
            t1 = time.time()
            if t1 - t0 > 1:
                sys.stderr.write(('\r' + fmt) % count)
                t0 = t1
        yield item
    if progress:
        sys.stderr.write(('\r' + fmt + '\n') % count)


class IOLogger(object):
    def __init__(self, logger, reader, writer=None, prefix=''):
        self._reader = reader
        self._writer = writer or reader
        self._logger = logger
        self._prefix = (prefix + ' ') if prefix else ''

    def read(self, length=0, level=logging.INFO):
        ret = self._reader.read(length)
        self._logger.log(level, LazyString(lambda: '%s<= %s'
                                           % (self._prefix, repr(ret))))
        return ret

    def readline(self, level=logging.INFO):
        ret = self._reader.readline()
        self._logger.log(level, LazyString(lambda: '%s<= %s'
                                           % (self._prefix, repr(ret))))
        return ret

    def write(self, data, level=logging.INFO):
        self._logger.log(level, LazyString(lambda: '%s=> %s'
                                           % (self._prefix, repr(data))))
        return self._writer.write(data)

    def flush(self):
        self._writer.flush()

    def __iter__(self):
        while True:
            l = self.readline()
            if not l:
                break
            yield l


class LazyString(object):
    def __init__(self, obj):
        self._obj = obj

    def __str__(self):
        if callable(self._obj):
            return self._obj()
        return self._obj

    def __len__(self):
        return len(str(self))


def one(l):
    l = list(l)
    if l:
        assert len(l) == 1
        return l[0]
    return None
