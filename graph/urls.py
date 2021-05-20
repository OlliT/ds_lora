from django.urls import path

from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.index),
    url(r'^lora/$', views.lora, name='lora'),
    url(r'^lora_log/$', views.lora_log, name='lora_log'),
    url(r'^lora_stats/$', views.lora_stats, name='lora_stats'),
]
