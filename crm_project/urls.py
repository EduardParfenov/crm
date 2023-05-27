"""
URL configuration for crm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from change_tasks import views as views_for_auth
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls), # админка
    path("", include('change_tasks.urls')), # регистрация урлов нашего приложения change_tasks
    path('register/', views_for_auth.register, name='register'), # функция регистрации
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # функция авторизации
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'), # функция выхода
]
# добавляет URL-адреса для отображения файлов медиа, если приложение работает в режиме отладки (DEBUG=True).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)  
