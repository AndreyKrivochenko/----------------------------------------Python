from pages import IndexPage, AboutPage, ContactPage, CoursesPage, NewCoursePage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/new/': NewCoursePage(),
    '/courses/<slug:category>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/edit/': CoursesPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
