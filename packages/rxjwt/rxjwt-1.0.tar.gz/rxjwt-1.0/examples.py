"""
File with examples.
"""

from .utils import generate_secret
from .token import AccessToken
if __name__ == "__main__":
    SECRET = generate_secret()
    token = str(AccessToken.generate(payload={"a": "b"}, secret=SECRET))
    print(AccessToken(token).verify(secret=SECRET))


    class UserAccessToken(AccessToken):

        @classmethod
        def for_user(cls, user_id, secret=SECRET):
            return cls.generate({"user_id": user_id}, secret)


    user_token = UserAccessToken.for_user(100)
    print(user_token, user_token.verify(SECRET), user_token.get_payload())
