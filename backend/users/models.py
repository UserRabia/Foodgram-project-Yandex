from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.constants import (
    USER_FIXED_STRING_LENGTH,
    EMAIL_FIXED_STRING_LENGTH
)


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    CHOICE_ROLE = (
        (USER, USER),
        (ADMIN, ADMIN),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_FIXED_STRING_LENGTH
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_FIXED_STRING_LENGTH
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=USER_FIXED_STRING_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_FIXED_STRING_LENGTH,
        unique=True
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Пользователи'
