from pages import IndexPage, AboutPage, ContactPage

routes = {
    '/': IndexPage(),
    '/about': AboutPage(),
    '/contact': ContactPage()
}
