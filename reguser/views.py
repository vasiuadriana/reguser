from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature
from django.http import HttpResponse, Http404
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
            helper.email_activation_link(get_current_site(request), user, activation_url_name)
            return redirect(next)
    else:
        form = ExtendedUserCreationForm(ALLOWED_EMAIL_DOMAINS=whitelist)
    context = {'form': form}
    return render(request, 'reguser/' + template, context)

def activate(request, next='/'):
    token = request.GET.get('t')
    helper = ReguserHelper()
    try:
        user = helper.validate_activation_token(token)
    except BadSignature:
        raise Http404
    except ObjectDoesNotExist:
        return render(request, 'reguser/activation_expired.html', {})
    if not user:
        return render(request, 'reguser/already_active.html', {})
    return redirect(next)
