from patterns import FileLoggerHandler, ConsoleLoggerHandler
from reusepatterns.singltones import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name
        self.file_log = FileLoggerHandler()
        self.console_log = ConsoleLoggerHandler()
        self.file_log.set_next(self.console_log)

    def log(self, text):
        self.file_log.handle(request={'name': self.name, 'text': text})
