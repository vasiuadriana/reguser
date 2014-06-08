from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateField()

    def __unicode__(self):
        return u"{} ({})".format(self.user.get_full_name, self.user.username)
