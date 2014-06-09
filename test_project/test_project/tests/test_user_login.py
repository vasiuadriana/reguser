from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django_webtest import WebTest
import re

class LoginPageTestCase(WebTest):
    def setUp(self):
        self.user = User.objects.create_user("tmpuser", "tmpuser@test.com", "tmppass")
        self.user.is_active = True
        self.user.save()
        self.login_page = self.app.get(reverse('login'))
        self.login_form = self.login_page.form

    def test_f_user_can_access_login_page(self):
        self.assertTemplateUsed(self.login_page, "reguser/login.html")
        self.assertEqual(self.login_form.method.upper(), 'POST')
        self.assertTrue(self.login_form.action.endswith('/accounts/login/'))

    def test_f_user_login_successful_with_valid_credentials(self):
        self.assertIsNone(self.app.session.get('_auth_user_id'))
        form = self.login_form
        form['username'] = 'tmpuser@test.com'
        form['password'] = 'tmppass'
        response = form.submit()
        self.assertRedirects(response, reverse('reguser-profile'))
        self.assertEqual(self.app.session['_auth_user_id'], self.user.pk)

    def _ensure_incorrect_login(self, response, expected_error=None):
        self.assertTemplateUsed(response, "reguser/login.html")
        response_form = response.form
        expected_error = expected_error or u"Please enter a correct username and password. Note that both fields may be case-sensitive."
        response.mustcontain(expected_error)
        self.assertFormError(response, 'form', None, expected_error)
        # Ensure they're NOT logged in!
        self.assertIsNone(self.app.session.get('_auth_user_id'))
        return response_form

    def test_f_user_login_unsuccessful_with_wrong_password(self):
        self.assertIsNone(self.app.session.get('_auth_user_id'))
        form = self.login_form
        form['username'] = 'tmpuser@test.com'
        form['password'] = 'tmppaZs'
        response = form.submit()
        response_form = self._ensure_incorrect_login(response)
        self.assertEqual(response_form['username'].value, 'tmpuser@test.com')

    def test_f_user_login_unsuccessful_with_non_existing_user(self):
        self.assertIsNone(self.app.session.get('_auth_user_id'))
        form = self.login_form
        form['username'] = 'tmpuserZZ@test.com'
        form['password'] = 'tmppass'
        response = form.submit()
        response_form = self._ensure_incorrect_login(response)
        self.assertEqual(response_form['username'].value, 'tmpuserZZ@test.com')

    def test_f_user_login_unsuccessful_with_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        self.assertIsNone(self.app.session.get('_auth_user_id'))
        form = self.login_form
        form['username'] = 'tmpuser@test.com'
        form['password'] = 'tmppass'
        response = form.submit()
        response_form = self._ensure_incorrect_login(response, expected_error=u"This account is inactive.")
        self.assertEqual(response_form['username'].value, 'tmpuser@test.com')
