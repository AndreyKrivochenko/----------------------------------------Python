import json
import pickle

from reusepatterns.prototypes import PrototypeMixin


class User:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

    def update_user(self, **kwargs):
        if kwargs.get('new_name'):
            self.name = kwargs.get('new_name')
        if kwargs.get('new_email'):
            self.email = kwargs.get('new_email')
        if kwargs.get('new_phone'):
            self.phone = kwargs.get('new_phone')
        return self


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name: str, email: str, phone: str):
        super().__init__(name, email, phone)
        self.courses = []

    def add_course(self, course: 'Course'):
        if course:
            self.courses.append(course)

    def update_user(self, **kwargs):
        super().update_user(**kwargs)
        if kwargs.get('course'):
            self.courses.append(kwargs.get('course'))
        return self


class SimpleFactory:
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name, email, phone):
        return cls.types[type_](name, email, phone)


class Course(PrototypeMixin):
    def __init__(self, category, name, description):
        self.category = category
        self.name = name
        self.description = description
        self.students = []

    def update_course(self, **kwargs):
        if kwargs.get('new_name'):
            self.name = kwargs.get('new_name')
        if kwargs.get('new_text'):
            self.description = kwargs.get('new_text')
        if kwargs.get('student'):
            self.students.append(kwargs.get('student'))
        return self


class InteractiveCourse(Course):
    def __init__(self, category, name, description, **kwargs):
        Course.__init__(self, category, name, description)
        self.url = kwargs.get('url') or ''
        self.type = 'interactive'

    def update_course(self, **kwargs):
        super(InteractiveCourse, self).update_course(**kwargs)
        self.url = kwargs.get('new_url')
        return self


class RecordCourse(Course):
    def __init__(self, category, name, description, **kwargs):
        Course.__init__(self, category, name, description)
        self.address = kwargs.get('address') or ''
        self.type = 'record'

    def update_course(self, **kwargs):
        super(RecordCourse, self).update_course(**kwargs)
        self.address = kwargs.get('new_address')
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
    def __init__(self, **kwargs):
        self.teachers: list = kwargs.get('file').get('teachers') if kwargs.get('file') else []
        self.students = kwargs.get('file').get('students') if kwargs.get('file') else []
        self.courses = kwargs.get('file').get('courses') if kwargs.get('file') else []
        self.categories_courses: list = kwargs.get('file').get('categories_courses') if kwargs.get('file') else []

    def __save_site(self):
        site_ = {
            'teachers': self.teachers,
            'students': self.students,
            'courses': self.courses,
            'categories_courses': self.categories_courses
        }
        with open('site_db.pkl', 'wb') as f:
            pickle.dump(site_, f, protocol=pickle.HIGHEST_PROTOCOL)
        return None

    def create_user(self, type_, name, email, phone):
        user = UserFactory.create(type_, name, email, phone)
        if type_ == 'student':
            self.students.append(user)
        elif type_ == 'teacher':
            self.teachers.append(user)
        self.__save_site()
        return None

    def update_user(self, user: User, **kwargs):
        user.update_user(**kwargs)
        self.__save_site()
        return None

    def create_course(self, type_, category, name, description, **kwargs):
        course = CourseFactory.create(type_, category, name, description, **kwargs)
        self.courses.append(course)
        self.__save_site()
        return None

    def update_course(self, course: Course, **kwargs):
        course.update_course(**kwargs)
        self.__save_site()
        return None

    def clone_course(self, course: Course):
        new_course = course.clone()
        new_course.name = f'{new_course.name} Clone'
        self.courses.append(new_course)
        self.__save_site()
        return None

    def create_category(self, name):
        if name and name not in self.categories_courses:
            self.categories_courses.append(name)
            self.__save_site()
        return None
