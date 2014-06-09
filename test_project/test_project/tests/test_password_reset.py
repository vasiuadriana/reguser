# -*- coding: utf-8 -*-
from django_webtest import WebTest
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from lunchbag.testutils import WebtestHelperMixin
import re

class PasswordResetTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        self.password_reset_page = self.app.get(reverse('password-reset'))
        self.user = User.objects.create_user("tmpuser", "tmpuser@test.com", "tmppass")
        self.user.is_active = True
        self.user.save()

    def test_f_password_reset_url_returns_password_reset_form(self):
        self.password_reset_page.mustcontain('Password reset', 'POST', 'Send link', 
                'csrfmiddlewaretoken', no=['error'])
        form = self.password_reset_page.form
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.action, reverse('password-reset'))
        self.assertTrue(set([u'csrfmiddlewaretoken', u'email']) < set(form.fields))

    def test_f_missing_required_fields_in_registration_form(self):
        form = self.password_reset_page.form
        form['email'] = ''
        response = form.submit()
        expected_error_msg = "This field is required."
        response.mustcontain('error', expected_error_msg)
        self.assertFormError(response, 'form', 'email', expected_error_msg)
        response_form = response.form

    def teXXst_f_when_valid_form_is_submitted_reset_link_is_emailed(self):
        form = self.registration_page.form
        with (self.assertRaises(ObjectDoesNotExist)):
            User.objects.get(email='mojo@jojo.com')
        self.fill_in_form(form)
        response = form.submit().follow()
        user = User.objects.get(email='mojo@jojo.com')
        self.assertEqual(user.first_name, u"Mojo")
        self.assertEqual(user.last_name, u"Джоджо")
        self.assertFalse(user.is_active)

    def teXXst_f_when_valid_form_is_submitted_activation_email_is_sent(self):
        form = self.registration_page.form
        self.fill_in_form(form)
        response = form.submit()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn(u"mojo@jojo.com", msg.to)
        self.assertEqual(msg.subject, u"Mojo, activate your registration!")
        self.assertTemplateUsed(response, "reguser/activation_email_subject.txt")
        self.assertTemplateUsed(response, "reguser/activation_email_body.txt")


class RegistrationActivationTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        self.registration_page = self.app.get(reverse('test-registration'))
        self.set_default_form_values(first_name = u"Mojo", last_name = u"Jojo",
                email = u"mojo@jojo.com", password1 = u"moPass", password2 = u"moPass")
        self.form = self.registration_page.form
        self.fill_in_form(self.form)
        self.registration_response = self.form.submit()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.token = re.search('t=(.+?)\s', msg.body).group(1)
        self.activation_link = reverse('reguser-activate')

    def tXXest_f_invalid_activation_link(self):
        token = self.token+'xxx' # Mangle the signature
        response = self.app.get(self.activation_link, {'t': token}, status=404)
        self.assertEqual(response.status_int, 404)
        self.assertFalse(response.context['user'].is_authenticated())

    def teXXst_f_activation_successful(self):
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertFalse(user.is_active)
        response = self.app.get(self.activation_link, {'t': self.token}).follow()
        user = User.objects.get(email=u"mojo@jojo.com")
        self.assertTrue(user.is_active)
        self.assertFalse(response.context['user'].is_authenticated())
