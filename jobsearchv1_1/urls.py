from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'jobsearchv1_1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^jobseeker/', include('jobseeker.urls', namespace='jobseeker')),
    url(r'^talentseeker/', include('talentseeker.urls', namespace='talentseeker')),
    url(r'^admin/', include(admin.site.urls)),
]
