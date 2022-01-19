from framework.page_controllers import Template


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
