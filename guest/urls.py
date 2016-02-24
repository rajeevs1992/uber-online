from django.conf.urls import url
from guest import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
