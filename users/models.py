from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
        related_name='custom_groups',
        related_query_name='custom_group',
    )

    def __str__(self):
        return self.name

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     date_joined = models.DateTimeField(default=timezone.now)
#
#     # Указываем, что поле "email" используется как имя пользователя    # Обязательные поля при создании пользователя через команду createsuperuser
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     def __str__(self):
#         return self.email
#
#     # Другие поля и отношения
#
#     custom_groups = models.ManyToManyField(
#         CustomGroup,
#         verbose_name=_('custom groups'),
#         blank=True,
#         related_name='custom_users',
#         related_query_name='custom_user',
#     )
