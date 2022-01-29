import json
from common import MAIN_MENU
from framework import Template
from models import TrainingSite

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
        with open('courses.json', 'r', encoding='utf-8') as f:
            courses = json.load(f)
        # print(site.categories_courses)
        self.context.update({
            'title': 'Courses page',
            # 'categories_courses': site.categories_courses
            'courses': courses
        })
        return self.context

    def post(self, request):
        super().post(request)
        new_category = request.request.get('POST').get('new-category')
        new_course = request.request.get('POST').get('new-course')
        if new_category:
            with open('courses.json', 'r', encoding='utf-8') as f:
                courses = json.load(f)
            if not courses.get(new_category):
                courses[new_category] = {}
                with open('courses.json', 'w', encoding='utf-8') as f:
                    json.dump(courses, f, indent=4)
        if new_course:
            with open('courses.json', 'r', encoding='utf-8') as f:
                courses = json.load(f)
            if not courses[request.request.get('course')].get(new_course):
                courses[request.request.get('course')][new_course] = {}
                with open('courses.json', 'w', encoding='utf-8') as f:
                    json.dump(courses, f, indent=4)


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
