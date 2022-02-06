import json
import pickle
import os.path

from common import MAIN_MENU
from framework import Template
from framework.decorators import Debug
from logging_mod import Logger
from models import TrainingSite

db = 'site_db.pkl'

if not os.path.exists(db) or os.stat(db).st_size == 0:
    site = TrainingSite()
else:
    with open('site_db.pkl', 'rb') as f:
        site = TrainingSite(file=pickle.load(f))

create_logger = Logger('create_log')
update_logger = Logger('update_log')


class AllPages(Template):
    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'main_menu': MAIN_MENU
        })
        return self.context


@Debug
class IndexPage(AllPages):
    template = 'index.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Index page'
        })
        return self.context


@Debug
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


@Debug
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


@Debug
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
        super().post(request)
        course = request.request['POST'].get('course')
        if course:
            for course_ in site.courses:
                if course == str(course_):
                    course = course_
        site.clone_course(course)


@Debug
class AboutPage(AllPages):
    template = 'about.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'About page'
        })
        return self.context


@Debug
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


@Debug
class StudentsPage(AllPages):
    template = 'students.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Students page',
            'students': site.students,
            'courses': site.courses
        })
        return self.context

    def post(self, request):
        super().post(request)
        data = request.request.get('POST')
        course = data.get('save_to_course')
        student = data.get('student')
        if course and student:
            for course_ in site.courses:
                if course == str(course_):
                    course = course_
            for student_ in site.students:
                if student == student_.name:
                    student = student_
            site.update_course(course, student=student)
            site.update_user(student, course=course)


@Debug
class CreateStudentPage(AllPages):

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Create student page'
        })
        return self.context

    def get(self, request):
        self.template = 'create_student.html'

    def post(self, request):
        super().post(request)
        data = request.request.get('POST')
        site.create_user('student', data['name'], data['email'], data['phone'])
        create_logger.log(f'Create student {data["name"]}')
        self.template = 'new_course_final.html'


class CoursesApi(AllPages):
    def get_json_file(self, request):
        result = []
        for course in site.courses:
            data = {}
            for key, value in course.__dict__.items():
                if key != '_observers':
                    if key == 'students':
                        data[key] = [str(i) for i in value]
                    else:
                        data[key] = value
            result.append(data)

        self.json_file = bytes(json.dumps(result, indent=4), 'utf-8')
