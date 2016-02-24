from django.conf.urls import url
from ride import views

urlpatterns = [
    url(r'^$', views.index, name='request'),
    url(r'^select/(?P<requestid>\d+)/$', views.select, name='select'),
    url(r'^action/(?P<target>\w+)/$', views.action),
    url(r'^book/(?P<productid>.+)/$', views.book, name='book'),
    url(r'^delete/(?P<requestid>\d+)/$', views.delete, name='delete'),
]
