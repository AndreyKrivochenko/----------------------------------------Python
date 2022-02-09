import abc

from models import Student, CourseFactory, UserFactory


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
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

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

    def find_by_id(self, id_obj):
        statement = f"SELECT NAME, EMAIL, PHONE, USER_ID FROM STUDENT WHERE USER_ID=?"

        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            # return Student(*result)
            return UserFactory.create('student', *result)
        else:
            raise RecordNotFoundException(f'record with userid={id_obj} not found')

    def find_by_name(self, obj_name):
        statement = f"SELECT NAME, EMAIL, PHONE, USER_ID FROM STUDENT WHERE NAME=?"

        self.cursor.execute(statement, (obj_name,))
        result = self.cursor.fetchone()
        if result:
            # return Student(*result)
            return UserFactory.create('student', *result)
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
    def find_by_id(self, id_obj):
        statement = f"SELECT type, category, name, description, address, url, course_id FROM course WHERE course_id=?"

        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            return CourseFactory.create(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_obj} not found')

    def find_by_name(self, obj_name):
        statement = f"SELECT type, category, name, description, address, url, course_id FROM course WHERE NAME=?"

        self.cursor.execute(statement, (obj_name,))
        result = self.cursor.fetchone()
        if result:
            return CourseFactory.create(*result)
        else:
            raise RecordNotFoundException(f'record with name={obj_name} not found')

    def insert(self, obj):
        statement = f"INSERT INTO course (type, category, name, description) VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.type, obj.category, obj.name, obj.description))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = "UPDATE course SET type=?, category=?, name=?, description=?, address=?, url=? WHERE course_id=?"
        self.cursor.execute(statement, (obj.type, obj.category, obj.name, obj.description, obj.address,
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
