import time
from abc import ABC

from framework.page_controllers import AbstractTemplate


class AbstractTemplateDecorator(AbstractTemplate, ABC):

    def __init__(self, cls: AbstractTemplate):
        self._cls = cls


class Debug(AbstractTemplateDecorator):

    def __call__(self):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = self._cls().__call__(*args, **kwargs)
            end_time = time.time()
            delta = (end_time - start_time) * 1000
            print(f'Длительность работы класса {self._cls.__name__} ({args[0].request.get("path")})'
                  f' равна {delta:2.2f} мс.')
            return result
        return wrapper
