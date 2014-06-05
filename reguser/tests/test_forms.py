from django.test import TestCase
from django import forms
from reguser.forms import UniqueUserEmailField, ExtendedUserCreationForm

class UniqueEmailFieldTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.field = UniqueUserEmailField
        self.USER_MODEL = get_user_model()

    def test_unique_email_field_checks_for_valid_email(self):
        self.assertFieldOutput(self.field, {'a@a.com': 'a@a.com'}, {'aaa': [u'Enter a valid email address.']})

    def test_unique_email_field_validates_email_uniqueness(self):
        self.USER_MODEL.objects.create_user('test', 'test@me.com', 'passwd')
        self.assertFieldOutput(self.field, {'unique@me.com': 'unique@me.com'}, 
                {'test@me.com': [u'A user with this e-mail address already exists.']})

class ExtendedUserCreationFormTestCase(TestCase):

    def test_form_is_valid_for_valid_input(self):
        data = {'email': 'test@me.com',
                'first_name': 'Test',
                'last_name': 'Me',
                'password1': 'myPass',
                'password2': 'myPass'}
        form = ExtendedUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_validation_fails_for_invalid_email(self):
        data = {'email': 'testme.com',
                'first_name': 'Test',
                'last_name': 'Me',
                'password1': 'myPass',
                'password2': 'myPass'}
        form = ExtendedUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_validation_fails_for_mismatched_passwords(self):
        data = {'email': 'test@me.com',
                'first_name': 'Test',
                'last_name': 'Me',
                'password1': 'myPass1',
                'password2': 'myPass2'}
        form = ExtendedUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
