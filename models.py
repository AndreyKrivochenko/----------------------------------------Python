import json

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
    def __init__(self, category, name, description):
        self.category = category
        self.name = name
        self.description = description


class InteractiveCourse(Course):
    def __init__(self, category, name, description):
        Course.__init__(self, category, name, description)
        self.url = ''
        self.type = 'interactive'


class RecordCourse(Course):
    def __init__(self, category, name, description):
        Course.__init__(self, category, name, description)
        self.address = ''
        self.type = 'record'


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, category, name, description):
        return cls.types[type_](category, name, description)


class TrainingSite:
    def __init__(self, file: dict):
        self.teachers = file.get('teachers')
        self.students = file.get('students')
        self.courses = self.__get_courses_from_file(file.get('courses'))
        self.categories_courses: list = file.get('categories_courses')

    def __get_courses_from_file(self, courses: list) -> list:
        courses_list = []
        for course in courses:
            courses_list.append(self.create_course(
                                    course.get('type'),
                                    course.get('category'),
                                    course.get('name'),
                                    course.get('description')
                                ))
        return courses_list

    def __save_site(self):
        site_ = {
            'teachers': self.teachers,
            'students': self.students,
            'courses': [item.__dict__ for item in self.courses],
            'categories_courses': self.categories_courses
        }
        with open('site_db.json', 'w', encoding='utf-8') as f:
            json.dump(site_, f, indent=4)
        return None

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_course(self, type_, category, name, description):
        return CourseFactory.create(type_, category, name, description)

    def create_category(self, name):
        if name and name not in self.categories_courses:
            self.categories_courses.append(name)
            self.__save_site()
        return None

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
