from django.shortcuts import render, redirect
from reguser.forms import ExtendedUserCreationForm

def registration(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            return redirect('/')
    else:
        form = ExtendedUserCreationForm()
    context = {'form': form}
    return render(request, 'reguser/registration_form.html', context)
