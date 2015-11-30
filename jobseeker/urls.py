__author__ = 'EricLiu'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login_submit/$', views.login_prepare, name='login_prepare'),
    url(r'^logout/$', views.logout_user, name='logout_user'),

    url(r'^$', views.index, name='index'),
    url(r'^new_candidate/$', views.create_candidate, name='create_candidate'),
    url(r'^$', views.create_candidate_cancelled, name='create_candidate_cancelled'),
    url(r'^create_submit/$', views.create_submit, name='create_submit'),


    url(r'^(?P<pk>[0-9]+)/search/$', views.search, name='search'),
    url(r'^(?P<pk>[0-9]+)/edit_profile$', views.edit_profile, name='edit_profile'),
    url(r'^(?P<pk>[0-9]+)/edit_profile_submit', views.edit_profile_submit, name='edit_profile_submit'),

    url(r'^(?P<pk>[0-9]+)/search_submit/$', views.search_submit, name='search_submit'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.result, name='result'),

    url(r'^(?P<pk>[0-9]+)/result_(?P<counter>[0-9]+)$', views.job_detail, name='job_detail'),
]