from django.urls import path

from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.index),
    url(r'^lora/$', views.lora, name='lora'),
]
