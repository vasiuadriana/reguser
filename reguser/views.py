from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset, password_reset_confirm
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


def reguser_activate(request, login_on_activation=False, next='/'):
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
    if login_on_activation:
        from django.conf import settings
        user = authenticate(username=user.email, password=user.password, passwordless=True)
        if user:
            login(request, user)
    return redirect(next)


def reguser_password_reset(request, template='reguser/password_reset_form.html',
        email_template = 'reguser/password_reset_email.html',
        email_subject_template = 'reguser/password_reset_subject.txt', next='login'):
    return password_reset(request, template_name=template, 
            email_template_name=email_template, subject_template_name=email_subject_template,
            post_reset_redirect=reverse(next))

def reguser_password_reset_confirm(request, uidb36=None, token=None,
        template = 'reguser/password_reset_confirm.html', next='login'):
    return password_reset_confirm(request, template_name=template, 
            uidb36=uidb36, token=token, post_reset_redirect=reverse(next))


def reguser_profile(request, profile_model=None):  #pragma: nocover
    user = request.user
    profile = None
    if profile_model:
        profile = profile_model.objects.get(user=user)
    if request.method == 'POST':
        # edit profile
        return redirect('reguser-profile')
    else:
        return render(request, 'reguser/edit_profile.html', {
            'user': user, 'profile': profile})
