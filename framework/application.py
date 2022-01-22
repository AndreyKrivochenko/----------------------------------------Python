from .request import Request
from .page_controllers import NotFoundPage


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if len(path) > 1 and path[-1] == '/':
            path = path[:-1]
        if path in self.routes:
            controller = self.routes[path]
        else:
            controller = NotFoundPage()
        req = Request(environ)
        for front in self.fronts:
            front(req.request)
        code, body = controller(req)
        start_response(code, [('Content-Type', 'text/html')])
        return [body]
