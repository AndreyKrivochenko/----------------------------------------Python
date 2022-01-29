import json
from common import MAIN_MENU
from framework import Template
from models import TrainingSite, Course

with open('site_db.json', 'r', encoding='utf-8') as f:
    site = TrainingSite(json.load(f))


class AllPages(Template):
    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'main_menu': MAIN_MENU
        })
        return self.context


class IndexPage(AllPages):
    template = 'index.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Index page'
        })
        return self.context


class CoursesPage(AllPages):
    template = 'courses.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Courses page',
            'categories_courses': site.categories_courses,
            'courses': site.courses
        })
        return self.context

    def post(self, request):
        super().post(request)
        new_category = request.request.get('POST').get('new-category')
        if new_category:
            site.create_category(new_category)
        course = request.request['POST'].get('course')
        if course:
            for course_ in site.courses:
                if course == str(course_):
                    course = course_



class AboutPage(AllPages):
    template = 'about.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'About page'
        })
        return self.context


class ContactPage(AllPages):

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Contact page'
        })
        return self.context

    def get(self, request):
        self.template = 'contact.html'

    def post(self, request):
        self.template = 'contact_final.html'
