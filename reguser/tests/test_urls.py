from lunchbag.testutils import URLTestCase
from reguser import views

class ReguserURLsTestCase(URLTestCase):

    def test_registration_url(self):
        self.assert_url_matches_view(views.registration, '/accounts/register/', 'reguser-registration')
