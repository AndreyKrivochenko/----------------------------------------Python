class AppRoutes:
    def __init__(self, routes: dict, urls: list[str]):
        self.routes = routes
        self.urls = urls

    def __call__(self, cls):
        for url in self.urls:
            self.routes[url] = cls()
