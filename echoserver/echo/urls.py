from django.urls import path

from .views import edit_book_page, add_book_page, homepage, delete_book_page

urlpatterns = [
    path('', homepage, name='home'),
    path('add', add_book_page, name='add_book'),
    path('<int:book_id>/edit', edit_book_page, name='edit_book'),
    path('<int:book_id>/delete', delete_book_page, name='delete_book')
]
