from lunchbag.testutils import URLTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import views as django_auth_views
from reguser import views

class ReguserURLsTestCase(URLTestCase):
    def setUp(self):
        reference_url = reverse('reguser-registration')
        self.assertTrue(reference_url.endswith('register/'))
        self.url_base = reference_url[:-len('register/')]

    def test_registration_url(self):
        self.assert_url_matches_view(views.registration, self.url_base+'register/', 'reguser-registration')

    def test_activation_url(self):
        self.assert_url_matches_view(views.reguser_activate, self.url_base+'register/activate/', 'reguser-activate')
    
    def test_login_url(self):
        self.assert_url_matches_view(django_auth_views.login, self.url_base+'login/', 'login')

    def test_logout_url(self):
        self.assert_url_matches_view(django_auth_views.logout, self.url_base+'logout/', 'logout')

    def test_user_profile_url(self):
        self.assert_url_matches_view(views.reguser_profile, self.url_base+'profile/', 'reguser-profile')
