import datetime
from abc import ABC, abstractmethod
from typing import Any


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class FileLoggerHandler(AbstractHandler):
    def handle(self, request: Any):
        with open(f'log/{request["name"]}.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.datetime.now()} | log[{request["name"]}]---> {request["text"]}\n')
        return super().handle(request)


class ConsoleLoggerHandler(AbstractHandler):
    def handle(self, request: Any):
        print(f'{datetime.datetime.now()} | log[{request["name"]}]---> {request["text"]}\n')
        return super().handle(request)
