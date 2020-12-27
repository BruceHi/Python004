from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('index2', views.show2),
    path('bar', views.bar),
    path('pie', views.pie),
    re_path(r'^tables', views.tables),
    re_path(r'^charts', views.charts),
    re_path(r'^index', views.show),
]