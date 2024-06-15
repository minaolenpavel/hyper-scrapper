import datetime
import os

class LogManager:
    def __init__(self, filename:str, encoding="utf-8"):
        self.filename = filename
        self.encoding = encoding
        if not os.path.exists(self.filename):
            open(self.filename, "x", encoding=self.encoding)

    def finish_logs(self):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"SCHEDULE SCRAPPER STOPPED {datetime.datetime.now()}\n")

    def start_logs(self):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"SCHEDULE SCRAPPER STARTED {datetime.datetime.now()}\n")

    def write(self, error: str, message: str):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"{datetime.datetime.now()} ; {error} ; {message}\n")