from framework.decorators import GetTime
from pages import IndexPage, AboutPage, ContactPage, CoursesPage, NewCoursePage, CopyCoursesPage

routes = {
    '/': GetTime(IndexPage()),
    '/courses/': GetTime(CoursesPage()),
    '/courses/new/': GetTime(NewCoursePage()),
    '/courses/copy/': GetTime(CopyCoursesPage()),
    '/courses/<slug:category>/': GetTime(CoursesPage()),
    '/courses/<slug:category>/<slug:course>/': GetTime(CoursesPage()),
    '/courses/<slug:category>/<slug:course>/edit/': GetTime(CoursesPage()),
    '/about/': GetTime(AboutPage()),
    '/contact/': GetTime(ContactPage())
}
