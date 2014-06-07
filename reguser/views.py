from django.shortcuts import render, redirect
from reguser.forms import ExtendedUserCreationForm

def registration(request, whitelist=[], template='registration_form.html'):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST, ALLOWED_EMAIL_DOMAINS=whitelist)
        if form.is_valid():
            return redirect('/')
    else:
        form = ExtendedUserCreationForm(ALLOWED_EMAIL_DOMAINS=whitelist)
    context = {'form': form}
    return render(request, 'reguser/' + template, context)
