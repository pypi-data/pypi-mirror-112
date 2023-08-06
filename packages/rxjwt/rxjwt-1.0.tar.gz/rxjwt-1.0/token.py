import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime, timedelta
from hashlib import sha512
from json import dumps as json_encode, loads as json_decode

from django.contrib.auth import get_user_model

from .exceptions import IncorrectTokenHeaderException, IncorrectTokenPayloadException, \
    InvalidAlgorithmException
from .models import ExpiredToken
from .utils import string_as_base64


class Token:
    """
    The abstract token class. This class is not intended to be instantiated. You
    must extend this class (as it is done in AccessToken and RefreshToken) in
    order to create jwt of your own type
    """

    SEPARATOR = "."

    HASH_ALGORITHMS = {
        "HS512": sha512,
        # Other algorithms may be here
    }

    def __init__(self, string: str):
        """
        The constructor. It calls get_type() just to check that it is implemented
        and prevent raw Token objects from being created.
        :param string: The token string
        """
        self.get_type()
        self.string = string
        self.__header = None
        self.__payload = None
        self.__signature = None
        self.__header_dict = None
        self.__payload_dict = None
        self.__is_correct = False
        self.payload = None
        try:
            self.__header, self.__payload, self.__signature = (bytes(i, "utf-8")
                                                               for i in
                                                               self.string.split(self.SEPARATOR))
            self.__header_dict, self.__payload_dict = (json_decode(urlsafe_b64decode(i))
                                                       for i in (self.__header, self.__payload))
            self.__is_correct = True
            self.payload = self.__payload_dict
        except ValueError or UnicodeDecodeError:
            self.__is_correct = False

    @classmethod
    def get_type(cls) -> str:
        """
        Returns the type of the token (as string which will be used in payload
        creation).
        :return: The token type.
        """
        raise NotImplementedError()

    @classmethod
    def get_lifetime(cls) -> timedelta:
        """
        Returns the lifetime of the token.
        :return: The lifetime of the token as timedelta object.
        """
        raise NotImplementedError()

    @classmethod
    def get_algorithm(cls) -> str:
        """
        Returns the hashing algorithm of the token. Possible algorithms are
        listed in HASH_ALGORITHMS
        :return: The hashing algorithm.
        """
        raise NotImplementedError

    @classmethod
    def get_hashing_function(cls, algorithm=None) -> callable:
        """
        Returns a hashing function for given algorithm.
        Raises an exception if given algorithm is not supported.
        :return: None
        """
        if algorithm is None:
            algorithm = cls.get_algorithm()
        if algorithm not in cls.HASH_ALGORITHMS:
            raise InvalidAlgorithmException(algorithm, cls.HASH_ALGORITHMS)
        return cls.HASH_ALGORITHMS[algorithm]

    @classmethod
    def generate_header(cls) -> bytes:
        """
        Generates the JWT header. This is a dictionary which contains two keys:
        "typ" (the token type, this is always "jwt") and "alg" (the hashing
        algorithm).
        :return: Generated header as base64-encoded bytes
        """
        return string_as_base64(json_encode({
            "typ": "jwt",
            "alg": cls.get_algorithm()
        }))

    @classmethod
    def process_payload(cls, payload=None) -> bytes:
        """
        Processes the JWT payload. Adds "exp" and "ttp" keys to the payload
        :param payload: The payload to process.
        :return: The processed payload.
        """
        if payload is None:
            payload = {}
        payload["exp"] = str(datetime.utcnow() + cls.get_lifetime())
        payload["ttp"] = cls.get_type()
        return string_as_base64(json_encode(payload))

    @classmethod
    def generate_signature(cls, header, payload, secret, algorithm=None) -> bytes:
        """
        Generates the JWT signature. A signature is a hashed string xxx.yyy where
        xxx is the JWT header and yyy is the JWT payload. A JWT payload is a JSON
        object which contains data stored in the JWT.
        :return: The signature as base64.
        """
        if isinstance(secret, str):
            secret = bytes(secret, "utf-8")
        hash_function = cls.get_hashing_function(algorithm)
        signature_payload = bytes("{}{}{}".format(header, cls.SEPARATOR, payload),
                                  "utf-8")
        return urlsafe_b64encode(
            hmac.new(secret, signature_payload, hash_function).digest()
        )

    @classmethod
    def generate(cls, payload: dict = None, secret: bytes = None):
        """
        Generates the JWT token using given payload, token type and algorithm.
        :return: The JWT token as object (of corresponding class,
        if you called AccessToken.generate() you will get an AccessToken object),
        JWT token parts are separated by dot.
        """
        if cls.__name__ == __class__.__name__:
            raise NotImplementedError()
        if secret is None:
            raise ValueError("Secret must not be None")
        header = cls.generate_header()
        payload = cls.process_payload(payload)
        signature = cls.generate_signature(header, payload, secret)
        return cls(cls.SEPARATOR.join(
            (e.decode("utf-8") for e in (header, payload, signature))
        ))

    def verify(self, secret) -> bool:
        """
        Verifies the token using given secret. This method will check that:
        - The token is not in the database of expired tokens
        - The token string is correct (contains valid header, payload and signature)
        - The header and the payload of the token are dictionaries after JSON
        decoding.
        - The token type is correct (equals to get_type() value)
        - The signature is correct
        - The expiration datetime is not passed
        :param secret: The secret to use in signature creation
        :return: True if the token is valid, False otherwise.
        """
        expired_token = ExpiredToken.objects.filter(token=self.string)
        if not self.__is_correct or expired_token.exists():
            return False
        header_dict, payload_dict, header, payload, signature = self.__header_dict, \
                                                                self.__payload_dict, self.__header, self.__payload, self.__signature
        if not isinstance(header_dict, dict) or "typ" not in header_dict \
                or header_dict["typ"] != "jwt" or "alg" not in header_dict:
            raise IncorrectTokenHeaderException()
        if not isinstance(payload_dict, dict) or "ttp" not in payload_dict:
            raise IncorrectTokenPayloadException()
        algorithm = header_dict["alg"]
        token_type = payload_dict["ttp"]
        if self.get_type() != token_type \
                or signature != self.generate_signature(header, payload, secret, algorithm):
            return False
        expiration_datetime = datetime.strptime(payload_dict["exp"], '%Y-%m-%d %H:%M:%S.%f')
        if expiration_datetime < datetime.utcnow():
            return False
        return True

    def __str__(self):
        """
        Converts Token object to string
        :return: The token string which is ready for usage in HTTP headers.
        """
        return self.string

    def get_payload(self):
        """
        Returns the token's payload as dictionary. This method will return the
        payload if the token is valid. Otherwise it will return None.
        :return:
        """
        return self.payload

    def mark_as_expired(self):
        """
        Marks the token as expired. This method adds the token to the list of expired tokens which
        is stored in the database.
        """
        ExpiredToken.objects.create(token=str(self))


class AccessToken(Token):
    """
    The short-term access token.
    """

    def __init__(self, string):
        """
        The constructor.
        :param string: The jwt string.
        """
        super(AccessToken, self).__init__(string)

    @classmethod
    def get_type(cls):
        """
        Returns the type of the token (as string which will be used in payload
        creation).
        :return: The token type.
        """
        return "access"

    @classmethod
    def get_lifetime(cls):
        """
        Returns the lifetime of the token.
        :return: The lifetime of the token as timedelta object.
        """
        return timedelta(minutes=5)

    @classmethod
    def get_algorithm(cls):
        """
        Returns the hashing algorithm of the token. Possible algorithms are
        listed in HASH_ALGORITHMS
        :return: The hashing algorithm.
        """
        return "HS512"


class RefreshToken(Token):
    """
    The long-term refresh token.
    """

    def __init__(self, string):
        """
        The constructor.
        :param string: The jwt string.
        """
        super(RefreshToken, self).__init__(string)

    @classmethod
    def get_type(cls):
        """
        Returns the type of the token (as string which will be used in payload
        creation).
        :return: The token type.
        """
        return "refresh"

    @classmethod
    def get_lifetime(cls):
        """
        Returns the lifetime of the token.
        :return: The lifetime of the token as timedelta object.
        """
        return timedelta(days=7)

    @classmethod
    def get_algorithm(cls):
        """
        Returns the hashing algorithm of the token. Possible algorithms are
        listed in HASH_ALGORITHMS
        :return: The hashing algorithm.
        """
        return "HS512"


class UserToken(Token):

    def __init__(self, string):
        super(UserToken, self).__init__(string)
        self.user = None

    @classmethod
    def get_secret_for_user(cls, user, secret=""):
        return bytes("{}{}{}".format(
            user.password.split("$")[-1],
            str(user.date_joined.timestamp()),
            secret), "utf-8")

    @classmethod
    def generate_for_user(cls, user, secret, payload=None):
        if payload is None:
            payload = {}
        payload["uid"] = user.id
        return super().generate(payload, cls.get_secret_for_user(user, secret))

    def verify(self, secret) -> bool:
        payload = self.get_payload()
        if not payload:
            return False
        user_id = payload["uid"]
        user = get_user_model().objects.filter(id=user_id)
        if user.exists():
            secret = self.get_secret_for_user(user[0], secret)
            if not super().verify(secret):
                return False
            self.user = user[0]
            return True
        return False

    def get_user(self):
        return self.user


class UserAccessToken(UserToken, AccessToken):
    pass


class UserRefreshToken(UserToken, RefreshToken):

    def generate_token_pair(self, secret):
        if not self.verify(secret):
            return None
        return generate_user_token_pair(self.user, secret, self.payload)


def generate_user_token_pair(user, secret, payload: dict = None):
    return UserAccessToken.generate_for_user(user, secret, payload), \
           UserRefreshToken.generate_for_user(user, secret, payload)


class ConfirmEmailToken(Token):

    @classmethod
    def get_type(cls) -> str:
        return "confemail"

    @classmethod
    def get_lifetime(cls) -> timedelta:
        return timedelta(days=1)

    @classmethod
    def get_algorithm(cls) -> str:
        return "HS512"


class ResetPasswordToken(Token):

    @classmethod
    def get_type(cls) -> str:
        return "resetpass"

    @classmethod
    def get_lifetime(cls) -> timedelta:
        return timedelta(days=1)

    @classmethod
    def get_algorithm(cls) -> str:
        return "HS512"


class UserConfirmEmailToken(UserToken, ConfirmEmailToken):
    pass


class UserResetPasswordToken(UserToken, ResetPasswordToken):
    pass
