from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from .forms import BookForm
from .models import Book
from .models import Order
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def add_book_page(request: HttpRequest):
    if request.method == "POST":
        form = BookForm(request.POST)
        tmp = form.save()
        return redirect('/')
    else:
        form = BookForm()

    return render(request, "add_book.html", {'form': form})


def homepage(request: HttpRequest):
    books = Book.objects.all()
    paginator = Paginator(books, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {"page_obj": page_obj})


def edit_book_page(request: HttpRequest, book_id):
    if not request.user.is_staff:
        return redirect(reverse_lazy('not_staff'))
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        tmp = form.save()
        return redirect("/")
    else:
        form = BookForm(instance=book)
    return render(request, "edit_book.html", {'form': form, 'book': book})


def delete_book_page(request: HttpRequest, book_id):
    if not request.user.is_staff:
        return redirect(reverse_lazy('not_staff'))
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("/")
    return render(request, "delete_book.html", {'book': book})


class SignUp(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request: HttpRequest):
    return render(request, "registration/profile.html")


def not_staff_view(request: HttpRequest):
    return render(request, "registration/not_staff.html")


@login_required
def cart_update(request: HttpRequest, book_id):
    cart = request.session.get('cart', None)
    if not cart:
        cart = []
    cart.append(book_id)
    request.session['cart'] = cart
    return redirect("/")


@login_required
def cart_view(request: HttpRequest):
    cart = request.session.get('cart', None)
    book_list = []
    total_price = 0
    if cart:
        for id in cart:
            book_in_book_list = False
            for i in range(len(book_list)):
                if id == book_list[i]['book'].id:
                    book_in_book_list = True
                    book_list[i]['count'] += 1
                    total_price += book_list[i]['book'].price
            if not book_in_book_list:
                book_list.append({'book': Book.objects.get(id=id), 'count': 1})
                total_price += book_list[-1]['book'].price
    return render(request, "cart.html",
                  {'book_list': book_list, 'total_price': total_price})


@login_required
def orders_view(request: HttpRequest):
    orders = Order.objects.filter(user_id=request.user)
    max_order_number = max(orders, key=lambda i: i.order_number, default=0)
    if type(max_order_number) != int:
        max_order_number = max(orders, key=lambda i: i.order_number, default=0).order_number
    order_list = [None] * max_order_number
    for order in orders:
        if order_list[order.order_number - 1]:
            order_list[order.order_number - 1]["books"].append(Book.objects.get(id=order.book_id.id))
        else:
            order_list[order.order_number - 1] = {"books": [Book.objects.get(id=order.book_id.id)],
                                                  "price": order.price, "date": order.date}
    return render(request, "orders.html", {"order_list": order_list, 'len': len(order_list)})


@login_required
def make_order(request: HttpRequest):
    cart = request.session.get('cart', None)
    if not cart:
        return render(request, "empty_cart.html")

    orders = Order.objects.filter(user_id=request.user.id)
    order_number = max(orders, key=lambda i: i.order_number, default=0)
    if type(order_number) != int:
        order_number = max(orders, key=lambda i: i.order_number, default=0).order_number
    order_number += 1
    order_price = 0
    for id in cart:
        order_price += Book.objects.get(id=id).price
    for id in cart:
        order = Order(book_id=Book.objects.get(id=id), user_id=request.user, price=order_price,
                      date=datetime.now().date(), order_number=order_number)
        order.save()
    request.session['cart'] = None
    return redirect("/")
