from typing import List

from patterns import SqliteStudentMapper, SqliteCourseMapper, SqliteStudentCourseMapper, SqliteCategoryMapper, \
    SmsNotifier, EmailNotifier
from models import CategoryCourse, Course, User, UserFactory, CourseFactory


class TrainingSite:
    def __init__(self, connection):
        self.student_mapper = SqliteStudentMapper(connection)
        self.course_mapper = SqliteCourseMapper(connection)
        self.sc_mapper = SqliteStudentCourseMapper(connection)
        self.cat_mapper = SqliteCategoryMapper(connection)
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
        course.update_course(**kwargs)
        return None

    def clone_course(self, course: Course):
        new_course = course.clone()
        new_course.name = f'{new_course.name} Clone'
        self.course_mapper.insert(new_course)
        self.courses.append(self.course_mapper.find_by_name(new_course.name))

    def create_category(self, name):
        category = CategoryCourse(name)
        self.cat_mapper.insert(category)
        self.categories_courses.append(self.cat_mapper.find_by_name(category.name))
