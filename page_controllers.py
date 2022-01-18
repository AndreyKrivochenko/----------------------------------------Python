class IndexPage:
    def __call__(self, request):
        print(request)
        return '200 OK', b'<h1>Hello from WSGI!</h1>'


class AboutPage:
    def __call__(self, request):
        print(request)
        return '200 OK', b'About page'


class NotFoundPage:
    def __call__(self, request):
        print(request)
        return '404 Not Found', b'404 page not found'
