from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'reguser.views.registration', name='reguser-registration'),
)
