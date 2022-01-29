from pages import IndexPage, AboutPage, ContactPage, CoursesPage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/<slug:course>/': CoursesPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
