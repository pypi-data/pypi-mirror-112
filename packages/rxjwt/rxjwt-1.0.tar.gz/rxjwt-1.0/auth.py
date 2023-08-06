from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .token import UserAccessToken as DefaultUserAceessToken
from .utils import import_class

try:
    UserAccessToken = import_class(settings.RXJWT["ACCESS_TOKEN_CLASS"])
except (ImportError, KeyError):
    UserAccessToken = DefaultUserAceessToken


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return None
        if not len(auth_header.split()):
            raise AuthenticationFailed({"error": "invalid-header",
                                        "detail": "Invalid authentication header."})
        auth_type, auth_token = auth_header.split()
        if auth_type != "Token":
            raise AuthenticationFailed({"error": "invalid-header",
                                        "detail": "Invalid authentication header."})
        user_access_token = UserAccessToken(auth_token)
        if not user_access_token.verify(settings.SECRET_KEY):
            raise AuthenticationFailed(
                {"error": "invalid-token",
                 "detail": "The token is either invalid or expired, or the token's"
                           " owner is not found."})
        current_user = user_access_token.get_user()
        try:
            soft_delete_attr = settings.RXJWT["SOFT_DELETE_ATTR"]
        except KeyError:
            soft_delete_attr = "datetime_removed"
        if hasattr(current_user, soft_delete_attr) and getattr(current_user,
                                                               soft_delete_attr) is not None:
            raise AuthenticationFailed(
                {"error": "invalid-token",
                 "detail": "The token is either invalid or expired, or the token's"
                           " owner is not found."})
        current_user.save()
        return current_user, str(user_access_token)
