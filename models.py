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
    def __init__(self, category, name):
        self.category = category
        self.name = name


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, category, name):
        return cls.types[type_](category, name)


class TrainingSite:
    def __init__(self, file: dict):
        self.teachers = file.get('teachers')
        self.students = file.get('students')
        self.courses = file.get('courses')
        self.categories_courses = file.get('categories_courses')

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_course(self, type_, category, name):
        return CourseFactory.create(type_, category, name)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
