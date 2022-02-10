import abc

from models import Course


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class SmsNotifier(Observer):
    def update(self, arg: Course):
        print(f'Sms notifier for {", ".join(arg)}, course "{arg.name}" changed')


class EmailNotifier(Observer):
    def update(self, arg: Course):
        print(f'Email notifier for {", ".join(arg)}, course "{arg.name}" changed')