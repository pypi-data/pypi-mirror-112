"""Module to hold all of the token based logic using within the library"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import auto, Enum
from typing import Tuple, Union
import logging  # noqa: I100
import os
import re
import json  # noqa: I100
import base64  # noqa: I100

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .exceptions import (
    BadlyFormattedTokenException,
    InvalidTokenException,
    MethodMismatchException,
    NoPrivateKeyException,
    PathMismatchException,
    TokenExpiredException,
)

# disbaled I100; in places where I think changing the import order
# would make the code less readable

LOGGER = logging.getLogger(__file__)


class HTTPMethods(Enum):
    """Class to hold the available HTTP request methods"""

    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    CONNECT = auto()
    OPTIONS = auto()
    TRACE = auto()
    PATCH = auto()


class RocketToken:
    """Class to represent a public key, private key pair used
    for encrypting, decrypting, creating and validating tokens
    """

    def __init__(
        self,
        public_key: Union[rsa.RSAPublicKey, None] = None,
        private_key: Union[rsa.RSAPrivateKey, None] = None,
    ) -> None:
        """Creates an instance of the RocketToken class, optionally providing
        a public and private key

        Args:
            public_key: The public key to use for encrypting the token.
            private_key: The private key that matches the public_key and is
            used for decrypting the token.
        """
        if os.environ.get("ROCKET_DEVELOPER_MODE", "false") == "true":
            self.public_key, self.private_key = RocketToken._load_keys_from_env()
        else:
            self.public_key = public_key
            self.private_key = private_key

    def decode_public_key(self) -> str:
        """
        Returns the Public key in PEM format.

        Returns (str): Public key

        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    @staticmethod
    def _load_keys_from_env() -> Tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """Loads a public key and private key from environmental variables.

        Expected names for the environmental variables are `public_key` and
        `private_key` respectively. The private_key is optional.

        Returns:
            public_key rsa.RSAPublicKey
            private_key rsa.RSAPrivateKey
        """
        if os.environ.get("ROCKET_DEVELOPER_MODE", "false") == "true":
            public_key = bytes(os.environ["RT_DEV_PUBLIC"], encoding="utf-8")
            private_key = os.environ.get("RT_DEV_PRIVATE", None)
        else:
            public_key = bytes(os.environ["public_key"], encoding="utf-8")
            private_key = os.environ.get("private_key", None)

        public_key = re.sub(b"\\\\n", b"\\n", public_key)
        public_key = serialization.load_pem_public_key(
            public_key, backend=default_backend()
        )

        if private_key is not None:
            private_key = bytes(private_key, encoding="utf-8")
            private_key = re.sub(b"\\\\n", b"\\n", private_key)
            private_key = serialization.load_pem_private_key(
                private_key, password=None, backend=default_backend()
            )

        return public_key, private_key

    @classmethod
    def rocket_token_from_env(cls: RocketToken) -> RocketToken:
        """Loads a public key and private key from environmental variables.

        Expected names for the environmental variables are public_key and
        private_key respectively. The private_key is optional.

        Args:
            cls (RocketToken): Instance of RocketToken class

        Returns: RocketToken
        """
        public_key, private_key = RocketToken._load_keys_from_env()
        return cls(public_key, private_key)

    @classmethod
    def rocket_token_from_path(
        cls, public_path: str = None, private_path: Union[str, None] = None
    ) -> RocketToken:
        """
        Creates an instance of the RocketToken class from a
        public and private key stored on disk. The private key
        is optional.

        Args:
            public_path (str): File path to the public key file.
            private_path (str): File path to the private key file.

        Returns (RocketToken): RocketToken

        """
        public_key, private_key = None, None

        with open(public_path, "rb") as public:
            public_key = serialization.load_pem_public_key(
                public.read(), backend=default_backend()
            )

        if private_path:
            with open(private_path, "rb") as keyfile:
                private_key = serialization.load_pem_private_key(
                    keyfile.read(), password=None, backend=default_backend()
                )

        return cls(public_key=public_key, private_key=private_key)

    @staticmethod
    def generate_key_pair(
        path: str,
        key_size: int = 4096,
        public_exponent: int = 65537,
    ) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        Generates and saves public and private key files in PEM format.

        Args:
            path (str): Directory Location to save public and private key pairs.
            key_size (int): How many bits long the key should be.
            public_exponent int: indicates what one mathematical property of the
            key generation will be. Unless you have a
            valid reason to do otherwise, always use 65537.

        Returns (tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]): private_key, public_key

        """
        if not os.path.isdir(path):
            os.mkdir(path)

        private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=default_backend(),
        )

        public_key = private_key.public_key()

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(f"{path}/id_rsa", "wb") as binaryfile:
            binaryfile.write(pem)

        with open(f"{path}/id_rsa.pub", "wb") as binaryfile:
            binaryfile.write(public)

        return private_key, public_key

    @staticmethod
    def validate_web_token(token: dict, path: str, method: str) -> Union[None, True]:
        """Verifies that the passed token has a `path` and `method`
        that matches those specified in the argument. It also checks
        that the token has not expired.

        Args:
            token (dict): User API token to validate.

        Raises:
            BadlyFormattedTokenException: Token is missing required keys.
            TokenExpiredException: Token has expired.
            PathMismatchException: Token Path != required path
            MethodMismatchException: Token Method != required method

        Returns: Union[None, True]

        """
        expected_keys = ["path", "exp", "method"]
        if not set(expected_keys).issubset(token.keys()):
            raise BadlyFormattedTokenException(
                f"Incorrect token keys; token must contain at least: {expected_keys}"
            )

        if not datetime.utcnow() < datetime.fromisoformat(token["exp"]):
            raise TokenExpiredException(f"token exp: `{token['exp']}` has expired.")

        if path.lower() != token["path"].lower():
            raise PathMismatchException(f"token path `{token['path']}` != `{path}`")

        if method.lower() != token["method"].lower():
            raise MethodMismatchException(
                f"token method `{token['method']}` != `{method}`"
            )

        return True

    def _encrypt_dict(self, d: dict) -> bytes:
        encrypted_token: bytes = self.public_key.encrypt(
            bytes(json.dumps(d), encoding="utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return base64.b64encode(encrypted_token)

    def generate_web_token(self, path: str, exp: int, method: str, **kwargs) -> str:
        """Generates a web token for the specified `path`, `method` and expires
        and after current_datetime + timedelata(minutes=exp)

        Args:
            path (str): The REST endpoint path that the token is valid for.
            exp (int): A +ve integer of minutes until the token should expire.
            method (str): The HTTP method that the token is valid for.

            kwargs: The extra key-value payloads to add to the dictionary.

        Raises:
            ValueError: Raised when an invalid HTTP method is passed in the `method`
            arguemnt.

        Returns:
            str: The web token.
        """
        try:
            HTTPMethods[method.upper()]
        except KeyError:
            raise ValueError(f"{method.upper()} is not a valid HTTP Method")

        if exp <= 0:
            raise ValueError("exp should be larger than 0.")

        token = {
            "path": path,
            "exp": (datetime.utcnow() + timedelta(minutes=exp)).isoformat(),
            "method": method.upper(),
            **kwargs,
        }
        encrypted_token = self._encrypt_dict(token)
        return f'Bearer {encrypted_token.decode("utf-8")}'

    def generate_token(self, **kwargs) -> str:
        """Creates a general purpose token using the payload values in kwargs

        Returns:
            str: The general token

        """
        encrypted_token = self._encrypt_dict(kwargs)
        return f'Bearer {encrypted_token.decode("utf-8")}'

    def decode_token(self, token: str) -> dict:
        """Decrypts an encrypted token.

        Args:
            token (str): Encrypted token to decrypt.

        Returns (dict): json.loads(plaintext.decode(encoding="utf-8"))

        """
        if self.private_key is None:
            raise NoPrivateKeyException("No private key loaded. Cannot decode token.")

        if token.count(" ") != 1:
            raise InvalidTokenException("Token must have exactly 1 space character.")

        _, token = token.split(" ")
        token = base64.b64decode(token.encode("utf-8"))

        self.private_key: rsa.RSAPrivateKey
        plaintext = self.private_key.decrypt(
            token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return json.loads(plaintext.decode(encoding="utf-8"))

    def decode_and_validate_web_token(self, token: str, path: str, method: str) -> bool:
        """
        A convenience function to bundle the logic of decoding the token and
        validating it into one function.

        Args:
            token (str): The token to decode and validate.
            path (str): The path of the requested resource.
            method (str): The HTTP method used to access the requested resource.

        Returns:
            bool: Indicates if the token was valid or not.
            NoReturn: No return when an exception is raised.

        Raises:
            NoPrivateKeyException: Raised when the RocketToken class is
            initialised without a private key and you attempt to decrypt a token.
            InvalidTokenException: Raised when token, path, exp, or method fail
            during validation.

        """
        token_dict = self.decode_token(token=token)
        return self.validate_web_token(token=token_dict, path=path, method=method)
