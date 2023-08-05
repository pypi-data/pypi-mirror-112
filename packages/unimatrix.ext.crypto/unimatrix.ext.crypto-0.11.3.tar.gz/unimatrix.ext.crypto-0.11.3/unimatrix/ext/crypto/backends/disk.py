"""Declares :class:`LocalDiskBackend`."""
import os

from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from .. import oid
from ..pkcs import RSAPublicKey
from ..keyloader import KeyLoader


class LocalDiskBackend(KeyLoader):
    algorithms = {
        RSAPrivateNumbers: [
            oid.RSAPKCS1v15SHA256,
            oid.RSAPKCS1v15SHA384,
            oid.RSAPKCS1v15SHA512,
        ]
    }

    async def sign(self, wrapper, digest, algorithm, padding, *args, **kwargs):
        return wrapper.private.sign(
            data=digest,
            padding=padding,
            algorithm=utils.Prehashed(algorithm)
        )

    def setup(self, opts):
        self.workdir = opts.dirname

    def get_algorithms(self, dto):
        if hasattr(dto, 'private_numbers'):
            cls = type(dto.private_numbers())
            return self.algorithms[cls]
        else:
            raise NotImplementedError

    def get_private_key(self, dto):
        return dto

    def get_public_key(self, client, dto):
        assert isinstance(dto.private_numbers(), RSAPrivateNumbers) # nosec
        return RSAPublicKey(dto.public_key())

    def get_qualname(self, dto):
        return ''

    def get_sync(self, name):
        with open(os.path.join(self.workdir, name), 'rb') as f:
            return self.key_factory(
                None, name, load_pem_private_key(f.read(), None))

    def get_version(self, dto):
        return None

