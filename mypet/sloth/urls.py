from django.urls import path
from . import views
from .views import Setting, CreateReport

urlpatterns = [
    path('', Setting.as_view(), name='index'),
    path('create/', CreateReport.as_view(), name='create'),
    path('update/', views.update_file, name='update'),
    path('result/', views.get_result, name='result'),
]