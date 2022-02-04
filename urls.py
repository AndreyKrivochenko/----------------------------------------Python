from pages import IndexPage, AboutPage, ContactPage, CoursesPage, NewCoursePage, CopyCoursesPage, StudentsPage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/new/': NewCoursePage(),
    '/courses/copy/': CopyCoursesPage(),
    '/courses/<slug:category>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/edit/': CoursesPage(),
    '/students/': StudentsPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
