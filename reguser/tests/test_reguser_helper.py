from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from reguser.models import ReguserHelper

class ReguserHelperTestCase(TestCase):
    def setUp(self):
        self.helper = ReguserHelper()

    def test_helper_creates_inactive_model(self):
        token = self.helper.create_inactive_user('mojojojo', 'mojo@jojo.hum', 'sikrit')
        user_id = ReguserHelper().signer.unsign(token) # Unsign with a new signer, just to be sure
        try:
            new_user = self.helper.USER_MODEL.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            self.fail("User object not created for user id: {}".format(user_id))
        self.assertFalse(new_user.is_active)


