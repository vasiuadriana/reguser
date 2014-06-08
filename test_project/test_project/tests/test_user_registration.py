from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

class RegistrationTestCase(WebTest):
    def setUp(self):
        self.registration_page = self.app.get(reverse('test-registration'))

    def test_f_registration_url_returns_registration_form(self):
        self.registration_page.mustcontain('Registration Form', 'Register', 'POST', 
                'csrfmiddlewaretoken', no=['error'])
        form = self.registration_page.form
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.action, '.')
        self.assertTrue(set([u'csrfmiddlewaretoken', u'first_name', u'last_name',
            u'email', u'password1', u'password2']) < set(form.fields))

    def test_f_missing_required_fields_in_registration_form(self):
        form = self.registration_page.form
        form['first_name'] = 'Mojo'
        response = form.submit()
        expected_error_msg = "This field is required."
        response.mustcontain('error', expected_error_msg)
        for field in ['last_name', 'email', 'password1', 'password2']:
            self.assertFormError(response, 'form', field, expected_error_msg)
        response_form = response.form
        self.assertEqual(response_form['first_name'].value, 'Mojo')

    def test_f_invalid_email_in_registration_form(self):
        form = self.registration_page.form
        form['email'] = 'mojojojo.com'
        response = form.submit()
        expected_error_msg = "Enter a valid email address."
        response.mustcontain('error', expected_error_msg)
        self.assertFormError(response, 'form', 'email', expected_error_msg)
        response_form = response.form
        self.assertEqual(response_form['email'].value, 'mojojojo.com')

    def test_f_email_not_in_whitelist_for_registration_form(self):
        registration_whitelist_page = self.app.get(reverse('test-registration-whitelist'))
        form = registration_whitelist_page.form
        form['email'] = 'mojo@jojo.com'
        response = form.submit()
        expected_error_msg = u"Only e-mail addresses from the following domains are allowed: test.com"
        response.mustcontain('error', expected_error_msg)
        self.assertFormError(response, 'form', 'email', expected_error_msg)
        response_form = response.form
        self.assertEqual(response_form['email'].value, 'mojo@jojo.com')

    def test_f_using_custom_registration_form_template(self):
        registration_page = self.app.get(reverse('test-cherry-registration'))
        registration_page.mustcontain('Cherry User Registration', 'Registration Form', 'Register', 'POST', 
                'csrfmiddlewaretoken', no=['error'])

    def test_f_when_valid_form_is_submitted_inactive_user_is_created(self):
        form = self.registration_page.form
        with (self.assertRaises(ObjectDoesNotExist)):
            User.objects.get(email='mojo@jojo.com')
        form['first_name'] = 'Mojo'
        form['last_name'] = 'Jojo'
        form['email'] = 'mojo@jojo.com'
        form['password1'] = 'moPass'
        form['password2'] = 'moPass'
        response = form.submit().follow()
        user = User.objects.get(email='mojo@jojo.com')
        self.assertEqual(user.first_name, 'Mojo')
        self.assertEqual(user.last_name, 'Jojo')
        self.assertFalse(user.is_active)

    def test_f_when_valid_form_is_submitted_inactive_user_is_created_with_group(self):
        vip_page = self.app.get(reverse('test-vip-registration'))
        form = vip_page.form
        with (self.assertRaises(ObjectDoesNotExist)):
            User.objects.get(email='m@jojo.com')
        form['first_name'] = 'Mojo'
        form['last_name'] = 'Jojo'
        form['email'] = 'm@jojo.com'
        form['password1'] = 'moPass'
        form['password2'] = 'moPass'
        response = form.submit().follow()
        user = User.objects.get(email='m@jojo.com')
        self.assertEqual(user.first_name, 'Mojo')
        self.assertEqual(user.last_name, 'Jojo')
        self.assertFalse(user.is_active)
        expected_group = Group.objects.get(name='VIP')
        self.assertIn(expected_group, user.groups.all())
