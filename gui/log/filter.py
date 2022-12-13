import time
from logging import Filter, LogRecord


class ExecuteFilter(Filter):

    def __init__(self):
        super().__init__()
        self.hooks = []

    def add_hook(self, hook):
        if not (hook in self.hooks):
            self.hooks.append(hook)

    def remove_hook(self, hook):
        if hook in self.hooks:
            self.hooks.remove(hook)

    def filter(self, record: LogRecord) -> bool:
        record.strftime = time.strftime('%H:%M:%S', time.localtime(record.created))

        for hook in self.hooks:
            if hasattr(hook, 'hook'):
                hook.hook(record)
            else:
                hook(record)

        return True
