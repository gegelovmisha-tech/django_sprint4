from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # Добавьте этот импорт


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = _('Блог')  # Добавьте эту строку
