from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Book(models.Model):
    name = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    price = models.FloatField(validators=[MinValueValidator(0)])


class Order(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField()
    order_number = models.IntegerField()
