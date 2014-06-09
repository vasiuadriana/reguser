from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'reguser.views.registration', name='reguser-registration'),
    url(r'^register/activate/$', 'reguser.views.reguser_activate', name='reguser-activate'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'reguser/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', 
        kwargs={'next_page': '/'}),
    url(r'^profile/$', 'reguser.views.reguser_profile', name='reguser-profile'),
)
