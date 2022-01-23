from .templator import render


class Template:
    template = ''
    context = {}

    def post(self, request):
        if request.request.get('POST'):
            self.context.update(request.request.get('POST'))
            return self.context

    def get(self, request):
        if request.request.get('GET'):
            self.context.update(request.request.get('GET'))
            return self.context

    def get_context(self):
        return self.context

    def __call__(self, request, **kwargs):
        if request.method == 'POST':
            self.post(request)
        elif request.method == 'GET':
            self.get(request)
        self.get_context()
        return '200 OK', bytes(
            render(self.template, secret=request.request['secret'], key=request.request['key'], context=self.context),
            encoding='utf-8'
        )


class NotFoundPage:
    def __call__(self, request):
        return '404 Not Found', b'404 page not found'
