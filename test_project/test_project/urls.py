from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # url(r'^$', 'test_project.views.home', name='home'),
    url(r'^accounts/', include('reguser.urls')),
    url(r'^reguser/register/$', 'reguser.views.registration', name='test-registration'),
    url(r'^reguser/register/whitelist/$', 'reguser.views.registration', name='test-registration-whitelist',
        kwargs={'whitelist': ['test.com',]}),
    url(r'^admin/', include(admin.site.urls)),
)
