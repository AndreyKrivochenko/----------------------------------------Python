from typing import List

from models import CategoryCourse, Course, User, UserFactory, CourseFactory
from patterns.data_mapper import SqliteStudentMapper, SqliteCourseMapper, SqliteStudentCourseMapper, \
    SqliteCategoryMapper
from patterns.observer import SmsNotifier, EmailNotifier


class TrainingSite:
    def __init__(self):
        self.student_mapper = SqliteStudentMapper()
        self.course_mapper = SqliteCourseMapper()
        self.sc_mapper = SqliteStudentCourseMapper()
        self.cat_mapper = SqliteCategoryMapper()
        self.students: List[User] = self.student_mapper.get_all()
        self.courses: List[Course] = self.course_mapper.get_all()
        self.categories_courses: List[CategoryCourse] = self.cat_mapper.get_all()

    def create_user(self, type_, name, email, phone):
        user = UserFactory.create(type_, name, email, phone)
        if type_ == 'student':
            self.student_mapper.insert(user)
            self.students.append(self.student_mapper.find_by_name(user.name))

    def update_user(self, user: User):
        pass

    def create_course(self, type_, category, name, description, **kwargs):
        course = CourseFactory.create(type_, category, name, description, **kwargs)
        self.course_mapper.insert(course)
        course = self.course_mapper.find_by_name(course.name)
        course.attach(SmsNotifier())
        course.attach(EmailNotifier())
        self.courses.append(course)

    def update_course(self, course: Course, **kwargs):
        course.name = kwargs.get('new_name')
        course.description = kwargs.get('new_text')
        course.url = kwargs.get('new_url')
        course.address = kwargs.get('new_address')
        self.course_mapper.update(course)
        course.notify()

    def clone_course(self, course: Course):
        new_course = course.clone()
        new_course.name = f'{new_course.name} Clone'
        self.course_mapper.insert(new_course)
        self.courses.append(self.course_mapper.find_by_name(new_course.name))

    def create_category(self, name):
        category = CategoryCourse(name)
        self.cat_mapper.insert(category)
        self.categories_courses.append(self.cat_mapper.find_by_name(category.name))

    def add_student_course(self, student: User, course: Course):
        self.sc_mapper.add_student_course(student, course)

    def get_all_courses_of_student(self, student: User):
        return self.sc_mapper.find_all_courses_of_student(student)
