from django.test import TestCase
from django import forms
from reguser.forms import UniqueUserEmailField

class UniqueEmailFieldTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.field = UniqueUserEmailField()
        self.USER_MODEL = get_user_model()

    def test_unique_email_field_fails_validation_with_duplicate_emails(self):
        self.USER_MODEL.objects.create_user('test', 'test@me.com', 'passwd')
        with self.assertRaises(forms.ValidationError):
            self.field.validate('test@me.com')

    def test_unique_email_field_validates_with_unique_email(self):
        unique_email = 'unique@me.com'
        try:
            self.field.validate(unique_email)
        except forms.ValidationError:
            self.fail('Unique e-mail {} does not pass validation!'.format(unique_email))
