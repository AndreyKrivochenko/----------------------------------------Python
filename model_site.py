from typing import List

from models import CategoryCourse, Course, User, UserFactory, CourseFactory, Student
from patterns.data_mapper import SqliteStudentMapper, SqliteCourseMapper, SqliteStudentCourseMapper, \
    SqliteCategoryMapper
from patterns.observer import SmsNotifier, EmailNotifier
from patterns.unit_of_work import UnitOfWork


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
        try:
            UnitOfWork.new_current()
            user = UserFactory.create(type_, name, email, phone)
            user.mark_new()
            UnitOfWork.get_current().commit()
            if type_ == 'student':
                self.students.append(self.student_mapper.find_by_name(user.name))
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    def update_user(self, user: User):
        pass

    def create_course(self, type_, category, name, description, **kwargs):
        try:
            UnitOfWork.new_current()
            course = CourseFactory.create(type_, category, name, description, **kwargs)
            course.mark_new()
            UnitOfWork.get_current().commit()
            course = self.course_mapper.find_by_name(course.name)
            course.attach(SmsNotifier())
            course.attach(EmailNotifier())
            self.courses.append(course)
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    @staticmethod
    def update_course(course: Course, **kwargs):
        course.name = kwargs.get('new_name')
        course.description = kwargs.get('new_text')
        course.url = kwargs.get('new_url')
        course.address = kwargs.get('new_address')
        try:
            UnitOfWork.new_current()
            course.mark_dirty()
            UnitOfWork.get_current().commit()
            course.notify()
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    def clone_course(self, course: Course):
        try:
            UnitOfWork.new_current()
            new_course = course.clone()
            new_course.name = f'{new_course.name} Clone'
            new_course.mark_new()
            UnitOfWork.get_current().commit()
            self.courses.append(self.course_mapper.find_by_name(new_course.name))
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    def create_category(self, name):
        try:
            UnitOfWork.new_current()
            category = CategoryCourse(name)
            category.mark_new()
            UnitOfWork.get_current().commit()
            self.categories_courses.append(self.cat_mapper.find_by_name(category.name))
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    def add_student_course(self, student: Student, course: Course):
        self.sc_mapper.add_student_course(student, course)
        try:
            UnitOfWork.new_current()
            student.courses.append(course)
            student.mark_dirty()
            course.students.append(student)
            course.mark_dirty()
            UnitOfWork.get_current().commit()
        except Exception as e:
            print(e.args)
        finally:
            UnitOfWork.set_current(None)

    def get_all_courses_of_student(self, student: User):
        return self.sc_mapper.find_all_courses_of_student(student)
