from pages import IndexPage, AboutPage, ContactPage, CoursesPage

routes = {
    '/': IndexPage(),
    '/courses': CoursesPage(),
    '/about': AboutPage(),
    '/contact': ContactPage()
}
