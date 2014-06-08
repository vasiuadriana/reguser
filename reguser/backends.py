from django.contrib.auth.models import check_password

class EmailAuthBackend(object):
    def authenticate(self, username=None, password=None, passwordless=False):
        from django.contrib.auth import get_user_model
        USER_MODEL = get_user_model()
        try:
            user = USER_MODEL.objects.get(email=username)
            if passwordless or user.check_password(password):
                return user
        except USER_MODEL.DoesNotExist:
            return None

    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        USER_MODEL = get_user_model()
        try:
            return USER_MODEL.objects.get(pk=user_id)
        except USER_MODEL.DoesNotExist:
            return None
