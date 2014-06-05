import re
from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from reguser.utils import generate_username

class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which is only valid if no User has that email.
    """
    def validate(self, value):
        from django.contrib.auth import get_user_model
        USER = get_user_model()
        super(forms.EmailField, self).validate(value)
        if USER.objects.filter(email=value).count() > 0:
            raise forms.ValidationError(_("A user with this e-mail address already exists."))

class ExtendedUserCreationForm(UserCreationForm):
    """
    Extends the built in UserCreationForm in several ways:
    
    * Adds an email field, which uses the custom UniqueUserEmailField,
      that is, the form does not validate if the email address already exists
      in the User table.
    * The username field is generated based on the email, and isn't visible.
    * first_name and last_name fields are added.
    * Data not saved by the default behavior of UserCreationForm is saved.
    """
    
    username = forms.CharField(required = False, max_length = 30)
    email = UniqueUserEmailField(required = True, label = _("e-Mail address"))
    first_name = forms.CharField(required = True, max_length = 30, label=_("First name"))
    last_name = forms.CharField(required = True, max_length = 30, label=_("Last name"))
    
    class Meta:
        from django.contrib.auth import get_user_model
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'username']

    def __init__(self, *args, **kwargs):
        """
        Changes the order of fields, and removes the username field.
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """
        Normal cleanup + username generation.
        """
        cleaned_data = super(UserCreationForm, self).clean(*args, **kwargs)
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = generate_username(cleaned_data['email'])
        return cleaned_data
        
    def save(self, commit=True):
        """
        Saves the email, first_name and last_name properties, after the normal
        save behavior is complete.
        """
        user = super(UserCreationForm, self).save(commit)
        if user:
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
        return user

