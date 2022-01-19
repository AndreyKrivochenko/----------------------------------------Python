class FrontController:
    data = {}

    def __call__(self, request):
        for key in self.data:
            request[key] = self.data[key]
