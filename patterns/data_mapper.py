import abc
import sqlite3

import models

from settings import DATABASE_NAME

connection = sqlite3.connect(DATABASE_NAME, check_same_thread=False)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class AbstractMapper(abc.ABC):
    def __init__(self):
        self.connection = connection
        self.cursor = connection.cursor()

    @abc.abstractmethod
    def get_all(self):
        pass

    @abc.abstractmethod
    def find_by_id(self, id_obj):
        pass

    @abc.abstractmethod
    def find_by_name(self, obj_name):
        pass

    @abc.abstractmethod
    def insert(self, obj):
        pass

    @abc.abstractmethod
    def update(self, obj):
        pass

    @abc.abstractmethod
    def delete(self, obj):
        pass


class SqliteStudentMapper(AbstractMapper):

    def get_all(self):
        statement = f"SELECT NAME, EMAIL, PHONE, USER_ID FROM STUDENT"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            student_list = []
            for student in result:
                student_list.append(models.UserFactory.create('student', *student))
            return student_list
        else:
            return []

    def find_by_id(self, id_obj):
        statement = f"SELECT NAME, EMAIL, PHONE, USER_ID FROM STUDENT WHERE USER_ID=?"

        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            return models.UserFactory.create('student', *result)
        else:
            raise RecordNotFoundException(f'record with userid={id_obj} not found')

    def find_by_name(self, obj_name):
        statement = f"SELECT NAME, EMAIL, PHONE, USER_ID FROM STUDENT WHERE NAME=?"

        self.cursor.execute(statement, (obj_name,))
        result = self.cursor.fetchone()
        if result:
            return models.UserFactory.create('student', *result)
        else:
            raise RecordNotFoundException(f'record with name={obj_name} not found')

    def insert(self, obj):
        statement = f"INSERT INTO STUDENT (NAME, EMAIL, PHONE) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.email, obj.phone))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = "UPDATE STUDENT SET NAME=?, EMAIL=?, PHONE=? WHERE USER_ID=?"
        self.cursor.execute(statement, (obj.name, obj.email, obj.phone, obj.user_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = "DELETE FROM STUDENT WHERE USER_ID=?"
        self.cursor.execute(statement, (obj.user_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class SqliteCourseMapper(AbstractMapper):

    def get_all(self):
        statement = f"SELECT type, category_id, name, description, address, url, course_id FROM course"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            course_list = []
            for course in result:
                course_list.append(models.CourseFactory.create(*course))
            return course_list
        else:
            return []

    def find_by_id(self, id_obj):
        statement = f"SELECT type, category_id, name, description, address, url, course_id FROM course WHERE course_id=?"

        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            return models.CourseFactory.create(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_obj} not found')

    def find_by_name(self, obj_name):
        statement = f"SELECT type, category_id, name, description, address, url, course_id FROM course WHERE NAME=?"

        self.cursor.execute(statement, (obj_name,))
        result = self.cursor.fetchone()
        if result:
            return models.CourseFactory.create(*result)
        else:
            raise RecordNotFoundException(f'record with name={obj_name} not found')

    def insert(self, obj):
        statement = f"INSERT INTO course (type, category_id, name, description) VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.type, obj.category_id, obj.name, obj.description))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = "UPDATE course SET type=?, category_id=?, name=?, description=?, address=?, url=? WHERE course_id=?"
        self.cursor.execute(statement, (obj.type, obj.category_id, obj.name, obj.description, obj.address,
                                        obj.url, obj.course_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = "DELETE FROM course WHERE course_id=?"
        self.cursor.execute(statement, (obj.course_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class SqliteCategoryMapper(AbstractMapper):
    def get_all(self):
        statement = f"SELECT name, category_id FROM category_course"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            category_list = []
            for category in result:
                category_list.append(models.CategoryCourse(*category))
            return category_list
        else:
            return []

    def find_by_id(self, id_obj):
        statement = f"SELECT name, category_id FROM category_course WHERE category_id=?"
        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            return models.CategoryCourse(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_obj} not found')

    def find_by_name(self, obj_name):
        statement = f"SELECT name, category_id FROM category_course WHERE NAME=?"
        self.cursor.execute(statement, (obj_name,))
        result = self.cursor.fetchone()
        if result:
            return models.CategoryCourse(*result)
        else:
            raise RecordNotFoundException(f'record with name={obj_name} not found')

    def insert(self, obj):
        statement = f"INSERT INTO category_course (NAME) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = "UPDATE category_course SET name=? WHERE category_id=?"
        self.cursor.execute(statement, (obj.name, obj.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = "DELETE FROM category_course WHERE category_id=?"
        self.cursor.execute(statement, (obj.category_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class AbstractStudentCourseMapper(abc.ABC):
    def __init__(self):
        self.connection = connection
        self.cursor = connection.cursor()

    @abc.abstractmethod
    def add_student_course(self, student, course):
        pass

    @abc.abstractmethod
    def find_all_courses_of_student(self, student):
        pass

    @abc.abstractmethod
    def find_all_student_of_course(self, course):
        pass


class SqliteStudentCourseMapper(AbstractStudentCourseMapper):

    def add_student_course(self, student, course):
        statement = f"INSERT INTO student_course (student_id, course_id) VALUES (?, ?)"
        self.cursor.execute(statement, (student.user_id, course.course_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def find_all_courses_of_student(self, student):
        statement = "SELECT type, category_id, name, description, address, url, c.course_id FROM course c LEFT JOIN " \
                    "student_course sc ON c.course_id = sc.course_id WHERE sc.student_id = ? "
        self.cursor.execute(statement, (student.user_id,))
        result = self.cursor.fetchall()
        if result:
            result_courses = []
            for course in result:
                result_courses.append(models.CourseFactory.create(*course))
            return result_courses
        else:
            return []

    def find_all_student_of_course(self, course):
        statement = f"SELECT name, email, phone, user_id FROM student s LEFT JOIN student_course sc ON s.user_id = " \
                    f"sc.student_id WHERE sc.course_id = ? ORDER BY name "
        self.cursor.execute(statement, (course.course_id, ))
        result = self.cursor.fetchall()
        if result:
            result_users = []
            for student in result:
                result_users.append(models.UserFactory.create('student', *student))
            return result_users
        else:
            return []
