from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import Signer, BadSignature

class ReguserHelper(object):
    def __init__(self):
        from django.contrib.auth import get_user_model
        self.USER_MODEL = get_user_model()
        self.signer = Signer(salt='reguser') # do not change

    @transaction.atomic
    def create_inactive_user(self, username, email, password, **kwargs):
        """ Creates a new inactive user and returns a signed activation token """
        user = self.USER_MODEL.objects.create_user(username, email, password)
        user.is_active = False
        for k,v in kwargs.iteritems():
            setattr(user, k, v)
        user.save()
        return self.signer.sign(user.pk)

    def validate_activation_token(self, token):
        """ Activates the user and returns the user object if the token is valid. 
        Raises BadSignature if the token is invalid. Raises ObjectDoesNotExist 
        if no user with the decoded ID exists in the database. Returns None if 
        the user exists but is already active. """
        user_pk = self.signer.unsign(token)
        user = self.USER_MODEL.objects.get(pk=user_pk)
        if user.is_active: return None
        user.is_active = True
        user.save()
        return user
