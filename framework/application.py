from framework.page_controllers import NotFoundPage

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
        request = {}
        for front in self.fronts:
            front(request)
        code, body = controller(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body]
