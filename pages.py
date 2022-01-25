from framework import Template


class IndexPage(Template):
    template = 'index.html'

    def get_context(self):
        super(IndexPage, self).get_context()
        self.context.update([('title', 'Index page')])
        return self.context


class AboutPage(Template):
    template = 'about.html'

    def get_context(self):
        self.context.update({'title': 'About page'})
        return self.context


class ContactPage(Template):
    template = 'contact.html'

    def get_context(self):
        self.context.update({'title': 'Contact page'})
        return self.context

    def post(self, request):
        form_post = super().post(request)
        print(f'Ваше сообщение:\nТема: {form_post["subject"]}\ne-mail: {form_post["email"]}\nСообщение:'
              f' {form_post["message"]}')
