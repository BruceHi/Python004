from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.show),  # 同样可以匹配以 index？为开头的所有字段。
]
