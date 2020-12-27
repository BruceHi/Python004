from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.show),
    path('bar', views.bar),
    path('pie', views.pie),
]