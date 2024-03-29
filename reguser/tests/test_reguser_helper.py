from django.test import TestCase, RequestFactory
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature
from django.core.urlresolvers import reverse
from django.core import mail
from reguser.models import ReguserHelper

class ReguserHelperTestCase(TestCase):
    def setUp(self):
        self.helper = ReguserHelper()
        self.helper2 = ReguserHelper()
        self.token = self.helper.create_inactive_user('mojojojo', 'mojo@jojo.hum', 'sikrit').activation_token
        self.token_parts = self.token.partition(':')
        self.assertEqual(len(self.token_parts), 3)

    def test_helper_creates_inactive_user(self):
        username = ReguserHelper().signer.unsign(self.token) # Unsign with a new signer, just to be sure
        new_user = self.helper.USER_MODEL.objects.get(username=username)
        self.assertFalse(new_user.is_active)

    def test_helper_sets_extra_attributes_on_user(self):
        token = self.helper.create_inactive_user('mojojojo2', 'mojo@jojo.hum', 'sikrit', 
                attrs={'first_name': 'Mojo', 'last_name':'Jojo'}).activation_token
        username = ReguserHelper().signer.unsign(token)
        new_user = self.helper.USER_MODEL.objects.get(username=username)
        self.assertFalse(new_user.is_active)
        self.assertEqual(new_user.first_name, 'Mojo')
        self.assertEqual(new_user.last_name, 'Jojo')

    def test_validate_raises_exception_with_tampered_username(self):
        parts = self.token_parts
        # Mangle the username
        bad_token_1 = ''.join([parts[0]+'1', parts[1], parts[2]])
        with self.assertRaises(BadSignature):
            self.helper2.validate_activation_token(bad_token_1)
        
    def test_validate_raises_exception_with_tampered_signature(self):
        parts = self.token_parts
        # Mangle the signature
        bad_token_2 = ''.join([parts[0], parts[1], parts[2][::-1]])
        with self.assertRaises(BadSignature):
            self.helper2.validate_activation_token(bad_token_2)

    def test_validate_raises_exception_with_tampered_separator(self):
        parts = self.token_parts
        # Mangle the separator
        bad_token_3 = ''.join([parts[0], '', parts[2]])
        with self.assertRaises(BadSignature):
            self.helper2.validate_activation_token(bad_token_3)

    def test_validate_raises_exception_if_user_does_not_exist(self):
        self.helper.USER_MODEL.objects.get(username=self.token_parts[0]).delete()
        with self.assertRaises(ObjectDoesNotExist):
            self.helper2.validate_activation_token(self.token)

    def test_validate_returns_none_if_user_already_active(self):
        user = 'no-user'
        self.helper.USER_MODEL.objects.filter(username=self.token_parts[0]).update(is_active=True)
        user = self.helper2.validate_activation_token(self.token)
        self.assertIsNone(user)

    def test_validate_activates_user_if_token_is_valid(self):
        user = self.helper2.validate_activation_token(self.token)
        self.assertEqual(str(user.username), self.token_parts[0])
        self.assertTrue(user.is_active)

    def test_email_activation_link_sends_correct_email(self):
        from django.contrib.sites.shortcuts import get_current_site
        site = get_current_site(RequestFactory().get(reverse('reguser-registration')))
        user = self.helper.create_inactive_user('supermario', 'super@mario.hum', 'broz',
                attrs={'first_name': 'Super', 'last_name': 'Mario'})
        self.helper.email_activation_link(site, user)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn('super@mario.hum', msg.to)
        self.assertEqual(msg.subject, u"Super, activate your registration!")
        self.assertIn("http://{}{}?t={}".format(site, reverse('reguser-activate'), user.activation_token), msg.body)
