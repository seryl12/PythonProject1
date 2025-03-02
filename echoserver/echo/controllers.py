from .models import Book
from django.core.paginator import Paginator
from django.shortcuts import render


class BookController:
    def add_book(self, name, author, price):
        book = Book(name=name, author=author, price=price)
        book.save()

    def list_books(self):
        return Book.objects.all()

    def get_book(self, id):
        return Book.objects.get(id=id)

    def edit_book(self, id, name, author, price):
        book = Book(id=id, name=name, author=author, price=price)
        book.save()

    def delete_book(self, id):
        book = Book.objects.get(id=id)
        book.delete()
