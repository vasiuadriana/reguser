# -*- coding: utf-8 -*-
from django_webtest import WebTest
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from lunchbag.testutils import WebtestHelperMixin
import re

class PasswordResetTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        self.password_reset_page = self.app.get(reverse('password-reset'))
        self.form = self.password_reset_page.form
        self.user = User.objects.create_user("tmpuser", "tmpuser@test.com", "tmppass")
        self.user.is_active = True
        self.user.save()

    def test_f_password_reset_url_returns_password_reset_form(self):
        self.password_reset_page.mustcontain('Password reset', 'POST', 'Send link', 
                'csrfmiddlewaretoken', no=['error'])
        self.assertEqual(self.form.method, 'POST')
        self.assertEqual(self.form.action, reverse('password-reset'))
        self.assertTrue(set([u'csrfmiddlewaretoken', u'email']) < set(self.form.fields))

    def test_f_missing_required_fields_in_registration_form(self):
        self.form['email'] = ''
        response = self.form.submit()
        expected_error_msg = "This field is required."
        response.mustcontain('error', expected_error_msg)
        self.assertFormError(response, 'form', 'email', expected_error_msg)

    def test_f_when_valid_form_is_submitted_reset_link_is_emailed(self):
        self.form['email'] = 'tmpuser@test.com'
        response = self.form.submit()
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn(u"tmpuser@test.com", msg.to)
        self.assertEqual(msg.subject, u"Your password reset link")
        self.assertTemplateUsed(response, "reguser/password_reset_subject.txt")
        self.assertTemplateUsed(response, "reguser/password_reset_email.html")


class PasswordResetConfirmActivationTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        self.password_reset_page = self.app.get(reverse('password-reset'))
        self.form = self.password_reset_page.form
        self.user = User.objects.create_user("tmpuser", "tmpuser@test.com", "tmppass")
        self.user.is_active = True
        self.user.save()
        self.form['email'] = 'tmpuser@test.com'
        response = self.form.submit().follow()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn(u"tmpuser@test.com", msg.to)
        self.uidb64, self.token = re.search('confirm\/(.+?)\/', msg.body).group(1).split('-', 1)
        self.reset_link = reverse('password-reset-confirm', kwargs={'uidb64':self.uidb64, 'token':self.token})

    def test_f_invalid_activation_link(self):
        token = self.token+'xxx' # Mangle the signature
        self.reset_link = reverse('password-reset-confirm', kwargs={'uidb64':self.uidb64, 'token':token})
        response = self.app.get(self.reset_link)
        response.mustcontain("This reset link is no longer valid.", no=['form', 'submit'])

    def test_f_activation_successful(self):
        response = self.app.get(self.reset_link)
        response.mustcontain('Password reset', 'POST', 'Reset', 
                'csrfmiddlewaretoken', no=['error'])
        form = response.form
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.action, '.')
        self.assertTrue(set([u'csrfmiddlewaretoken', 'new_password1', 'new_password2']) < set(form.fields))
        auth_user = authenticate(username='tmpuser@test.com', password='tmppass')
        self.assertEqual(auth_user, self.user)
        form['new_password1'] = 'newPass'
        form['new_password2'] = 'newPass'
        response = form.submit().follow()
        auth_user = authenticate(username='tmpuser@test.com', password='tmppass')
        self.assertIsNone(auth_user)
        auth_user = authenticate(username='tmpuser@test.com', password='newPass')
        self.assertEqual(auth_user, self.user)
