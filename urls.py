from pages import IndexPage, AboutPage, ContactPage, CoursesPage, NewCoursePage, CopyCoursesPage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/new/': NewCoursePage(),
    '/courses/copy/': CopyCoursesPage(),
    '/courses/<slug:category>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/edit/': CoursesPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
