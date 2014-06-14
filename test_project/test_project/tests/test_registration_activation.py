from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core import mail
from django_webtest import WebTest
from lunchbag.testutils import WebtestHelperMixin
import re

class RegistrationActivationTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        registration_page = self.app.get(reverse('test-registration'))
        form = registration_page.form
        self.set_default_form_values(first_name = u"Mojo", last_name = u"Jojo",
                email = u"mojo@jojo.com", password1 = u"moPass", password2 = u"moPass")
        self.fill_in_form(form)
        response = form.submit().follow()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.token = re.search('t=(.+?)\s', msg.body).group(1)
        self.activation_link = reverse('test-activate-registration')

    def test_f_activation_with_login_successful(self):
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertFalse(user.is_active)
        response = self.app.get(self.activation_link, {'t': self.token}).follow()
        response.mustcontain("Your account is now active!")
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertTrue(user.is_active)
        self.assertEqual(self.app.session['_auth_user_id'], user.pk)
