import sqlite3

from data_mapper import SqliteStudentMapper, SqliteCourseMapper
from models import Student, CourseFactory

connection = sqlite3.connect('site_db.sqlite')

# mapper = SqliteStudentMapper(connection)
# student = Student('Andrey Krivochenko', 'mail@mail.com', '+79632587458')
# mapper.insert(student)
# student = mapper.find_by_name('Andrey Krivochenko')
# print(student.__dict__)

mapper = SqliteCourseMapper(connection)

course = CourseFactory.create('interactive', 'Python', 'Python for beginner', 'some desc')
mapper.insert(course)
course = mapper.find_by_name('Python for beginner')
print(course.course_id)
