import logging


class LogFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.excluded = []
        self.included = []

    def clear(self):
        self.excluded.clear()
        self.included.clear()

    def include(self, logger_name):
        self.included.append(logger_name)

    def exclude(self, logger_name):
        self.excluded.append(logger_name)

    def filter(self, record):
        if record.name in self.excluded:
            return False

        if self.included and record.name not in self.included:
            return False

        return True

