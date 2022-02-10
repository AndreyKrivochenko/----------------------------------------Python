from patterns.iterator import StudentCourseIterator
from reusepatterns.prototypes import PrototypeMixin
from collections.abc import Iterable
from typing import Any, List


class User:
    def __init__(self, name: str, email: str, phone: str, user_id: int):
        self.name = name
        self.email = email
        self.phone = phone
        self.user_id = user_id

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
    def __init__(self, name: str, email: str, phone: str, user_id: int):
        super().__init__(name, email, phone, user_id)
        self.courses = []

    def add_course(self, course: 'Course'):
        if course:
            self.courses.append(course)

    def update_user(self, **kwargs):
        super().update_user(**kwargs)
        if kwargs.get('course'):
            self.courses.append(kwargs.get('course'))
        return self

    def __str__(self):
        return self.name


class SimpleFactory:
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name, email, phone, user_id=None):
        return cls.types[type_](name, email, phone, user_id)


class CategoryCourse:
    def __init__(self, name, category_id=None):
        self.name = name
        self.category_id = category_id

    def update(self):
        pass


class Course(PrototypeMixin, Iterable):
    def __init__(self, category_id: int, name: str, description: str, address: str, url: str, course_id: int):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.address = address
        self.url = url
        self.course_id = course_id
        self.students: List[Any] = []
        self._observers = set()

    def __iter__(self) -> StudentCourseIterator:
        return StudentCourseIterator(self.students)

    def update_course(self, **kwargs):
        if kwargs.get('new_name'):
            self.name = kwargs.get('new_name')
        if kwargs.get('new_text'):
            self.description = kwargs.get('new_text')
        if kwargs.get('student'):
            self.students.append(kwargs.get('student'))
        self._notify()
        return self

    def attach(self, observer: User) -> None:
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer: User) -> None:
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self)


class InteractiveCourse(Course):
    def __init__(self, category_id, name, description, address: str, url: str, course_id: int):
        Course.__init__(self, category_id, name, description, address, url, course_id)
        self.type = 'interactive'

    def update_course(self, **kwargs):
        super(InteractiveCourse, self).update_course(**kwargs)
        self.url = kwargs.get('new_url')
        return self


class RecordCourse(Course):
    def __init__(self, category_id, name, description, address: str, url: str, course_id: int):
        Course.__init__(self, category_id, name, description, address, url, course_id)
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
    def create(cls, type_, category_id, name, description, address=None, url=None, course_id=None):
        return cls.types[type_](category_id, name, description, address, url, course_id)
