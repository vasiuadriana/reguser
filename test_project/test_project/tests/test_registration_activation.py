from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core import mail
import re

class RegistrationActivationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post(reverse('test-registration'), {'first_name': 'mojo', 'last_name': 'jojo',
            'email': 'mojo@jojo.com', 'password1': 'sikrit', 'password2': 'sikrit'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.token = re.search('t=(.+?)\s', msg.body).group(1)
        self.activation_link = reverse('test-activate-registration')

    def test_f_activation_with_login_successful(self):
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertFalse(user.is_active)
        response = self.client.get(self.activation_link, {'t': self.token})
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertTrue(user.is_active)
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)
