from templator import render


class Template:
    template = ''
    context = {}

    def __call__(self, request):
        return '200 OK', bytes(render(self.template, secret=request['secret'], context=self.context), encoding='utf-8')


class IndexPage(Template):
    template = 'templates/index.html'
    context = {
        'title': 'Index page'
    }


class AboutPage(Template):
    template = 'templates/about.html'
    context = {
        'title': 'About page'
    }


class NotFoundPage:
    def __call__(self, request):
        print(request)
        return '404 Not Found', b'404 page not found'
