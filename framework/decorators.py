import abc
import time

from framework.page_controllers import AbstractTemplate


class AbstractTemplateDecorator(AbstractTemplate, metaclass=abc.ABCMeta):
    def __init__(self, cls: AbstractTemplate):
        self._cls = cls

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Route:
    def __init__(self, route):
        print(route)
        self._route = route

    def __call__(self, cls):

        class RoutedClass(AbstractTemplateDecorator):

            def __call__(self, *args, **kwargs):
                return self._cls(*args, **kwargs)

        return RoutedClass


# class Debug(AbstractTemplateDecorator):
#     def __call__(self, *args, **kwargs):
#         start_time = time.time()
#         result = self._cls(*args, **kwargs)
#         end_time = time.time()
#         delta = (end_time - start_time) * 1000
#         print(f'Класс {self._cls.__name__} отработал за {delta} мс.')
#         return result
