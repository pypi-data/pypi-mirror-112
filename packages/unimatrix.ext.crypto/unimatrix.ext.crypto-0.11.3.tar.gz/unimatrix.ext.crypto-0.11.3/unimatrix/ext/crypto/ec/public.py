"""Declares :class:`EllipticCurvePublicKey`."""
import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from ..public import PublicKey
from .verifier import EllipticCurveVerifier


class EllipticCurvePublicKey(EllipticCurveVerifier, PublicKey):
    curve = None

    @property
    def keyid(self):
        return hashlib.md5(bytes(self)).hexdigest() # nosec

    @property
    def y(self):
        return self.__numbers.y

    @property
    def x(self):
        return self.__numbers.x

    @property
    def public(self):
        return self.__public

    @classmethod
    def fromjwk(cls, jwk):
        if jwk.crv != 'SECP256K1':
            raise NotImplementedError
        return cls.fromnumbers(
            int.from_bytes(jwk.x, 'big'),
            int.from_bytes(jwk.y, 'big'),
            curve=ec.SECP256K1()
        )

    @classmethod
    def fromnumbers(cls, x, y, curve):
        assert isinstance(x, int) # nosec
        assert isinstance(y, int) # nosec
        return cls(ec.EllipticCurvePublicNumbers(x, y, curve).public_key())

    @classmethod
    def frompem(cls, pem):
        if isinstance(pem, str):
            pem = str.encode(pem)
        return cls(serialization.load_pem_public_key(pem))

    def __init__(self, key, capabilities=None):
        self.__public = key
        self.__numbers = self.__public.public_numbers()
        self.capabilities = capabilities or self.capabilities

    async def encrypt(self, *args, **kwargs):
        raise NotImplementedError

    def __bytes__(self):
        buf = bytearray()
        buf.append(0x04)
        buf.extend(int.to_bytes(self.__numbers.x, 32, 'big'))
        buf.extend(int.to_bytes(self.__numbers.y, 32, 'big'))
        return bytes(buf)
