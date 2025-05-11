from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout

# наша вьюшка: разлогинивает и сразу перенаправляет на форму логина админа
def admin_logout_and_redirect(request):
    django_logout(request)
    return redirect('admin:login')

urlpatterns = [
    # сначала перехватываем /admin/logout/
    path('admin/logout/', admin_logout_and_redirect, name='admin_logout'),
    # затем всё остальное админ-урлы
    path('admin/', admin.site.urls),
    # и ваш фронтенд
    path('', include('quiz.urls')),
]

