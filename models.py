import json

from reusepatterns.prototypes import PrototypeMixin


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class SimpleFactory:
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Course(PrototypeMixin):
    def __init__(self, category, name, description):
        self.category = category
        self.name = name
        self.description = description


class InteractiveCourse(Course):
    def __init__(self, category, name, description, **kwargs):
        Course.__init__(self, category, name, description)
        self.url = kwargs.get('url') or ''
        self.type = 'interactive'

    def update_course(self, new_name, new_description, new_url):
        self.name = new_name
        self.description = new_description
        self.url = new_url
        return self


class RecordCourse(Course):
    def __init__(self, category, name, description, **kwargs):
        Course.__init__(self, category, name, description)
        self.address = kwargs.get('address') or ''
        self.type = 'record'

    def update_course(self, new_name, new_description, new_address):
        self.name = new_name
        self.description = new_description
        self.address = new_address
        return self


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, category, name, description, **kwargs):
        return cls.types[type_](category, name, description, **kwargs)


class TrainingSite:
    def __init__(self, file: dict):
        self.teachers = file.get('teachers')
        self.students = file.get('students')
        self.courses = []
        self.categories_courses: list = file.get('categories_courses')
        self.__get_courses_from_file(file.get('courses'))

    def __get_courses_from_file(self, courses: list):
        for course in courses:
            self.create_course(
                course.get('type'),
                course.get('category'),
                course.get('name'),
                course.get('description'),
                **{'url': course.get('url'), 'address': course.get('address')}
            )
        return None

    def __save_site(self):
        site_ = {
            'teachers': self.teachers,
            'students': self.students,
            'courses': [item.__dict__ for item in self.courses],
            'categories_courses': self.categories_courses
        }
        with open('site_db.json', 'w', encoding='utf-8') as f:
            json.dump(site_, f, indent=4)
        return None

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_course(self, type_, category, name, description, **kwargs):
        course = CourseFactory.create(type_, category, name, description, **kwargs)
        self.courses.append(course)
        self.__save_site()
        return None

    def update_course(self, course: Course, **kwargs):
        if isinstance(course, InteractiveCourse):
            course.update_course(kwargs.get('new_name'), kwargs.get('new_text'), kwargs.get('new_url'))
        elif isinstance(course, RecordCourse):
            course.update_course(kwargs.get('new_name'), kwargs.get('new_text'), kwargs.get('new_address'))
        self.__save_site()
        return None

    def create_category(self, name):
        if name and name not in self.categories_courses:
            self.categories_courses.append(name)
            self.__save_site()
        return None
