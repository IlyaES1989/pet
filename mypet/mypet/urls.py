"""mypet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.contrib.auth import views as auth_views

from sloth import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('sloth/', include('sloth.urls')),
    path('accounts/', RegistrationView.as_view(), name='registration_register'),
    path('accounts/register/complete/', auth_views.LoginView.as_view()),
    path('accounts/password_reset/done/', auth_views.LoginView.as_view(
        template_name='registration/password_reset_done.html', )),
    path('accounts/reset/done/', auth_views.LoginView.as_view(
        template_name='registration/password_reset_complete.html', )),
    path('accounts/activate/', ActivationView.as_view(), name='registration_activate'),
    path('accounts/activate/complete/', auth_views.LoginView.as_view(
        template_name='django_registration/activation_complete.html', )),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
