from django.test import TestCase
from django import forms
from reguser.forms import UniqueUserEmailField

class UniqueEmailFieldTestCase(TestCase):
    def setUp(self):
        self.field = UniqueUserEmailField()

    def test_unique_email_field_fails_validation_with_duplicate_emails(self):
        self.field.validate()
