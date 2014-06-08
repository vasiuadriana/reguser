from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse
from reguser.forms import ExtendedUserCreationForm
from reguser.models import ReguserHelper

def registration(request, whitelist=[], template='registration_form.html', 
        activation_url_name='reguser-activate', groups=[], next='/'):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST, ALLOWED_EMAIL_DOMAINS=whitelist)
        if form.is_valid():
            helper = ReguserHelper()
            user = helper.create_inactive_user(form.cleaned_data['username'],
                    form.cleaned_data['email'], form.cleaned_data['password1'], groups=groups, 
                    attrs = {'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name']})
            activation_link = reverse(activation_url_name) + '?t=' + user.activation_token
            subject = render_to_string('reguser/activation_email_subject.txt', {'user': user}).strip()
            msg = render_to_string('reguser/activation_email_body.txt', {'user': user, 
                                                'activation_link': activation_link})
            user.email_user(subject, msg)
            return redirect(next)
    else:
        form = ExtendedUserCreationForm(ALLOWED_EMAIL_DOMAINS=whitelist)
    context = {'form': form}
    return render(request, 'reguser/' + template, context)

def activate(request):
    return HttpResponse('ok')
