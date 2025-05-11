from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # сюда можно вынести маршруты, не зависящие от языка
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    prefix_default_language=False,
)

