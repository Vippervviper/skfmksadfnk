# quiz/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _   # «ленивый» перевод

class QuizConfig(AppConfig):
    name = 'quiz'            # путь к пакету
    verbose_name = _('Викторины')   # так заголовок будет отображаться в админке

