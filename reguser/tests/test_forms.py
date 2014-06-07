from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
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
    
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.field = UniqueUserEmailField
        self.USER_MODEL = get_user_model()

    def get_form_data(*args, **kwargs):
        data = {'email': 'test@me.com',
                'first_name': 'Test',
                'last_name': 'Me',
                'password1': 'myPass',
                'password2': 'myPass'}
        data.update(**kwargs)
        return data

    def test_form_is_valid_for_valid_input(self):
        form = ExtendedUserCreationForm(data=self.get_form_data())
        self.assertTrue(form.is_valid())

    def test_form_is_valid_for_valid_input_with_whitelist(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(), ALLOWED_EMAIL_DOMAINS=['other.com', 'me.com'])
        self.assertTrue(form.is_valid())

    def test_form_is_valid_for_valid_input_with_whitelist_subdomain(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email="jojo@find.me.com"), ALLOWED_EMAIL_DOMAINS=['.me.com', '.other.com'])
        self.assertTrue(form.is_valid())
    
    def test_form_is_valid_for_valid_input_with_whitelist_hidden_domain(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email="jojo@hide.com"), ALLOWED_EMAIL_DOMAINS=['hide.com!', 'me.com'])
        self.assertTrue(form.is_valid())

    def test_form_is_valid_for_valid_input_with_whitelist_hidden_subdomain(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email="jojo@i.hide.com"), ALLOWED_EMAIL_DOMAINS=['.hide.com!', 'me.com'])
        self.assertTrue(form.is_valid())

    def test_valid_form_generates_username(self):
        form = ExtendedUserCreationForm(data=self.get_form_data())
        self.assertTrue(form.is_valid())
        self.assertIn('username', form.cleaned_data)
        self.assertTrue(len(form.cleaned_data['username']) > 1)

    def test_form_validation_fails_for_invalid_email(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email='testme.com'))
        self.assertFalse(form.is_valid())
        self.assertIn(u"Enter a valid email address.", form.errors['email'])

    def test_form_validation_fails_for_email_not_in_whitelist(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email='test@me.com'), ALLOWED_EMAIL_DOMAINS=['allowed.com', 'allowed2.com'])
        self.assertFalse(form.is_valid())
        self.assertIn(u"Only e-mail addresses from the following domains are allowed: allowed.com, allowed2.com", form.errors['email'])
    
    def test_hidden_whitelist_domain_not_shown_in_error_message(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email='test@not.allowed.com'), ALLOWED_EMAIL_DOMAINS=['allowed.com', 'hidden.com!'])
        self.assertFalse(form.is_valid())
        self.assertIn(u"Only e-mail addresses from the following domains are allowed: allowed.com", form.errors['email'])
    
    def test_form_validation_fails_for_email_not_in_whitelist_2(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email='test@me.com'), ALLOWED_EMAIL_DOMAINS=['.allowed.com'])
        self.assertFalse(form.is_valid())
        self.assertIn(u"Only e-mail addresses from the following domains are allowed: .allowed.com", form.errors['email'])

    def test_form_validation_fails_for_email_subdomain_not_in_whitelist(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(email='test@me.allowed.com'), ALLOWED_EMAIL_DOMAINS=['allowed.com'])
        self.assertFalse(form.is_valid())
        self.assertIn(u"Only e-mail addresses from the following domains are allowed: allowed.com", form.errors['email'])

    def test_form_validation_fails_for_duplicate_email(self):
        self.USER_MODEL.objects.create_user('test', 'existing@me.com', 'passwd')
        form = ExtendedUserCreationForm(data=self.get_form_data(email='existing@me.com'))
        self.assertFalse(form.is_valid())
        self.assertIn(u"A user with this e-mail address already exists.", form.errors['email'])

    def test_form_validation_fails_for_mismatched_passwords(self):
        form = ExtendedUserCreationForm(data=self.get_form_data(password2='myPass2'))
        self.assertFalse(form.is_valid())
        self.assertIn(u"The two password fields didn't match.", form.errors['password2'])

    def test_valid_form_creates_user_when_saved(self):
        data = self.get_form_data()
        form = ExtendedUserCreationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        retrieved_user = self.USER_MODEL.objects.get(pk=user.pk)
        self.assertEqual(retrieved_user.email, data['email'])
        self.assertEqual(retrieved_user.first_name, data['first_name'])
        self.assertEqual(retrieved_user.last_name, data['last_name'])
        self.assertTrue(len(retrieved_user.username) > 1)

    def test_valid_form_does_not_save_user_when_commit_is_false(self):
        data = self.get_form_data()
        form = ExtendedUserCreationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue(len(user.username) > 1)
        with self.assertRaises(ObjectDoesNotExist):
            self.USER_MODEL.objects.get(username=user.username)
