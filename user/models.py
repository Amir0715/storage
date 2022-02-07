from datetime import datetime
from unicodedata import name
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    """
    """
    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an Email")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(self, email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        
        kwargs.setdefault("birthday", datetime.now())
        kwargs.setdefault("city", City.objects.first())
        # kwargs.setdefault()
        return self._create_user(email, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя.
    """

    # главнные поля для регистрации
    email = models.EmailField(verbose_name="Электронная почта", max_length=30, unique=True)
    first_name = models.CharField(verbose_name="Фамилия", max_length=22)
    last_name = models.CharField(verbose_name="Имя", max_length=22)
    other_name = models.CharField(verbose_name="Другое имя", max_length=22)
    phone = PhoneNumberField()
    birthday = models.DateField(verbose_name="День рождения")
    city = models.ForeignKey("City", related_name="users", on_delete=models.CASCADE)
    additional_info = models.TextField(verbose_name="Дополнительная информация")
    
    # служебнные
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Строковое представление объекта
        """
        return self.email

    class Meta:
        ordering = ["email"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class City(models.Model):

    name = models.CharField(verbose_name="Название", max_length=55)