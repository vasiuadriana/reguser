from django.db import transaction
from django.core.signing import Signer, BadSignature

class ReguserHelper(object):
    def __init__(self):
        from django.contrib.auth import get_user_model
        self.USER_MODEL = get_user_model()
        self.signer = Signer(salt='reguser') # do not change

    @transaction.atomic
    def create_inactive_user(self, username, email, password):
        """ Creates a new inactive user and returns a signed activation token """
        user = self.USER_MODEL.objects.create_user(username, email, password)
        user.is_active = False
        user.save()
        return self.signer.sign(user.pk)

    def validate_activation_token(self, token):
        """ Activates the user and returns the user object if the token is valid. 
        Otherwise, returns None. """
        try:
            user_pk = self.signer.unsign(token)
        except BadSignature:
            return None
        try:
            user = self.USER_MODEL.objects.get(user_pk)
            if user.is_active: return None
            user.is_active = True
            user.save()
            return user
        except self.USER_MODEL.DoesNotExist:
            return None