class Request:

    def __init__(self, env, request=None):
        if request is None:
            request = {}
        self.env = env
        self.method = self.env.get('REQUEST_METHOD')
        self.request = request
        self.fill_request()

    def fill_request(self):
        if self.method == 'GET':
            query_string = self.env.get('QUERY_STRING')
            if query_string:
                self.parse_input_data(query_string, self.method)
        elif self.method == 'POST':
            content_length_data = self.env.get('CONTENT_LENGTH')
            content_length = int(content_length_data) if content_length_data else 0
            data = self.env['wsgi.input'].read(content_length) if content_length > 0 else b''
            if data:
                data_str = data.decode(encoding='utf-8')
                self.parse_input_data(data_str, self.method)
        else:
            print(f'Мы обрабатываем только GET и POST запросы, ваш запрос - {self.method}')

    def parse_input_data(self, data: str, request_type: str):
        if data:
            params = data.split('&')
            self.request[request_type] = {}
            for item in params:
                k, v = item.split('=')
                self.request[request_type][k] = v
