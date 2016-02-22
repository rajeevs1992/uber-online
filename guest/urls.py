from django.conf.urls import url
from guest import views

urlpatterns = [
    url(r'^welcome/$', views.welcome),
]
