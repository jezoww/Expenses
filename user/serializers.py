from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
import re

from user.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'fullname', 'email', 'password'


    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[*/!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("Password must contain at least one special character.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one number.")
        return make_password(value)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email number already registered!")
        return value



class RegisterCheckSerializer(Serializer):
    email = EmailField(required=True)
    code = CharField(required=True)
    verify_code = CharField(read_only=True)

    def validate_code(self, value):
        if not check_password(value, self.initial_data.get('verify_code')):
            raise ValidationError("Incorrect code!")
        return value

    def save(self, **kwargs):
        User.objects.filter(email=self.initial_data.get('email')).update(is_active=True)
        return super().save(**kwargs)
