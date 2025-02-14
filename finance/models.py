from django.db.models import *

from finance.choices import ExpenseTypeChoice


class Category(Model):
    name = CharField(max_length=128)
    image = TextField()
    type = CharField(max_length=10, choices=ExpenseTypeChoice, null=False, blank=False)


class Expense(Model):
    money = DecimalField(max_digits=25, decimal_places=2)
    user = ForeignKey('user.User', on_delete=CASCADE, related_name='profit')
    category = ForeignKey('finance.Category', on_delete=CASCADE, related_name='profit')
    created_at = DateTimeField(auto_now_add=True)
    description = TextField()
    type = CharField(choices=ExpenseTypeChoice, max_length=128)
