from django.shortcuts import render, redirect
from django.http import HttpRequest
from .controllers import BookController
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book


# Create your views here.
def add_book_page(request: HttpRequest):
    if request.method == "POST":
        form = request.POST
        controller = BookController()
        controller.add_book(form.get("name"), form.get("author"), form.get("price"))

        return redirect("/")

    return render(request, "add_book.html")


def homepage(request: HttpRequest):
    controller = BookController()
    books = controller.list_books()
    paginator = Paginator(books, 2)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {"page_obj": page_obj})


def edit_book_page(request: HttpRequest, book_id):
    controller = BookController()
    book = controller.get_book(book_id)
    if request.method == "POST":
        form = request.POST
        controller = BookController()
        controller.edit_book(form.get("id"), form.get("name"), form.get("author"), form.get("price"))

        return redirect("/")
    return render(request, "edit_book.html", {'book': book})


def delete_book_page(request: HttpRequest, book_id):
    controller = BookController()
    book = controller.get_book(book_id)
    if request.method == "POST":
        form = request.POST
        controller = BookController()
        controller.delete_book(form.get("id"))

        return redirect("/")
    return render(request, "delete_book.html", {'book': book})
