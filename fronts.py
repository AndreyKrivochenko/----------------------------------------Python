from framework.front_controllers import FrontController


class SecretFront(FrontController):
    data = {
        'secret': 'some secret'
    }

class OtherFront(FrontController):
    data = {
        'key': 'value'
    }
