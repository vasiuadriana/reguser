from django.shortcuts import render

def home(request):
    from django.contrib.auth import get_user_model
    USER_MODEL = get_user_model()
    return render(request, 'index.html', {
        'users': USER_MODEL.objects.all(),
        })
