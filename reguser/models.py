from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import Signer, BadSignature
from django.template.loader import render_to_string
from django.contrib.auth.models import Group

class ReguserHelper(object):
    def __init__(self):
        from django.contrib.auth import get_user_model
        self.USER_MODEL = get_user_model()
        self.signer = Signer(salt='reguser') # do not change

    @transaction.atomic
    def create_inactive_user(self, username, email, password, groups=[], attrs={}):
        """ Creates a new inactive user and assings the supplied groups, if any. 
        Generates a signed activation token """
        user = self.USER_MODEL.objects.create_user(username, email, password)
        user.is_active = False
        for k,v in attrs.iteritems():
            setattr(user, k, v)
        user.save()
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            group.user_set.add(user)
        user.activation_token = self.signer.sign(user.username)
        return user

    def email_activation_link(self, site, user, activation_url_name='reguser-activate'):
        """ Sends an e-mail to the user, containing their secure activation link. """
        from django.core.urlresolvers import reverse
        activation_link = reverse(activation_url_name) + '?t=' + user.activation_token
        subject = render_to_string('reguser/activation_email_subject.txt', 
                {'user': user, 'site': site}).strip()
        msg = render_to_string('reguser/activation_email_body.txt', {'user': user, 
                'site': site, 'activation_link': activation_link})
        user.email_user(subject, msg)

    def validate_activation_token(self, token):
        """ Activates the user and returns the user object if the token is valid. 
        Raises BadSignature if the token is invalid. Raises ObjectDoesNotExist 
        if no user with the decoded ID exists in the database. Returns None if 
        the user exists but is already active. """
        user = self.USER_MODEL.objects.get(username=self.signer.unsign(token))
        if user.is_active: return None
        user.is_active = True
        user.save()
        return user
