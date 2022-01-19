from framework.templator import render


class Template:
    template = ''
    context = {}

    def __call__(self, request):
        return '200 OK', bytes(render(self.template, secret=request['secret'], key=request['key'], context=self.context),
            encoding='utf-8')


class NotFoundPage:
    def __call__(self, request):
        return '404 Not Found', b'404 page not found'
