from pages import IndexPage, AboutPage, ContactPage, CoursesPage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/<slug:category>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/': CoursesPage(),
    '/courses/<slug:category>/<slug:course>/edit/': CoursesPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
