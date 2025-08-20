from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Allow authentication with either email or username.
        Django passes the first credential as `username` by convention.
        """
        identifier = username or kwargs.get(UserModel.USERNAME_FIELD)
        if not identifier or not password:
            return None

        # Try by email first
        user = None
        try:
            user = UserModel.objects.get(email__iexact=identifier)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username__iexact=identifier)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', False)

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None