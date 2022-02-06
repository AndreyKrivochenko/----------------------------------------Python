from pages import IndexPage, AboutPage, ContactPage, CoursesPage, NewCoursePage, CopyCoursesPage, StudentsPage, \
    CreateStudentPage, CoursesApi

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/new/': NewCoursePage(),
    '/courses/copy/': CopyCoursesPage(),
    '/courses/<slug:category>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/edit/': CoursesPage(),
    '/students/': StudentsPage(),
    '/students/new/': CreateStudentPage(),
    '/students/<slug:student>/': StudentsPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage(),
    '/favicon.ico': '',
    '/api/courses/': CoursesApi()
}
