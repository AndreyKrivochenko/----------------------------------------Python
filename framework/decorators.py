import abc
import time

from framework.page_controllers import AbstractTemplate


class AbstractTemplateDecorator(AbstractTemplate, metaclass=abc.ABCMeta):
    _cls: AbstractTemplate = None

    def __init__(self, cls: AbstractTemplate):
        self._cls = cls

    @property
    def cls(self):
        return self._cls

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        return self._cls.__call__(*args, **kwargs)


class GetTime(AbstractTemplateDecorator):

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self._cls.__call__(*args, **kwargs)
        end_time = time.time()
        delta = (end_time - start_time) * 1000
        print(f'Длительность работы класса {self._cls.__class__.__name__} равна {delta:2.2f} мс.')
        return result
