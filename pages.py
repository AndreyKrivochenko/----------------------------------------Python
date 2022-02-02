import json

from common import MAIN_MENU
from framework import Template
from logging_mod import Logger
from models import TrainingSite

with open('site_db.json', 'r', encoding='utf-8') as f:
    site = TrainingSite(json.load(f))

create_logger = Logger('create_log')
update_logger = Logger('update_log')


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
            create_logger.log(f'Created category {new_category}')
        course = request.request['POST'].get('course')
        if course:
            for course_ in site.courses:
                if course == str(course_):
                    course = course_
            new_data = {}
            for item in request.request['POST']:
                if item.startswith('new_'):
                    new_data[item] = request.request['POST'].get(item)
            site.update_course(course, **new_data)
            update_logger.log(f'Update course {course.name}')


class NewCoursePage(AllPages):

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'New course',
            'categories': site.categories_courses
        })
        return self.context

    def get(self, request):
        self.template = 'new_course.html'

    def post(self, request):
        super().post(request)
        data = request.request.get('POST')
        site.create_course(data['type'], data['category'], data['name'], data['new_text'])
        create_logger.log(f'Create course {data["name"]}')
        self.template = 'new_course_final.html'


class CopyCoursesPage(AllPages):
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
        super(CopyCoursesPage, self).post(request)
        course = request.request['POST'].get('course')
        if course:
            for course_ in site.courses:
                if course == str(course_):
                    course = course_
        site.clone_course(course)


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