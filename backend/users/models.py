from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    CHOICE_ROLE = (
        (USER, USER),
        (ADMIN, ADMIN),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=CHOICE_ROLE,
        default=USER,
        max_length=100
    )

    REQUIRED_FIELDS = ['email']

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
