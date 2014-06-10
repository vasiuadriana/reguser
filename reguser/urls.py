from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'reguser.views.registration', name='reguser-registration'),
    url(r'^register/activate/$', 'reguser.views.reguser_activate', name='reguser-activate'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'reguser/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', 
        kwargs={'next_page': '/'}),
    url(r'^reset/$', 'reguser.views.reguser_password_reset', name='password-reset'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                'reguser.views.reguser_password_reset_confirm', name='password-reset-confirm'),
    url(r'^change/$', 'reguser.views.reguser_password_change', name='password-change'),
    url(r'^profile/$', 'reguser.views.reguser_profile', name='reguser-profile'),
)
