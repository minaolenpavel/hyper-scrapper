import datetime
import os

class LogManager:
    def __init__(self, filename:str, program_name:str, encoding="utf-8"):
        self.filename = filename
        self.encoding = encoding
        self.program_name = program_name
        self.start_time = None
        if not os.path.exists(self.filename):
            open(self.filename, "x", encoding=self.encoding)

    def finish_logs(self):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"{self.program_name} STOPPED {datetime.datetime.now()}\n")
            logs.write(f"{self.program_name} TOOK {datetime.datetime.now()-self.start_time} TO EXECUTE")

    def start_logs(self):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"{self.program_name} STARTED {datetime.datetime.now()}\n")
        self.start_time = datetime.datetime.now()

    def write(self, error: str, message: str):
        with open(self.filename, "a", encoding=self.encoding) as logs:
            logs.write(f"{datetime.datetime.now()} ; {error} ; {message}\n")