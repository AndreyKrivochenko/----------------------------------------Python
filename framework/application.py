from .request import Request
from .page_controllers import NotFoundPage


class Application:
    def __init__(self, routes, fronts):
        self.routes: dict = routes
        self.fronts = fronts
        self.path = None

    def path_processing(self, path: str, request: Request):
        if len(path) > 1 and path[-1] != '/':
            path = f'{path}/'
        path = path.strip('/').split('/')
        _path = '/'
        if len(path) > 1:
            _routes = [key.strip('/').split('/') for key, value in self.routes.items()]
            for item in _routes:
                if len(item) == 1:
                    continue
                if len(item) == len(path):
                    for i, value in enumerate(item):
                        if value == path[i]:
                            _path = f'{_path}{value}/'
                        elif value.find('slug') and path[i].replace('_', '').isalpha():
                            _path = f'{_path}{value}/'
                            _value = value.lstrip('<').rstrip('>').split(':')
                            request.request[_value[1]] = path[i].replace('_', ' ')
        elif len(path[0]) > 1:
            _path = f'/{path[0]}/'
        else:
            _path = '/'
        self.path = _path
        return self.path

    def __call__(self, environ, start_response):
        req = Request(environ)
        path = environ['PATH_INFO']
        self.path_processing(path, req)
        if self.path in self.routes:
            controller = self.routes[self.path]
        else:
            controller = NotFoundPage()
        for front in self.fronts:
            front(req.request)
        code, body = controller(req)
        start_response(code, [('Content-Type', 'text/html')])
        return [body]
