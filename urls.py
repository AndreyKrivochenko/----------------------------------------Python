from pages import IndexPage, AboutPage, ContactPage, CoursesPage, CoursesDetailPage

routes = {
    '/': IndexPage(),
    '/courses/': CoursesPage(),
    '/courses/<slug:course>/': CoursesDetailPage(),
    '/about/': AboutPage(),
    '/contact/': ContactPage()
}
