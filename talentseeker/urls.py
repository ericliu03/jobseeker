__author__ = 'EricLiu'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search_submit/$', views.search_submit, name='search_submit'),
    url(r'^result/$', views.result, name='result'),
]