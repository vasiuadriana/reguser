from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature
from reguser.models import ReguserHelper

class ReguserHelperTestCase(TestCase):
    def setUp(self):
        self.helper = ReguserHelper()
        self.helper2 = ReguserHelper()
        self.token = self.helper.create_inactive_user('mojojojo', 'mojo@jojo.hum', 'sikrit')
        self.token_parts = self.token.partition(':')
        self.assertEqual(len(self.token_parts), 3)

    def test_helper_creates_inactive_user(self):
        user_id = ReguserHelper().signer.unsign(self.token) # Unsign with a new signer, just to be sure
        new_user = self.helper.USER_MODEL.objects.get(pk=user_id)
        self.assertFalse(new_user.is_active)

    def test_helper_sets_extra_attributes_on_user(self):
        token = self.helper.create_inactive_user('mojojojo2', 'mojo@jojo.hum', 'sikrit', 
                first_name='Mojo', last_name='Jojo')
        user_id = ReguserHelper().signer.unsign(token)
        new_user = self.helper.USER_MODEL.objects.get(pk=user_id)
        self.assertFalse(new_user.is_active)
        self.assertEqual(new_user.first_name, 'Mojo')
        self.assertEqual(new_user.last_name, 'Jojo')

    def test_validate_raises_exception_with_tampered_user_id(self):
        parts = self.token_parts
        # Mangle the user ID
        bad_token_1 = ''.join([str(int(parts[0])+1), parts[1], parts[2]])
        with self.assertRaises(BadSignature):
            user = self.helper2.validate_activation_token(bad_token_1)
        
    def test_validate_raises_exception_with_tampered_signature(self):
        parts = self.token_parts
        # Mangle the signature
        bad_token_2 = ''.join([parts[0], parts[1], parts[2][::-1]])
        with self.assertRaises(BadSignature):
            user = self.helper2.validate_activation_token(bad_token_2)

    def test_validate_raises_exception_with_tampered_separator(self):
        parts = self.token_parts
        # Mangle the separator
        bad_token_3 = ''.join([parts[0], '', parts[2]])
        with self.assertRaises(BadSignature):
            user = self.helper2.validate_activation_token(bad_token_3)

    def test_validate_raises_exception_if_user_does_not_exist(self):
        self.helper.USER_MODEL.objects.get(pk=self.token_parts[0]).delete()
        with self.assertRaises(ObjectDoesNotExist):
            user = self.helper2.validate_activation_token(self.token)

    def test_validate_returns_none_if_user_already_active(self):
        user = 'no-user'
        self.helper.USER_MODEL.objects.filter(pk=self.token_parts[0]).update(is_active=True)
        user = self.helper2.validate_activation_token(self.token)
        self.assertIsNone(user)

    def test_validate_activates_user_if_token_is_valid(self):
        user = self.helper2.validate_activation_token(self.token)
        self.assertEqual(str(user.pk), self.token_parts[0])
        self.assertTrue(user.is_active)
