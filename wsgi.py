from urls import routes
from page_controllers import NotFoundPage
from front_controllers import secret_front, other_front


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
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


app_object = Application(routes, [secret_front, other_front])
