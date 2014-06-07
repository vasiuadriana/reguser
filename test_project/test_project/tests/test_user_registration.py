from django_webtest import WebTest
from django.core.urlresolvers import reverse

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
        response.mustcontain('error', 'This field is required.')
        response_form = response.form
        self.assertEqual(response_form['first_name'].value, 'Mojo')

    def test_f_invalid_email_in_registration_form(self):
        form = self.registration_page.form
        form['email'] = 'mojojojo.com'
        response = form.submit()
        response.mustcontain('error', 'Enter a valid email address.')
        response_form = response.form
        self.assertEqual(response_form['email'].value, 'mojojojo.com')

    def test_f_email_not_in_whitelist_for_registration_form(self):
        registration_whitelist_page = self.app.get(reverse('test-registration-whitelist'))
        form = registration_whitelist_page.form
        form['email'] = 'mojo@jojo.com'
        response = form.submit()
        response.mustcontain('error', 'Only e-mail addresses from the following domains are allowed: test.com')
        response_form = response.form
        self.assertEqual(response_form['email'].value, 'mojo@jojo.com')
