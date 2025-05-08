from django.urls import path

from .views import (edit_book_page, add_book_page, homepage, delete_book_page, cart_view, make_order,
                    SignUp, logout_view, not_staff_view, profile_view, cart_update, orders_view, check_username)

urlpatterns = [
    path('', homepage, name='home'),
    path('add', add_book_page, name='add_book'),
    path('<int:book_id>/edit', edit_book_page, name='edit_book'),
    path('<int:book_id>/delete', delete_book_page, name='delete_book'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', logout_view, name='logged_out'),
    path('profile', profile_view, name='profile'),
    path('not_staff', not_staff_view, name='not_staff'),
    path('<int:book_id>/cart_update', cart_update, name='cart_update'),
    path('cart', cart_view, name='cart_view'),
    path('orders', orders_view, name='orders_view'),
    path('make_order', make_order, name='make_order'),
    path('check_username/', check_username, name='check_username'),
]
