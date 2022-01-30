from reusepatterns.singltones import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        with open(f'log/{self.name}.txt', 'a', encoding='utf-8') as f:
            f.write(f'log[{self.name}]---> {text}\n')
