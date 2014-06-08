from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'reguser.views.registration', name='reguser-registration'),
    url(r'^register/activate/$', 'reguser.views.reguser_activate', name='reguser-activate'),
    url(r'^login/$', 'reguser.views.reguser_login', name='reguser-login'),
    url(r'^profile/$', 'reguser.views.reguser_profile', name='reguser-profile'),
)
