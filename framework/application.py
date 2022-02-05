from .request import Request
from .page_controllers import NotFoundPage


class Application:
    def __init__(self, routes, fronts):
        self.routes: dict = routes
        self.fronts = fronts
        self.path = None

    def path_processing(self, path: str, request: Request):
        def search_rout(rout_list, path_list):
            if rout_list and path_list:
                if (rout_list[0] == path_list[0] or rout_list[0].startswith('<')) and len(rout_list) == len(path_list):
                    return f'{rout_list[0]}/{search_rout(rout_list[1:], path_list[1:])}'
                else:
                    return False
            else:
                return ''
        if path == '/':
            self.path = path
            return self.path

        def add_slug_to_request(path, route):
            path = path.strip('/').split('/')
            route = route.strip('/').split('/')
            for i, value in enumerate(route):
                if value.startswith('<slug'):
                    _value = value.lstrip('<').rstrip('>').split(':')
                    request.request[_value[1]] = path[i].replace('_', ' ')

        _path_list = path.strip('/').split('/')
        _routes = [key.strip('/').split('/') for key, value in self.routes.items()]
        _path = ''
        result_list = []
        for rout in _routes:
            if search_rout(rout, _path_list) and not search_rout(rout, _path_list).endswith('False'):
                result_list.append(f'/{search_rout(rout, _path_list)}')
        if len(result_list) > 1:
            _path = path
        else:
            _path = result_list[0]
        add_slug_to_request(path, _path)
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
