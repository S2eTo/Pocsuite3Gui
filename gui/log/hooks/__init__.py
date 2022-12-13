from logging import LogRecord


class Hook(object):

    def hook(self, record: LogRecord):
        raise NotImplementedError
