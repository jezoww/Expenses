from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import *


class CustomUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):

        if not phone:
            raise ValueError("The given phone must be set")
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    email = None
    fullname = CharField(max_length=128)
    username = CharField(max_length=128, unique=False, null=True, blank=True)
    phone = CharField(max_length=20, unique=True)

    objects = CustomUserManager()
    EMAIL_FIELD = "phone"
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
