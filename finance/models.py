from django.db.models import *

from finance.choices import KirimChiqimStatusChoice


class Category(Model):
    name = CharField(max_length=128)
    image = ImageField(upload_to='images/categories/', null=True, blank=True)
    status = CharField(max_length=10, choices=KirimChiqimStatusChoice, null=False, blank=False)


class KirimChiqim(Model):
    money = DecimalField(max_digits=25, decimal_places=2)
    user = ForeignKey('user.User', on_delete=CASCADE, related_name='profit')
    category = ForeignKey('finance.Category', on_delete=CASCADE, related_name='profit')
    created_at = DateTimeField(auto_now_add=True)
    description = TextField()
    status = CharField(choices=KirimChiqimStatusChoice, max_length=128)
