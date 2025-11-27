from views.header import render_header
from views.books import books_catalog
from views.firends import friends_catalog
from views.loans import loans_management
from views.footer import render_footer


def app():
    render_header()
    books_catalog()
    friends_catalog()
    loans_management()
    render_footer()
