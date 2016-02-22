from django.conf.urls import url
from ride import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^confirm/$', views.confirm, name='confirm'),
]
