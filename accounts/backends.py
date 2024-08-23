from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None

        if email:
            try:
                user = UserModel.objects.get(email=email)
            except ObjectDoesNotExist:
                return None
        elif username:
            try:
                user = UserModel.objects.get(username=username)
            except ObjectDoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
