import abc
import sqlite3

from models import Student


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


class AbstractMapper(metaclass=abc.ABC):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @abc.abstractmethod
    def find_by_id(self, id_obj):
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
        statement = f"SELECT ID, NAME, EMAIL, PHONE FROM STUDENT WHERE ID=?"

        self.cursor.execute(statement, (id_obj,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_obj} not found')

    def insert(self, obj):
        statement = f"INSERT INTO PERSON (FIRSTNAME, LASTNAME) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.first_name, obj.last_name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = "UPDATE PERSON SET FIRSTNAME=?, LASTNAME=? WHERE IDPERSON=?"
        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.id_person))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = "DELETE FROM PERSON WHERE IDPERSON=?"
        self.cursor.execute(statement, (obj.id_person,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)