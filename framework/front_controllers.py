class SecretFront:
    data = {
        'secret': 'some secret'
    }

    def __call__(self, request):
        for key in self.data:
            request[key] = self.data[key]


class OtherFront:
    data = {
        'key': 'value'
    }

    def __call__(self, request):
        for key in self.data:
            request[key] = self.data[key]
