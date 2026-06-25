from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class MultiIdentifierBackend(ModelBackend):
    """
    Authenticates against email, phone_number, or nrc_number in addition to
    the standard username. Order tried: email → phone_number → nrc_number → username.
    Registered in AUTHENTICATION_BACKENDS before allauth's backend so it takes
    precedence when any of these identifiers match.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        user = (
            User.objects.filter(email__iexact=username).first()
            or User.objects.filter(phone_number=username).first()
            or User.objects.filter(nrc_number__iexact=username).first()
            or User.objects.filter(username__iexact=username).first()
        )

        if user is None:
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
