# -*- coding: utf-8 -*-
from django_webtest import WebTest
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from lunchbag.testutils import WebtestHelperMixin
import re

class PasswordChangeTestCase(WebTest, WebtestHelperMixin):
    def setUp(self):
        self.user = User.objects.create_user("tmpuser", "tmpuser@test.com", "tmppass")
        self.user.is_active = True
        self.user.save()
        self.password_change_page = self.app.get(reverse('password-change'), user="tmpuser")
        self.form = self.password_change_page.form

    def test_f_password_change_url_returns_password_change_form(self):
        self.password_change_page.mustcontain('Password change', 'POST', 'Change password', 
                'csrfmiddlewaretoken', no=['error'])
        self.assertEqual(self.form.method, 'POST')
        self.assertEqual(self.form.action, reverse('password-change'))
        self.assertTrue(set(['csrfmiddlewaretoken', 'old_password', 'new_password1', 'new_password2']) < set(self.form.fields))

    def test_f_when_valid_form_is_submitted_user_password_has_changed(self):
        auth_user = authenticate(username='tmpuser@test.com', password='tmppass')
        self.assertEqual(auth_user, self.user)
        form = self.form
        form['old_password'] = 'tmppass'
        form['new_password1'] = 'newPass'
        form['new_password2'] = 'newPass'
        response = form.submit()
        self.assertRedirects(response, reverse('login'))
        auth_user = authenticate(username='tmpuser@test.com', password='tmppass')
        self.assertIsNone(auth_user)
        auth_user = authenticate(username='tmpuser@test.com', password='newPass')
        self.assertEqual(auth_user, self.user)
