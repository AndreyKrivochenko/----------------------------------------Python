import json

from common import MAIN_MENU
from framework import Template
from framework.decorators import Debug
from logging_mod import Logger
from model_site import TrainingSite
from patterns.decorators import AppRoutes

site = TrainingSite()
routes: dict = {}

create_logger = Logger('create_log')
update_logger = Logger('update_log')


class AllPages(Template):
    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'main_menu': MAIN_MENU
        })
        return self.context


@AppRoutes(routes=routes, urls=['/'])
@Debug
class IndexPage(AllPages):
    template = 'index.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'Index page'
        })
        return self.context


@AppRoutes(routes=routes, urls=[
    '/courses/',
    '/courses/<slug:category>/',
    '/courses/<slug:category>/<slug:course>/',
    '/courses/<slug:category>/<slug:course>/edit/'
])
@Debug
class CoursesPage(AllPages):
    template = 'courses.html'

    def get_context(self, request):
        super().get_context(request)
        category = None
        for cat in site.categories_courses:
            if cat.name == request.request.get('category'):
                category = cat
        courses_list = [item for item in site.courses if item.category_id == category.category_id] if category else []
        self.context.update({
            'title': 'Courses page',
            'categories_courses': site.categories_courses,
            'courses': courses_list
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
                if course == course_.__str__():
                    course = course_
            new_data = {}
            for item in request.request['POST']:
                if item.startswith('new_'):
                    new_data[item] = request.request['POST'].get(item)
            if site.check_input_course_url(**new_data):
                site.update_course(course, **new_data)
                update_logger.log(f'Update course {course.name}')


@AppRoutes(routes=routes, urls=['/courses/new/'])
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
        site.create_course(data['type'], int(data['category']), data['name'], data['new_text'])
        create_logger.log(f'Create course {data["name"]}')
        self.template = 'new_course_final.html'


@AppRoutes(routes=routes, urls=['/courses/copy/'])
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


@AppRoutes(routes=routes, urls=['/about/'])
@Debug
class AboutPage(AllPages):
    template = 'about.html'

    def get_context(self, request):
        super().get_context(request)
        self.context.update({
            'title': 'About page'
        })
        return self.context


@AppRoutes(routes=routes, urls=['/contact/'])
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


@AppRoutes(routes=routes, urls=['/students/', '/students/<slug:student>/'])
@Debug
class StudentsPage(AllPages):
    template = 'students.html'

    def get_context(self, request):
        super().get_context(request)
        student_name = request.request.get('student')
        student = None
        if student_name:
            for student_ in site.students:
                if student_name == student_.name:
                    student = student_
        courses_list = []
        if student:
            courses_list = site.get_all_courses_of_student(student)
        self.context.update({
            'title': 'Students page',
            'students': site.students,
            'courses_of_student': courses_list,
            'courses': site.courses,
            'categories': site.categories_courses
        })
        return self.context

    def post(self, request):
        super().post(request)
        data = request.request.get('POST')
        course_id = int(data.get('save_to_course'))
        student_name = data.get('student')
        course = None
        student = None
        if course_id and student_name:
            for course_ in site.courses:
                if course_id == course_.course_id:
                    course = course_
            for student_ in site.students:
                if student_name == student_.name:
                    student = student_
            site.add_student_course(student, course)


@AppRoutes(routes=routes, urls=['/students/new/'])
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
        if site.check_input_user(username=data['name'], email=data['email'], phone=data['phone']):
            site.create_user('student', data['name'], data['email'], data['phone'])
            create_logger.log(f'Create student {data["name"]}')
        self.template = 'new_course_final.html'


@AppRoutes(routes=routes, urls=['/api/courses/'])
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
