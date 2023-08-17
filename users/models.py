from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_users_groups',  # Обратный доступ для groups
        related_query_name='custom_user_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_users_permissions',  # Обратный доступ для user_permissions
        related_query_name='custom_user_permission',
    )
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        null=True,  # Установите null=True
        default='temp_username'  # Задайте временное значение по умолчанию
    )
