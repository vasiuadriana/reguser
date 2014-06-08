from lunchbag.testutils import URLTestCase
from django.core.urlresolvers import reverse
from reguser import views

class ReguserURLsTestCase(URLTestCase):
    def setUp(self):
        reference_url = reverse('reguser-registration')
        self.assertTrue(reference_url.endswith('register/'))
        self.url_base = reference_url[:-len('register/')]

    def test_registration_url(self):
        self.assert_url_matches_view(views.registration, self.url_base+'register/', 'reguser-registration')

    def test_activation_url(self):
        self.assert_url_matches_view(views.activate, self.url_base+'register/activate/', 'reguser-activate')
