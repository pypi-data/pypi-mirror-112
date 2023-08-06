from datetime import datetime
from threading import Lock
import tzlocal
import logging.config


class IsoFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        if fmt is None:
            fmt = "%(asctime)-6s: %(count)2s - %(name)s - %(levelname)s - "\
                  "%(thread)d:%(threadName)s - %(module)s:%(filename)s:%(lineno)s:%(funcName)s - "\
                  "%(message)s"
        super(IsoFormatter, self).__init__(fmt, datefmt)
        self.lock = Lock()
        self.count = 0
        self.max_count = 99

    def get_count(self):
        with self.lock:
            self.count += 1
            if self.count > self.max_count:
                self.count = 1
            return self.count

    def formatTime(self, record, date_fmt=None):
        value = datetime.fromtimestamp(record.created, tzlocal.get_localzone())
        base_date = datetime.strftime(value, "%Y-%m-%dT%H:%M:%S")
        base_date += "." + str(int(record.msecs)).zfill(3)
        base_date += datetime.strftime(value, "%z")
        return base_date

    def format(self, record):
        if not hasattr(record, "count"):
            record.count = str(self.get_count()).zfill(2)
        return super(IsoFormatter, self).format(record)
